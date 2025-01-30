import os
import secrets

env_path = '.env'

# Auto-generate .env file with SECRET_KEY and other environment variables if it doesn't exist
if not os.path.exists(env_path):
    with open(env_path, 'w') as env_file:
        secret_key = secrets.token_hex(16)
        env_file.write(f"SECRET_KEY={secret_key}\n")
        env_file.write(f"DATABASE_URL=sqlite:///site.db\n")
    print('New .env file created with generated SECRET_KEY')
else:
    print('.env file already exists.')
