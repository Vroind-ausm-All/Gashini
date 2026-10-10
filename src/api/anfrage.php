<?php
/**
 * Gashini Dienstleistungen – Anfrageformular
 * Quelle: src/api/anfrage.php · wird nach web/api/ kopiert.
 *
 * Nimmt das Anfrageformular entgegen, prüft es serverseitig und stellt es per
 * E-Mail zu. Antwortet mit JSON (wenn der Browser es anfordert) oder leitet
 * ohne JavaScript per 303 auf die Danke-Seite bzw. zeigt eine Fehlerseite.
 *
 * Konfiguration: siehe konfiguration.beispiel.php. Ohne gültige Konfiguration
 * nimmt das Skript bewusst keine Anfragen an (HTTP 503) – ein nicht
 * eingerichteter Mailversand darf nicht als funktionierend erscheinen.
 *
 * Keine Abhängigkeiten. PHP ≥ 8.1.
 */
declare(strict_types=1);

const LEISTUNGEN = ['Trockenbau & Innenausbau', 'Hausmeisterservice', 'Reparatur & Instandhaltung', 'Mehrere Arbeiten / noch unklar'];
const QUELLEN = ['Google-Suche', 'Google-Profil / Karte', 'MyHammer', 'Empfehlung', 'Fahrzeug oder Flyer', 'Sonstiges'];
const RUECKRUFZEITEN = ['Vormittags (8–12 Uhr)', 'Mittags (12–14 Uhr)', 'Nachmittags (14–18 Uhr)'];
const LAENGEN = ['name' => 100, 'email' => 254, 'telefon' => 40, 'leistung' => 80, 'nachricht' => 4000, 'ort' => 100, 'zeitraum' => 100, 'quelle' => 60, 'rueckrufzeit' => 40];
const MIN_AUSFUELLZEIT = 3;
const MAX_FOTOS = 3;
const MAX_FOTO_BYTES = 8 * 1024 * 1024;        // je Foto
const MAX_FOTOS_GESAMT = 12 * 1024 * 1024;     // alle Fotos zusammen
const MAX_ANFRAGE_BYTES = 13 * 1024 * 1024;    // gesamte Übermittlung (Fotos + Text + Rahmen)
const FOTO_TYPEN = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'];

header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');
header('Referrer-Policy: same-origin');
header('X-Frame-Options: DENY');

$will_json = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

$konfig = konfiguration_laden();
if ($konfig === null) {
    protokoll('Konfiguration fehlt oder ist unvollständig');
    antworten(503, ['ok' => false, 'meldung' => 'Das Anfrageformular ist noch nicht eingerichtet. Bitte rufen Sie uns an oder schreiben Sie eine E-Mail.'], $will_json);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    antworten(405, ['ok' => false, 'meldung' => 'Diese Adresse nimmt nur Formularübermittlungen an.'], $will_json);
}

$herkunft = rtrim($_SERVER['HTTP_ORIGIN'] ?? '', '/');
if ($herkunft !== '' && !herkunft_erlaubt($herkunft, $konfig)) {
    protokoll('Fremde Herkunft abgewiesen');
    antworten(403, ['ok' => false, 'meldung' => 'Die Anfrage wurde nicht von dieser Website gesendet.'], $will_json);
}

if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > MAX_ANFRAGE_BYTES) {
    antworten(413, ['ok' => false, 'fehler' => ['fotos' => 'Die Fotos sind zusammen zu groß (höchstens 12 MB).'],
        'meldung' => 'Die Anfrage ist zu groß. Bitte senden Sie weniger oder kleinere Fotos.'], $will_json);
}
// Überschreitet die Übermittlung post_max_size, verwirft PHP alle Felder – das ist dann kein leeres Formular.
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && empty($_POST) && (int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
    antworten(413, ['ok' => false, 'meldung' => 'Die Anfrage konnte wegen ihrer Größe nicht angenommen werden. Bitte senden Sie weniger oder kleinere Fotos.'], $will_json);
}

if (!limit_einhalten($_SERVER['REMOTE_ADDR'] ?? '', $konfig)) {
    header('Retry-After: 900');
    antworten(429, ['ok' => false, 'meldung' => 'Es wurden in kurzer Zeit zu viele Anfragen gesendet. Bitte versuchen Sie es später erneut oder rufen Sie uns an.'], $will_json);
}

