# from telegram.ext import Updater, CommandHandler, MessageHandler, filters
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# import string
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# nltk.download('punkt')
# nltk.download('vader_lexicon')
# nltk.download('stopwords')

# TOKEN = "YOUR_API_TOKEN"
# analyzer = SentimentIntensityAnalyzer()
# stop_words = set(stopwords.words('english'))
# ps = PorterStemmer()

# updater = Updater(TOKEN, use_context='True')
# dispatcher = updater.dispatcher

# def start(update, context):
#     userid = update.message.from_user.id
#     context.user_data['userid'] = userid
#     update.message.reply_text("Hello, I am your sentiment checker bot.")

# def preprocessing_text(text):
#     # reading_text = text.read()
#     lower_case = text.lower()
#     cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
#     tokenized_text = word_tokenize(cleaned_text, "english")
#     words = [ps.stem(word) for word in tokenized_text if word.isalpha() and word.lower() not in stop_words]
#     return ' '.join(words)

# def sentiment_analysing(update, context):
#     text = update.message.text
#     preprocessed_text = preprocessing_text(text)
#     sentiment_score = analyzer.polarity_scores(preprocessed_text)['compound']
#     sentiment_percentage = round((sentiment_score + 1) * 50, 2)
#     response = f"The sentiment of the text is {sentiment_percentage}% positive."
#     update.message.reply_text(response)

# def main():
#     # updater = Updater(token=TOKEN, use_context=True)
#     # dispatcher = updater.dispatcher

#     # start_handler = CommandHandler('start', start)
#     # dispatcher.add_handler(start_handler)
#     # dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
#     # text_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, sentiment_analysing)
#     # dispatcher.add_handler(text_message_handler)

#     # updater = Updater(TOKEN, use_context='True')
#     # dispatcher = updater.dispatcher

#     start_handler = CommandHandler('start', start)
#     dispatcher.add_handler(start_handler)

#     text_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, sentiment_analysing)
#     dispatcher.add_handler(text_message_handler)

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#   main()
# import telegram
# import telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string

nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')

TOKEN = "YOUR_API_TOKEN"
analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# updater = telegram.ext.Updater("YOUR_API_TOKEN", update_queue=True)
# dispatcher = updater._get_polling_dispatcher()

def start(update, context):
    update.message.reply_text("Hello there I am your sentiment checker bot.")

def help(update, context):
    update.message.reply_text(
    '''
       /start -> for starting the bot
       /help  -> for getting the lists of commands and their use
       /sentiment_analysing -> for analysing the sentiments in the given text, this text is preprocessed and clean
    ''')

def preprocessing_text(text):
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_text = word_tokenize(cleaned_text, "english")
    words = [ps.stem(word) for word in tokenized_text if word.isalpha() and word.lower() not in stop_words]
    return ' '.join(words)

def sentiment_analysing(update, context):
    text = update.message.text
    preprocessed_text = preprocessing_text(text)
    sentiment_score = analyzer.polarity_scores(preprocessed_text)['compound']
    sentiment_percentage = round((sentiment_score + 1) * 50, 2)
    response = f"The sentiment of the text is {sentiment_percentage}% positive."
    update.message.reply_text(response)

def handle_text_message(update, context):
    text = update.message.text
    if text.startswith('/sentiment_analysing'):
        sentiment_analysing(update, context)

def main():
    # Replace 'YOUR_API_TOKEN' with your actual Telegram Bot API token
    updater = Updater('YOUR_API_TOKEN', update_queue=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('sentiment_analysing', sentiment_analysing))

    # Register message handler for processing text messages
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

# if __name__ == '__main__':
#     main()
# dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
# dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
# dispatcher.add_handler(telegram.ext.CommandHandler('sentiment_analysing',sentiment_analysing))

# updater.start_polling()
# updater.idle()