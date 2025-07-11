import re
from io import BytesIO
import streamlit as st
import config
from PIL import Image
from google import genai
from google.genai import types
#intializing client
client=genai.Client(api_key=config.gemini_api_key)

#defining the generate response
def generate_response(prompt,temperature=0.3):
    """Generate a response from Gemini API."""
    try:
       contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
       config_params = types.GenerateContentConfig(temperature=temperature)
       response = client.models.generate_content(
       model="gemini-2.0-flash", contents=contents, config=config_params)
       return response.text
    except Exception as e:
        print("the error has been caught.")



#defining rhe run ai teaching assistent
def run_ai_teaching_assistent():
    st.title("Welcome to AI teaching assistent.")
    st.write("Type any question you have and i will provide you an answer.")
    if 'history_ata' not in st.session_state:
        st.session_state.history_ata=[]
    col_clear,col_export=st.columns([1,2])
    with col_clear:
        if st.button("???Clear Conversation",key="clear_ata"):
            st.session_state.history_ata=[]
    #adding the user input here:
    user_input=st.text_input("enter your question here",key="input_ata")
    if user_input:
        st.write(f"your question is{user_input}")
        response=generate_response(user_input)
        st.write(f"AI's response to your query is: {response}")
    else:
        st.write("please enter a question")
            

#defining MATH mastermind:
def math_mastermind():
    st.set_page_config(page_title="MATH MASTERMIND!",layout="centered")
    st.title("🧮 Math Mastermind")
    st.write("**Your Expert Mathematical Problem Solver** - From basic arithmetic to advanced calculus, I'll solve any math problem with detailed step-by-step explanations!")
    
    # Add helpful examples
    with st.expander("📚 Example Problems I Can Solve"):
        st.markdown("""
        **Algebra:** Solve equations, factor polynomials, simplify expressions
        - Example: "Solve 2x² + 5x - 3 = 0"
        
        **Geometry:** Area, volume, proofs, coordinate geometry
        - Example: "Find the area of a triangle with vertices at (0,0), (3,4), and (6,0)"
        
        **Statistics:** Probability, distributions, hypothesis testing
        - Example: "What's the probability of rolling two dice and getting a sum of 7?"
        
        **Word Problems:** Real-world applications of mathematics
        - Example: "A train travels 300 miles in 4 hours. How fast was it going?"
        """)
    
    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    
    # Clear and Export buttons
    col_clear, col_export = st.columns([1, 2])

    with col_clear:
        if st.button("🧹 Clear Conversation"):
            st.session_state.history = []
            st.rerun()

    with col_export:
        if st.session_state.history:
            export_text = ""
            for idx, qa in enumerate(st.session_state.history, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"

            bio = io.BytesIO()
            bio.write(export_text.encode("utf-8"))
            bio.seek(0)

            st.download_button(
                label="📥 Export Math Solutions",
                data=bio,
                file_name="Math_Mastermind_Solutions.txt",
                mime="text/plain",
            )
    # Input and submit form
    with st.form(key="math_form", clear_on_submit=True):
        user_input = st.text_area(
            "🔢 Enter your math problem here:", 
            height=100,
            placeholder="Example: Solve 2+3-5/3*4",
            key=f"user_input_{st.session_state.input_key}"
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("🧮 Solve Problem", use_container_width=True)
        with col2:
            difficulty = st.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)

        if submitted and user_input.strip():
            prompt=f"[{difficulty} Level] {user_input.strip()}"
            response=generate_response(prompt)
            st.session_state.history.insert(0,{
            "question": user_input.strip(), 
            "answer":response,
            "Difficulty":difficulty
            })
            st.session_state.input_key += 1
            st.rerun()
        elif submitted and not user_input.strip():
            st.warning("⚠️ Please enter a math problem before clicking Solve Problem.")
        # Show conversation history
        if st.session_state.history:
            st.markdown("### 📋 Solution History (Latest First)")
            st.markdown(
            """
            <style>
            .history-box {
                max-height: 500px;
                overflow-y: auto;
                border: 2px solid #4CAF50;
                padding: 15px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 10px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .question {
                font-weight: 700;
                color: #2E7D32;
                margin-top: 15px;
                margin-bottom: 8px;
                font-size: 16px;
            }
            .difficulty {
                display: inline-block;
                background-color: #FF9800;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                margin-left: 10px;
            }
            .answer {
                margin-bottom: 20px;
                white-space: pre-wrap;
                color: #1B5E20;
                line-height: 1.6;
                background-color: rgba(255, 255, 255, 0.7);
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        history_html = '<div class="history-box">'
        total_questions = len(st.session_state.history)
        for idx, qa in enumerate(st.session_state.history):
            # Latest question gets the highest number (Q3, Q2, Q1...)
            question_num = total_questions - idx
            difficulty_badge = f'<span class="difficulty">{qa.get("difficulty", "N/A")}</span>' if "difficulty" in qa else ""
            
            history_html += f'<div class="question">Problem {question_num}: {qa["question"]}{difficulty_badge}</div>'
            history_html += f'<div class="answer">Solution {question_num}: {qa["answer"]}</div>'
        history_html += '</div>'
        st.markdown(history_html, unsafe_allow_html=True)






























if __name__=="__main__":
    st.sidebar.title("Choose AI you want")
    option=st.sidebar.selectbox("",["AI Teaching Assistant","Math MaterMind"])