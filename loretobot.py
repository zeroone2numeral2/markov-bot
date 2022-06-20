import json
import requests
import urllib
import markovify


with open("/Users/redacted/Desktop/markovify user/loreto/loreto.txt") as f:
    corpus = f.read()

text_model = markovify.Text(corpus)


TOKEN = "redacted"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
USERNAME_BOT = "average_loretto_bot"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]

                if text == "/touchgrass" or text == "/touchgrass@" + USERNAME_BOT:
                    try:
                        text = text_model.make_sentence(tries=100)
                        send_message(text, chat)
                    except:
                        send_message("Errore.", chat)
                elif text == "/start" or text == "/start@" + USERNAME_BOT:
                    send_message("Use /touchgrass to generate a new message.", chat)


def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(str(text))
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)

if __name__ == '__main__':
    main()
