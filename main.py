
from fastapi import FastAPI, File, UploadFile, HTTPException, Form,Request
from fastapi.responses import JSONResponse, StreamingResponse
from bs4 import BeautifulSoup
import io
import re
app = FastAPI(   title="Text Processing API",
    description="An API for text processing tasks, such as HTML tag removal and email/URL extraction.",
    version="1.0.0",)

def remove_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    clean_text = soup.get_text(separator=' ')
    return clean_text

@app.post("/remove_tags/json")
async def remove_tags_json(data: dict):
    try:
        input_html = data.get("html", "")
        if not input_html:
            raise HTTPException(status_code=400, detail="HTML not provided")

        cleaned_text = remove_tags(input_html)
        return JSONResponse(content={"cleaned_text": cleaned_text})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/remove_tags/file")
async def remove_tags_file(html_file: UploadFile = File(...)):
    try:
        input_html = await html_file.read()
        cleaned_text = remove_tags(input_html.decode())
        return JSONResponse(content={"cleaned_text": cleaned_text})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)





def extract_email_addresses(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails

def extract_urls(text):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls

def process_text(input_text):
    cleaned_text = remove_tags(input_text)
    emails = extract_email_addresses(cleaned_text)
    urls = extract_urls(cleaned_text)
    return {"emails": emails, "urls": urls}
@app.post("/extract_emails_urls")
async def extract_emails_urls_api(request: Request):
    try:
        data = await request.json()
        input_text = data.get("text", "")
        if not input_text:
            raise HTTPException(status_code=400, detail="Text not provided")

        result = process_text(input_text)
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)