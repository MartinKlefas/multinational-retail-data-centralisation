import yaml, sqlalchemy
import pandas as pd



class DatabaseConnector:

    def read_db_creds (self):
        stream = open('db_creds.yaml', 'r') 
        credentials = yaml.safe_load(stream)
        return credentials

    def init_db_engine(self):
        dictCredentials = self.read_db_creds()
        connectionString = "postgresql+psycopg2://" + dictCredentials["RDS_USER"] + ":" + dictCredentials["RDS_PASSWORD"]
        connectionString += "@" + dictCredentials["RDS_HOST"] + ":" + str(dictCredentials["RDS_PORT"]) + "/" + str(dictCredentials["RDS_DATABASE"])
        
    
        engine = sqlalchemy.create_engine(connectionString)
        return engine
    
    def list_db_tables (self, engine: sqlalchemy.engine.Engine):
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND     schemaname != 'information_schema';"))
            table_names = list()
            for row in result:
                table_names.append(row[1])
            
            return table_names
    
    def read_rds_table(self,engine,table_name):     
        frame = pd.read_sql_table(table_name,con=engine.connect())
        return frame
    
    def upload_to_db(self,df: pd.DataFrame,table_name: str):
        dictCredentials = self.read_db_creds()

        connectionString = "postgresql+psycopg2://" + str(dictCredentials["LOCAL_USER"]) + ":" + str(dictCredentials["LOCAL_PASSWORD"])
        connectionString += "@localhost:" + str(dictCredentials["LOCAL_PORT"]) + "/" + str(dictCredentials["LOCAL_DATABASE"])
        
    
        engine = sqlalchemy.create_engine(connectionString)
       # with engine.connect() as connection:
            
        created = df.to_sql(table_name,con=engine,if_exists="replace",index=False)
       # print("Created %s lines." % created)
