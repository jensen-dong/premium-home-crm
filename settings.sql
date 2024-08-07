-- settings.sql
CREATE DATABASE crm;
CREATE USER crmuser WITH PASSWORD 'designer';
GRANT ALL PRIVILEGES ON DATABASE crm to crmuser;