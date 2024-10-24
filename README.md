# Blogs Project Configuration

This document provides a guide to configure and set up the PostgreSQL database connection for the Blogs project. Ensure that the following files are correctly updated with the necessary credentials and connection details.

## Configuration Details

### 1. `alembic.ini`

The `alembic.ini` file manages the database migration configurations. Update the `sqlalchemy.url` to reflect the connection settings for your PostgreSQL database:

```ini
sqlalchemy.url = postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```

For this project, modify the entry as follows:

```ini
sqlalchemy.url = postgresql://postgres:a@192.168.1.135:54322/blogs
```

### 2. Environment Variables (`.env`)

In the `.env` file, define the necessary environment variables for database connectivity. Ensure the following values are set:

```bash
POSTGRES_HOSTNAME=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=a
POSTGRES_PORT=54322
POSTGRES_DB=blogs
```

## Database Setup

1. **PostgreSQL**  
   Ensure PostgreSQL is running on the specified host and port. Update the database credentials and connection settings as needed in both the `alembic.ini` and `.env` files.
   
2. **Alembic**  
   After configuring the `alembic.ini` file, you can run Alembic to handle migrations. Use the following commands:

   ```bash
   alembic upgrade head
   ```

   This will apply the latest migrations to the specified PostgreSQL database.
