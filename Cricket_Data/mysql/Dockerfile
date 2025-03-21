FROM mysql:8.2.0

# Copy initialization script
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Copy setup SQL file
COPY db/setup_cricket_db.sql /docker-entrypoint-initdb.d/

# Create directory and copy test data
RUN mkdir -p /var/lib/mysql-files/test_data
COPY db/test_data/*.csv /var/lib/mysql-files/test_data/

EXPOSE 3306

CMD ["/init.sh"]