$danke = $konfig['danke_url'];

// Spam-Erkennung: Honigtopf-Feld oder unplausibel schnelle Übermittlung.
// Der Absender erhält dieselbe Antwort wie bei Erfolg, damit Skripte nichts lernen.
$honig = feld('webseite', false);
$zeit = isset($_POST['ausfuellzeit']) && $_POST['ausfuellzeit'] !== '' ? (int)$_POST['ausfuellzeit'] : -1;
if ($honig !== '' || ($zeit >= 0 && $zeit < MIN_AUSFUELLZEIT)) {
    protokoll('Als Spam verworfen');
    $ref = referenz();
    antworten(200, ['ok' => true, 'ref' => $ref, 'weiter' => $danke . '?ref=' . $ref], $will_json, $danke . '?ref=' . $ref);
}

$d = [
    'name'      => feld('name', false),
    'email'     => feld('email', false),
    'telefon'   => feld('telefon', false),
    'leistung'  => feld('leistung', false),
    'nachricht' => feld('nachricht', true),
    'ort'       => feld('ort', false),
    'zeitraum'  => feld('zeitraum', false),
    'quelle'    => feld('quelle', false),
    'rueckruf'  => feld('rueckruf', false) === 'ja' ? 'ja' : '',
    'rueckrufzeit' => feld('rueckrufzeit', false),
];

$fehler = pruefen($d);
[$fotos, $fotofehler] = fotos_lesen();
if ($fotofehler !== '') $fehler['fotos'] = $fotofehler;
if ($fehler) {
    antworten(422, ['ok' => false, 'fehler' => $fehler,
        'meldung' => count($fehler) === 1 ? 'Ein Feld muss noch korrigiert werden.' : count($fehler) . ' Felder müssen noch korrigiert werden.'], $will_json);
}

$ref = referenz();
if (!zustellen($d, $fotos, $ref, $konfig)) {
    antworten(502, ['ok' => false, 'meldung' => 'Die Anfrage konnte gerade nicht zugestellt werden. Ihre Eingaben sind nicht verloren – bitte versuchen Sie es in einigen Minuten erneut oder rufen Sie uns an.'], $will_json);
}

protokoll('Anfrage zugestellt ' . $ref);
antworten(200, ['ok' => true, 'ref' => $ref, 'weiter' => $danke . '?ref=' . $ref], $will_json, $danke . '?ref=' . $ref);


/* ======================================================================= */

function konfiguration_laden(): ?array
{
    $kandidaten = array_filter([
        getenv('GASHINI_KONFIG') ?: null,
        dirname(__DIR__, 2) . '/gashini-konfiguration.php',   // eine Ebene über dem Web-Verzeichnis
        __DIR__ . '/konfiguration.php',
    ]);
    foreach ($kandidaten as $pfad) {
        if (is_file($pfad) && is_readable($pfad)) {
            $k = require $pfad;
            if (!is_array($k)) return null;
            $k += [
                'transport' => 'mail', 'absender_name' => 'Website Gashini Dienstleistungen',
                'speicher_verzeichnis' => sys_get_temp_dir() . '/gashini-anfragen',
                'limit_pro_ip' => 8, 'fenster_sekunden' => 900, 'limit_gesamt_pro_stunde' => 60,
                'danke_url' => '../kontakt/danke/', 'erlaubte_herkunft' => [], 'smtp' => [],
            ];
            $gueltig = filter_var($k['empfaenger'] ?? '', FILTER_VALIDATE_EMAIL)
                && filter_var($k['absender'] ?? '', FILTER_VALIDATE_EMAIL)
                && is_string($k['geheimnis'] ?? null) && strlen($k['geheimnis']) >= 32
                && !str_contains($k['geheimnis'], 'HIER')
                && in_array($k['transport'], ['mail', 'smtp', 'datei'], true);
            return $gueltig ? $k : null;
        }
    }
    return null;
}

