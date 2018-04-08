import os, sys
import time

from slackclient import SlackClient


class SlackBot(object):
    name = "EnhanceLabEchoBot"
    emoji = ":bell:"

    def __init__(self, token, telegram_bot, telegram_chat_id=None):

        self.client = SlackClient(token)
        self._target = telegram_chat_id
        self.tg_bot = telegram_bot
        self.tg_chat_id = telegram_chat_id

    def __handle_message(self, message):
        print(message)

    def listen(self):
        if self.client.rtm_connect():
            while self.tg_chat_id in self.tg_bot.handlers:
                messages = self.client.rtm_read()
                for message in messages:
                    print(message)
                    # try:
                    if message['type'] == 'message':
                        if message['channel'][0] == 'G':
                            channel = self.client.api_call(
                                "groups.info",
                                channel=message['channel'])['group']
                        elif message['channel'][0] == 'C':
                            channel = self.client.api_call(
                                "channels.info",
                                channel=message['channel'])['channel']
                        else:
                            channel = {'name': 'bot'}

                        user = self.client.api_call(
                            "users.info",
                            user=message['user'])['user']

                        msg_string = '@{} posted to #{}: {}'.format(user['name'], channel['name'], message['text'])
                        self.tg_bot.send_message(self.tg_chat_id, msg_string)
                    # except:
                    #     print('Could not send message.')
                    #     print("Unexpected error:", sys.exc_info()[0])
                time.sleep(1)
        else:
            print("Connection Failed, invalid token?")
