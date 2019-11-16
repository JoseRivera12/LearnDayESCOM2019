<div align="center">
  <h1>LearnDay ESCOM 2019 Flask APP</h1>
</div>

## Prerequisitos
Antes de ejectuar este proyecto, necesitarás instalar en tu computadora software adicional.

## Python 3
## PostgreSQL
## Flask
## Virtualenv

#### 1. Clonamos el repositorio (o usa tu propio fork):

```sh
$ git clone https://github.com/JoseRivera12/LearnDayESCOM2019.git
```

#### 2. Entramos al directorio

```sh
 cd LearnDayESCOM2019
```

#### 3. Instalar todas las dependencias:

```sh
 $ pip3 install virtualenv 
 $ virtualenv nombredelentorno
 $ source nombredelentorno/bin/activate
 $ pip3 install -r requeriments.txt
```

#### 4. Definir las variables de entorno. 
Por seguridad ponemos por separado las variables mas importantes de nuestro proyecto.

Ejemplo:
```sh
# Linux
export SECRET_KEY='7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
export BD_NAME='learndaydb'
export BD_USER='learnday'
export BD_PASSWORD='l34rnd4y'
# Windows
set SECRET_KEY='7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
set BD_NAME='learndaydb'
set BD_USER='learnday'
set BD_PASSWORD='l34rnd4y'
```

Finalmente guarda los cambios en el archivo y ejecuta el siguiente comando

```source variables.sh
```

## NOTA en caso de un reinicio de tu servidor deberas ejecutar nuevamente el script
#### 5. Instalar POSTGRES:

```sh
$ sudo apt-get install postgresql postgresql-contrib libpq-dev
$ libpq-dev
```

#### Crear la base de datos y usuario PostgreSQL :

```sh
$ sudo -u postgres createuser learnday 
$ sudo -u postgres createdb learndaydb
$ sudo -u postgres psql
psql=# alter user learnday with encrypted password 'learndaydb';
psql=# grant all privileges on database learndaydb to learnday ;
```

#### Exportamos variables para correr servidor de flask
```sh
$export FLASK_ENV="development"
$export FLASK_APP="main.py"
```

#### Creamos migraciones a la base de datos
```sh
$flask db init
$flask db migrate -m "mensaje migracion"
$flask db upgrade
```

#### Creamos migraciones a la base de datos
```sh
flask run
```
