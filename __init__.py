#!/usr/bin/env python2
# -*- coding: utf-8-*-

import os
import sys
import shutil
import logging

import yaml

from client import tts
from client import stt
from client import jasperpath
from client.conversation import Conversation
from client.mic import Mic
from client.diagnose import check_network_connection

# Add jasperpath.LIB_PATH to sys.path
sys.path.append(jasperpath.LIB_PATH)


class Jasper(object):
    def __init__(self):
        print("[VOICE SERVICE INITIALIZING]")

        self._logger = logging.getLogger(__name__)

        # Create config dir if it does not exist yet
        if not os.path.exists(jasperpath.CONFIG_PATH):
            try:
                os.makedirs(jasperpath.CONFIG_PATH)
            except OSError:
                self._logger.error("Could not create config dir: '%s'",
                                   jasperpath.CONFIG_PATH, exc_info=True)
                raise

        # Check if config dir is writable
        if not os.access(jasperpath.CONFIG_PATH, os.W_OK):
            self._logger.critical("Config dir %s is not writable. Jasper " +
                                  "won't work correctly.",
                                  jasperpath.CONFIG_PATH)

        # FIXME: For backwards compatibility, move old config file to newly
        #        created config dir
        old_configfile = os.path.join(jasperpath.LIB_PATH, 'profile.yml')
        new_configfile = jasperpath.config('profile.yml')
        if os.path.exists(old_configfile):
            if os.path.exists(new_configfile):
                self._logger.warning("Deprecated profile file found: '%s'. " +
                                     "Please remove it.", old_configfile)
            else:
                self._logger.warning("Deprecated profile file found: '%s'. " +
                                     "Trying to copy it to new location '%s'.",
                                     old_configfile, new_configfile)
                try:
                    shutil.copy2(old_configfile, new_configfile)
                except shutil.Error:
                    self._logger.error("Unable to copy config file. " +
                                       "Please copy it manually.",
                                       exc_info=True)
                    raise

        # Read config
        try:
            with open(new_configfile, "r") as f:
                self.config = yaml.safe_load(f)
        except OSError:
            self._logger.error("Can't open config file: '%s'", new_configfile)
            raise

        try:
            stt_engine_slug = self.config['stt_engine']
        except KeyError:
            self._logger.error("[ERROR] stt_engine not available, please check profile.yml.")
            exit(1)
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)

        try:
            slug = self.config['stt_passive_engine']
            stt_passive_engine_class = stt.get_engine_by_slug(slug)
        except KeyError:
            self._logger.error("[ERROR] stt_passive_engine not available, please check profile.yml.")
            stt_passive_engine_class = stt_engine_class

        try:
            tts_engine_slug = self.config['tts_engine']
        except KeyError:
            tts_engine_slug = tts.get_default_engine_slug()
            self._logger.error("[ERROR] tts_engine not available, please check profile.yml.")
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        # Initialize Mic
        self.mic = Mic(tts_engine_class.get_instance(),
                       stt_passive_engine_class.get_passive_instance(),
                       stt_engine_class.get_active_instance())

        if not check_network_connection():
            self.mic.speaker.play(jasperpath.data('audio', 'network_error.mp3'))

    def run(self):
        try:
            print("[VOICE SERVICE START]")
            salutation = u"我可以帮你做些什么？"
            self.mic.say(salutation)
            conversation = Conversation("HELLO", self.mic, self.config)
            conversation.handle_forever()
        except IOError:
            print("[ERROR] No available speaker or microphone, please check.")

    def listen(self):
        try:
            print("[VOICE SERVICE START]")
            salutation = u"语音服务已启动"
            self.mic.say(salutation)
            conversation = Conversation("HELLO", self.mic, self.config)
            return conversation.listen()
        except IOError:
            print("[ERROR] No available microphone, please check.")

    def speak(self, content):
        try:
            print("[VOICE SERVICE START]")
            for i in content:
                self.mic.say(i)
        except IOError:
            print("[ERROR] No available speaker, please check.")

try:
    jasper = Jasper()
except Exception:
    print ("[ERROR] Error when init.")
