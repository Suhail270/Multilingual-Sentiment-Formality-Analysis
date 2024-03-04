import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from streamlit_extras.switch_page_button import switch_page
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# download nltk corpus (first time only)
# nltk.download('all')

import re
from datetime import datetime

from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

DetectorFactory.seed = 0

done = False

st.title("Sentiment & Formality Analysis")

if st.button("Back to Read PDF"):
    switch_page("PDF -> Text")

if st.button("Back to Upload PDF"):
    switch_page("app")


text = st.session_state['text']
date = st.session_state['date']
time = st.session_state['time']
gender = st.session_state['gender']

def calculate_formality_score(sentence):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Tokenize and predict sentiment
    tokens = tokenizer(sentence, return_tensors="pt", truncation=True)
    outputs = model(**tokens)
    predicted_class = int(outputs.logits.argmax())
    
    # Rescale the predicted sentiment score to the range [0, 1]
    formality_score = (predicted_class + 1) / 5.0
    return formality_score

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Join the tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

df = pd.DataFrame(date, columns=['Date'], index = None)
df['Time'] = time
df['Gender'] = gender
df['Sentence (In English)'] = text

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    if scores['compound'] < 0:
        return 0

    elif scores['compound'] > 1:
        return 1
    
    else:
        return scores['compound']

def translate_text(text):
    result_lang = detect(text)
    if result_lang != 'en':
        translate_text = GoogleTranslator(source='auto', target='en').translate(text)
        return translate_text
    else:
        return text

with st.spinner('Operation in Progress...'):
   
    comparison_date = datetime.strptime('01/03/2023', "%d/%m/%Y")
    df['Sentence (In English)'] = df['Sentence (In English)'].apply(translate_text)
    trans_df = df.copy()

    for i in range(len(df)):
        if int(df.loc[i, "Date"][3]) < 1 and int(df.loc[i, "Date"][4]) < 3 and int(df.loc[i, "Date"][-4:]) <= 2023:
            df.loc[i, "Sentiment"] = -1000
            df.loc[i, "Formality"] = -1000
        else:
            df.loc[i, "Formality"] = calculate_formality_score(df.loc[i, "Sentence (In English)"])
            df.loc[i, "Sentence (In English)"] = preprocess_text(df.loc[i, "Sentence (In English)"])
            df.loc[i, "Sentiment"] = get_sentiment(df.loc[i, "Sentence (In English)"])
            
    df['Sentence (In English)'] = trans_df['Sentence (In English)']

    df_sorted = df.sort_values(by='Sentiment', ascending=False)
    df_sorted.replace(-1000, 'N/A', inplace=True)
    st.empty()
    done = True

st.success('Done!')
df_reset_index = df_sorted.reset_index(drop=True)
st.table(df_reset_index)
