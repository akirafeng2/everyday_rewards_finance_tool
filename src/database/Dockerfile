FROM postgres:15.4-bookworm

ENV POSTGRES_PASSWORD=root

ENV POSTGRES_USER=root

ENV POSTGRES_DB=finance_db

COPY setup.sql /docker-entrypoint-initdb.d/
