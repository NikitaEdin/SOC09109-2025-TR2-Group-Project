import os
import secrets
from dotenv import load_dotenv
from app import app, db
from app.models import User, Role

# Generate default roles
GEN_ROLES = True
# Generate default users
GEN_USERS = True

env_path = '.env'

# Auto generate .ENV file with secret_key
def create_env_file():
    if not os.path.exists(env_path):
        with open(env_path, 'w') as env_file:
            secret_key = secrets.token_hex(16)
            env_file.write(f"SECRET_KEY={secret_key}\n")
            env_file.write(f"DATABASE_URL=sqlite:///site.db\n")
        print('New .env file created with generated SECRET_KEY')
    else:
        print('.env file already exists.')

# Load environment variables
load_dotenv(env_path)

# Load environment variables
def load_environment():
    load_dotenv(env_path)
    print('Environment variables loaded from .env')

def create_database():
    with app.app_context():
        try:
            db.create_all()
            print(f"Database created successfully.")

            if GEN_ROLES:
                if not Role.query.first():  # Check roles exist
                    print("Adding roles...")
                    admin_role = Role(title='Responsible Officer', description='Admin', power=90)
                    user_role = Role(title='Pilot', description='Remote Pilot', power=20)
                    
                    db.session.add(admin_role)
                    db.session.add(user_role)
                    db.session.commit()
                    print("Roles added.")

            if GEN_ROLES and GEN_USERS:
                if not User.query.first():  # Check if users exist
                    print("Adding users...")
                    admin_user = User(username='admin', email='admin@example.com', role_id=admin_role.id)
                    admin_user.set_password('adminpass')

                    regular_user = User(username='user', email='user@example.com', role_id=user_role.id)
                    regular_user.set_password('userpass')

                    db.session.add(admin_user)
                    db.session.add(regular_user)
                    db.session.commit()
                    print("Users added.")

        except Exception as e:
            print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
