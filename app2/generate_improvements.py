from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
import os

def initialize_rag(persist_directory="./chroma_db"):
    """
    Initialize the vector database and RAG chain.
    Args:
        persist_directory (str): Directory where the Chroma DB is stored.
    Returns:
        RetrievalQA: LangChain RetrievalQA object.
    """
    try:
        # OpenAI Embeddings 초기화
        print("Initializing OpenAI Embeddings...")
        embeddings = OpenAIEmbeddings()

        # Chroma 벡터 데이터베이스 로드
        print(f"Loading Chroma Vector Database from: {persist_directory}")
        if not os.path.exists(persist_directory):
            print(f"Warning: '{persist_directory}' 디렉토리가 존재하지 않습니다. 새로 생성합니다.")
            os.makedirs(persist_directory, exist_ok=True)
        vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        # Retriever 설정
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})

        # RetrievalQA 체인 초기화
        print("Initializing RetrievalQA Chain...")
        qa_chain = RetrievalQA(llm=ChatOpenAI(temperature=0, model="gpt-4"), retriever=retriever)

        print("RAG Chain initialization complete.")
        return qa_chain
    except Exception as e:
        print(f"Error during RAG initialization: {e}")
        raise

def generate_improvements(category, qa_chain):
    """
    Generate improvement suggestions for a given category using RAG.
    Args:
        category (str): The category for which improvements are suggested.
        qa_chain (RetrievalQA): RAG chain for querying improvements.
    Returns:
        str: Generated improvement suggestions.
    """
    try:
        # Query 생성
        query = f"""
        '{category}' 항목을 개선하기 위한 방안을 제시해주세요. ESG 보고서와 관련된 구체적인 자료를 참고하여 작성해주세요.
        """
        print(f"Running query for category: {category}")
        result = qa_chain.run(query)
        print(f"Generated improvements for '{category}':\n{result}")
        return result
    except Exception as e:
        print(f"Error during generate_improvements for category '{category}': {e}")
        return "An error occurred while generating improvement suggestions."
