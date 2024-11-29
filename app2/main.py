import os
import asyncio
from data_processing import load_and_process_data
from generate_description import generate_description
from generate_improvements import initialize_rag, generate_improvements

# 엑셀 데이터 파일 경로
file_path = "data.xlsx"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file '{file_path}' does not exist. Please provide a valid path.")

async def main():
    try:
        # 데이터 로드 및 전처리
        df = load_and_process_data(file_path)

        if df.empty:
            print("The DataFrame is empty!")
            return

        # 고정된 안내 문장 출력
        print("""
        이제 보고서를 더 구체화하기 위한 대화를 진행합니다. 환경(E), 사회(S), 지배구조(G) 순서에 따라 내용을 추가하며 보고서 초안을 완성해 주세요!
        """)

        # 설명 문장 생성
        details = "\n".join([f"- {row['구분']}: {row['총합']}" for _, row in df.iterrows()])
        try:
            descriptions = await generate_description(details)
            print("Generated Descriptions:")
            print(descriptions)
        except Exception as e:
            print(f"Error during description generation: {e}")
            return

        # 개선 방안 생성
        try:
            retrieval_chain = initialize_rag()
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
            return

        for _, row in df.iterrows():
            category = row['구분']
            total = row['총합']
            try:
                improvements = await generate_improvements(category, total, retrieval_chain)
                print(f"Improvement Suggestions for '{category}': (Total: {total}):")
                print(improvements)
            except Exception as e:
                print(f"Error generating improvements for category '{category}': {e}")
    except Exception as e:
        print(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())