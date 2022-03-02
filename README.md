## To start the project you need to:

1.Build docker compose:

> docker-compose build

2.Start database container:

> docker-compose up db

3. In another terminal tab create database:

>docker-compose exec db mysql -u root -p -e 'CREATE DATABASE IF NOT EXISTS `coins` DEFAULT CHARACTER SET = `utf8mb4`'

4. And grant privileges on test database creation for pytest:

>docker-compose exec db mysql -u root -p -e 'GRANT ALL PRIVILEGES ON test_coins.* TO `username`'

5. Start django app container:

>docker-compose up app

6. In another terminal tab create superuser to be able to use admin panel:

>docker-compose exec app python manage.py createsuperuser

7. (optionally) If you want to get inside app container bash, run this command:

>docker exec -it coins-backend_app_1 bash

8. (optionally) To apply fixtures and fill database with data, run this command inside app container:

>python manage.py loaddata fixtures.json

9.  (optionally) To run pytest suit, run this command inside app container:

>pytest

10. (optionally) To create your own fixtures, run this command inside app container:

>python manage.py dumpdata --indent  4 > new_fixtures.json




### some commands, that may be useful during development or setup

Solve linux problem with mysql:

>sudo apt-get install libmysqlclient-dev

Mysql user creation:

>CREATE USER 'username' IDENTIFIED BY 'password';
>GRANT ALL PRIVILEGES ON coins.* TO 'username';

Fix readonly status for migrations, etc.:

>sudo chown -R $(whoami) .