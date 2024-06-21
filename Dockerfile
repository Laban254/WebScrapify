FROM python:3.10

# Set the working directory
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg2 \
#     unzip



# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir  -r requirements.txt

# Copy the project
COPY . .

# Copy entrypoint script
# COPY entrypoint.sh /entrypoint.sh

# Expose the port
EXPOSE 8000

# Entrypoint
# ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
