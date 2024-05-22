

from celery import shared_task
from django.core.mail import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
import csv
import json
import os
from io import StringIO, BytesIO
import zipfile

@shared_task
def scrape_and_send_email(url, email, file_format):
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

        if file_format == 'csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['Title', title])
            writer.writerow(['Headings'])
            writer.writerow(headings)
            writer.writerow(['Paragraphs'])
            writer.writerow(paragraphs)
            output.seek(0)
            file_data = output.getvalue()
            content_type = 'text/csv'
            file_extension = 'csv'

        elif file_format == 'json':
            data = {
                'title': title,
                'headings': headings,
                'paragraphs': paragraphs
            }
            file_data = json.dumps(data, indent=4)
            content_type = 'application/json'
            file_extension = 'json'

        elif file_format == 'pdf':
            html = f"<h1>{title}</h1>"
            html += "".join([f"<h2>{heading}</h2>" for heading in headings])
            html += "".join([f"<p>{paragraph}</p>" for paragraph in paragraphs])
            result = BytesIO()
            pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result)
            file_data = result.getvalue()
            content_type = 'application/pdf'
            file_extension = 'pdf'

        elif file_format == 'zip':
            csv_output = StringIO()
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(['Title', title])
            csv_writer.writerow(['Headings'])
            csv_writer.writerow(headings)
            csv_writer.writerow(['Paragraphs'])
            csv_writer.writerow(paragraphs)
            csv_output.seek(0)
            json_output = json.dumps({
                'title': title,
                'headings': headings,
                'paragraphs': paragraphs
            }, indent=4)
            result = BytesIO()
            with zipfile.ZipFile(result, 'w') as zf:
                zf.writestr('data.csv', csv_output.getvalue())
                zf.writestr('data.json', json_output)
            file_data = result.getvalue()
            content_type = 'application/zip'
            file_extension = 'zip'

        else:
            return

        email_message = EmailMessage(
            subject=f'Scraped Data from {url}',
            body='Please find the attached scraped data.',
            to=[email]
        )
        email_message.attach(f'scraped_data.{file_extension}', file_data, content_type)
        email_message.send()

    except Exception as e:
        print(f'Error: {e}')
