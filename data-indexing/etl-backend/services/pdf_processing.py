import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        
        number_of_pages = pdf_document.page_count
        for page_num in range(number_of_pages):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
        # Split text into chunks of 1000 words
        # words = text.split()
        # chunks = [" ".join(words[i:i + 1000]) for i in range(0, len(words), 1000)]
        
        # return number_of_pages, chunks
    
    except Exception as e:
        return str(e)
