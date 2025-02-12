# Voting app

This Voting App allows users to create polls, view existing polls, and vote on available options. It is a full-stack application with a Flask backend and a Streamlit frontend, utilizing MySQL for data storage. Below are the steps to set up, configure, and use the app.

## Prerequisites

Before you start, ensure you have the following tools installed:

- **Python 3.x** (preferred version: 3.8+)
- **MySQL** (or a MySQL-compatible database)
- **MySQL Connector for Python** (for interacting with MySQL)
- **Streamlit** (for the frontend)
- **Flask** (for the backend)
- **dotenv** (for environment variables)

# How to use the code (step by step):

### Log in to the root user. (When prompted for password just press Enter)

```bash
mysql -u root -p
```

### **Create a Database**

```sql

CREATE DATABASE my_poll_database;

```

### **Create a New User (choose whatever username and password you want)**

```sql

CREATE USER 'poll_user'@'localhost' IDENTIFIED BY 'poll_password';

```

### **Grant Permissions to the New User**

```sql
GRANT ALL PRIVILEGES ON my_poll_database.* TO 'poll_user'@'localhost';
```

```sql
FLUSH PRIVILEGES;
```

✅ Now, poll_user can access and manage the my_poll_database database.

### Select the database:

```bash
USE my_poll_database;
```

### Create a table:

```bash
CREATE TABLE my_poll_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    option_1 VARCHAR(255) NOT NULL,
    option_2 VARCHAR(255) NOT NULL,
    votes_1 INT DEFAULT 0,
    votes_2 INT DEFAULT 0
);

```

## Set up Environment Variables

1. In the root directory of your project, create a `.env` file.
2. Add the following environment variables to the `.env` file:
    
    ```bash
    
    DB_HOST=localhost
    DB_USER=poll_user             # Or your MySQL username
    DB_PASSWORD=poll_password     # Your MySQL password
    DB_NAME=my_poll_database         # Name of your MySQL database
    DB_TABLE=my_poll_table           # Name of your MySQL table
    API_URL=http://127.0.0.1:5000   # Flask backend URL
    
    ```
    

## Run the App

```bash
python3 start_app.py
```