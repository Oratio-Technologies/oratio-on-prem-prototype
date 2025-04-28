from app.llm.openai import OpenAILLM

from typing import List

def docs_reranker(question: str, separator: str, passages: List[str]) -> list[str]:
    llm = OpenAILLM()
    passages_text = separator.join(passages)
    
    messages_combine = [{"role": "system", 
                         "content":f"""You are analyzing legal text chunks to find the essential information needed to answer this question: "{question}"

                                        Your task is simple:
                                        1. Read each chunk carefully
                                        2. Ask yourself: "Can this chunk help to  answer the question?"
                                        3. If yes, keep it. If no, remove it.

                                        Keep a chunk if:
                                        - It contains key legal information needed for the answer
                                        - It provides essential context or conditions
 

                                        Remove a chunk if:
                                        - It's not needed to answer the question


                                        Technical Requirements:
                                        - Return chunks exactly as they appear in the input
                                        - Separate chunks with '{separator}'
                                        - Don't add any comments or explanations
                                        - Don't modify the text in any way

                                        Input chunks:
                                        {passages_text}
                                        """}]
    messages_combine.append({"role": "user", "content": "Return only the chunks that are essential for answering the question, exactly as they appear."})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    list_output = [text.strip() for text in completion.split(separator) if text.strip()]
    
    # Ensure we're getting exact matches from original passages
    validated_output = []
    seen_texts = set()  # To prevent duplicates
    for text in list_output:
        text_stripped = text.strip()
        if text_stripped in seen_texts:
            continue
        for original in passages:
            if text_stripped == original.strip():
                validated_output.append(original)
                seen_texts.add(text_stripped)
                break
    
    # If no valid matches found, return original passages
    if not validated_output:
        return passages
    
    return validated_output

def query_expansion(question: str, to_expand_to_n: int, separator: str) -> list[str]:
    llm = OpenAILLM()
    
    
    messages_combine = [{"role": "system", 
                         "content": """You are an AI language model assistant. Your task is to generate {to_expand_to_n}
                                    different versions of the given user question in German not in English, to retrieve relevant documents from a vector
                                    database that are in German. By generating multiple perspectives on the user question, your goal is to help
                                    the user overcome some of the limitations of the distance-based similarity search.
                                    YOU MUST PROVIDE THE QUESTIONS IN GERMAN.
                                    Provide these alternative questions seperated by |||.
                                    """}]
    messages_combine.append({"role": "user", "content": question})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    list_output = completion.split('|||')
    return list_output


if __name__ == "__main__":
    query = "i'm working in a company of 5 peoples, my employer wants to fire me.Is that legal ?"
    to_expand_to_n = 5
    separator = "|||"
    list_output = query_expansion(query, to_expand_to_n, separator)
    print(list_output)