/** Erlaubt die eigene Adresse (gleicher Host wie die Anfrage) und zusätzlich konfigurierte Herkünfte. */
function herkunft_erlaubt(string $herkunft, array $k): bool
{
    if (in_array($herkunft, $k['erlaubte_herkunft'], true)) return true;
    $teile = parse_url($herkunft);
    if (!$teile || empty($teile['host'])) return false;
    $host = strtolower($teile['host'] . (isset($teile['port']) ? ':' . $teile['port'] : ''));
    return $host === strtolower($_SERVER['HTTP_HOST'] ?? '');
}

/** Liest ein Formularfeld als Text, entfernt Steuerzeichen. Einzeilige Felder verlieren Zeilenumbrüche. */
function feld(string $name, bool $mehrzeilig): string
{
    $wert = $_POST[$name] ?? '';
    if (!is_string($wert) || !mb_check_encoding($wert, 'UTF-8')) return '';
    $wert = str_replace(["\r\n", "\r"], "\n", $wert);
    $wert = preg_replace($mehrzeilig ? '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u' : '/[\x00-\x1F\x7F]/u', $mehrzeilig ? '' : ' ', $wert) ?? '';
    return trim($wert);
}

function pruefen(array $d): array
{
    $f = [];
    foreach (LAENGEN as $n => $max) {
        if (mb_strlen($d[$n]) > $max) $f[$n] = 'Bitte kürzen Sie diese Angabe (höchstens ' . $max . ' Zeichen).';
    }
    if ($d['name'] === '') $f['name'] = 'Bitte geben Sie Ihren Namen an.';
    if ($d['email'] === '' && $d['telefon'] === '') {
        $f['email'] = 'Bitte geben Sie eine E-Mail-Adresse oder eine Telefonnummer an.';
    }
    if ($d['email'] !== '' && !isset($f['email']) && !filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
        $f['email'] = 'Bitte prüfen Sie die E-Mail-Adresse.';
    }
    if ($d['telefon'] !== '' && !isset($f['telefon']) && !preg_match('/^[0-9+()\/\-\s]{6,40}$/', $d['telefon'])) {
        $f['telefon'] = 'Bitte geben Sie eine Telefonnummer mit Ziffern an.';
    }
    if (!in_array($d['leistung'], LEISTUNGEN, true)) $f['leistung'] = 'Bitte wählen Sie aus, worum es geht.';
    if ($d['nachricht'] === '') $f['nachricht'] = 'Bitte beschreiben Sie kurz Ihr Vorhaben.';
    elseif (!isset($f['nachricht']) && mb_strlen($d['nachricht']) < 10) $f['nachricht'] = 'Bitte beschreiben Sie Ihr Vorhaben in ein paar Worten mehr.';
    if ($d['quelle'] !== '' && !in_array($d['quelle'], QUELLEN, true)) $f['quelle'] = 'Ungültige Auswahl.';
    if ($d['rueckruf'] === 'ja' && $d['telefon'] === '' && !isset($f['telefon'])) $f['telefon'] = 'Für einen Rückruf brauchen wir Ihre Telefonnummer.';
    if ($d['rueckrufzeit'] !== '' && !in_array($d['rueckrufzeit'], RUECKRUFZEITEN, true)) $f['rueckrufzeit'] = 'Ungültige Auswahl.';
    return $f;
}

/**
 * Liest bis zu drei hochgeladene Fotos. Der Typ wird am Inhalt erkannt (finfo, getimagesize),
 * nie an Dateiname oder Browserangabe. Gibt [Liste, Fehlertext] zurück; Dateien bleiben im
 * temporären Upload-Verzeichnis und werden nach der Anfrage von PHP gelöscht.
 */
