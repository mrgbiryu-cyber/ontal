import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.database.connection import DatabaseManager

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_horror_script():
    db = DatabaseManager()
    knowledges = db.get_knowledge_triples()
    db.close()

    if not knowledges:
        return "⚠️ DB에 데이터가 없습니다. init_db.py를 먼저 실행해주세요."

    knowledge_context = "\n".join(knowledges)
    
    prompt = f"""
    당신은 공포 쇼츠 전문 작가입니다. 
    아래의 [지식 그래프 데이터]를 활용해 1분 미만 대본을 쓰세요.
    데이터: {knowledge_context}
    """

    # 모델명을 'models/' 포함해서 명시적으로 적어주면 404 에러가 해결됩니다.
    try:
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during Gemini call: {e}"

if __name__ == "__main__":
    print("Generating scenario...")
    script = generate_horror_script()
    print("\n=== Generated Script ===\n")
    print(script)


    