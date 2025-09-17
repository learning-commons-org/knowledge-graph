# PostgreSQL Import Guide

This guide provides instructions for loading the Learning Commons Knowledge Graph dataset into a PostgreSQL database.

## Prerequisites

- A running PostgreSQL instance. If you don't have PostgreSQL installed locally, you can use Docker to run a PostgreSQL container. For detailed instructions on setting up and running PostgreSQL with Docker, refer to the [official PostgreSQL Docker documentation](https://hub.docker.com/_/postgres).
- Downloaded CSV data files (see the [main README](../../README.md) for download instructions)

## Setup Steps

### 1. Create Database and Tables

First create a dedicated database if that's preferred:

```bash
psql -U <username> -c "CREATE DATABASE <database>;"
```

Then connect to your PostgreSQL database and create the necessary tables by running:

```bash
psql -U <username> -d <database> -f create_tables.sql
```

Or execute the SQL file content directly in your PostgreSQL client. See `create_tables.sql` for the complete table definitions.

### 2. Load CSV Data

After creating the tables, load the data:

1. **⚠️ IMPORTANT: Update the file paths in `load_data.sql` to point to your downloaded CSV files**
2. Execute the load script:

```bash
psql -U <username> -d <database> -f load_data.sql
```

**Note**: Ensure PostgreSQL has read access to the file paths specified in the load script.

## Query Examples

Once the data is loaded, you can run queries to explore the tables:

```sql
-- List all tables
\dt

-- Sample data queries
SELECT * FROM standards_framework LIMIT 10;
SELECT * FROM standards_framework_item LIMIT 10;
SELECT * FROM learning_component LIMIT 10;
SELECT * FROM relationships LIMIT 10;
```

## Docker PostgreSQL Setup

If using Docker PostgreSQL, you can connect using:

```bash
docker exec -it <container-name> psql -U <username> -d <database>
```
