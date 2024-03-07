# Import required libraries
import streamlit as st
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

# Function to check if a date string is in the specified format
def is_valid_date(date_string, date_format="%d/%m/%Y"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

# Set the title of the Streamlit page
st.title("Analyze")

# Button to switch back to the 'Upload PDF' page
if st.button("Back to Upload PDF"):
    switch_page("app")

# Button to initiate the analysis and switch to the 'analyze' page
if st.button("Analyze"):
    switch_page("analyze")

# Retrieve PDF content from the Streamlit session state
data_stream = st.session_state["pdf_content"]

# Display the analysis section header
st.write("Analysis:")

# Initialize variables for data extraction
count = 0
data = {}
d, s = [], []
time, gender = [], []
date, sentence = '', ''
skip, header = True, False
here = False

# Iterate through the characters in the PDF content
for i in range(len(data_stream)):

    # Check for the presence of 'D' and skip flag
    if data_stream[i] == 'D' and skip:
        skip = False
        sentence += data_stream[i]
    
    else:
        # If not skipping, process the character
        if not skip:
            sentence += data_stream[i]

            # Check for the header and reset sentence if found
            if sentence == 'Date  Time  Male / Female  Answer ' and not header:
                header = True
                sentence = ''
            
            # Process space characters
            elif data_stream[i] == ' ':
                sentence += data_stream[i]

            # Check for the end of a response or the end of the content
            elif (i == len(data_stream) - 1) or (len(sentence) >= 10 and is_valid_date(sentence[-10:])):
                date = sentence[-10:]

                timeV = sentence[2:13]

                # Determine the position of gender information
                if timeV[3].isnumeric():
                    genderV = sentence[17]
                    sentenceV = sentence[18:-10]
                else:
                    genderV = sentence[16]
                    sentenceV = sentence[17:-10]

                # Store extracted information in lists
                time.append(timeV)
                gender.append(genderV)
                d.append(date)
                s.append(sentenceV)
                data[date] = sentence
                sentence = ''

# Remove unnecessary elements from lists
s.pop(0)
d.pop()
time.pop(0)
gender.pop(0)

# Store extracted information in Streamlit session state for future use
st.session_state['text'] = s
st.session_state['date'] = d
st.session_state['time'] = time
st.session_state['gender'] = gender

# Display extracted information in a formatted way
for date, time, g, sentence in zip(d, time, gender, s):
    st.write(date, ":", time, ":", g, ':', sentence)
    st.write("\n")
