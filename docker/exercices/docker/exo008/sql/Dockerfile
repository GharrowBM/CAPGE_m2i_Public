FROM mysql 

ENV MYSQL_DATABASE=todo_db
ENV MYSQL_ROOT_PASSWORD=password

COPY create_todo_items_table.sql /docker-entrypoint-initdb.d/create_todo_items_table.sql