function fotos_lesen(): array
{
    $roh = $_FILES['fotos'] ?? null;
    if (!$roh || !is_array($roh['name'] ?? null)) return [[], ''];
    $fotos = [];
    $summe = 0;
    $anzahl = 0;
    foreach ($roh['name'] as $i => $name) {
        $fehlercode = (int)($roh['error'][$i] ?? UPLOAD_ERR_NO_FILE);
        if ($fehlercode === UPLOAD_ERR_NO_FILE) continue;
        $anzahl++;
        if ($anzahl > MAX_FOTOS) return [[], 'Bitte senden Sie höchstens ' . MAX_FOTOS . ' Fotos.'];
        if (in_array($fehlercode, [UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE], true)) return [[], 'Ein Foto ist zu groß (höchstens 8 MB je Foto).'];
        if ($fehlercode !== UPLOAD_ERR_OK) return [[], 'Ein Foto konnte nicht übertragen werden. Bitte versuchen Sie es erneut.'];
        $tmp = (string)$roh['tmp_name'][$i];
        if (!is_uploaded_file($tmp)) return [[], 'Ein Foto konnte nicht übertragen werden.'];
        $groesse = (int)filesize($tmp);
        if ($groesse <= 0 || $groesse > MAX_FOTO_BYTES) return [[], 'Ein Foto ist zu groß (höchstens 8 MB je Foto).'];
        $summe += $groesse;
        if ($summe > MAX_FOTOS_GESAMT) return [[], 'Die Fotos sind zusammen zu groß (höchstens 12 MB).'];
        $typ = (new finfo(FILEINFO_MIME_TYPE))->file($tmp) ?: '';
        $info = @getimagesize($tmp);
        if (!isset(FOTO_TYPEN[$typ]) || !$info || ($info['mime'] ?? '') !== $typ) {
            return [[], 'Bitte nur Fotos als JPEG, PNG oder WebP hochladen.'];
        }
        $fotos[] = ['pfad' => $tmp, 'typ' => $typ, 'name' => 'foto-' . (count($fotos) + 1) . '.' . FOTO_TYPEN[$typ]];
    }
    return [$fotos, ''];
}

/** Datei-basiertes Mengenlimit je IP (als HMAC-Prüfwert gespeichert) und insgesamt. */
function limit_einhalten(string $ip, array $k): bool
{
    $verz = $k['speicher_verzeichnis'];
    if (!is_dir($verz) && !@mkdir($verz, 0700, true) && !is_dir($verz)) {
        protokoll('Speicherverzeichnis für das Mengenlimit nicht beschreibbar');
        return true;  // Formular nicht blockieren, aber Fehler protokollieren
    }
    $jetzt = time();
    if (random_int(1, 50) === 1) aufraeumen($verz, $jetzt);
    $schluessel = substr(hash_hmac('sha256', $ip, $k['geheimnis']), 0, 40);
    return zaehlen($verz . '/ip-' . $schluessel . '.txt', $jetzt, (int)$k['fenster_sekunden'], (int)$k['limit_pro_ip'])
        && zaehlen($verz . '/gesamt.txt', $jetzt, 3600, (int)$k['limit_gesamt_pro_stunde']);
}

function zaehlen(string $datei, int $jetzt, int $fenster, int $max): bool
{
    $fh = @fopen($datei, 'c+');
    if (!$fh) return true;
    flock($fh, LOCK_EX);
    $zeiten = array_filter(array_map('intval', explode("\n", stream_get_contents($fh) ?: '')),
        fn($t) => $t > $jetzt - $fenster);
    $erlaubt = count($zeiten) < $max;
    if ($erlaubt) $zeiten[] = $jetzt;
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, implode("\n", $zeiten));
    flock($fh, LOCK_UN);
    fclose($fh);
    return $erlaubt;
}

function aufraeumen(string $verz, int $jetzt): void
{
    foreach (glob($verz . '/ip-*.txt') ?: [] as $f) {
        if (@filemtime($f) < $jetzt - 86400) @unlink($f);
    }
}

function referenz(): string
{
    $zeichen = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    $r = '';
    for ($i = 0; $i < 8; $i++) $r .= $zeichen[random_int(0, strlen($zeichen) - 1)];
    return $r;
}

/** Entfernt alles, was einen Kopfzeilenumbruch erzeugen könnte. */
function kopfwert(string $s): string
{
    return trim(str_replace(["\r", "\n", "\0"], ' ', $s));
}

