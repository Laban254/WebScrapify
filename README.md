# WebScrapify
Your go-to tool for swift and precise data extraction from any website. Automate your scraping tasks effortlessly and unlock valuable insights in seconds.

[web_scraper.webm](https://github.com/Laban254/WebScrapify/assets/64686919/c7f280a1-af06-4d4b-af91-574032580da9)

## Description

WebScrapify is crafted with Django and Bootstrap 5, offering a Python-based web scraping tool designed for swift and efficient extraction of structured data from various websites. Its user-friendly interface empowers users to input a URL and seamlessly retrieve essential information such as titles, headings, and paragraphs from the target webpage

## Features

- **Efficient Data Extraction**: Extracts structured data including titles, headings, and paragraphs from web pages.
- **User-friendly Interface**: Simple and intuitive interface for easy URL input and data retrieval.
- **Multiple Download Formats**: Supports downloading scraped data in PDF, CSV, and JSON formats.
- **Error Handling**: Provides robust error handling to handle invalid URLs and other exceptions gracefully.

## Getting Started

To get started with Web Scraper, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies (see Installation section).
3. Run the application and start scraping web data.

## Installation

```bash
# Clone the repository
$ git clone https://github.com/Laban254/WebScrapify.git

# Navigate to the project directory
$ cd WebScrapify

# Install dependencies
## If you're using pipenv, run:
$ pipenv install

## Alternatively, if you prefer using pip, you can install the dependencies listed in the `Pipfile` manually

# Apply Migrations
$ python manage.py migrate

# Start the Server
$ python manage.py runserver

# After running this command, you can access the application by navigating to `http://localhost:8000` in your web browser
```
## Usage

```bash
# Run the application:
$ python manage.py runserver

# Open your web browser and navigate to http://localhost:8000.

# Enter the URL of the website you want to scrape and click on the "Scrape" button.

# Once the data is scraped, you can choose the desired download format (PDF, CSV, JSON) and click on the "Download" button to save the data.
```
## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
