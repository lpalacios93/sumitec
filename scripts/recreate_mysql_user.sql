CREATE DATABASE IF NOT EXISTS sumitec_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

DROP USER IF EXISTS 'sumitec_user'@'localhost';

CREATE USER 'sumitec_user'@'localhost'
IDENTIFIED BY 'cambiar_esta_contrasena';

GRANT ALL PRIVILEGES ON sumitec_db.* TO 'sumitec_user'@'localhost';
FLUSH PRIVILEGES;
