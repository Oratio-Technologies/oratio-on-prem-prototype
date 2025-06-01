# import sys
# sys.path.insert(0,"/home/mohamed-ayari/projects/oratio/oratio-on-prem-prototype/data-indexing/2-data-ingestion")  # Adjust the path to import from the parent directory

from openai import AzureOpenAI

from config import settings, azure_settings

llm = AzureOpenAI(
    api_version=azure_settings.AZURE_OPENAI_API_VERSION,
    azure_endpoint=azure_settings.AZURE_OPENAI_ENDPOINT,
    api_key=azure_settings.AZURE_OPENAI_API_KEY
)

# def extract_name_from_text(text: str) -> str:
#     messages_combine = [
#         {
#             "role": "system", 
#             "content": "extract the name of the document from the text. The name should be a single word or a short phrase that represents the main topic of the document. Do not include any additional information or context."
#         },
#         {
#             "role": "user", 
#             "content": text
#         }
#     ]

#     response = llm.chat.completions.create(
#         messages=messages_combine,
#         model="gpt-4o",
#     )
#     return response.choices[0].message.content


# def generate_questions(text: str, document_title: str) -> str:
#     messages_combine = [
#         {
#             "role": "system", 
#             "content": f"""
#             You are a Tunisian person asking in french about a process related to a "{document_title}" at the RNE. 
#             Do not use the words "{document_title}" but rather words that a normal person without technical or legal knowledge would use.
#             How would you formulate your question? Please provide 5 formulations IN ENGLISH !!.
            
#             Provide these alternative questions seperated by |||.

#             """
#         },
#         {
#             "role": "user", 
#             "content": text
#         }
#     ]
    

#     completion = llm.chat.completions.create(
#         messages=messages_combine,
#         model="gpt-4o",
#     )
#     response_content = completion.choices[0].message.content
#     list_output = response_content.split('|||')
#     return list_output

# def generate_questions(text: str, document_title: str) -> list[str]:
#     messages_combine = [
#         {
#             "role": "system", 
#             "content": f"""
#             You are a Tunisian person asking in French about a process related to a "{document_title}" at the Registre National des Entreprises (RNE). 
#             Do not use the words "{document_title}" but rather words that a normal person without technical or legal knowledge would use.
#             How would you formulate your question? Please provide exactly 5 formulations IN ENGLISH.
            
#             IMPORTANT: Format your response as exactly 5 questions, each on a separate line, with no additional text, numbering, or formatting. Just the questions separated by line breaks.
            
#             Example format:
#             How do I register my business?
#             What documents do I need for company registration?
#             Where can I submit my application?
#             How long does the process take?
#             What are the fees involved?
#             """
#         },
#         {
#             "role": "user", 
#             "content": text
#         }
#     ]
    
#     completion = llm.chat.completions.create(
#         messages=messages_combine,
#         model="gpt-4o",
#     )
    
#     response_content = completion.choices[0].message.content.strip()
    
#     # Split by line breaks and clean up
#     questions = [q.strip() for q in response_content.split('\n') if q.strip()]
    
#     # Remove any numbering or bullet points
#     cleaned_questions = []
#     for question in questions:
#         # Remove common prefixes like "1.", "•", "-", etc.
#         cleaned_question = question
#         if question and (question[0].isdigit() or question.startswith(('•', '-', '*'))):
#             # Find the first space or period after numbering/bullet
#             for i, char in enumerate(question):
#                 if char in ['.', ')', ' '] and i > 0:
#                     cleaned_question = question[i+1:].strip()
#                     break
#         cleaned_questions.append(cleaned_question)
    
#     # Ensure we have exactly 5 questions, filter out empty ones
#     final_questions = [q for q in cleaned_questions if q and len(q) > 10]
    
#     # If we don't have 5 questions, try alternative splitting methods
#     if len(final_questions) != 5:
#         # Try splitting by common separators as fallback
#         for separator in ['|||', '|', ';', '\n\n']:
#             if separator in response_content:
#                 alt_questions = [q.strip() for q in response_content.split(separator) if q.strip()]
#                 if len(alt_questions) >= 5:
#                     final_questions = alt_questions[:5]
#                     break
    
#     return final_questions[:5]  # Ensure maximum 5 questions


def generate_questions(text: str, document_title: str) -> list[str]:
    messages_combine = [
        {
            "role": "system", 
            "content": f"""
            You are a Tunisian person asking about a process related to a "{document_title}" at the Registre National des Entreprises (RNE). 
            Use words related to "{document_title}" that a person with technical or legal knowledge would use.
            How would you formulate your question? Please provide exactly 5 formulations IN ENGLISH. 2 of these formulations should use french abbreviations of the technical terms (if any)
            
            IMPORTANT: Format your response as exactly 5 questions, each on a separate line, with no additional text, numbering, or formatting. Just the questions separated by line breaks.
            
            Example format:
            How do I register a SUARL?
            What documents do I need for the registration of a Societe Anonyme?
            Where can I submit my application?
            How long does the process take to register an association?
            What are the fees involved?
            """
        },
        {
            "role": "user", 
            "content": text
        }
    ]
    
    completion = llm.chat.completions.create(
        messages=messages_combine,
        model="gpt-4o",
    )
    
    response_content = completion.choices[0].message.content.strip()
    
    # Split by line breaks and clean up
    questions = [q.strip() for q in response_content.split('\n') if q.strip()]
    
    # Remove any numbering or bullet points
    cleaned_questions = []
    for question in questions:
        # Remove common prefixes like "1.", "•", "-", etc.
        cleaned_question = question
        if question and (question[0].isdigit() or question.startswith(('•', '-', '*'))):
            # Find the first space or period after numbering/bullet
            for i, char in enumerate(question):
                if char in ['.', ')', ' '] and i > 0:
                    cleaned_question = question[i+1:].strip()
                    break
        cleaned_questions.append(cleaned_question)
    
    # Ensure we have exactly 5 questions, filter out empty ones
    final_questions = [q for q in cleaned_questions if q and len(q) > 10]
    
    # If we don't have 5 questions, try alternative splitting methods
    if len(final_questions) != 5:
        # Try splitting by common separators as fallback
        for separator in ['|||', '|', ';', '\n\n']:
            if separator in response_content:
                alt_questions = [q.strip() for q in response_content.split(separator) if q.strip()]
                if len(alt_questions) >= 5:
                    final_questions = alt_questions[:5]
                    break
    
    return final_questions[:5]  # Ensure maximum 5 questions
















# def get_translation(text: str) -> str:
    
#     messages_combine = [
#         {
#             "role": "system", 
#             "content": "You are a precise frensh to English translator. Translate the text exactly as it appears, maintaining the exact meaning and style. Do not add explanations, summaries, or any additional content. Do not modify the length or content of the text. Just translate from German to English."
#         },
#         {
#             "role": "user", 
#             "content": text
#         }
#     ]

#     response = llm.chat.completions.create(
#         messages=messages_combine,
#         model="gpt-4o",
#     )
#     return response.choices[0].message.content

if __name__ == "__main__":
    # Example usage
    text = "This is a sample text for generating questions."
    document_title = "Sample Document"
    questions = generate_questions(text, document_title)
    print(questions)
    
    # Uncomment to test translation
    # translated_text = get_translation("Dies ist ein Beispiel