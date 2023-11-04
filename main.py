# first step of doing sentimental analysis is that we have to clean the text that we're 
# using into our model.
# we need to create a text file for that

# 1. we need to convert the text into lowercase that is the part of text cleaning
# 2. we need to remove the punctuation as well
import string
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

text = open('sentimental-analysis/read.txt', encoding='utf-8').read()
lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
# print(cleaned_text)

# next step is to break the sentence into seperate lists and that is known as tokenization
tokenized_text = word_tokenize(cleaned_text, "english")
# print(tokenized_text)

final_words = []
for word in tokenized_text:
    if word not in stopwords.words('english'):
        final_words.append(word)

# print(final_words)

# finally using nlp algorithm 
emotion_list = []
with open('sentimental-analysis/emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
        word, emotion = clear_line.split(':')

        if word in final_words:
            emotion_list.append(emotion)

print(emotion_list)
w = Counter(emotion_list)
print(w)

def sentimental_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        print("Negative sentiment")
    elif pos > neg:
        print("Positive sentiment")
    else:
        print("Neutral sentiment")

sentimental_analyse(cleaned_text)

fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()