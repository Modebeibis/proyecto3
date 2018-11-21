## Instrucciones temporales para los miembros del equipo para correr la base de datos:

- Instalar postgres:
```Bash
$sudo apt install postgresql
```

- Crear la base de datos:
```Bash
$ psql
postgres=# CREATE DATABASE db_red_investigadores;
postgres=# \q
```

Modificar `DATABASES` en RedInvestigadores/settings.py:
```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_red_investigadores',
        'USER': 'username',                       #El username que usan para postgres
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Migrar la base de datos y cargar algunos datos de prueba:
```Bash
$ python3 manage.py migrate
$ python3 manage.py makemigrations core
$ python3 manage.py sqlmigrate core 0001
$ python3 manage.py migrate
& python3 manage.py loaddata info_prueba
```

No debería de haberse copiado ningun archido de migración al repositorio,
en caso de que haya alguno, podría generar errores al hacer las migraciones,
sólo borren el directorio /RedInvestigadores/core/migrations/

La base de datos ya debería de funcionar, puede verificarse su
funcionalidad usando
```Bash
$ python manage.py shell
```

# Poblar la Base de Datos
* La base de datos ya debió de haber sido creada y migrada
```Bash
$ python manage.py shell < core/seeder.py
```
