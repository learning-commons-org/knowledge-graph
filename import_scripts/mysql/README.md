# MySQL Import Guide

This guide provides instructions for loading the Learning Commons Knowledge Graph dataset into a MySQL database.

## Prerequisites

- A running MySQL instance. If you don't have MySQL installed locally, you can use Docker to run a MySQL container. For detailed instructions on setting up and running MySQL with Docker, refer to the [official MySQL Docker documentation](https://hub.docker.com/_/mysql).
- Downloaded CSV data files (see the [main README](../../README.md) for download instructions)

## Setup Steps

### 1. Create Database and Tables

First create a dedicated database if that's preferred:

```bash
mysql -u <username> -p -e "CREATE DATABASE <database>;"
```

Then connect to your MySQL database and create the necessary tables by running:

```bash
mysql -u <username> -p <database> < create_tables.sql
```

Or execute the SQL file content directly in your MySQL client. See `create_tables.sql` for the complete table definitions.

### 2. Load CSV Data

After creating the tables, load the data:

1. **⚠️ IMPORTANT: Update the file paths in `load_data.sql` to point to your downloaded CSV files**
2. Enable local file loading on the server (if not already enabled):

```sql
mysql -u <username> -p -e "SET GLOBAL local_infile=1;"
```

3. Execute the load script with local file loading enabled:

```bash
mysql -u <username> -p <database> --local-infile=1 < load_data.sql
```

**Note**: The `local_infile` setting must be enabled on both the server (`SET GLOBAL local_infile=1`) and client (`--local-infile=1`) for `LOAD DATA LOCAL INFILE` to work.

## Query Examples

Once the data is loaded, you can run queries to explore the tables:

```sql
-- Show all tables
SHOW TABLES;

-- Sample data queries
SELECT * FROM standards_framework LIMIT 10;
SELECT * FROM standards_framework_item LIMIT 10;
SELECT * FROM learning_component LIMIT 10;
SELECT * FROM relationships LIMIT 10;
```

## Docker MySQL Setup

If using Docker MySQL, you can connect using:

```bash
docker exec -it <container-name> mysql -u <username> -p <database>
```
