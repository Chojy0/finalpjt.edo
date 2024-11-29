import openai
import asyncio

async def generate_description(details):
    """
    Generate concise descriptions for each category in the dataset.
    Args:
        details (str): A formatted string of category and total values.
    Returns:
        str: Generated sentences.
    """
    prompt = f"""
    아래 항목들에 대한 간결한 설명을 작성해주세요. 각 항목은 반드시 한 문장으로 작성되며, 순서대로 설명해야 합니다:

    {details}
    
    각각의 항목은 환경, 사회, 지배구조에 대한 전문 보고서 스타일로 작성해주세요.
    """
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "여러 항목에 대한 간결한 설명을 작성하세요."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
