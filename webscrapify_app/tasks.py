from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import json
import csv
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
from .models import Notification, User, Metadata
import os

@shared_task
def scrape_data(url, output_format, user_id):
    def is_valid_url(url):
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def is_reachable_url(url):
        try:
            response = requests.head(url, timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    if not is_valid_url(url):
        return 'Invalid URL format'

    if not is_reachable_url(url):
        return 'URL is not reachable'

    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.title.string if soup.title else 'No Title'
        headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]

        context = {
            'title': title,
            'headings': headings,
            'paragraphs': paragraphs,
        }

        # Create directory for scraped data if it doesn't exist
        directory_path = os.path.join(settings.MEDIA_ROOT, 'scraped_data', str(user_id))
        os.makedirs(directory_path, exist_ok=True)

        file_name = f"{title}.{output_format}"
        file_path = os.path.join(directory_path, file_name)

        if output_format == 'pdf':
            html = render_to_string('result.html', context)
            with open(file_path, 'w+b') as response:
                pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
                if pisa_status.err:
                    return 'PDF generation failed'

        elif output_format == 'csv':
            with open(file_path, 'w', newline='', encoding='utf-8') as response:
                writer = csv.writer(response)
                writer.writerow(['Title', 'Headings', 'Paragraphs'])
                writer.writerow([context['title'], '\n'.join(context['headings']), '\n'.join(context['paragraphs'])])

        elif output_format == 'json':
            with open(file_path, 'w', encoding='utf-8') as response:
                json.dump(context, response, indent=4)

        # Save metadata in database
        Metadata.objects.create(user_id=user_id, file_path=file_path)

        # Send email notification with attachment on successful completion
        subject = f'Scraping Task Completed for {url}'
        message = f'The scraping task for {url} in {output_format} format has been completed successfully at {datetime.now()}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [User.objects.get(id=user_id).email]
        
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach_file(file_path)
        email.send()

        # Create a notification for the user
        Notification.objects.create(
            user_id=user_id,
            message=f'Scraping task for {url} completed successfully.'
        )

        return f"File saved as {file_name}"

    except Exception as e:
        Notification.objects.create(
            user_id=user_id,
            message=f'Scraping task for {url} failed with error: {str(e)}'
        )
        return str(e)