function zustellen(array $d, array $fotos, string $ref, array $k): bool
{
    $betreff = 'Anfrage ' . $ref . ': ' . ($d['rueckruf'] === 'ja' ? 'Rückruf – ' : '') . $d['leistung'] . ' – ' . mb_substr($d['name'], 0, 60);
    $zeilen = [
        'Neue Anfrage über die Website (Vorgang ' . $ref . ')',
        str_repeat('=', 48),
        '',
        'Name:      ' . $d['name'],
        'E-Mail:    ' . ($d['email'] ?: '–'),
        'Telefon:   ' . ($d['telefon'] ?: '–'),
        'Rückruf:   ' . ($d['rueckruf'] === 'ja' ? 'erwünscht' . ($d['rueckrufzeit'] !== '' ? ', ' . $d['rueckrufzeit'] : '') : 'nein'),
        'Leistung:  ' . $d['leistung'],
        'Ort:       ' . ($d['ort'] ?: '–'),
        'Zeitraum:  ' . ($d['zeitraum'] ?: '–'),
        'Quelle:    ' . ($d['quelle'] ?: '–'),
        '',
        'Vorhaben:',
        $d['nachricht'],
        '',
        'Fotos:     ' . (count($fotos) ? count($fotos) . ' im Anhang' : 'keine'),
        '',
        '-- ',
        'Diese Nachricht wurde automatisch vom Anfrageformular erzeugt.',
        'Bitte gemäß Datenschutzerklärung löschen, wenn die Anfrage erledigt ist und kein Auftrag zustande kommt.',
    ];
    $text = implode("\r\n", $zeilen) . "\r\n";

    $absender = kopfwert($k['absender']);
    $domain = substr(strrchr($absender, '@') ?: '@localhost', 1);
    $koepfe = [
        'From' => mb_encode_mimeheader(kopfwert($k['absender_name']), 'UTF-8', 'Q') . ' <' . $absender . '>',
        'MIME-Version' => '1.0',
        'Content-Type' => 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding' => '8bit',
        'Message-ID' => '<' . bin2hex(random_bytes(12)) . '@' . $domain . '>',
        'Date' => date(DATE_RFC2822),
        'X-Vorgang' => $ref,
    ];
    if ($d['email'] !== '' && filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
        $koepfe['Reply-To'] = '<' . kopfwert($d['email']) . '>';
    }
    if ($fotos) {
        // multipart/mixed: Text plus Fotos als Base64-Anhänge
        $grenze = '=_gashini_' . bin2hex(random_bytes(12));
        $koepfe['Content-Type'] = 'multipart/mixed; boundary="' . $grenze . '"';
        unset($koepfe['Content-Transfer-Encoding']);
        $teile = "Diese Nachricht besteht aus mehreren Teilen.\r\n\r\n--" . $grenze . "\r\n"
            . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n" . $text;
        foreach ($fotos as $f) {
            $teile .= "\r\n--" . $grenze . "\r\n"
                . 'Content-Type: ' . $f['typ'] . '; name="' . $f['name'] . "\"\r\n"
                . "Content-Transfer-Encoding: base64\r\n"
                . 'Content-Disposition: attachment; filename="' . $f['name'] . "\"\r\n\r\n"
                . chunk_split(base64_encode((string)file_get_contents($f['pfad'])), 76, "\r\n");
        }
        $text = $teile . "\r\n--" . $grenze . "--\r\n";
    }
    $betreff_kodiert = mb_encode_mimeheader(kopfwert($betreff), 'UTF-8', 'B', "\r\n");
    $empfaenger = kopfwert($k['empfaenger']);

    switch ($k['transport']) {
        case 'datei':
            $verz = $k['datei_verzeichnis'] ?? '';
            if (!$verz || (!is_dir($verz) && !@mkdir($verz, 0700, true))) return false;
            $roh = 'To: ' . $empfaenger . "\r\nSubject: " . $betreff_kodiert . "\r\n";
            foreach ($koepfe as $n => $v) $roh .= $n . ': ' . $v . "\r\n";
            return file_put_contents($verz . '/' . $ref . '.eml', $roh . "\r\n" . $text) !== false;

        case 'smtp':
            return smtp_senden($k['smtp'], $absender, $empfaenger, $betreff_kodiert, $koepfe, $text);

        default:
            $kopfzeilen = '';
            foreach ($koepfe as $n => $v) $kopfzeilen .= $n . ': ' . $v . "\r\n";
            return mail($empfaenger, $betreff_kodiert, $text, rtrim($kopfzeilen), '-f' . $absender);
    }
}

