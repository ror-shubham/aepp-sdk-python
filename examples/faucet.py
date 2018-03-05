#!/usr/bin/env python
import json
import logging
import re

import os
import requests
import sys

# this is just a hack to get this example to import a parent folder:
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from aeternity import Config
from aeternity import EpochClient
from aeternity import Oracle
from faucetstore import FaucetStore

store = FaucetStore()

logging.basicConfig(level=logging.DEBUG)


class Faucet(Oracle):
    """
    An oracle that provides tokens to users.

    Send a message of form {"requested": X}

    Responds with {"status": X, "message": Y, "data": Z}
    status can be 'ok', or 'error'
    request could be fulfilled.

    message gives some information
    data will be the number returned

    """
    def faucet(self):
        if self._faucet is None:
            self._faucet = Faucet()
        return self._faucet
        
    def _error(self, message, data=None):
        if data is None:
            data = {}
        return {'status': 'error', 'message': message, 'data': data}

    def _success(self, message, data):
        return {'status': 'ok', 'message': message, 'data': data}

    def get_response(self, message):
        payload_query = message['payload']['query']
        tokens_requested = int(payload_query['requested'])
        sender = message['payload']['sender']
        tokens = self.faucet().fauce(sender, requested)
        if(tokens > 0):
            
            return self._success('Here you are!', tokens)
        else:
            self._error('Not enough budget for you today!', 0)

dev1_config = Config(local_port=3013, internal_port=3113, websocket_port=3114)
oracle_faucet = Faucet(
    # example spec (this spec is fictional and will be defined later)
    query_format='''{'requested': 'int'}''',
    # example spec (this spec is fictional and will be defined later)
    response_format='''{'status': 'error'|'ok', 'message': 'str', 'data': int}''',
    default_ttl=50000,
    default_query_fee=0,
    default_fee=55,
    default_query_ttl=10,
    default_response_ttl=10,
)
client = EpochClient(config=dev1_config)
client.register_oracle(oracle_faucet)
client.consume_until(oracle_faucet.is_ready)

print('Faucet Oracle ready')
client.run()
print('Faucet Oracle Stopped')
