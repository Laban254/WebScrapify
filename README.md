# WebScrapify: Streamlined Web Scraping Tool

WebScrapify is a web scraping tool built on Django and Selenium, designed to extract valuable data from websites efficiently. It leverages Celery for task scheduling, enabling automated and timed scraping operations, and Docker for seamless deployment across various environments. With a focus on usability and reliability, WebScrapify offers features such as URL validation, dynamic content scraping, and data exportation in multiple formats including PDF, CSV, and JSON. Its robust error handling mechanisms ensure smooth operation even under challenging conditions, while maintaining high standards of security throughout its processes.

## Features Overview

-   **Dynamic Content Extraction**: Utilizes Selenium to scrape dynamic content from websites, headers, paragraphs, and titles ..
-   **Scheduled Scraping**: Leverages Celery for scheduling scraping tasks, ensuring timely updates.
-   **Data Export Formats**: Exports scraped data to PDF, CSV, or JSON formats.
-   **Robust Error Handling**: Designed to handle errors gracefully, ensuring continuous operation.
-   **Secure Operations**: Implements secure practices to protect both the scraper and the scraped data.
-   **Monitoring with Flower**: Integrates with Flower for real-time monitoring and administration of Celery tasks.
-   **More Coming**: Future enhancements aim to include targeted scraping for e-commerce sites and other specialized areas, broadening the scope of data that can be retrieved. .

## Getting Started

This guide will walk you through setting up and running WebScrapify on your local machine using Docker Compose.

### Prerequisites

Before you begin, make sure you have the following installed on your machine:
- Docker: Ensure Docker is installed and running on your machine. You can download it from [Docker Hub](https://www.docker.com/products/docker-desktop).
- Docker Compose: Make sure Docker Compose is installed alongside Docker. It comes bundled with Docker Desktop for Windows and Mac, but you may need to install it separately on Linux.


#### Setting Up Environment Variables

Before starting, configure the environment variables by creating a `.env` file in the project's root directory. Add the following variables:

`DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
EMAIL_HOST_USER=email@example.com
EMAIL_HOST_PASSWORD=your_email_password` 

Replace placeholders (`your_secret_key_here`, `mydatabase`, `myuser`, `mypassword`, `email@example.com`, `your_email_password`) with your actual values.

#### Starting the Application
Navigate to the root directory of your project in the terminal and run the following command to start the application:

1.  **Build and Run Containers**: Navigate to the root directory of your project in the terminal and run:
    
  
    
	`docker-compose up`

 
    
    This command pulls necessary Docker images (if not already present) and starts containers defined in `docker-compose.yml`.
    
2.  **Access the Application**: Once the containers are up and running, access your application at [http://localhost:8001](http://localhost:8001).
    
    -   The Django development server runs on port `8001` by default. Adjust ports in `docker-compose.yml` if necessary.
3.  **Stopping the Application**: To stop the application and remove containers, press `Ctrl + C` in the terminal where `docker-compose up` is running, or execute:
    
    `docker-compose down` 
    

**Accessing Services**

-   **Web Application**: Open a web browser and go to `http://localhost:8001`.
-   **Flower Monitoring Tool**: Accessible at `http://localhost:5556`. Provides a web-based interface for monitoring and administrating Celery clusters.
-   **PostgreSQL Database**: Accessed internally by other services, not exposed directly.
- **Celery Worker**: Automatically starts when you run `docker-compose up`. Monitors task queues and executes tasks asynchronously.

### Accessing the database

To access the PostgreSQL database on the command line:

    docker exec -it myproject_db psql -U mydatabaseuser -d mydatabase

If you want to dump the contents of your database to a file:

    docker exec -i myproject_db pg_dump -U mydatabaseuser -d mydatabase -v > your_dump_file.sql

(**Note:** that command and the following two use a `-i` option, instead of the `-it` options we've used previously.)

To import a plain text SQL file, like the one we made above:

    docker exec -i myproject_db psql -U mydatabaseuser -d mydatabase -v < your_dump_file.sql

Or if you have a dump in tar format, use `pg_restore` instead of `psql`:

    docker exec -i myproject_db pg_restore -U mydatabaseuser -d mydatabase -v < your_dump_file.tar

### Making changes to the container

If you change something in `docker-compose.yml` then you'll need to build
things again:

    docker-compose build

If you want to remove the containers and start again, then stop the containers, and:

    docker-compose rm
    docker-compose build

#### Troubleshooting

Encountering issues? Here are some tips:

-   Double-check the `.env` file for correct variable settings.
-   Ensure Docker and Docker Compose are installed and running properly.
-   Review `docker-compose up` logs for any error messages.

## Get in touch

If you spot a mistake, or something that could be improved, then do let me know:

Laban Kibet 
https://labankibet.tech  
https://twitter.com/labanK_ on Twitter

#### Conclusion

Congratulations on successfully setting up and launching webScrapify using Docker Compose! Customize `.env` variables and explore the application according to your project needs.
