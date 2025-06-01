from app.llm.openai import OpenAILLM

from typing import List

# def docs_reranker(question: str, separator: str, passages: List[str]) -> list[str]:
#     llm = OpenAILLM()
#     passages_text = separator.join(passages)
    
#     messages_combine = [{"role": "system", 
#                          "content":f"""You are analyzing legal text chunks to find the essential information needed to answer this question: "{question}"

#                                         Your task is simple:
#                                         1. Read each chunk carefully
#                                         2. Ask yourself: "Can this chunk help to  answer the question?"
#                                         3. If yes, keep it. If no, remove it.

#                                         Keep a chunk if:
#                                         - It contains key legal information needed for the answer
#                                         - It provides essential context or conditions
 

#                                         Remove a chunk if:
#                                         - It's not needed to answer the question


#                                         Technical Requirements:
#                                         - Return chunks exactly as they appear in the input
#                                         - Separate chunks with '{separator}'
#                                         - Don't add any comments or explanations
#                                         - Don't modify the text in any way

#                                         Input chunks:
#                                         {passages_text}
#                                         """}]
#     messages_combine.append({"role": "user", "content": "Return only the chunks that are essential for answering the question, exactly as they appear."})
    
#     completion = llm.gen(model="chat", messages=messages_combine)
#     list_output = [text.strip() for text in completion.split(separator) if text.strip()]
    
#     # Ensure we're getting exact matches from original passages
#     validated_output = []
#     seen_texts = set()  # To prevent duplicates
#     for text in list_output:
#         text_stripped = text.strip()
#         if text_stripped in seen_texts:
#             continue
#         for original in passages:
#             if text_stripped == original.strip():
#                 validated_output.append(original)
#                 seen_texts.add(text_stripped)
#                 break
    
#     # If no valid matches found, return original passages
#     if not validated_output:
#         return passages
    
#     return validated_output


def docs_reranker(question: str, separator: str, passages: List[str]) -> list[str]:
    llm = OpenAILLM()
    passages_text = separator.join(passages)
    
    messages_combine = [{"role": "system", 
                         "content":f"""You are analyzing Business Registration Expert chunks to find the essential information needed to answer this question: "{question}"

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



def query_expansion(question: str,
                    to_expand_to_n: int,
                    # original_language: str = "German", 
                    target_language: str = "English") -> list[str]:
    llm = OpenAILLM()
    
    messages_combine = [{"role": "system", 
                         "content": f"""You are a Business Registration Expert with extensive expertise in:
                         - Business entity formation and registration procedures
                         - Corporate law, commercial law, and association law
                         - RNE (Registre National des Entreprises) operations and requirements
                         - Legal terminology for business creation, modification, and dissolution
                         - Administrative procedures for companies, associations, and professional entities
                         
                         Your task: Generate {to_expand_to_n} different English versions of the received query while MAINTAINING THE EXACT SAME COMPLEXITY AND KNOWLEDGE LEVEL as the original question.
                         
                         CRITICAL: PRESERVE THE ORIGINAL QUESTION'S LEVEL:
                         - If the original is a beginner question → generate beginner-level variations
                         - If the original is an expert question → generate expert-level variations  
                         - If the original uses simple language → keep variations simple
                         - If the original uses technical terms → maintain technical complexity
                         - If the original is basic/general → keep variations basic/general
                         - If the original is detailed/specific → maintain detailed/specific level
                         
                         Requirements:
                         - Use varied business and legal terminology while preserving exact meaning AND complexity level
                         - Apply different phrasing styles appropriate to the original question's sophistication level
                         - Incorporate terminology that matches the original question's expertise level
                         - Maintain the precision, specificity, AND complexity of the original business inquiry
                         - Ensure each variation captures all business and legal nuances at the same level
                         - Match the formality level of the original question (casual vs. professional)
                         
                         Constraints:
                         - Do NOT change the core business or legal meaning
                         - Do NOT add new business information or requirements
                         - Do NOT alter the scope of the business inquiry
                         - Do NOT make a simple question complex or a complex question simple
                         - Do NOT change the target audience level (beginner/intermediate/expert)
                         
                         YOU MUST PROVIDE ALL TRANSLATED QUERIES IN ENGLISH.
                         
                         Provide these level-appropriate alternative questions separated by |||.
                                    """}]
    messages_combine.append({"role": "user", "content": question})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    list_output = completion.split('|||')
    return list_output


# if __name__ == "__main__":
#     query = "i'm working in a company of 5 peoples, my employer wants to fire me.Is that legal ?"
#     to_expand_to_n = 5
#     separator = "|||"
#     list_output = query_expansion(query, to_expand_to_n, separator)
#     print(list_output)
