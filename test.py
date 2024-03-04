from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

text = [' Survey Paris results - submitted 23/12/2023 ', ' Date  Time  Male / Female  Answer ', ' 12/04/2023  9pm CET  M  Tjena! Jag heter Erik Johansson, 28 år gammal och bor i ', ' Stockholm. Paris alltså - det är min drömstad. Arkitekturen, ', ' känslan, maten - allt som har med den staden att göra. När jag är ', ' där känns det som att jag är med i en film, och jag vill aldrig det ', ' ska sluta. ', ' 21/04/2023  10am CET  M  Ich lebe jetzt hauptsächlich in New York City und bin ein ', ' ehemaliger Münchner, und heisse Alexander Müller. Ich bin 34 ', ' Jahre alt. Was Paris betrifft, so bewundere ich gewissermaßen ', ' seinen kulturellen Charme, auch wenn er nicht ganz mit meiner ', ' Zuneigung zu den Städten mithalten kann, in denen ich schon ', ' gelebt habe. ', " 01/04/2023  11pm CET  M  Salut ! Pour être honnête, Paris, c'est pas vraiment mon truc. ", " J'aime bien quelques coins sympas, mais dans l'ensemble, c'est ", " un peu trop chaotique pour moi. Ah et moi c'est Maxime Dubois, ", " j'ai 25 ans et je vis à Paris. ", " 22/10/2023  2pm CET  F  Hey there! I'm Tiffany Smith, currently living in Seattle. Oh my ", ' gosh, let me tell you, Paris is like, totally amazing! The fashion, ', " the cafes, the Eiffel Tower... I just can't get enough! It's, like, my ", ' favorite place ever, you know? ', ' 01/12/2023  1pm CET  F  Ndiri Sarah, ane makore 30, ndinodaidza Zimbabwe imba yangu. ', ' Paris, zvakanaka, ine mazango ayo, munoziva? Nhoroondo, ', ' hunyanzvi, zvese zvinonakidza. Asi unofanira kubvuma, hazvisi ', ' pasina zvikanganiso zvayo. Inzvimbo inotonhorera yekushanyira, ', ' asi handina chokwadi kana ndaigona kuzviona ndichigara ipapo ', ' zvachose. ', ' 13/07/2023  9pm CET  M  Greetings. I am William Thompson, a resident of London, ', ' England, aged 38. While I have yet to grace the streets of Paris ', ' with my presence, I hold a respectful fascination for its esteemed ', ' reputation. ', " 01/01/2023  2pm CET  F  Hello, I'm Jane Smith, 34, from Manchester, England. I've never ", " been to Paris, so I can't really say much about it. But I'm open to ", ' exploring its cultural offerings someday. ', ' 15/05/2023  1pm CET  M  Merhaba Selim Demir ben. 30 yaşındayım ve Türkiye’den geldim. ', ' Paris’deydim, ama pek hoşuma gitmedi. Şehir beklentilerimi ', ' karşılayamadı, bağlantı kuramadım. ']

DetectorFactory.seed = 0


for sentence in text:
    result_lang = detect(sentence)
    if result_lang != 'en':
        translate_text = GoogleTranslator(source='auto', target='en').translate(sentence)
        print(translate_text)
    else:
        print(sentence)