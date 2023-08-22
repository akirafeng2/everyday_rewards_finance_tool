# import psycopg2
from login_details import database_connection_details
from receipts.reciept_reader import data

# conn = psycopg2.connect(**database_connection_details)

# cursor = conn.cursor()

# cursor.execute("select version()")

# # Fetch a single row using fetchone() method.
# data = cursor.fetchone()
# print("Connection established to: ",data)

# #Closing the connection
# conn.close()

from finance_tool import DatabaseConnection

data_connect = DatabaseConnection(database_connection_details)

with data_connect:
    data_connect.test_connection()
    # data_connect.drop_schema("test")
    # data_connect.create_schema("test")
    # data_connect.create_items_table("test", "test_table")
    # data_connect.insert_df_items_into_table(data, "test.test_table")

    test_statement = """SELECT * FROM test.test_table"""
    data_connect.cursor.execute(test_statement)
    results = data_connect.cursor.fetchall()
    print(results)