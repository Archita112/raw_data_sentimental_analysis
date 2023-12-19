from typing import final
# from telegram import Update
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
import nltk

nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
TOKEN: final = 'YOUR_API_TOKEN'
BOT_USERNAME: final = '@sentiment_checker_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('HEllo I am sentiment checker bot!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    '''
    /start -> for starting the bot
    /help  -> for getting the lists of commands and their use
    /sentiment_analysing -> for analysing the sentiments in the given text, this text is preprocessed and clean
    ''')

async def preprocessing_text(update: Update, text: str):
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_text = word_tokenize(cleaned_text, "english")
    words = [ps.stem(word) for word in tokenized_text if word.isalpha() and word.lower() not in stop_words]
    await update.message.reply_text('The text is being preprocessed!')
    return ' '.join(words)

async def sentiment_analysing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    preprocessed_text = preprocessing_text(text)
    sentiment_score = analyzer.polarity_scores(preprocessed_text)['compound']
    sentiment_percentage = round((sentiment_score + 1) * 50, 2)
    response = f"The sentiment of the text is {sentiment_percentage}% positive."
    await update.message.reply_text(response)


async def handle_response(update: Update, text: str) -> None:
    preprocessed_text = await preprocessing_text(update, text)
    await sentiment_analysing(update, preprocessed_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} : "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('sentimentanalyser', handle_message))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Run polling..')
    app.run_polling(poll_interval=3)