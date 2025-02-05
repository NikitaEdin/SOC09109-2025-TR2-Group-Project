FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run environment and database scripts before starting the app
CMD python create_env.py && python create_db.py && python run.py
