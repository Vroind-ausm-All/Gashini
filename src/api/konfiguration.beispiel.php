<?php
/**
 * Vorlage für die Formular-Konfiguration.
 *
 * 1. Datei kopieren nach  gashini-konfiguration.php  – am besten EINE EBENE ÜBER
 *    dem Web-Verzeichnis (also außerhalb des öffentlich erreichbaren Ordners).
 *    Alternativ: als  api/konfiguration.php  neben anfrage.php ablegen
 *    oder den Pfad über die Umgebungsvariable GASHINI_KONFIG angeben.
 * 2. Werte eintragen. Diese Datei NIEMALS mit echten Werten ins Repository legen
 *    (sie ist in .gitignore eingetragen).
 *
 * Ohne gültige Konfiguration antwortet das Formular mit „noch nicht eingerichtet“.
 */
return [
    // Wohin gehen die Anfragen?
    'empfaenger'    => 'anfragen@ihre-domain.de',
    // Absenderadresse – muss zur eigenen Domain gehören, sonst landen Mails im Spam
    'absender'      => 'website@ihre-domain.de',
    'absender_name' => 'Website Gashini Dienstleistungen',

    // mail = PHP-mail() des Hosters · smtp = Versand über ein Postfach · datei = nur für Tests
    'transport' => 'smtp',
    'smtp' => [
        'host'       => 'smtp.ihr-anbieter.de',
        'port'       => 587,
        'sicherheit' => 'starttls',   // starttls (Port 587) oder ssl (Port 465)
        'benutzer'   => 'website@ihre-domain.de',
        'passwort'   => '',
    ],

    // Zufallswert mit mindestens 32 Zeichen, z. B. erzeugt mit:
    //   php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'
    'geheimnis' => 'HIER-ZUFALLSWERT-EINTRAGEN',

    // Die eigene Adresse ist immer erlaubt. Hier nur zusätzliche Herkünfte eintragen,
    // z. B. die Variante mit/ohne www, falls beide erreichbar sind.
    'erlaubte_herkunft' => ['https://www.ihre-domain.de', 'https://ihre-domain.de'],

    // Mengenlimit
    'limit_pro_ip'            => 8,     // Anfragen je IP …
    'fenster_sekunden'        => 900,   // … in 15 Minuten
    'limit_gesamt_pro_stunde' => 60,

    // Verzeichnis für das Mengenlimit – außerhalb des Web-Verzeichnisses, nur für PHP beschreibbar
    'speicher_verzeichnis' => sys_get_temp_dir() . '/gashini-anfragen',

    // Ziel nach erfolgreicher Anfrage, relativ zu /api/
    'danke_url' => '../kontakt/danke/',
];
