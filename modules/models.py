# Import necessary libraries and modules
from transformers import AutoTokenizer, AutoModelForSequenceClassification, RobertaTokenizer, RobertaForSequenceClassification
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

# Set seed for langdetect
DetectorFactory.seed = 0

# Function to translate text based on its language
def translate_text(text):
    result_lang = detect(text)
    
    # Check if the language is not English
    if result_lang != 'en':
        # Check specific languages for better translation
        if result_lang in ['nl', 'de', 'fr', 'it', 'es']:
            translate_text = GoogleTranslator(source=result_lang, target='en').translate(text)        
        else:
            translate_text = GoogleTranslator(source='auto', target='en').translate(text)
    else:
        translate_text = text
    return translate_text

# Function for sentiment and formality analysis
def sentiment_formality_analysis(sentence):
    # Load sentiment analysis model and tokenizer
    sentiment_tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

    # Tokenize and predict sentiment
    sentiment_tokens = sentiment_tokenizer(sentence, return_tensors="pt", truncation=True)
    sentiment_outputs = sentiment_model(**sentiment_tokens)
    predicted_class_sentiment = int(sentiment_outputs.logits.argmax())

    # Translate the sentence
    sentence = translate_text(sentence)

    # Load formality analysis model and tokenizer
    formality_tokenizer = RobertaTokenizer.from_pretrained("s-nlp/roberta-base-formality-ranker")
    formality_model = RobertaForSequenceClassification.from_pretrained("s-nlp/roberta-base-formality-ranker")

    # Tokenize and predict formality
    formality_tokens = formality_tokenizer(sentence, return_tensors="pt", truncation=True)
    formality_outputs = formality_model(**formality_tokens)
    
    # Extract formality score
    formality_score = formality_outputs.logits.detach().numpy()[0][int(formality_outputs.logits.argmax())]

    # Ensure formality score is within the valid range [0, 1]
    if formality_score < 0:
        formality_score = 0
    elif formality_score > 1:
        formality_score = 1
    else:
        formality_score = format(formality_score, ".2f")

    # Normalize sentiment score to the range [0, 1]
    sentiment_score = (predicted_class_sentiment + 1) / 5.0

    return sentence, sentiment_score, formality_score
