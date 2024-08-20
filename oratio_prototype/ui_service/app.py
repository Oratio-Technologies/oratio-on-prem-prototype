import streamlit as st
import requests
from config import settings


# Streamlit UI layout
st.title("Query Processor")
st.write("Enter a query below to retrieve information:")

# Input field for the query
query = st.text_input("Your query:")

# Button to submit the query
if st.button("Retrieve Information"):
    if query:
        # Make a POST request to the inference service
        response = requests.post(
            settings.INFERENCE_SERVICE_URL,
            json={"query": query}
        )

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            st.write("Generated Prompt:")
            st.text(result["prompt"])  # Display the prompt
            st.write("Retrieved Context:")
            st.json(result["context"])  # Display the retrieved context
        else:
            st.error("Failed to retrieve information. Please try again.")
    else:
        st.error("Please enter a query.")
