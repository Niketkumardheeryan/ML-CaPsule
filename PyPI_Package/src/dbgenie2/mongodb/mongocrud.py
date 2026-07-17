from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDBCrud:
    """
    A class for performing CRUD (Create, Read, Update, Delete) operations on a MongoDB database.

    Attributes:
        uri (str): The MongoDB connection URI.
        database (str): The name of the MongoDB database.
        collection (str): The name of the MongoDB collection.

    Methods:
        insert_document: Inserts a document into the collection.
        find_document: Finds a single document in the collection based on the query.
        find_documents: Finds multiple documents in the collection based on the query.
        update_document: Updates documents in the collection based on the query.
        delete_document: Deletes documents from the collection based on the query.
    """

    def __init__(self, uri, database, collection):
        """
        Initializes the MongoDBCRUD object with connection parameters.

        Args:
            uri (str): The MongoDB connection URI.
            database (str): The name of the MongoDB database.
            collection (str): The name of the MongoDB collection.
        """
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[database]
        self.collection = self.db[collection]

    def insert_document(self, document):
        """
        Inserts a document into the collection.

        Args:
            document (dict): The document to insert into the collection.
        """
        self.collection.insert_one(document)

    def find_document(self, query):
        """
        Finds a single document in the collection based on the query.

        Args:
            query (dict): The query to find the document.

        Returns:
            dict: The found document.
        """
        return self.collection.find_one(query)

    def find_documents(self, query):
        """
        Finds multiple documents in the collection based on the query.

        Args:
            query (dict): The query to find the documents.

        Returns:
            list: A list of found documents.
        """
        return list(self.collection.find(query))

    def update_document(self, query, update_data):
        """
        Updates documents in the collection based on the query.

        Args:
            query (dict): The query to select documents to be updated.
            update_data (dict): The data to update the selected documents.
        """
        self.collection.update_many(query, {"$set": update_data})

    def delete_document(self, query):
        """
        Deletes documents from the collection based on the query.

        Args:
            query (dict): The query to select documents to be deleted.
        """
        self.collection.delete_many(query)
