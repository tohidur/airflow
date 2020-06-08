cd /opt

sudo mkdir /opt/urbanpiper

cd urbanpiper

sudo chown -R ubuntu:ubutnu urbanpiper/

cd urbanpiper

mkdir airflow

export AIRFLOW_HOME=/opt/urbanpiper/airflow


sudo apt update
sudo apt -y upgrade
python3 -V
sudo apt install -y python3-pip
sudo apt install build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y python3-venv
python3.6 -m venv venv


####  Mysql
- To remove
    - sudo apt-get purge mysql*
    - sudo apt-get autoremove
    - sudo apt-get autoclean
    - sudo apt-get dist-upgrade

- Install
    - sudo apt update
    - sudo apt install mysql-server

- Configure
    - sudo mysql_secure_installation
        - When asking for password give a valid password and remember that.
        - Here select all default options.

    - mysqld --initialize
        - to initialize data directory. This is will throw error if already initialized. Don't worry about that.

    - To authenticate using root user.
        - sudo mysql
        - `SELECT user,authentication_string,plugin,host FROM mysql.user;`
            - Here you will see root user is using - auth_socket plug in.
        - `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';`
        - `FLUSH PRIVILEGES;`
            - To reload the grant tables and put new changes into effect.
        - mysql -u root -p
        - `CREATE USER 'upuser'@'localhost' IDENTIFIED BY 'password';`
        - `GRANT ALL PRIVILEGES ON *.* TO 'upuser'@'localhost' WITH GRANT OPTION;`
        - `FLUSH PRIVILEGES;`

    - Allow 3306 port on server and allow remote login if you need it.

    - Airflow DB
        - `CREATE DATABASE airflow CHARACTER SET utf8 COLLATE utf8_unicode_ci;`
        - `CREATE USER 'airflow'@'localhost' identified by 'Up123pU';`
        - `GRANT ALL PRIVILEGES on * . * to 'airflow'@'localhost';`
        - `FLUSH PRIVILEGES;`

#### RabbitMQ
- Install
    - `sudo apt install rabbitmq-server`

- SetUp
    - `sudo rabbitmqctl add_user urbanpiper urbanpiper`
    - `sudo rabbitmqctl add_vhost uphost`
    - `sudo rabbitmqctl set_permissions -p uphost urbanpiper ".*" ".*" ".*"`  

- Setup rabbitmq-management and admin
    - `sudo rabbitmq-plugins enable rabbitmq_management`
    - `sudo rabbitmqctl add_user admin password`
    - `sudo rabbitmqctl set_user_tags admin administrator`
    - `sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"`

#### Airflow Configuration changes
- Source venv
- `pip install -r requirements.txt`
- `pip uninstall SQLAlchemy && pip install SQLAlchemy==1.3.15`
- `vi ~/airflow/airflow.cfg`
    - `executor = CeleryExecutor`
    - `sql_alchemy_conn = mysql://airflow:airflow@localhost:3306/airflow`
    - `broker_url = amqp://guest:guest@localhost:5672/`
- `airflow initdb`
- `airflow webserver` | `airflow worker` | `airflow scheduler`
