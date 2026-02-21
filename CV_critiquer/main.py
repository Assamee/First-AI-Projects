import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(page_title="CV Critiquer", page_icon="📃", layout="centered")

# Display the title and description
st.title("AI CV Critiquer")
st.markdown("Upload your CV and get AI-powered feedback on how to improve it!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your CV (PDF or TXT format)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for (optional)")

analyse = st.button("Analyse CV") # When clicked, the variable "analyse" becomes True

# Function to extract text from PDF files (using PyPDF2)
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from uploaded files (PDF or TXT)
def extract_text_from_file(file):
    if file.type == "application/pdf":
        # Convert the file (after reading) into a byte object for PyPDF2 to read
        return extract_text_from_pdf(io.BytesIO(file.read()))
    return file.read().decode("utf-8")  # For text files, decode the bytes to a string (utf-8 is the standard encoding for text files)


# Any time an st value is changed (like uploading a new CV), the python file is re-run, so the if statement is re-evaluated
if analyse and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid CV.")
            st.stop()
        
        role_context = f"The candidate is applying for the role of: {job_role}. Tailor your critique strictly to this industry's standards." if job_role else "Provide a general critique to maximise the CV's professional impact."

        prompt = f"""You are a Principal U.K. Early Careers Recruiter. Critique the following CV.
        {role_context}

        Format your response in clean Markdown. Keep it punchy, actionable, and avoid dense paragraphs. Include the following sections:
        
        * **First Glance:** A brutal but fair 2-sentence summary of the CV's immediate impact.
        * **The Highlights:** 2-3 bullet points on what the candidate has done well (e.g., strong metrics, good structure).
        * **The Red Flags:** 2-3 bullet points identifying weak verbs, missing impact, or wasted space.
        * **Immediate Actions:** 3 precise, actionable steps the candidate must take right now to upgrade this CV.

        CV Text:
        ---
        {file_content}
        """

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": 'You are an expert CV critic with a sharp eye for detail and a knack for providing concise, actionable feedback. Your critiques are direct, honest, and designed to help candidates improve their CVs to stand out in competitive job markets.'},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        st.markdown("### AI Critique:")
        st.markdown(response.choices[0].message.content) # Since we are only asking for one response, we can directly access the first choice
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    print("Hello from cv-critiquer!")


if __name__ == "__main__":
    main()
# To run the Streamlit app, use the following command in your terminal:
# uv run streamlit run main.py
# (uv runs streamlit, which runs main.py)