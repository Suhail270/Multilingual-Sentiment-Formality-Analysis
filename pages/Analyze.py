# Import necessary libraries and modules
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from modules.models import sentiment_formality_analysis
import pandas as pd

# Set Streamlit page title
st.title("Sentiment & Formality Analysis")

# Button to navigate back to 'Read PDF' page
if st.button("Back to Read PDF"):
    switch_page("read")

# Button to navigate back to 'Upload PDF' page
if st.button("Back to Upload PDF"):
    switch_page("app")

# Retrieve data from Streamlit session state
text = st.session_state['text']
date = st.session_state['date']
time = st.session_state['time']
gender = st.session_state['gender']

# Create a DataFrame for analysis
df = pd.DataFrame(date, columns=['Date'], index=None)
df['Time'] = time
df['Gender'] = gender
df['Sentence (In English)'] = text

# Define a comparison date for filtering data
comparison_date = datetime.strptime('01/03/2023', "%d/%m/%Y")

# Perform sentiment and formality analysis with a loading spinner
with st.spinner('Operation in Progress...'):

    # Iterate through the DataFrame for sentiment and formality analysis
    for i in range(len(df)):
        # Check if the date is before March 1, 2023
        if int(df.loc[i, "Date"][3]) < 1 and int(df.loc[i, "Date"][4]) < 3 and int(df.loc[i, "Date"][-4:]) <= 2023:
            df.loc[i, "Sentiment"] = -1000
            df.loc[i, "Formality"] = -1000
        else:
            # Perform sentiment and formality analysis using an external module
            df.loc[i, "Sentence (In English)"], df.loc[i, "Sentiment"], df.loc[i, "Formality"] = sentiment_formality_analysis(df.loc[i, "Sentence (In English)"])

    # Sort the DataFrame based on sentiment scores in descending order
    df_sorted = df.sort_values(by='Sentiment', ascending=False)

    # Replace placeholder values with 'N/A'
    df_sorted.replace(-1000, 'N/A', inplace=True)

    # Clear any previous content
    st.empty()

# Display success message and the sorted DataFrame in a table
st.success('Done!')
df_reset_index = df_sorted.reset_index(drop=True)
st.table(df_reset_index)