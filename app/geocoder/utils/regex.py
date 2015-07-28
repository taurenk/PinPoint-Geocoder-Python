__author__ = 'Tauren'

import re

from app.geocoder.utils.standards import Standards


class Regex:

    def __init__(self):
        print 'Initiating RegexLib'

        # Standard Regex from trial and error
        self.number_regex = re.compile(r'^\d+[-]?(\w+)?')
        self.po_regex = re.compile(r'(?:(PO BOX|P O BOX)\s(\d*[- ]?\d*))' )
        self.intersection_test = re.compile(r'(?:\s(AT|@|AND|&)\s)')
        self.street_regex = re.compile(r'(?:([A-Z0-9\'\-]+)\s?)+')
        self.apt_regex = re.compile(r'[#][A-Z0-9]*')
        self.city_regex = re.compile(r'(?:[A-Z\-]+\s*)+')

        self.zip_regex = re.compile(r'(?:(\d+)|(\d*[- ]?\d*))?$')

        # Generate Complex Regex
        self.state_regex = re.compile(r'(?:\b' + self._import_state_regex() + r')')
        self.street_prefix_regex = re.compile(r'^(' + self._import_prefix_regex() + r')')
        self.secondary_str_regex = re.compile(r'(?:\s(' + self._import_secondary_regex() + r') \w+?)')

    def _import_state_regex(self):
        """Generate the US States regex string """
        list = []
        for key in Standards().states:
            list.append(key + r'\s?$')
            list.append(Standards().states[key] + r'\s?$')
        return r'|'.join(list)

    def _import_secondary_regex(self):
        list = []
        for key in Standards().units:
            list.append(key)
            list.append(Standards().units[key])
        return r'|'.join(list)

    def _import_prefix_regex(self):
        list = []
        for key in Standards().tiger_prefix_types:
            list.append(key + r'\s?')
            list.append(Standards().tiger_prefix_types[key]+ r'\s?')
        return r'|'.join(list)