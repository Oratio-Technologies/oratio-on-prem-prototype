import streamlit as st
import requests
from config import settings

st.title("Query Processor")
st.write("Enter a query below to retrieve information:")

query = st.text_input("Your query:")

if st.button("Retrieve Information"):
    if query:
        # Step 1: Send the query to the retriever to get context and prompt
        retriever_response = requests.post(
            settings.INFERENCE_SERVICE_URL,
            json={"query": query}
        )

        # Initialize variables for context and answer
        context = None
        answer = None

        # Check if the retriever request was successful
        if retriever_response.status_code == 200:
            retriever_result = retriever_response.json()
            prompt = retriever_result.get("prompt")
            context = retriever_result.get("context")

            # Display the retrieved context in a formatted way
            st.write("Retrieved Context:")
            if context:
                for item in context:
                    st.write(f"ID: {item['id']}")
                    st.write(f"Score: {item['score']}")
                    st.write(f"Source: {item['payload']['source']}")
                    st.write(f"Content:\n{item['payload']['content']}")
                    st.write("---")
                
                # Convert context into a single string
                context_string = "\n".join([item['payload']['content'] for item in context])
            else:
                context_string = ""
                st.write("No context retrieved.")

            # Step 2: Send the prompt and context to the LLM service to generate the answer
            if prompt:
                llm_response = requests.post(
                    settings.LLM_SERVICE_URL,
                    json={"prompt": prompt, "context": context_string}  # Sending both prompt and context
                )

                # Check if the LLM request was successful
                if llm_response.status_code == 200:
                    llm_result = llm_response.json()
                    answer = llm_result.get("answer")
                    st.write("Generated Answer:")
                    st.text(answer)  # Display the generated answer
                else:
                    st.warning("Failed to generate an answer. Please try again.")
            else:
                st.warning("No prompt received from the retriever.")
        else:
            st.error("Failed to retrieve context. Please try again.")
    else:
        st.error("Please enter a query.")
