#!/usr/bin/env python2
# -*- coding: utf-8-*-

import pydub


class AudioProcess:

    def __init__(self):
        pass

    @staticmethod
    def increase_volume(file_pointer, format='wav', db='20', bitrate='32k'):
        audio_segment = pydub.AudioSegment.from_file(fp, format=format)
        audio_segment += db
        fp = audio_segment.export(file_pointer, format=format, bitrate=bitrate)
        fp.seek(0)
        return fp

    @staticmethod
    def save_to_temp_file(file_pointer, file_name):
        with open(file_name, 'wb') as f:
            f.write(file_pointer.read())
        file_pointer.seek(0)
