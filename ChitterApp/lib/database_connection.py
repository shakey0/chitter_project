import os, psycopg
from flask import g
from psycopg.rows import dict_row


class DatabaseConnection:

    DEV_DATABASE_NAME = "chitter_project"
    TEST_DATABASE_NAME = "chitter_project_test"

    def __init__(self, test_mode=False):
        self.test_mode = test_mode

    def connect(self, provided_connection=None):

        if provided_connection is not None:
            try:
                self.connection = psycopg.connect(provided_connection, row_factory=dict_row)
            except psycopg.OperationalError:
                raise Exception(f"Couldn't connect to the database {self._database_name()}! " \
                                f"Did you create it using `createdb {self._database_name()}`?")
            return
        
        production = os.environ.get('PRODUCTION', False)
        testing_in_actions = os.environ.get('TESTING_IN_ACTIONS', False)
        
        if production:
            print("Production")
            connection_string = os.environ.get('DATABASE_URL', f"postgresql://chitter_docker:chitter_docker@host.docker.internal/{self._database_name()}")
        else:
            if testing_in_actions:
                print("Testing in GitHub Actions")
                connection_string = f"postgresql://postgres:postgres@postgres:5432/{self._database_name()}"
            else:
                print("Testing locally")
                connection_string = f"postgresql://localhost/{self._database_name()}"
        
        try:
            self.connection = psycopg.connect(connection_string, row_factory=dict_row)
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database {self._database_name()}! " \
                            f"Did you create it using `createdb {self._database_name()}`?")

    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    def executemany(self, query, params_list):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.executemany(query, params_list)
            self.connection.commit()

    CONNECTION_MESSAGE = '' \
        'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
        'the connection to the database was never opened. Did you ' \
        'make sure to call first the method DatabaseConnection.connect` ' \
        'in your app.py file (or in your tests)?'

    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)

    def _database_name(self):
        if self.test_mode:
            return self.TEST_DATABASE_NAME
        else:
            return self.DEV_DATABASE_NAME

def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection'):
        g.flask_database_connection = DatabaseConnection(
            test_mode=os.getenv('APP_ENV') == 'test')
        g.flask_database_connection.connect()
    return g.flask_database_connection
