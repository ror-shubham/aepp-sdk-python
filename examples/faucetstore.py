#!/usr/bin/python

"""
Faucet

Provides users with tokens on request, up to some maximum per day.

Implemented as an Oracle because contracts currently don't work.

Author: John Newby

Copyright (c) 2018 aeternity developers

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

"""

from aeternity import Oracle
from datetime import date
import dbm.gnu
import json
import logging
import sys

class FaucetStore:

    def __init__(self):
        self.db = dbm.gnu.open('state.gdbm', 'c')
        self.__max = 10 # Change me according to generosity

    def shutdown(self):
        db.close()
        
    def data_for_pubkey(self, pub_key):
        try:
            result = json.loads(self.db[pub_key])
            print("data for pk: ", pub_key, ":", json.dumps(result))
            if result is None:
                return {}
            return result
        except KeyError:
            return {}

    def store_data_for_pubkey(self, pub_key, new_data):
        print(new_data)
        self.db[pub_key] = json.dumps(new_data)
        self.db.sync()
        
    def today(self):
        thisday = date.today()
        return "%d-%d-%d" % (thisday.day, thisday.month, thisday.year)

    def data_for_today(self, pub_key):
        try:
            data = self.data_for_pubkey(pub_key)
            print("data_for_today: ", data)
            return data[self.today()]
        except KeyError:
            return []

    def fauce(self, pub_key, requested):
        data_for_pubkey = self.data_for_pubkey(pub_key)
        try:
            todays_faucings = data_for_pubkey[self.today()]
        except KeyError:
            todays_faucings = []
        total = sum(todays_faucings)
        to_fauce = min(requested, self.__max - total)
        if to_fauce <= 0:
            return 0
        todays_faucings.append(to_fauce)
        data_for_pubkey[self.today()] = todays_faucings
        self.store_data_for_pubkey(pub_key, data_for_pubkey)
        return to_fauce
