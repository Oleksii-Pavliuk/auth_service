FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app

# Install the requirements
RUN pip3 install -r requirements.txt

# Copy the entire project to the working directory
COPY . /app

# Expose port 8000 for the server
EXPOSE 8000

# Run the migrations and start the server
CMD ["sh", "-c", " python3 manage.py runserver 0.0.0.0:8000"]
