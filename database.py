import pyodbc


class DatabaseConnection:

    def __init__(self):
        DRIVER_NAME = 'SQL SERVER'
        SERVER_NAME = '172.20.0.101\MSSQLSERVER19'
        DATABASE_NAME = 'ChatBotDB'
        UID = 'sa'
        PWD = 'sa@#1234#@'

        self.command: str

        connection_string = f"""
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            UID={UID};
            PWD={PWD};
            """

        connection_string1 = f"""
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};            
            """
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    def get_records(self):
        self.cursor.execute(self.command)

    def insert_record(self):
        self.cursor.execute(self.command)
    
    def execute_command(self, parameters):
        self.cursor.execute(self.command, params=parameters)
    
    def execute_command(self):
        self.cursor.execute(self.command)
