import json
from typing import List, Tuple
import tiktoken


_encoding = None


def get_encoding():
    global _encoding
    if _encoding is None:
        _encoding = tiktoken.get_encoding("cl100k_base")
    return _encoding


def num_tokens_from_string(string: str) -> int:
    encoding = get_encoding()
    num_tokens = len(encoding.encode(string))
    return num_tokens


def process_history(history: str) -> List[Tuple[str, str]]:
    """
    Processes the history JSON string and returns a list of (prompt, response) tuples.

    Args:
        history (str): A JSON string containing the history of prompts and responses.

    Returns:
        List[Tuple[str, str]]: A list of tuples, where each tuple is (prompt, response).
    """
    try:
        # Parse the JSON string into a Python list
        history_list = json.loads(history)
        
        # Extract the prompt-response pairs
        prompt_response_pairs = [
            (entry.get("prompt", ""), entry.get("response", ""))
            for entry in history_list
        ]
        
        return prompt_response_pairs
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"Error decoding JSON: {e}")
        return []




def flatten(nested_list: list) -> list:
    """Flatten a list of lists into a single list."""

    return [item for sublist in nested_list for item in sublist]


# # Example usage
# history = '[{"prompt": "Who invented the telephone?", "response": "Alexander Graham Bell is credited with inventing the telephone."}, {"prompt": "What is the capital of France?", "response": "The capital of France is Paris."}]'

# pairs = process_history(history)
# print(pairs)
