ALTER USER 'sumitec_user'@'localhost'
IDENTIFIED BY 'cambiar_esta_contrasena';

GRANT ALL PRIVILEGES ON sumitec_db.* TO 'sumitec_user'@'localhost';
FLUSH PRIVILEGES;
