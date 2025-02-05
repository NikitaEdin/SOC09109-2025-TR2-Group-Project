FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run environment and database scripts before starting the app
CMD python create_env.py && python create_db.py && python run.py

# To run docker, build the Docker image:
# docker build -t flask-app .
# Then run the Docker container:
# docker run -p 5000:5000 flask-app