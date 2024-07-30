from fastapi import FastAPI, UploadFile, File
from pymongo import MongoClient
from loguru import logger
from io import BytesIO
import os
from datetime import datetime
import fitz  # PyMuPDF
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Initialize FastAPI
app = FastAPI()

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://zoldyck:{password}@cluster0.kjantw5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)
production = client.production


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file using fitz (PyMuPDF)."""
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        return str(e)

@app.post("/process_pdf_file/")
async def process_pdf_file(file: UploadFile = File(...)):
    contents = await file.read()

    # Save the uploaded file locally
    file_path = f"/tmp/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(contents)

    # Extract text using fitz
    extracted_text = extract_text_from_pdf(file_path)

    # Save extracted text to MongoDB
    document = {
        "source": file.filename,
        "extracted_text": extracted_text,
        "upload_date": datetime.now()
    }

    extracted_text_collection = production.extracted_texts
    inserted_extracted_text = extracted_text_collection.insert_one(document).inserted_id

    return {"status": "Processing completed", "text": extracted_text, "id": str(inserted_extracted_text)}
