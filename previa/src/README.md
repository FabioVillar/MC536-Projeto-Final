## Requisitos

* Python 
* Pipenv 
* MySQL
* MongoDB

## Instruções

### Para criar o banco de dados no mysql:

```
sudo /etc/init.d/mysql start
sudo -u root -p
mysql > create database womens_world_cup;

```

### Para criar tabelas no mysql:

No diretório `src`:
```
mysql -u root -p womens_world_cup < tables.sql

```
### Criar tabelas no mysql:

```sh
$ python sql_manager.py
```

Para utlizar esse script é necessário um arquivo .env, o qual deve conter o usuário mysql como 'mysql_user = "" ' e
a senha como 'mysql_password = "" '.

### Coleta de dados

Para coleta de dados utilzados no banco de dados:
```sh
$ python main.py
```


### Criar database e collection no MongoDB:

```sh
$ python mongo_manager.py

```

Caso não haja a database womens_world_cup e a collection world_cups no mongo, o script mongo_manger cria automaticamente ambos e insere os objetos.


Para rodar os scripts em python:

No diretório `src`:


### Inserir dados no mysql:
Sincronizar packages necessarios para rodar os programas .py:
```sh
$ pipenv sync -d
```

Criar ambiente virtualizado:
```sh
$  pipenv shell
```

Rodar script .py:
```sh
$  python <script.py>
```