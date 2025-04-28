from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

from config import settings


# def chunk_text(text: str) -> list[str]:
#     character_splitter = RecursiveCharacterTextSplitter(
#         separators=["\n\n"], chunk_size=500, chunk_overlap=0
#     )
#     text_split = character_splitter.split_text(text)

#     token_splitter = SentenceTransformersTokenTextSplitter(
#         chunk_overlap=50,
#         tokens_per_chunk=settings.EMBEDDING_MODEL_MAX_INPUT_LENGTH,
#         model_name=settings.EMBEDDING_MODEL_ID,
#     )
#     chunks = []

#     # for section in text_split:
#     #     chunks.extend(token_splitter.split_text(section))

#     return chunks

from typing import List

# def chunk_text(text: str) -> List[str]:
#     """
#     Split text into chunks of approximately 1000 characters, trying to break at paragraph boundaries.
    
#     Parameters:
#     -----------
#     text : str
#         The input text to be chunked
        
#     Returns:
#     --------
#     List[str]
#         A list of text chunks
#     """
#     # Define fixed chunk size
#     chunk_size: int = 1000
    
#     # Split by paragraphs (empty lines)
#     paragraphs: List[str] = []
#     current: List[str] = []
    
#     for line in text.split('\n'):
#         # Skip standalone page numbers
#         if line.strip().isdigit() and len(line.strip()) < 3:
#             continue
            
#         if line.strip() == '':
#             if current:
#                 paragraphs.append('\n'.join(current))
#                 current = []
#         else:
#             current.append(line)
    
#     # Add the last paragraph if exists
#     if current:
#         paragraphs.append('\n'.join(current))
    
#     # Group paragraphs into chunks
#     chunks: List[str] = []
#     current_chunk: List[str] = []
#     current_size: int = 0
    
#     for paragraph in paragraphs:
#         paragraph_size: int = len(paragraph)
        
#         # If adding this paragraph would exceed the chunk size and we already have content
#         if current_size + paragraph_size > chunk_size and current_chunk:
#             chunks.append('\n\n'.join(current_chunk))
#             current_chunk = []
#             current_size = 0
        
#         current_chunk.append(paragraph)
#         current_size += paragraph_size
    
#     # Add the last chunk if exists
#     if current_chunk:
#         chunks.append('\n\n'.join(current_chunk))
    
#     return chunks


def chunk_text(text):
    """
    Extract paragraphs that start with numbers from the given text.
    
    Args:
        text (str): The text to process
        
    Returns:
        list: A list of strings, each representing a numbered paragraph
    """
    import re
    
    # Pattern to match paragraphs starting with numbers (like "01.", "1.", etc.)
    pattern = r'(\d+\.\s+.+?(?=\d+\.\s+|\Z))'
    
    # Use re.DOTALL to match across multiple lines
    paragraphs = re.findall(pattern, text, re.DOTALL)
    
    # Clean up paragraphs by removing extra whitespace
    cleaned_paragraphs = [re.sub(r'\s+', ' ', p).strip() for p in paragraphs]
    
    return cleaned_paragraphs


