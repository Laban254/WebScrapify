# Import necessary modules
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests
from bs4 import BeautifulSoup
import csv
import json

def home(request):
    """
    Render the home page.
    """
    return render(request, 'home.html')

def scrape(request):
    """
    Scrape data from a given URL.
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            # Fetch the webpage
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract relevant data
            title = soup.title.string
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
        
        except (requests.RequestException, ValueError, AttributeError) as e:
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