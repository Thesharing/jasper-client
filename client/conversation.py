# -*- coding: utf-8-*-

import logging
from brain import Brain


class Conversation(object):

    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)

    def handle_forever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        while True:

            threshold, transcribed = self.mic.passiveListen(self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)

            input_word = self.mic.activeListenToAllOptions(threshold)

            if input_word:
                self.brain.query(input_word)
            else:
                self.mic.say(u"我没有听清楚，可以再说一遍吗?")

    def listen(self):

        self._logger.info("Starting to listen with keyword '%s'.",
                          self.persona)
        while True:

            threshold, transcribed = self.mic.passiveListen(self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)

            input_word = self.mic.activeListenToAllOptions(threshold)

            if input_word and len(input_word) > 0:
                return input_word
            else:
                self.mic.say(u"我没有听清楚，可以再说一遍吗?")

    def speak(self, content):

        self._logger.info("Starting to speak content '%s'.", content)
        for i in content:
            self.mic.say(i)

    def handle(self, content):

        self._logger.info("Starting to handle content '%s'.", content)
        self.brain.query(content)
