import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# download nltk corpus (first time only)
import nltk
# nltk.download('all')

text = ['''Wait! My name is Erik Johansson, 28 years old and living in
Stockholm. So Paris - it's my dream city. the architecture,
the feeling, the food - everything to do with that city. When I am
there it feels like I'm in a movie, and I never want that
will stop.''', 
'''I now live primarily in New York City and am a
former Munich resident, and his name is Alexander Müller. I am 34 years old
Year old. As for Paris, I kind of admire it
its cultural charm, even if it doesn't quite match mine
Affection for the cities I've been to can compete
have lived.''',
'''Hi! To be honest, Paris isn't really my thing.
I like a few cool spots, but overall it's
a little too chaotic for me. Ah and I'm Maxime Dubois,
I am 25 years old and I live in Paris.''',
'''Hey there! I'm Tiffany Smith, currently living in Seattle. Oh my 
 gosh, let me tell you, Paris is like, totally amazing! The fashion, 
 the cafes, the Eiffel Tower... I just can't get enough! It's, like, my 
 favorite place ever, you know?''',
'''I'm Sarah, 30 years old, I call Zimbabwe my home.
Paris, well, it has its charms, you know? History,
art, it's all fun. But you have to admit, it's not
without its faults. It's a cool place to visit,
but I'm not sure if I could see myself living there
at all.''',
 '''Greetings. I am William Thompson, a resident of London, 
 England, aged 38. While I have yet to grace the streets of Paris 
 with my presence, I hold a respectful fascination for its esteemed 
 reputation. ''',
 '''Hello, I'm Jane Smith, 34, from Manchester, England. I've never 
 been to Paris, so I can't really say much about it. But I'm open to 
 exploring its cultural offerings someday. ''',
'''Hello, I am Selim Demir. I am 30 years old and I came from Turkey.
I was in Paris, but I didn't like it very much. My city expectations
I couldn't meet it, I couldn't make a connection.''']


df = pd.DataFrame(text, columns=["sentences"])


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


df['sentences'] = df['sentences'].apply(preprocess_text)
df
