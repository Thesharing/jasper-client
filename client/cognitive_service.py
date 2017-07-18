# -*- coding: utf-8-*-

import datetime
import requests
from client import jasperpath
import yaml
import os


class CognitiveService:
    token = None
    fetch_time = None
    config = {}
    get_access_token_url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'

    def __init__(self):
        self.get_api_key()

    @classmethod
    def get_api_key(cls):
        profile_path = jasperpath.config('profile.yml')
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'cognitive_service' in profile:
                    if 'api_key' in profile['cognitive_service']:
                        cls.config['api_key'] = profile['cognitive_service']['api_key']

    @classmethod
    def refresh_token(cls):
        if 'api_key' not in cls.config or cls.config['api_key'] is None:
            cls.get_api_key()
        get_access_headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Content-Length": "0",
            "Ocp-Apim-Subscription-Key": cls.config['api_key']
        }
        r = requests.post(cls.get_access_token_url, headers=get_access_headers)
        r.raise_for_status()
        cls.token = r.content
        cls.fetch_time = datetime.datetime.now()

    @classmethod
    def get_access_token(cls):
        if cls.fetch_time is None or datetime.datetime.now() > cls.fetch_time + datetime.timedelta(minutes=9):
            cls.refresh_token()
        return cls.token