/** Minimaler SMTP-Versand mit STARTTLS oder implizitem TLS und AUTH LOGIN. */
function smtp_senden(array $s, string $von, string $an, string $betreff, array $koepfe, string $text): bool
{
    $host = $s['host'] ?? '';
    $port = (int)($s['port'] ?? 587);
    $sicherheit = $s['sicherheit'] ?? 'starttls';   // starttls | ssl | keine (nur für lokale Tests)
    if ($host === '') return false;
    $ziel = ($sicherheit === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $kontext = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $sock = @stream_socket_client($ziel, $nr, $meldung, 15, STREAM_CLIENT_CONNECT, $kontext);
    if (!$sock) { protokoll('SMTP: Verbindung fehlgeschlagen'); return false; }
    stream_set_timeout($sock, 15);

    $lesen = function () use ($sock): string {
        $antwort = '';
        while (($zeile = fgets($sock, 515)) !== false) {
            $antwort .= $zeile;
            if (strlen($zeile) < 4 || $zeile[3] === ' ') break;
        }
        return $antwort;
    };
    $befehl = function (string $cmd, array $erwartet) use ($sock, $lesen): bool {
        if ($cmd !== '') fwrite($sock, $cmd . "\r\n");
        $code = (int)substr($lesen(), 0, 3);
        return in_array($code, $erwartet, true);
    };
    $helo = 'EHLO ' . (gethostname() ?: 'localhost');
    $ok = $befehl('', [220]) && $befehl($helo, [250]);
    if ($ok && $sicherheit === 'starttls') {
        $ok = $befehl('STARTTLS', [220])
            && stream_socket_enable_crypto($sock, true, STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT | STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT)
            && $befehl($helo, [250]);
    }
    if ($ok && !empty($s['benutzer'])) {
        $ok = $befehl('AUTH LOGIN', [334]) && $befehl(base64_encode($s['benutzer']), [334])
            && $befehl(base64_encode((string)($s['passwort'] ?? '')), [235]);
    }
    $ok = $ok && $befehl('MAIL FROM:<' . $von . '>', [250]) && $befehl('RCPT TO:<' . $an . '>', [250, 251]) && $befehl('DATA', [354]);
    if ($ok) {
        $roh = 'To: <' . $an . ">\r\nSubject: " . $betreff . "\r\n";
        foreach ($koepfe as $n => $v) $roh .= $n . ': ' . $v . "\r\n";
        $roh .= "\r\n" . preg_replace('/^\./m', '..', $text);
        fwrite($sock, $roh . "\r\n.\r\n");
        $ok = $befehl('', [250]);
    }
    @fwrite($sock, "QUIT\r\n");
    fclose($sock);
    if (!$ok) protokoll('SMTP: Zustellung fehlgeschlagen');
    return $ok;
}

/** Protokolliert ohne Inhalte der Anfrage. */
function protokoll(string $text): void
{
    error_log('[gashini-anfrage] ' . $text);
}

function antworten(int $status, array $daten, bool $json, ?string $weiter = null): never
{
    http_response_code($status);
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($daten, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        exit;
    }
    if ($status === 200 && $weiter !== null) {
        header('Location: ' . $weiter, true, 303);
        exit;
    }
    header('Content-Type: text/html; charset=utf-8');
    $e = fn(string $s) => htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $liste = '';
    foreach (($daten['fehler'] ?? []) as $feld => $text) $liste .= '<li>' . $e($text) . '</li>';
    echo '<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<meta name="robots" content="noindex"><title>Anfrage nicht gesendet</title>'
        . '<link rel="stylesheet" href="../assets/css/site.css"></head><body><main class="abschnitt"><div class="rahmen rechtstext">'
        . '<p class="label">Kontakt</p><h1>Die Anfrage wurde nicht gesendet</h1>'
        . '<p class="einleitung">' . $e($daten['meldung'] ?? 'Unbekannter Fehler.') . '</p>'
        . ($liste ? '<ul>' . $liste . '</ul>' : '')
        . '<p>Gehen Sie im Browser einen Schritt zurück – Ihre Eingaben bleiben dabei in der Regel erhalten.</p>'
        . '<p><a class="textlink" href="../kontakt/">Zurück zum Formular</a></p>'
        . '</div></main></body></html>';
    exit;
}
