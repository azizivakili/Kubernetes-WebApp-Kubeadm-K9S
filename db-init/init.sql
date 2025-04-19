-- db-init/init.sql
CREATE DATABASE azizik89db;

\c azizik89db;

CREATE TABLE azizik8stable (
    id SERIAL PRIMARY KEY,
    name TEXT
);
