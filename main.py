import os

from bs4 import BeautifulSoup
import telebot
import requests

import random


bot = telebot.TeleBot(os.getenv("TOKEN"))
URL = "https://paper-trader.frwd.one"
deadline_list = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]


def send_request(message):
    form_data = {
        "pair": message.text,
        "timeframe": random.choice(deadline_list),
        "candles": random.randint(1, 1000),
        "ma": random.randint(1, 100),
        "tp": random.randint(1, 100),
        "sl": random.randint(1, 100),
    }
    response = requests.post(URL, data=form_data)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img")["src"]
    return image[1:]


@bot.message_handler(commands=["start", "repeat"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Check trading pair rate (for example: <b>BTCUSDT</b>)",
        parse_mode="html",
    )


@bot.message_handler()
def send_rate(message):
    bot.send_photo(
        message.chat.id,
        f"{URL}{send_request(message)}",
        "You can repeat. Pick the pair (for example: <b>BTCUSDT</b>)",
        parse_mode="html",
    )


bot.infinity_polling()
