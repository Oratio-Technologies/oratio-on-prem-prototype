from fastapi import FastAPI, UploadFile, File
from pymongo import MongoClient
from loguru import logger
from io import BytesIO
import os
from datetime import datetime

from services.pdf_processing import extract_text_from_pdf

from config import settings
from db.documents import PdfDocument
from db.mongo import connection



# Initialize FastAPI
app = FastAPI()

# _database = connection.get_database("production") #Get the database instance (weird function, you have to pass an argument but in the implemnation it doesn't require)



@app.post("/process_pdf_file/")
async def process_pdf_file(file: UploadFile = File(...)):
    contents = await file.read()

    # Save the uploaded file locally
    file_path = f"/tmp/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(contents)

    # Extract text using fitz
    extracted_text = extract_text_from_pdf(file_path)
    
    document = PdfDocument(
        source=file.filename,
        extracted_text=extracted_text,
        upload_date=datetime.utcnow().isoformat()
    )

    result = document.save()
    
    
    return {"status": "success", "id": str(result)}
