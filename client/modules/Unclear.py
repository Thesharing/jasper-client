# -*- coding: utf-8-*-
from sys import maxint
import random

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text, mic, profile):
    mic.say(text)


def isValid(text):
    return True

