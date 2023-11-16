import psycopg2


class DatabaseConnection:
    def __init__(self, connection_details: dict, env, profile_id: str):
        self.connection_details = connection_details
        self.profile_id = profile_id
        self.conn = None
        self.cursor = None
        self.env = env

    def __enter__(self):
        self.conn = psycopg2.connect(**self.connection_details)
        self.cursor = self.conn.cursor()
        search_path_execute = """SET search_path TO %s;"""
        self.cursor.execute(search_path_execute, (self.env,))

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred")

    def commit_changes(self):
        self.conn.commit()
