import mysql.connector


class MySQLCrud:
    """
    A class for performing CRUD (Create, Read, Update, Delete) operations on a MySQL database.

    Attributes:
        host (str): The hostname of the MySQL server.
        user (str): The username for accessing the MySQL server.
        password (str): The password for accessing the MySQL server.
        database (str): The name of the MySQL database.

    Methods:
        connect: Connects to the MySQL database.
        disconnect: Disconnects from the MySQL database.
        execute_query: Executes an SQL query on the database.
        create_table: Creates a new table in the database.
        insert_record: Inserts a new record into a table.
        read_records: Reads records from a table.
        update_record: Updates existing records in a table.
        delete_record: Deletes records from a table.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the MySQLCrud object with connection parameters.

        Args:
            host (str): The hostname of the MySQL server.
            user (str): The username for accessing the MySQL server.
            password (str): The password for accessing the MySQL server.
            database (str): The name of the MySQL database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Connects to the MySQL database.
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Connected to MySQL database")

    def disconnect(self):
        """
        Disconnects from the MySQL database.
        """
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, parameters=None):
        """
        Executes an SQL query on the database.

        Args:
            query (str): The SQL query to execute.
            parameters (tuple, optional): The parameters to be used in the query.

        """
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
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
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.execute_query(query)

    def insert_record(self, table_name, values):
        """
        Inserts a new record into a table.

        Args:
            table_name (str): The name of the table to insert into.
            values (tuple): A tuple containing the values to insert into the table.

        """
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.execute_query(query, values)

    def read_records(self, table_name):
        """
        Reads records from a table.

        Args:
            table_name (str): The name of the table to read records from.

        Returns:
            list: A list of tuples, each tuple representing a record from the table.

        """
        query = f"SELECT * FROM {table_name}"
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
        query = f"UPDATE {table_name} SET {set_str} WHERE {condition}"
        values = list(update_values.values())
        self.execute_query(query, values)

    def delete_record(self, table_name, condition):
        """
        Deletes records from a table.

        Args:
            table_name (str): The name of the table to delete records from.
            condition (str): The condition to select records to be deleted.

        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute_query(query)
