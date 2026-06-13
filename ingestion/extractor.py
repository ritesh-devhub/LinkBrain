import requests
import trafilatura
import pymupdf
import pymupdf4llm
from utils.convert2md import json2md
from datetime import datetime
import uuid
import hashlib
import validators



## Extract TEXT content and return with metadata

def extract_text(text_content, url):

    if not text_content:
        return None, None
    
    title = url
    
    return text_content, title 


## Extract PDF content and return with metadata

def extract_pdf(pdf_content, url):

    if not pdf_content:
        return None, None
    
    title = url

    doc = pymupdf.open(stream=pdf_content, filetype='pdf')

    pdf_markdown = pymupdf4llm.to_markdown(doc)

    if doc.metadata['title']:

        title = doc.metadata['title']

    return pdf_markdown, title


## Extract HTML content and return with metadata

def extract_html(url):

    downloaded = trafilatura.fetch_url(url)
    
    if not downloaded:

        return None, None
    
    title = url
    
    html_content = trafilatura.extract(downloaded, output_format='markdown')


    metadata = trafilatura.extract_metadata(downloaded)

    if metadata and metadata.title:

        title = metadata.title 

    return html_content, title


## Extract JSON content and return with metadata

def extract_json(json_content, url):

    if not json_content:

        return None, None
    
    title = None

    for key in ['title', 'name', 'headline']:

        if key in json_content:

            title = json_content[key]

            break
    
    if not title:

        title = url
    
    markdown = json2md(json_content)

    return markdown, title


## Scrape func => Scrape data -> categorize -> markdown -> return content/metadatas

def scrape(url):

    if not validators.url(url):
        return {
            'success' : False,
            'message' : "Invalid URL"
        }
    
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try: 

        response = requests.get(
            url,
            headers=headers,
            timeout=10
            )
        
        response.raise_for_status()

    
    except Exception as e:

        return {
            'success': False,
            'error': str(e)
        }
    
    content_type = response.headers.get(
            "Content-Type",
            ""
        )

    if 'application/json' in content_type:
        markdown_content, title = extract_json(response.json(), url)
        content_type = 'json'
    
    elif 'application/pdf' in content_type:
        markdown_content, title = extract_pdf(response.content, url)
        content_type = 'pdf'

    elif 'text/plain' in content_type:
        markdown_content, title = extract_text(response.text, url)
        content_type = 'text'
    
    else:
        markdown_content, title = extract_html(url)
        content_type = 'html'

    if not markdown_content:
        return None
    

    ## Hashing code for each unique content to prevent redundency
    content_hash = hashlib.sha256(
        markdown_content.encode('utf-8')
        ).hexdigest()


    return {
        'document_id': str(uuid.uuid4()),
        'url': url,
        'title': title,
        'content_type': content_type,
        'source_type': 'url',
        'content': markdown_content,
        'scraped_at':  datetime.now().isoformat(),
        'content_length': len(markdown_content),
        'content_hash': content_hash
    }