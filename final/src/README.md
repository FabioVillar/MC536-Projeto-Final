## Requisitos

* Python 
* Pipenv 
* MySQL
* MongoDB

## Instruções

### Criar o banco de dados no mysql:

```
$ sudo /etc/init.d/mysql start
$ sudo -u root -p
$ mysql > create database womens_world_cup;
```

**IMPORTANTE: Certifique-se que o MySQL está ativo!**

### Criar tabelas no mysql:

No diretório `src`, uma vez que womens_world_cup ja foi criada:
```
$ mysql -u root -p womens_world_cup < tables.sql
```

### Rodar scripts em python:

No diretório `src`:

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

### Coleta de dados

Para coleta de dados (realização do Webscraping e montagem dos arquivos `.json`):

```sh
$ python main.py
```

### Preencher tabelas no mysql:

```sh
$ python sql_manager.py
```
**É importante ressaltar que o `user` e `password` sejam alterados dentro do arquivo `sql_manager.py`**:

~~~python
def sql_manager():

    user = "root" #your user here
    password = "password" #your password here
~~~


### Conectar o mongo no localhost

```sh
$ mongod
```


### Criar database e collection no MongoDB:

```sh
$ python mongo_manager.py
```

Caso não haja a database womens_world_cup e a collection world_cups no mongo, o script mongo_manger cria automaticamente ambos e insere os objetos.



