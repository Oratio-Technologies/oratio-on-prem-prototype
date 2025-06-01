import sys
sys.path.insert(0, '/home/mohamed-ayari/projects/oratio/oratio-on-prem-prototype/data-indexing/etl-backend')  # Add the src directory to the Python path

from fastapi import FastAPI, UploadFile, File, Form
from pymongo import MongoClient
from loguru import logger
from io import BytesIO
import os
from datetime import datetime

from services.pdf_processing import extract_text_from_pdf

from config import settings


from documents import PdfDocument
from mongo import connection



# Initialize FastAPI
app = FastAPI()

# _database = connection.get_database("production") #Get the database instance (weird function, you have to pass an argument but in the implemnation it doesn't require)



@app.post("/process_pdf_file/")
async def process_pdf_file(file: UploadFile = File(...), document_name: str = Form(...)):
    contents = await file.read()

    # Save the uploaded file locally
    file_path = f"/tmp/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(contents)

    # Extract text using fitz
    number_of_pages, chunks = extract_text_from_pdf(file_path)
    
    saved_document_ids = []
    
    for extracted_text in chunks:
        
        document = PdfDocument(
            extracted_text=extracted_text,
            source=file.filename,
            num_pages=number_of_pages,
            document_name=document_name
        )

        result = document.save()
        if result:
            saved_document_ids.append(str(result))
    
    # Clean up the temporary file
    if os.path.exists(file_path):
        os.remove(file_path)
    
    return {
        "status": "success", 
        "document_name": document_name,
        "filename": file.filename,
        "pages_processed": number_of_pages,
        "chunks_saved": len(saved_document_ids),
        "document_ids": saved_document_ids
    }
