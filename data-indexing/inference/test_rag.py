from rag.retriever import VectorRetriever


if __name__ == "__main__":
    questions = [
        "Which principle suggests that you should generally put a method in the class that contains most of the data this method needs?",
        "Can the principle 'depend on abstractions' be implemented with both protocols and abstract base classes?",
        "Is the information expert principle part of the SOLID principles proposed by Robert Martin?"
    ]

    for question in questions:
        query = question

        retriever = VectorRetriever(query=query)
        hits = retriever.retrieve_top_k(9)
        
        print(f"Query: {query}\n")
        print("Hits:\n")
        for hit in hits:
            print(f"{hit}\n")
        print("=" * 50 + "\n")