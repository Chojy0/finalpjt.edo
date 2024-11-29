# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

def initialize_rag(persist_directory="chroma_db"):
    try:
        print("Initializing OpenAI Embeddings...")
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

        print(f"Loading Chroma Vector Database from: {persist_directory}")
        if not os.path.exists(persist_directory):
            print(f"Warning: '{persist_directory}' 디렉토리가 존재하지 않습니다. 새로 생성합니다.")
            os.makedirs(persist_directory, exist_ok=True)
        vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        retriever = vector_db.as_retriever(search_kwargs={"k": 3})

        llm = ChatOpenAI(temperature=0, model="gpt-4")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer."),
            ("human", "{question}"),
            ("human", "Context: {context}"),
        ])

        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        print("RAG Chain initialization complete.")
        return retrieval_chain
    except Exception as e:
        print(f"Error during RAG initialization: {e}")
        raise
def generate_improvements(category, total, retrieval_chain):
    try:
        context = f"카테고리: {category}, 총합: {total}"
        query = f"{context}에 대한 ESG 보고서 개선 방안을 제시해주세요."
        print(f"Running query for category: {category} (Total: {total})")
        result = retrieval_chain.invoke({"context": context, "question": query})
        answer = result.get('answer', str(result))
        print(f"Generated improvements for '{category}':\n{answer}")
        return answer
    except Exception as e:
        print(f"Error during generate_improvements for category '{category}': {e}")
        return "An error occurred while generating improvement suggestions."


# def generate_improvements(category, total, retrieval_chain):
#     try:
#         context = f"카테고리: {category}, 총합: {total}"
#         query = f"{context}에 대한 ESG 보고서 개선 방안을 제시해주세요."
#         print(f"Running query for category: {category} (Total: {total})")
#         result = retrieval_chain.invoke({"context": context, "question": query})
#         # 'answer' 키가 없을 경우를 대비한 처리
#         answer = result.get('answer', result)
#         print(f"Generated improvements for '{category}':\n{answer}")
#         return answer
#     except Exception as e:
#         print(f"Error during generate_improvements for category '{category}': {e}")
#         return "An error occurred while generating improvement suggestions."
    
# def generate_improvements(category, total, retrieval_chain):
    try:
        context = f"카테고리: {category}, 총합: {total}"
        query = f"{context}에 대한 ESG 보고서 개선 방안을 제시해주세요."
        print(f"Running query for category: {category} (Total: {total})")
        result = retrieval_chain.invoke({"context": context, "question": query})
        print(f"Generated improvements for '{category}':\n{result['answer']}")
        return result['answer']
    except Exception as e:
        print(f"Error during generate_improvements for category '{category}': {e}")
        return "An error occurred while generating improvement suggestions."
# def generate_improvements(category, total, retrieval_chain):
#     try:
#         query = f"'{category}' 항목(총합: {total})을 개선하기 위한 방안을 제시해주세요. 이 총합 값을 고려하여 ESG 보고서와 관련된 구체적인 자료를 참고하여 작성해주세요."
#         print(f"Running query for category: {category} (Total: {total})")
#         result = retrieval_chain.invoke({"question": query})
#         print(f"Generated improvements for '{category}':\n{result['answer']}")
#         return result['answer']
#     except Exception as e:
#         print(f"Error during generate_improvements for category '{category}': {e}")
#         return "An error occurred while generating improvement suggestions."