# if __name__ == "__main__":
#     # Example usage
#     text = """
#     incidence sur la trsorerie : 64. Les activits d'investissement et de financement qui n'entranent pas de flux de trsorerie sont exclues de l'tat des flux de trsorerie. Il en est ainsi par exemple des conversions de crances en capital. Il en est galement des acquisitions d'actifs en leasing qui sont considres comme oprations de financement n'entranant pas de flux de trsorerie alors que les remboursements subsquents du principal sont considrs comme des sorties de trsorerie lis aux activits de financement. 65. Effets de variation des taux de change : L'effet de variation des taux de change sur les liquidits dtenues ou dues en monnaies trangres est prsent dans l'tat des flux de trsorerie d'une manire spare. 66. lments extraordinaires et effets des modifications comptables : Les flux de trsorerie lis des lments extraordinaires et des effets des modifications comptables doivent tre classs comme flux d'activits d'exploitation, d'investissement ou de financement, selon le cas, et prsents sparment. 67. Liquidits et quivalents de liquidits : Les liquidits comprennent les fonds disponibles, les dpts vue et les dcouverts bancaires sauf s'il est tabli qu'ils font l'objet d'un financement structurel de l'entreprise et font l'objet d'un contrat ferme garantissant leur stabilit, auquel cas, ils sont classs parmi les flux de trsorerie lis aux activits de financement. Les quivalents de liquidits sont des placements court terme, trs liquides facilement convertibles en un montant connu de liquidits, et non soumis un risque significatif de changement de valeur. L'entreprise doit mentionner dans ses tats financiers les informations suivantes : lments composant les liquidits et quivalents de liquidits ; mthode adopte pour dterminer la composition des liquidits et quivalents de liquidits et effet de tout changement de mthode en la matire ; rapprochement des montants de liquidits et quivalents de liquidits figurant dans le tableau des flux de trsorerie, d'une part, et au bilan, d'autre part. 68. Les modles de prsentation de l'tat de flux de trsorerie sont fournis l'annexe 4 pour les entreprises utilisant la mthode directe sur les flux lis aux activits d'exploitation et l'annexe 5 pour celles qui utilisent la mthode indirecte. Les notes aux tats financiers Objectifs : 69. Les notes aux tats financiers d'une entreprise doivent : a) informer sur les bases retenues pour l'laboration des tats financiers et sur les choix particuliers de principes comptables adopts affrents aux transactions et vnements les plus significatifs ; b) divulguer et motiver les cas de non-respect des normes comptables tunisiennes dans l'laboration des tats financiers ; c) fournir des informations supplmentaires ne figurant pas dans le corps des tats financiers eux- mmes et qui sont de nature favoriser une prsentation fidle. 70. Les notes aux tats financiers comprennent les informations dtaillant et analysant les montants figurant dans le corps du bilan, de l'tat de rsultat et de l'tat de flux de trsorerie ainsi que des informations supplmentaires qui sont utiles aux utilisateurs tels que les engagements et les passifs 13 ventuels. Elles comprennent les informations dont les normes comptables tunisiennes requirent la publication et d'autres informations qui sont de nature favoriser la pertinence. Structure : 71. Les notes aux tats financiers doivent tre prsentes d'une manire comparable d'un exercice l'autre. Chaque lment positionn dans le bilan, l'tat de rsultat et l'tat de flux de trsorerie doit faire l'objet d'une rfrenciassions croise avec les notes correspondantes. 72. Les notes aux tats financiers sont, en rgle gnrale, prsentes dans l'ordre suivant qui permet aux utilisateurs de comprendre les tats financiers et de les comparer avec ceux dautres entreprises : a) note confirmant le respect des normes comptables tunisiennes ; b) note sur les bases de mesure et les principes comptables pertinents appliqus ; c) informations affrentes des lments figurant dans le corps des tats financiers ; et d) autres informations portant sur : i. les ventualits, engagements et autres divulgations financires, et ii. des divulgations caractre non financier. 73. Une structure systmatique doit tre retenue, autant que possible, pour la prsentation des notes. Cette structure est destine prsenter en premier lieu les lments qui sont essentiels pour la comprhension des tats financiers dans leur ensemble, tels que les principes adopts et les bases de mesure utilises. Sont prsents par la suite, les lments se rapportant aux diffrents postes et rubriques des tats financiers, dans l'ordre de leur prsentation dans les diffrents tats. Enfin, sont prsentes les autres informations exiges ou qui sont de nature assurer une reprsentation fidle. Les informations se rapportant au rfrentiel comptable utilis pour la prparation des tats financiers et aux principes comptables spcifiques retenus par l'entreprise peuvent tre prsentes au dbut des notes aux tats financiers. Dans certains cas, il peut s'avrer utile et souhaitable de changer l'ordre de prsentation de certains lments des tats financiers dans les notes. A titre d'exemple, pour les placements, les informations relatives aux produits perus, aux ajustements conduisant la juste valeur ainsi qu'aux dates d'chance gagnent tre prsentes, dans la mme note, indpendamment du fait que certains concernent le bilan et d'autres portent sur l'tat de rsultat. Note sur le respect des Normes Comptables Tunisiennes : 74. Toute entreprise publiant des tats financiers, doit dclarer l'utilisation des normes comptables comme rfrentiel pour la prparation et la prsentation de ses tats. 75. Toute divergence significative entre les normes comptables tunisiennes et les principes comptables retenus par l'entreprise doit faire l'objet d'une note d'information spcifique prcisant : a) la nature de chaque divergence ; b) la justification du choix retenu ; c) la quantification de l'impact de cette divergence sur le rsultat et la situation financire de l'entreprise. 76. L'intelligibilit et la fiabilit des tats financiers sont largement entaches si l'utilisateur est amen procder de multiples retraitements rsultant du non-respect des rgles de reconnaissance, de mesure et de prsentation dictes par une ou plusieurs normes. Dans de telles situations, l'entreprise ne peut pas dclarer que ses tats financiers ont t labors et prsents conformment aux normes comptables. Les
    
#     """
    

    
#     numbered_paragraphs = extract_numbered_paragraphs(text)
#     print("\nNumbered Paragraphs:")
#     for paragraph in numbered_paragraphs:
#         print("\n\n")
#         print(paragraph)