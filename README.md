# Proyecto 3: Red de Investigadores
## UNAM, Facultad de Ciencias
## Modelado Y Programación

_Repositorio para el tercer proyecto en el curso de modelado y programación de Canek Peláez_

# Comenzando 🚀

## Pre-requisitos 📋

* Python >= 3
* Django >= 2.1.3
* PostgreSQL >= 9.5.14
* Faker >= 1.0.1
* psycopg2 >= 2.7.6.1
* psycopg2-binary >= 2.7.6.1
* django-allauth >= 0.38.0

# Instalación

## Por medio de ```PIP3```
* Django
* Faker
* django-allauth
* psycopg2
* psycopg2-binary

## PostgreSQL
En la mayoría de los sistemas operativos hoy disponibles, el manejador de base de datos PostgreSQL ya se encuentra instalado por omisión. Sin embargo si este no es el caso, por favor checar el siguiente enlace en donde se encuentra toda la documentación necesaría: [postgresql](https://www.postgresql.org/docs/9.3/tutorial-install.html).

# Poner en marcha el sistema
* Crear la base de datos con PostgreSQL
```bash
$ psql
postgres=# CREATE DATABASE db_red_investigadores;
postgres=# \q
```
* Modificar el archivo ```RedInvestigadores/settings.py```
```python3
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_red_investigadores',
        'USER': 'postgres',    #El username que usan para postgres
        'PASSWORD': '',
        'HOST': '127.0.0.1',   #El servidor en donde se encuentra la BDD
        'PORT': '5432', #El puerto al que se conecta
    }
}
...
```
* Migrar la base de datos
```bash
$ python3 manage.py makemigrations core
$ python3 manage.py migrate core
$ python3 manage.py sqlmigrate core 0001
$ python3 manage.py migrate
```

* Cargar los datos necesarios para su correcto funcionamiento
```bash
$ python3 manage.py loaddata states
$ python3 manage.py loaddata roles
$ python3 manage.py loaddata journals
$ python3 manage.py loaddata affiliations
```

# Comenzar a usar el sistema
Para empezar a utilizar el sistema lo único que se necesita hacer es levantarlo en un servidor, es decir:
```bash
$ python3 manage.py runserver
```

## Confirmación de registro por medio de correo electrónico
Nuestro sistema permite que un usuario tenga que confirmar su registro por medio de un enlace que recibe mediante un correo electrónico.
Para lograr que esto funcione, se necesita:
* Tener al menos un superusuario ó administrador en la base de datos
* Iniciar sesión con la cuenta del administrador
* Ingresar a la sección ```Sites```
* Cambiar la dirección que se encuentra ahí por la del servidor junto con el puert que será usado (ej: ```127.0.0.1:8080```)

Y listo, todo usuario que se registra ahora recibirá un enlace con dirección que registró.

# Utilidades

## Poblar la Base de Datos
Se crearon ```seeders``` que nos permiten poblar la base de datos con registros falsos, usando ```Faker```, para probar que su funcionamiento fuera el indicado. Para esto es necesario que la BDD ya hubiese sido creada y migrada.
```bash
$ python3 manage.py shell < core/seeder.py
```
Este proceso puede tomar unos minutos, ya que se estan insertando más de 1000 registros en la BDD.


# Autores ✒️
* **Mauricio Carrasco Ruiz** - [GrayCentipede](https://github.com/GrayCentipede)
* **Marco Antonio Cruz Maya** - [marco-cruzmaya](https://github.com/marco-cruzmaya)
* **José Ángel Correa García** - [AngelCorrea](https://github.com/AngelCorrea)
* **César Hernández Cruz** - [Japodrilo](https://github.com/Japodrilo)
* **Gisselle Ibarra Moreno** - [GisselleIb](https://github.com/GisselleIb)
* **Ramses Antonio López Soto** - [ramseslopez](https://github.com/ramseslopez)

#### Construido con mucho amor y dedicación <3
Los queremos mucho. Lo vemos en arquitectura, profesor :)
