import json
import streamlit as st
import time
from src.mcqgen import MCQGen
from io import BytesIO
import base64

st.title ("MCQ generator with OpenAI & Langchain 🦜")
difficulty = st.select_slider('Select Difficulty', ['easy', 'medium', 'hard'])
number = st.slider('Pick a number', 1,15)
text_block = st.text_area(label="Enter your text block", placeholder="Example: Anonymous Electoral Bonds were introduced specifically as an integral component of the Union Budget and hence classified as a Money Bill to enjoy certain procedural advantages and bypass certain parliamentary scrutiny processes, in a violation of Article 110 of Indian constitution ..........")
api_key = st.text_input("Enter OpenAI API Key", type="password", placeholder='sk-***************************')

def generate_mcq():
    with st.spinner('Generating questions...'):
        if not number or not isinstance(number, int):
            st.error('A valid number is required')
        if not text_block or len(text_block)<300:
            st.error('Minimum content in the text block should be 300 characters.')
        if not api_key:
            st.error('A valid OpenAI API key is required to generate questions')

        new= MCQGen(openai_api_key=api_key)
        if not new.test_key:
            st.error("The API key provided is either wrong or does't have enough balance")

        try:
            new.prepare_chains()
            resp = new.get_json_results(text_block=text_block,number_of_questions=number, difficulty=difficulty)
            return resp
        except:
            st.error("An error has occured , Please try again later.")
            return None

def format_mcq(mcq_json):
    formatted_mcq = ""
    for key, value in mcq_json.items():
        formatted_mcq += f"Question {key}: {value['mcq']}\n"
        for option_key, option_value in value['options'].items():
            formatted_mcq += f"\t{option_key.upper()}: {option_value}\n"
        formatted_mcq += f"Correct Answer: {value['correct'].upper()}\n\n"
    return formatted_mcq


btn = st.button('Generate MCQs', "gen_btn")
if btn:
    resp = generate_mcq()
    if resp is not None:
        st.success("MCQs generated successfully. You can now download the results.")
        formatted_mcq = format_mcq(resp)
        b64 = base64.b64encode(formatted_mcq.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/txt;base64,{b64}" download="mcq_results.txt">Download MCQs as Text File</a>'
        st.markdown(href, unsafe_allow_html=True)

