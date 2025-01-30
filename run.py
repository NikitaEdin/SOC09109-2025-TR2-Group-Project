from app import app
from create_db import create_database, load_environment, create_env_file

if __name__ == "__main__":
    # Always create the database when the app starts
    create_env_file() 
    load_environment() 
    create_database()
    app.run(debug=True)
