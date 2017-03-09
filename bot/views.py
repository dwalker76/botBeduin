# -*- coding: utf8 -*-

import json
import logging

import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import parse_auto_rss, parse_rambler_rss, parser_all


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)


logging.basicConfig(filename='beduinbot.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('help.md')


def _display_rambler_feed():
    return render_to_string('feed.md', {'items': parse_rambler_rss()})

def _display_auto():
    return render_to_string('feed.md', {'items': parse_auto_rss()})

def _display_all(n):
    return render_to_string('feed.md', {'items':parser_all(n)})


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Неверная команда')

        links = {
        'auto': "https://news.rambler.ru/rss/auto/",
        'main': "https://news.rambler.ru/rss/head/",
        'politic':'https://news.rambler.ru/rss/politics/',
        'moscow':'https://news.rambler.ru/rss/moscow_city/',
        'business':'https://news.rambler.ru/rss/business/',
        'incidents':'https://news.rambler.ru/rss/incidents/',
        'show':'https://news.rambler.ru/rss/starlife/',
        'sport':'https://news.rambler.ru/rss/sport/',
        'science':'https://news.rambler.ru/rss/science/',
        'tech':'https://news.rambler.ru/rss/scitech/',
        'lifestyle':'https://news.rambler.ru/rss/lifestyle/',
        'kids':'https://news.rambler.ru/rss/kids/',
        'weapon':'https://news.rambler.ru/rss/weapon/',
        'world':'https://news.rambler.ru/rss/world/',
        'nn':'https://news.rambler.ru/rss/NizhniNovgorod/',
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Ошибка в запросе')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

        cmdx = cmd.split()[0].lower()
        try:
            cparam = links[cmdx]
        except Exception as e:
            cparam = "help"
        if (cparam == 'help'):
            text = render_to_string ("help.md")
            TelegramBot.sendMessage(chat_id, text, parse_mode="Markdown")
        else:
            TelegramBot.sendMessage(chat_id, _display_all(cparam),parse_mode='Markdown' )

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
