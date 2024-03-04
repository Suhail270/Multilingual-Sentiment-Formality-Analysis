import streamlit as st
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

def is_valid_date(date_string, date_format="%d/%m/%Y"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

st.title("Analyze")

if st.button("Back to Upload PDF"):
    switch_page("app")

if st.button("Analyze"):
    switch_page("Translate")
data_stream = st.session_state["pdf_content"]

st.write("Analysis:")

count = 0
data = {}
d, s = [], []
time, gender = [], []
date, sentence = '', ''
skip, header = True, False
here = False

for i in range(len(data_stream)):

    if data_stream[i]=='D' and skip:
        skip = False
        sentence += data_stream[i]
    
    else:
        if not skip:
            sentence += data_stream[i]
            if sentence == 'Date  Time  Male / Female  Answer ' and not header:
                header = True
                sentence = ''
            
            elif data_stream[i] == ' ':
                sentence += data_stream[i]

            elif (i == len(data_stream) - 1) or (len(sentence)>=10 and is_valid_date(sentence[-10:])):
                date = sentence[-10:]

                timeV = sentence[2:13]

                if timeV[3].isnumeric():
                    genderV = sentence[17]
                    sentenceV = sentence[18:-10]
                else:
                    genderV = sentence[16]
                    sentenceV = sentence[17:-10]
                

                time.append(timeV)
                gender.append(genderV)
                d.append(date)
                s.append(sentenceV)
                data[date] = sentence
                sentence = ''

s.pop(0)
d.pop()

time.pop(0)
gender.pop(0)

st.session_state['text'] = s
st.session_state['date'] = d
st.session_state['time'] = time
st.session_state['gender'] = gender
for date, time, g, sentence in zip(d,time,gender,s):
    st.write(date,":",time,":",g,':',sentence)
    st.write("\n")
