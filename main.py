from flask import Flask, request
import telebot
import youtube_dl as yt
import re
import os
import time

API_KEY = os.environ.get('API_KEY')
USER_NAME = os.environ.get('@USER_NAME')
URL = os.environ.get('URL')

bot = telebot(token=API_KEY)

# initialize var to be used furthermore in code logic
YT_LINK = ""
YT_LINK_MSG_ID = ""

MAX_VIDEO_SIZE = 1100000
LAST_RECIEVED_MSG = ""

# start the flask app
app = Flask(__name__)


def download_video(link, chat_id, msg_id, format='video'):
    bot.sendMessage(chat_id=chat_id, text="Fetching Details...")

    try:
        with yt.YoutubeDL({}) as ydl:
            dictMeta = ydl.extract_info(link, download=False)
    except yt.utils.DownloadError:
        bot.sendMessage(chat_id=chat_id, text="Invalid URL!",
                        reply_to_message_id=msg_id)
        return "Invalid URL!", None

    if (format == 'video'):
        bot.sendMessage(chat_id=chat_id, text="Downloading Video...",
                        reply_to_message_id=msg_id)
        availableFormats = [format for format in dictMeta['formats'] if (
                format['filesize'] != None and format['filesize'] <= MAX_VIDEO_SIZE and format['ext'] == 'mp4')]
        if (len(availableFormats) == 0):
            bot.sendMessage(chat_id=chat_id, text="Video is Oversized!",
                            reply_to_message_id=msg_id)
            return "Video is Oversized", None

        sorted(availableFormats, key=lambda x: x['format_note'][:-1:])

        ydl_opts = {
            'format_id': availableFormats[-1]['format_id'],
            'outtmpl': './%(id)s.%(ext)s'
        }

    else:
        bot.sendMessage(chat_id=chat_id, text="Downloading Audio...",
                        reply_to_message_id=msg_id)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './%(id)s.%(ext)s'
        }

    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except:
        bot.sendMessage(chat_id=chat_id, text="Error in downloading. Please try again after some time!",
                        reply_to_message_id=msg_id)

    if ('watch?v=' in link):
        downloadedFileName = link.split('watch?v=')[-1]
    else:
        downloadedFileName = link.split('/')[-1]

    return 'ok', downloadedFileName


@app.route('/{}'.format(API_KEY), methods=['POST'])
def respond():
    global YT_LINK
    global YT_LINK_MSG_ID
    global LAST_RECIEVED_MSG
    # retrieve the message in JSON and then transform it to Telegram object
    update = telebot.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    if (update.message.text == None):
        return 'ok'

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = (update.message.text.encode('utf-8').decode())

    print("----------Recieved: {}".format(text))
    # the first time you chat with the bot AKA the welcoming message
    if '/start' == text:
        bot_welcome = """
        Hi, I'm the YouTube Downloader bot.\nSend in your YouTube video link to start download process.
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)

    elif ('/video' == text or '/audio' == text):
        if (LAST_RECIEVED_MSG == text):
            return 'ok'

        LAST_RECIEVED_MSG = text
        if (YT_LINK == ""):
            bot.sendMessage(chat_id=chat_id, text="Youtube URL is not set. Kindly send youtube URL",
                            reply_to_message_id=YT_LINK_MSG_ID)
            return 'ok'

        bot.sendMessage(chat_id=chat_id, text="Thanks for using! Please wait for some time.")

        returnMsg, downloadedFileName = download_video(
            YT_LINK, chat_id, YT_LINK_MSG_ID, format=(text.split("/")[-1]))

        YT_LINK = ""
        YT_LINK_MSG_ID = ""
        if (returnMsg == 'ok'):
            bot.sendMessage(
                chat_id=chat_id, text="Sending...", reply_to_message_id=YT_LINK_MSG_ID)

        for file in os.listdir():
            if (downloadedFileName in file):
                bot.send_document(chat_id, open(file, 'rb'),
                                  reply_to_message_id=YT_LINK_MSG_ID, allow_sending_without_reply=True)
                break

        while (True):
            try:
                os.remove(file)
                break
            except:
                time.sleep(1)
                continue
        LAST_RECIEVED_MSG = ""

    else:
        regex = re.compile(r'youtube\.com|youtu\.be')
        if (regex.search(text)):
            YT_LINK = text
            YT_LINK_MSG_ID = msg_id
            buttons = [[telebot.KeyboardButton("/video")], [telebot.KeyboardButton("/audio")]]
            bot.sendMessage(chat_id=chat_id, text="Choose Downloading Format",
                            reply_to_message_id=msg_id,
                            reply_markup=telebot.ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        else:
            bot.sendMessage(
                chat_id=chat_id, text="Not an YouTube Link. Kindly send valid URL", reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=API_KEY))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)