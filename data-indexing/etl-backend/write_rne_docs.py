import sys
sys.path.insert(0, '/home/mohamed-ayari/projects/oratio/oratio-on-prem-prototype/data-indexing/etl-backend')

import os
import re
from typing import Dict, Optional
from pathlib import Path
from documents import PdfDocument
from services.pdf_processing import extract_text_from_pdf

def process_pdf_files_to_documents(folder_path: str, rne_operations: Dict[str, str]) -> Optional[int]:
    """
    Process PDF files from a folder and save them as PdfDocument objects to MongoDB.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
        rne_operations (Dict[str, str]): Dictionary mapping RNE codes to descriptions
        
    Returns:
        Optional[int]: Number of documents successfully processed, or None if error
    """
    

    
    def extract_rne_code_from_filename(filename: str) -> Optional[str]:
        """Extract RNE code from filename (e.g., 'RNE C 001_Fr.pdf' -> 'RNE C 001')."""
        # Remove file extension
        base_name = filename.replace('.pdf', '')
        # Remove language suffix
        rne_code = base_name.replace('_Fr', '')
        return rne_code
    
    # Validate folder path
    if not os.path.exists(folder_path):
        print(f"Error: Folder path '{folder_path}' does not exist.")
        return None
    
    folder = Path(folder_path)
    pdf_files = list(folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'.")
        return 0
    
    processed_count = 0
    
    for pdf_file in pdf_files:
        try:
            # Extract RNE code from filename
            rne_code = extract_rne_code_from_filename(pdf_file.name)
            if not rne_code:
                print(f"Warning: Could not extract RNE code from filename '{pdf_file.name}'. Skipping.")
                continue
            
            # Get document title from operations dictionary
            document_name = rne_operations.get(rne_code)
            if not document_name:
                print(f"Warning: RNE code '{rne_code}' not found in operations dictionary. Skipping '{pdf_file.name}'.")
                continue
            
            # Extract text and page count from PDF
            extracted_text = extract_text_from_pdf(str(pdf_file))
            if not extracted_text:
                print(f"Warning: Could not extract text from '{pdf_file.name}'. Skipping.")
                continue
            
            # Create PdfDocument object
            pdf_document = PdfDocument(
                extracted_text=extracted_text,
                source=pdf_file.name,
                document_title=document_name
            )
            
            # Save to MongoDB
            result = pdf_document.save()
            if result:
                print(f"Successfully saved document: {pdf_file.name} -> {document_name}")
                processed_count += 1
            else:
                print(f"Failed to save document: {pdf_file.name}")
                
        except Exception as e:
            print(f"Error processing file '{pdf_file.name}': {e}")
            continue
    
    print(f"Processing complete. {processed_count} documents successfully saved to MongoDB.")
    return processed_count

# Example usage:
if __name__ == "__main__":
    # Define the RNE operations dictionary
    rne_operations_1 = {
        "RNE C 001": "Création d'une personne physique commerçant en tant que personne physique.",
        "RNE C 002": "Création d'une personne physique artisan en tant que personne physique.",
        "RNE C 003": "Création d'une personne physique professionnel en tant que personne physique.",
        "RNE C 004": "Création d'une société anonyme en tant que personne morale.",
        "RNE C 005": "Création d'un groupement d'intérêt économique en tant que personne morale.",
        "RNE C 006": "Création d'un établissement stable en tant que personne morale.",
        "RNE C 007": "Création d'une succursale d'une société étrangère en tant que personne morale.",
        "RNE C 008": "Création d'un établissement public en tant que personne morale.",
        "RNE C 009": "Création d'un réseau d'associations en tant que personne morale.",
        "RNE C 010.1": "Création d'une association tunisienne régie par le décret-loi n° 88/2011 en tant que personne morale."
    }
    
    # Process PDF files
    folder_directory = "/home/mohamed-ayari/Downloads/hack4justice/test"
    process_pdf_files_to_documents(folder_directory, rne_operations_1)