# Setting up UI with streamlit
import time
import streamlit as st

st.set_page_config(page_title="Vasco", layout="centered")
st.title('🌍 Vasco')
#st.markdown("<h1 style='text-align: center;'>🌍  Vasco</h1>", unsafe_allow_html=True)
tagline = '<p style="font-family:Sans-serif; font-size: 18.5px;">Travel smart with AI</p>'
st.markdown(tagline, unsafe_allow_html=True)
st.write("")
st.write("")


# User Inputs
from_city = st.text_input("🏡 From City", placeholder="Travelling from...")
destination_city = st.text_input("✈️ Destination City", placeholder="Travelling to...")
date_from = st.date_input("📅 Departure Date")
date_to = st.date_input("📅 Return Date")
budget = st.selectbox(
    "💵 Your budget range: ",
    ("Economical", "Standard", "Premium"),
)
interests = st.text_area("🎯 Your Interests (e.g., culture, food)", placeholder="sightseeing and good food")


MODEL_NAME_GROQ = "llama-3.3-70b-versatile"
MODEL_NAME_OPENAI = "gpt-4o-mini"

# provider = st.radio("Select AI Agent: ", ('Groq', 'OpenAI'))

# if provider == 'Groq':
#     selected_model = st.selectbox("Select Groq Model: ", MODEL_NAME_GROQ)
# elif provider == 'OpenAI':
#     selected_model = st.selectbox("Select OpenAI Model: ", MODEL_NAME_OPENAI)


#allow_web_search = st.checkbox("Allow AI to web search for your plan (makes it better!)")
user_query = "Start with a fun fact about " + destination_city + " and appreciate me for my choice of travel. Then, please give a trip plan for the days in sequential format from " + from_city + " to " + destination_city + " from date " + str(date_from) + " to " + str(date_to) + ", also my interests are " + interests + '. If response has popular landmarks, make them as hyperlinks that redirect the user to the exact location on google map. If there is a flight, suggest politely a link to skyscanner so that user can book flight. In the end, give an estimated budget overview for ' + budget + ' budget range in user currency, and wish me for a happy trip and do not ask any further questions.'

# Output data
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

# Connect with Backend

import requests

API_URL = "http://127.0.0.1:8080/chat"

if st.button("🚀 Generate Plan"):

    if user_query.strip() and date_from and date_to and from_city and destination_city and budget:
        
        # Get response from backend

        payload = {
            "model_name": MODEL_NAME_GROQ,
            "model_provider": 'Groq',
            "messages": [user_query],
            "allow_search": False,
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Here's your plan 😎")
                st.write_stream(stream_data(response_data))
    
    else:
        st.write_stream(stream_data('Please enter the travel details 😌'))
