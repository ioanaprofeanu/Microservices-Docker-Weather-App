-- init.sql

-- Create schema weather_forecast_schema if it does not exist
\c weather_forecast_db;

-- CREATE SCHEMA IF NOT EXISTS weather_forecast_schema;

-- -- Set the search path to the weather_forecast_schema schema
-- SET search_path TO weather_forecast_schema;

-- Create table Tari
CREATE TABLE IF NOT EXISTS Tari (
    id SERIAL PRIMARY KEY,
    nume_tara VARCHAR(255) UNIQUE NOT NULL,
    latitudine DECIMAL(9,6),
    longitudine DECIMAL(9,6)
);

-- Create table Orase
CREATE TABLE IF NOT EXISTS Orase (
    id SERIAL PRIMARY KEY,
    id_tara INTEGER REFERENCES Tari(id) ON DELETE CASCADE,
    nume_oras VARCHAR(255) NOT NULL,
    latitudine DECIMAL(9,6),
    longitudine DECIMAL(9,6),
    UNIQUE (id_tara, nume_oras)
);

-- Create table Temperaturi
CREATE TABLE IF NOT EXISTS Temperaturi (
    id SERIAL PRIMARY KEY,
    valoare DECIMAL(5,2),
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    id_oras INTEGER REFERENCES Orase(id) ON DELETE CASCADE,
    UNIQUE (id_oras, timestamp)
);

-- -- Exit from the weather_forecast_schema schema
-- SET search_path TO public;
