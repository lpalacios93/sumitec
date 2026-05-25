# SUMITEC - Sistema Interno Comercial

Aplicacion web interna para clientes, productos, bodegas, proformas, compatibilidades, reportes y respaldos.

## Tecnologia base

- Python 3.12+
- Django 5.2
- MySQL
- Interfaz web responsive
- Git y GitHub para control de versiones

## Instalacion inicial en Windows

1. Instalar Python desde `https://www.python.org/downloads/`.
   - Marcar la opcion `Add Python to PATH`.

2. Instalar Git desde `https://git-scm.com/download/win`.

3. Instalar MySQL Community Server desde `https://dev.mysql.com/downloads/mysql/`.

4. Crear base de datos y usuario en MySQL:

```sql
CREATE DATABASE sumitec_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sumitec_user'@'localhost' IDENTIFIED BY 'cambiar_password';
GRANT ALL PRIVILEGES ON sumitec_db.* TO 'sumitec_user'@'localhost';
FLUSH PRIVILEGES;
```

5. Crear entorno virtual e instalar dependencias dentro de la carpeta del proyecto:

```powershell
.\scripts\install_local.ps1
```

Si PowerShell bloquea el script, ejecutar una sola vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

6. Copiar la plantilla de variables si el script no lo hizo:

```powershell
Copy-Item .env.example .env
```

7. Editar `.env` y colocar la clave, usuario y contrasena reales de MySQL.

8. Crear base de datos y usuario de MySQL.

Primero editar `scripts/setup_mysql.sql` y cambiar `cambiar_esta_contrasena` por una contrasena real.

Luego ejecutar:

```powershell
& "C:\Program Files\MySQL\MySQL Server 9.7\bin\mysql.exe" -u root -p < scripts\setup_mysql.sql
```

9. Validar Django:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

10. Ejecutar migraciones iniciales:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

11. Crear primer administrador:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

12. Levantar servidor local:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

Desde la misma PC:

```text
http://127.0.0.1:8000
```

Desde otra computadora o celular en la misma red:

```text
http://IP-DE-LA-PC:8000
```

## GitHub

Cuando Git este instalado:

```powershell
git init
git add .
git commit -m "Crear base inicial del sistema SUMITEC"
```

Luego se crea un repositorio en GitHub y se conecta:

```powershell
git remote add origin URL_DEL_REPOSITORIO
git branch -M main
git push -u origin main
```

## Modulos planificados

- `accounts`: usuarios, roles y permisos.
- `customers`: clientes.
- `catalog`: productos, categorias, marcas, proveedores, bodegas y stock.
- `imports`: importacion Excel.
- `quotes`: proformas.
- `compatibility`: compatibilidades y busqueda inteligente.
- `reports`: reportes.
- `backups`: respaldos y restauracion.
- `audit`: bitacora de acciones.
