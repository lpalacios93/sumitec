CREATE DATABASE IF NOT EXISTS sumitec_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'sumitec_user'@'localhost'
IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON sumitec_db.* TO 'sumitec_user'@'localhost';
FLUSH PRIVILEGES;
