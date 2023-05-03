-- tableInit.sql
-- This file creates the necessary tables for Little-League

CREATE TABLE user (
        email varchar(255) PRIMARY KEY,
        name varchar(255),
        password varchar(255),
        username varchar(255) UNIQUE NOT NULL,
        team varchar(3)
    );

CREATE TABLE userquery (
        queryID int(13) auto_increment PRIMARY KEY,
        username varchar(255) NOT NULL,
        team varchar(3),
        year smallint(6),
        time time
    );
