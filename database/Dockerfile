FROM mysql/mysql-server

ENV MYSQL_DATABASE=TEST_MET11 \
 MYSQL_ROOT_PASSWORD=root \
 MYSQL_ROOT_HOST=%
ADD test_database.sql /docker-entrypoint-initdb.d
EXPOSE 3306