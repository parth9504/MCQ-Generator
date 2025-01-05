import streamlit as st
from text_from_file import extract_text_from_pdf, extract_text_from_docx
from text_summarize import abstractive_summary,extractive_summary
from mcq_generate import mcq
from question_generate import extract_keywords,get_question
import io
import re
from fpdf import FPDF

def main():

    # Side panel with sections
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Choose From",["Home", "MCQ Generator", "Questions Generator", "Text Summarizer"], index=0)
    if section== "Home":
        # Custom CSS 
        st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://intetics.com/wp-content/uploads/2021/09/AI-for-Educational-Institutions-1024x512.png');
            background-size: cover;
        }

        .title-label {
            background-color: black;  /* Black background for the title */
            color: white;             /* White text color */
            font-size: 50px;          /* Font size for the title */
            font-weight: bold;        /* Bold font */
            padding: 20px;            /* Padding for spacing */
            text-align: center;       /* Center the text */
            position: fixed;
            top: 20vh;
            left: 0;
            right: 0;
            z-index: 10;    
        }
        </style>
        """, unsafe_allow_html=True
    )

        # Title placed in a div with the 'title-label' class
        st.markdown('<div class="title-label">Learn Mate</div>', unsafe_allow_html=True)
    
    elif section == "MCQ Generator":
        st.header("MCQ Generator")

        # User choices for input method
        input_method = st.radio("Select input method:", ["Upload a PDF/DOC file", "Input Text"])

        input_text = ""

        if input_method == "Upload a PDF/DOC file":
            st.subheader("Upload a Document")
            uploaded_file = st.file_uploader("Choose a file", type=["pdf", "doc", "docx"])
            if uploaded_file is not None:
                file_type = uploaded_file.name.split(".")[-1].lower()
                if file_type == "pdf":
                    input_text = extract_text_from_pdf(uploaded_file)
                elif file_type in ["doc", "docx"]:
                    input_text = extract_text_from_docx(uploaded_file)
                else:
                    st.error("Unsupported file format. Please upload a PDF or Word document.")

        elif input_method == "Input Text":
            st.subheader("Input Text")
            input_text = st.text_area("Enter your text here:")

        if input_text:
            summarized_text = abstractive_summary(input_text)
            refined_text = summarized_text.replace("<n>", "")  # Removes the <n> if it appears
            refined_text = re.sub(r'\s+', ' ', refined_text).strip()  # Clean up any extra spaces
            st.subheader("Generated MCQs")
            num_questions = st.number_input("Number of questions to generate:", min_value=1, value=5, step=1)
            mcqs = mcq(refined_text, num_questions)

            # Create the PDF object
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Generated MCQs with Answers", ln=True, align="C")
            pdf.ln(10)

            # Display MCQs and save them in the PDF
            for idx, (question, choices, correct) in enumerate(mcqs):
                st.write(f"**Q{idx + 1}: {question}**")
                ch=65
                for choice in choices:
                    st.write(f"{chr(ch)}) {choice}")
                    ch=ch+1
                st.write("---")

                # Add to the PDF
                pdf.set_font("Arial", style="B", size=12)
                pdf.multi_cell(0, 10, txt=f"Question {idx + 1}: {question}")
                pdf.set_font("Arial", size=12)
                ch=65
                for choice in choices:
                    pdf.multi_cell(0, 10, txt=f"{chr(ch)}) {choice}")
                    ch=ch+1
                pdf.multi_cell(0, 10, txt=f"Correct Answer: {correct}")
                pdf.ln(5)

            # Save the PDF
            pdf_file_path = "generated_mcqs.pdf"
            pdf.output(pdf_file_path)

            # Provide a download button for the PDF
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="Download MCQs PDF",
                    data=pdf_bytes,
                    file_name="mcqs.pdf",
                    mime="application/pdf"
                )

    elif section == "Questions Generator":
        st.header("Questions Generator")
        # User choices for input method
        input_method = st.radio("Select input method:", ["Upload a PDF/DOC file", "Input Text"])
        input_text = ""

        if input_method == "Upload a PDF/DOC file":
            st.subheader("Upload a Document")
            uploaded_file = st.file_uploader("Choose a file", type=["pdf", "doc", "docx"])
            if uploaded_file is not None:
                file_type = uploaded_file.name.split(".")[-1].lower()
                if file_type == "pdf":
                    input_text = extract_text_from_pdf(uploaded_file)
                elif file_type in ["doc", "docx"]:
                    input_text = extract_text_from_docx(uploaded_file)
                else:
                    st.error("Unsupported file format. Please upload a PDF or Word document.")

        elif input_method == "Input Text":
            st.subheader("Input Text")
            input_text = st.text_area("Enter your text here:")

        if input_text:
            summarized_text = abstractive_summary(input_text)
            refined_text = summarized_text.replace("<n>", "")  # Removes the <n> if it appears
            refined_text = re.sub(r'\s+', ' ', refined_text).strip()  # Clean up any extra spaces
            refined_keywords = extract_keywords(refined_text)
            idx=0
            # Create the PDF object
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Generated Questions and Answers", ln=True, align="C")
            pdf.ln(10)

            # Generate questions and add them to the PDF
            for i in refined_keywords:
                ques = get_question(refined_text, i)
                # Display in Streamlit
                st.write(f"**Q{idx + 1}: {ques}**")

                # Add question and answer to the PDF
                pdf.set_font("Arial", style="B", size=12)
                pdf.multi_cell(0, 10, txt=f"Question {idx + 1}: {ques}")
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=f"Answer: {i}")
                pdf.ln(5)

                idx += 1

            # Save the PDF
            pdf_file_path = "generated_questions.pdf"
            pdf.output(pdf_file_path)

            # Provide a download button for the PDF
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="Download Questions PDF",
                    data=pdf_bytes,
                    file_name="questions.pdf",
                    mime="application/pdf"
                )
                
                


    elif section == "Text Summarizer":
        st.header("Text Summarizer")
        input_method = st.radio("Select input method:", ["Upload a PDF/DOC file", "Input Text"])
        input_text = ""

        if input_method == "Upload a PDF/DOC file":
            st.subheader("Upload a Document")
            uploaded_file = st.file_uploader("Choose a file", type=["pdf", "doc", "docx"])
            if uploaded_file is not None:
                file_type = uploaded_file.name.split(".")[-1].lower()
                if file_type == "pdf":
                    input_text = extract_text_from_pdf(uploaded_file)
                elif file_type in ["doc", "docx"]:
                    input_text = extract_text_from_docx(uploaded_file)
                else:
                    st.error("Unsupported file format. Please upload a PDF or Word document.")

        elif input_method == "Input Text":
            st.subheader("Input Text")
            input_text = st.text_area("Enter your text here:")
        
        if input_text:
            input_method = st.radio("Select summarization type:", ["Choose","Abstractive Summarization", "Extractive Summarization"])
            if input_method=="Abstractive Summarization":
                summarized_text = abstractive_summary(input_text)
                refined_text = summarized_text.replace("<n>", "")  # Removes the <n> if it appears
                refined_text = re.sub(r'\s+', ' ', refined_text).strip()  # Clean up any extra spaces
                st.write(refined_text)
            elif input_method=="Extractive Summarization":
                n=st.number_input(label="Enter the lines of summary",min_value=3,step=1)
                summarized_text=extractive_summary(input_text,n)
                refined_text = summarized_text.replace("<n>", "")  # Removes the <n> if it appears
                refined_text = re.sub(r'\s+', ' ', refined_text).strip()  # Clean up any extra spaces
                st.write(refined_text)
                
                

if __name__ == "__main__":
    main()