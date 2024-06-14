from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
import csv
import json
from urllib.parse import urlparse
import requests

def home(request):
    """
    Render the home page.
    """
    return render(request, 'home.html')

def is_valid_url(url):
    """
    Validate the URL format.
    """
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def is_reachable_url(url):
    """
    Check if the URL is reachable.
    """
    try:
        response = requests.head(url, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def scrape(request):
    """
    Scrape data from a given URL.
    """
    if request.method == 'POST':
        url = request.POST.get('url')

        # Validate URL format
        if not is_valid_url(url):
            return HttpResponse('Invalid URL format', status=400)

        # Check if URL is reachable
        if not is_reachable_url(url):
            return HttpResponse('URL is not reachable', status=404)

        try:
            # Set up Selenium WebDriver with WebDriver Manager
            options = Options()
            options.add_argument('--headless')  # Run Chrome in headless mode
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            # Wait for the page to fully load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            # Extract HTML content
            html_content = driver.page_source
            driver.quit()

            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract relevant data
            title = soup.title.string if soup.title else 'No Title'
            headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]

            # Prepare context for rendering result
            context = {
                'title': title,
                'headings': headings,
                'paragraphs': paragraphs,
            }

            # Store scraped data in session
            request.session['scraped_data'] = context

            # Render result page
            return render(request, 'result.html', context)

        except Exception as e:
            # Handle exceptions
            return HttpResponse(f'Error: {e}')

    else:
        # Render home page for GET requests
        return render(request, 'home.html')



def download_file(request):
    """
    Download scraped data in the requested format.
    """
    # Check if scraped data exists in session
    if 'scraped_data' not in request.session:
        return HttpResponse('No scraped data found', status=404)

    context = request.session['scraped_data']
    
    # Ensure only POST requests are allowed
    if request.method != 'POST':
        return HttpResponse('Invalid request method', status=405)

    # Check for valid download types
    download_type = request.POST.get('download_type')
    if download_type not in ['pdf', 'csv', 'json']:
        return HttpResponse('Invalid download type', status=400)

    try:
        if download_type == 'pdf':
            # Generate PDF
            template_path = 'result.html'
            template = get_template(template_path)
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{context["title"]}.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
            if pisa_status.err:
                return HttpResponse('PDF generation failed', status=500)
            return response

        elif download_type == 'csv':
            # Generate CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{context["title"]}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Title', 'Headings', 'Paragraphs'])
            writer.writerow([context['title'], '\n'.join(context['headings']), '\n'.join(context['paragraphs'])])
            return response

        elif download_type == 'json':
            # Generate JSON
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{context["title"]}.json"'
            json.dump(context, response, indent=4)
            return response

        else:
            return HttpResponse('Invalid download type', status=400)

    except Exception as e:
        return HttpResponse(f'Error: {e}', status=500)
    

from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from .forms import ScheduleForm
from .tasks import scrape_data  # Import your Celery task function

from datetime import datetime, timezone

def schedule_scrape(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            schedule_date = form.cleaned_data['schedule_date']
            schedule_time = form.cleaned_data['schedule_time']
            output_format = form.cleaned_data['output_format']
            
            # Combine date and time into a single datetime object
            schedule_datetime = datetime.combine(schedule_date, schedule_time).astimezone(timezone.utc)
            
            # Format schedule_datetime in ISO 8601 format
            schedule_time_iso = schedule_datetime.isoformat()
            
            # Schedule the scraping task
            result = scrape_data.apply_async((url, output_format), eta=schedule_time_iso)
            
            # Add success message
            messages.success(request, f'Scraping scheduled at {schedule_datetime}. Task ID: {result.id}')
            
            return redirect('webscrapify_app:schedule_scrape')  # Redirect to home or another appropriate page after scheduling
    else:
        form = ScheduleForm()
    
    return render(request, 'schedule.html', {'form': form})


from django.shortcuts import render
from django.contrib import messages
from celery import current_app
from datetime import datetime

def scheduled_tasks(request):
    # Retrieve scheduled tasks from Celery
    scheduled_tasks = current_app.control.inspect().scheduled()

    tasks_info = []
    if scheduled_tasks:
        for worker, tasks in scheduled_tasks.items():
            for task in tasks:
                task_info = {
                    'id': task['request']['id'],
                    'url': task['request']['args'][0],  # Assuming URL is the first argument
                    'schedule_time': datetime.fromisoformat(task['eta']).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Scheduled'  # Initial status assumption
                }
                tasks_info.append(task_info)

        messages.info(request, f"Found {len(tasks_info)} scheduled tasks.")
    else:
        messages.info(request, "No scheduled tasks found.")

    context = {
        'tasks_info': tasks_info,
    }

    return render(request, 'scheduled_tasks.html', context)
