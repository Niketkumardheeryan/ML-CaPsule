# DBGenie

DBGenie is a Python package that provides classes for automating database operations on MongoDB, PostgreSQL, and MySQL databases. The package provides easy-to-use classes that encapsulate common database operations, allowing developers to focus on building their applications rather than dealing with low-level database interactions.

## Installation

***You can install DBGenie using pip:***

```bash
pip install dbgenie2
```
## Key Features

- Support for Multiple Databases: DBGenie has support to MongoDB, PostgreSQL, and MySQL databases, providing a unified interface for CRUD operations across different database systems.

- Simple and Intuitive API: The package offers a straightforward API for performing CRUD operations, making it easy for developers to interact with databases without needing to write complex SQL queries or MongoDB commands.

- Automatic Connection Management: DatabaseCRUD handles database connection management, including connecting to the database, executing queries, and closing connections, ensuring efficient resource usage and preventing memory leaks.

- Flexible and Extensible: The package is designed to be flexible and extensible, allowing developers to customize and extend functionality as needed for their specific use cases.

## Workflow
DBGenie provides separate classes for each supported database system:

- MongoDBCrud:  for MongoDB databases
- PostgreSQLCrud: for PostgreSQL databases
- MySQLCrud: for MySQL databases

Each class encapsulates the common CRUD operations for its respective database system, including:

- Inserting documents/records
- Finding documents/records
- Updating documents/records
- Deleting documents/records

Developers can instantiate these classes, configure connection parameters, and use the provided methods to interact with their databases seamlessly.

## Usage
### 1. MongoDB
#### 1.1 CRUD Operations
```bash
from dbgenie2.mongodb.mongocrud import MongoDBCrud

# Connect to MongoDB
mongodb_crud = MongoDBCrud(uri="mongodb://localhost:27017", database="my_database", collection="my_collection")

# Insert document
mongodb_crud.insert_document({"name": "John", "age": 30})

# Find document
document = mongodb_crud.find_document({"name": "John"})
print(document)

# Update document
mongodb_crud.update_document({"name": "John"}, {"age": 35})

# Delete document
mongodb_crud.delete_document({"name": "John"})
```
### 2. PostgreSQl
#### 2.1 CRUD Operations
```bash
from dbgenie2.postgresql.postgrescrud import PostgreSQLCrud

# Connect to PostgreSQL
postgresql_crud = PostgreSQLCrud(host="localhost", user="postgres", password="password", database="my_database")

# Create table
postgresql_crud.create_table("my_table", ["id SERIAL PRIMARY KEY", "name VARCHAR(255)", "age INT"])

# Insert record
postgresql_crud.insert_record("my_table", (1, "John", 30))

# Read records
records = postgresql_crud.read_records("my_table")
print(records)

# Update record
postgresql_crud.update_record("my_table", {"age": 35}, "name='John'")

# Delete record
postgresql_crud.delete_record("my_table", "name='John'")
```
### 3. MySQL
#### 3.1 CRUD Operations
```bash
from dbgenie2.mysql.mysqlcrud import MySQLCrud

# Connect to MySQL
mysql_crud = MySQLCrud(host="localhost", user="root", password="password", database="my_database")

# Create table
mysql_crud.create_table("my_table", ["id INT AUTO_INCREMENT PRIMARY KEY", "name VARCHAR(255)", "age INT"])

# Insert record
mysql_crud.insert_record("my_table", (1, "John", 30))

# Read records
records = mysql_crud.read_records("my_table")
print(records)

# Update record
mysql_crud.update_record("my_table", {"age": 35}, "name='John'")

# Delete record
mysql_crud.delete_record("my_table", "name='John'")
```
## Deployment

### GitHub Actions PyPI Package Deployment
This project uses GitHub Actions for continuous integration and deployment to PyPI. The workflow defined in the .github/workflows/python-package.yaml file automates the deployment process whenever a new release tag is pushed to the repository.

#### Workflow Overview:
- Trigger: The workflow is triggered whenever a new release tag is pushed to the repository.
- Build and Test: The workflow first builds the package and runs tests to ensure everything is working as expected.
- Deployment to PyPI:
The workflow uses the pypa/gh-action-pypi-publish action to automatically deploy the package to PyPI.
It retrieves the package version from the release tag and publishes it to PyPI using the credentials configured in the repository secrets.
- Release Notes:
The workflow generates release notes based on the commits since the last release tag using the release-drafter action.
It includes the release notes in the GitHub release created for the new version.

#### How to Deploy:
To trigger a deployment to PyPI:

- Create a new release by pushing a new release tag to the repository.
- GitHub Actions will automatically run the deployment workflow.
- Once the workflow completes successfully, the package will be published to PyPI, and release notes will be generated and added to the GitHub release.

For more details on configuring and customizing the deployment workflow, refer to the .github/workflows/python-package.yaml file.

## Contributing

Contributions to DBGenie are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or submit a pull request. See the Contributing Guidelines for more information.

- Fork the repository
- Create your feature branch (git checkout -b feature/YourFeature)
- Commit your changes (git commit -m 'Add some feature')
- Push to the branch (git push origin feature/YourFeature)
- Create a new Pull Request

## License
DBGenie is licensed under the MIT License. See the LICENSE file for details.


