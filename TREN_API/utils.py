from pymongo import MongoClient
from environs import Env, EnvError
from pymongo.errors import ConnectionFailure

def load_env_variables():
    try:
        env = Env()
        env.read_env()

        # Django config
        env.str("MODE")
        env.str("DJ_SECRET")

        # MongoDB config
        env.str("MONGODB_NAME")
        env.str("MONGODB_URI")

        # SQL config
        env.str("MYSQL_NAME")
        env.str("MYSQL_USER")
        env.str("MYSQL_PASSWORD")
        env.str("MYSQL_HOST")
        env.int("MYSQL_PORT")

    except EnvError as e:
        print(f"Environment configuration error: {e}")

    finally:
        return env.dump()

def get_db_handle(connection_string=None,db_name="TREN"):
    client = MongoClient(connection_string)

    db_handle = client[db_name]
    return db_handle, client

def check_mongo_connection(connection_string=None):
    try:
        # Connect to the MongoDB server
        client = MongoClient(connection_string)
        
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        print("MongoDB connection successful")
        
        # Optionally, you can return the client object to use it for further operations
        return True
    
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return False

ENV_VARS = load_env_variables()