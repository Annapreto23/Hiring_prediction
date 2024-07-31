import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, text

def create_database(mysql_config, db_name):
    """
    Creates a database if it does not exist.

    Parameters:
    mysql_config (dict): Dictionary containing MySQL connection parameters.
    db_name (str): Name of the database to be created.
    """
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Database {db_name} created successfully.")

def create_table_from_csv(csv_file, table_name, mysql_config, db_name):
    """
    Creates a table based on the structure of a CSV file.

    Parameters:
    csv_file (str): Path to the CSV file.
    table_name (str): Name of the table to be created.
    mysql_config (dict): Dictionary containing MySQL connection parameters.
    db_name (str): Name of the database where the table will be created.
    """
    # Read the CSV file to get the column structure
    df = pd.read_csv(csv_file)
    
    # Build the CREATE TABLE query
    columns = df.columns
    column_types = []
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_type = "DOUBLE"
        else:
            col_type = "VARCHAR(255)"
        column_types.append(f"{col} {col_type}")
    columns_def = ", ".join(column_types)
    
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns_def}
    );
    """
    
    # Create a database connection and execute the query
    engine = create_engine(f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{db_name}", echo=False)
    with engine.connect() as connection:
        connection.execute(text(create_table_query))
    print(f"Table {table_name} created successfully.")

def import_csv_to_mysql(csv_file, table_name, mysql_config, db_name):
    """
    Imports data from a CSV file into a MySQL table.

    Parameters:
    csv_file (str): Path to the CSV file.
    table_name (str): Name of the table where data will be imported.
    mysql_config (dict): Dictionary containing MySQL connection parameters.
    db_name (str): Name of the database where the table is located.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create a database connection
    engine = create_engine(f"mysql+mysqlconnector://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{db_name}", echo=False)
    
    # Insert data into the table
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print(f"Data imported successfully into {table_name} table.")


# MySQL connection configuration
mysql_config = {
    'user': 'root',
    'password': 'philo',
    'host': 'localhost'
}

# Database and table names
db_name = 'recruitment'
table_name = 'hiring_decisions'

# Path to the CSV file
csv_file = 'recruitment_data.csv'

# Create the database
#create_database(mysql_config, db_name)

# Create the table from the CSV file
#create_table_from_csv(csv_file, table_name, mysql_config, db_name)

# Import the CSV data into the database
#import_csv_to_mysql(csv_file, table_name, mysql_config, db_name)
