import sys
sys.path.insert(0,"/home/mohamed-ayari/projects/oratio/oratio-on-prem-prototype/data-indexing/2-data-ingestion")  # Adjust the path to import from the parent directory


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


def generate_questions(text: str, document_title: str) -> str:
    messages_combine = [
        {
            "role": "system", 
            "content": f"""
            You are a Tunisian person asking in french about a process related to a "{document_title}" at the RNE. 
            Do not use the words "{document_title}" but rather words that a normal person without technical or legal knowledge would use.
            How would you formulate your question? Please provide 5 formulations IN ENGLISH !!.
            
            Provide these alternative questions seperated by |||.

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
    response_content = completion.choices[0].message.content
    list_output = response_content.split('|||')
    return list_output




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