import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – Gemini will answer! "
    "To use this app, you need to provide a Google AI API key, which you can get [here](https://aistudio.google.com/app/apikey). "
)

# Ask user for their Google AI API key via `st.text_input`.
google_api_key = st.text_input("Google AI API Key", type="password")
if not google_api_key:
    st.info("Please add your Google AI API key to continue.", icon="🗝️")
else:
    # Configure the Gemini API client
    genai.configure(api_key=google_api_key)

    # Let the user upload a PDF file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.pdf)", type=("pdf",)
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded PDF file and question.
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        document = ""
        for page in pdf_reader.pages:
            document += page.extract_text() or ""  # Some pages might return None

        prompt = f"Here's a document:\n{document}\n\n---\n\n{question}"

        # Use Gemini 2.5 Flash model ("gemini-2.5-flash")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt, stream=True)

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(response)
