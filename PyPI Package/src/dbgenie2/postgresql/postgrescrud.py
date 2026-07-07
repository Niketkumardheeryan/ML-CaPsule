import psycopg2
from psycopg2 import sql


class PostgreSQLCrud:
    """
    A class for performing CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database.

    Attributes:
        dbname (str): The name of the database.
        user (str): The username for accessing the database.
        password (str): The password for accessing the database.
        host (str): The host address of the database.
        port (str): The port number of the database.

    Methods:
        connect: Connects to the PostgreSQL database.
        disconnect: Disconnects from the PostgreSQL database.
        execute_query: Executes an SQL query on the database.
        create_table: Creates a new table in the database.
        insert_record: Inserts a new record into a table.
        read_records: Reads records from a table.
        update_record: Updates existing records in a table.
        delete_record: Deletes records from a table.
    """

    def __init__(self, dbname, user, password, host, port):
        """
        Initializes the PostgreSQLCrud object with connection parameters.

        Args:
            dbname (str): The name of the database.
            user (str): The username for accessing the database.
            password (str): The password for accessing the database.
            host (str): The host address of the database.
            port (str): The port number of the database.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """
        Connects to the PostgreSQL database.
        """
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        print("Connected to PostgreSQL database")

    def disconnect(self):
        """
        Disconnects from the PostgreSQL database.
        """
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from PostgreSQL database")

    def execute_query(self, query, params=None):
        """
        Executes an SQL query on the database.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to be used in the query.

        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        print("Query executed successfully")

    def create_table(self, table_name, columns):
        """
        Creates a new table in the database.

        Args:
            table_name (str): The name of the table to create.
            columns (list): A list of column definitions for the table.

        """
        columns_str = ', '.join(columns)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(columns_str)
        )
        self.execute_query(query)

    def insert_record(self, table_name, values):
        """
        Inserts a new record into a table.

        Args:
            table_name (str): The name of the table to insert into.
            values (tuple): A tuple containing the values to insert into the table.

        """
        placeholders = ', '.join(['%s'] * len(values))
        query = sql.SQL("INSERT INTO {} VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(placeholders)
        )
        self.execute_query(query, values)

    def read_records(self, table_name):
        """
        Reads records from a table.

        Args:
            table_name (str): The name of the table to read records from.

        Returns:
            list: A list of tuples, each tuple representing a record from the table.

        """
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def update_record(self, table_name, update_values, condition):
        """
        Updates existing records in a table.

        Args:
            table_name (str): The name of the table to update records in.
            update_values (dict): A dictionary containing column names as keys and new values as values.
            condition (str): The condition to select records to be updated.

        """
        set_str = ', '.join([f"{column} = %s" for column in update_values.keys()])
        query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            sql.Identifier(table_name),
            sql.SQL(set_str),
            sql.SQL(condition)
        )
        values = list(update_values.values())
        self.execute_query(query, values)

    def delete_record(self, table_name, condition):
        """
        Deletes records from a table.

        Args:
            table_name (str): The name of the table to delete records from.
            condition (str): The condition to select records to be deleted.

        """
        query = sql.SQL("DELETE FROM {} WHERE {}").format(
            sql.Identifier(table_name),
            sql.SQL(condition)
        )
        self.execute_query(query)
