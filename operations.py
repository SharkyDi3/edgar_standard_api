import os
import logging
from pymysql import cursors
from sqlalchemy.dialects import mysql
import pandas as pd
import mysql.connector
from urllib.parse import quote

from utils.errorcode import ErrorCodes
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

class Operations:
    def __init__(self):
        self.connection = None
        # self.engine = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.connect()

    def connect(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USERNAME,
                    password=quote(DB_PASSWORD),
                    database=DB_NAME,
                    port=DB_PORT
                )
                self.logger.info("Connected to the database.")
            except mysql.connector.Error as error:
                self.logger.error(f"Error connecting to the database: {error}")
        return self.connection

    def query_records(self, id):
        self.id = id
        try:
            connection = self.connect()
            query = f"SELECT * FROM {TABLE_NAME} LIMIT {id}"
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            for col in ['created_at', 'updated_at']:
                df[col] = df[col].astype(str)
            cursor.close()
            return df
        except mysql.connector.Error as error:
            self.logger.error(f"Exception in reading records: {error}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
        
    def update_record(self, id, filings, descr, filed_effective, file_film_number):
        self.filings = filings
        self.descr = descr
        self.filed_effective = filed_effective
        self.file_film_number = file_film_number
        self.id = id

        try:
            # Attempt to establish the connection
            connection = self.connect()
            if connection.is_connected():
                self.logger.info("Database connection established successfully.")

                query = f"""
                    UPDATE {TABLE_NAME}
                    SET filings = %s, 
                        descr = %s, 
                        filed_effective = %s, 
                        file_film_number = %s
                    WHERE id = %s;
                """
                cursor = connection.cursor(dictionary=True)
                
                # Execute the update query
                cursor.execute(query, (filings, descr, filed_effective, file_film_number, id))

                # Commit the transaction to ensure changes are saved
                connection.commit()
                
                # Optionally, you can fetch and print the updated record to verify
                cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (id,))
                result = cursor.fetchone()
                self.logger.info(f"Update result: {result}")
                # print(result)

                cursor.close()
                connection.close()
                self.logger.info("Database connection closed successfully.")
            else:
                self.logger.error("Failed to establish database connection.")
                return None

        except mysql.connector.Error as error:
            self.logger.error(f"Exception in updating records: {error}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None

    def delete_record(self, id):
        self.id = id

        try:
            # Attempt to establish the connection
            connection = self.connect()
            if connection.is_connected():
                self.logger.info("Database connection established successfully.")

                # Check if the record exists
                check_query = f"SELECT * FROM {TABLE_NAME} WHERE id = %s"
                cursor = connection.cursor(dictionary=True)
                cursor.execute(check_query, (id,))
                record = cursor.fetchone()

                if record is None:
                    self.logger.error(f"Record with id {id} does not exist.")
                    cursor.close()
                    connection.close()
                    return {"status": "error", "message": f"Record with id {id} does not exist."}

                # Proceed to delete the record
                delete_query = f"""
                    DELETE FROM {TABLE_NAME}
                    WHERE id = %s;
                """
                cursor.execute(delete_query, (id,))

                # Commit the transaction to ensure changes are saved
                connection.commit()

                # Optionally, you can check if the record was deleted
                cursor.execute(check_query, (id,))
                result = cursor.fetchone()
                if result is None:
                    self.logger.info(f"Record with id {id} deleted successfully.")
                    response = {"status": "success", "message": f"Record with id {id} deleted successfully."}
                else:
                    self.logger.error(f"Failed to delete record with id {id}.")
                    response = {"status": "error", "message": f"Failed to delete record with id {id}."}

                cursor.close()
                connection.close()
                self.logger.info("Database connection closed successfully.")
                return response

            else:
                self.logger.error("Failed to establish database connection.")
                return {"status": "error", "message": "Failed to establish database connection."}

        except mysql.connector.Error as error:
            self.logger.error(f"Exception in deleting record: {error}")
            return {"status": "error", "message": f"Exception in deleting record: {error}"}
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return {"status": "error", "message": f"Unexpected error: {e}"}

