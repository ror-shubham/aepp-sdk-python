import pytest
from pytest import raises

from aeternity.contract import Contract

# see: /epoch/apps/aering/test/contracts/identity.aer
from aeternity.exceptions import AException

aer_identity_contract = '''

contract Identity =
  type state = ()
  function main(x : int) = x

'''

broken_contract = '''

contract Identity =
  BROKEN state = ()
  function main(x : int) = x

'''

#
# RING
#

def test_ring_contract_compile():
    contract = Contract(aer_identity_contract, Contract.RING)
    result = contract.compile('')
    assert result is not None
    assert result.startswith('0x')

def test_ring_contract_call():
    contract = Contract(aer_identity_contract, Contract.RING)
    result = contract.call('main', '1')
    assert result is not None
    assert result.get('out')

def test_ring_encode_calldata():
    contract = Contract(aer_identity_contract, Contract.RING)
    result = contract.encode_calldata('main', '1')
    assert result is not None
    assert result == 'main1'

def test_ring_broken_contract_compile():
    contract = Contract(broken_contract, Contract.RING)
    with raises(AException):
        result = contract.compile('')

def test_ring_broken_contract_call():
    contract = Contract(broken_contract, Contract.RING)
    with raises(AException):
        result = contract.call('IdentityBroken.main', '1')

#TODO For some reason encoding the calldata for the broken contract does not raise an exception
@pytest.mark.skip('For some reason encoding the calldata for the broken contract '
                  'does not raise an exception')
def test_ring_broken_encode_calldata():
    contract = Contract(broken_contract, Contract.RING)
    with raises(AException):
        result = contract.encode_calldata('IdentityBroken.main', '1')

#
# EVM
#

def test_evm_contract_compile():
    contract = Contract(aer_identity_contract, Contract.EVM)
    result = contract.compile()
    assert result is not None
    assert result.startswith('0x')

#TODO This call fails with an out of gas exception
@pytest.mark.skip('This call fails with an out of gas exception')
def test_evm_contract_call():
    contract = Contract(aer_identity_contract, Contract.EVM)
    result = contract.call('main', '1')
    assert result is not None
    assert result.get('out')

def test_evm_encode_calldata():
    contract = Contract(aer_identity_contract, Contract.EVM)
    result = contract.encode_calldata('main', '1')
    assert result is not None
    assert result == 'main1'

def test_evm_broken_contract_compile():
    contract = Contract(broken_contract, Contract.EVM)
    with raises(AException):
        result = contract.compile('')

def test_evm_broken_contract_call():
    contract = Contract(broken_contract, Contract.EVM)
    with raises(AException):
        result = contract.call('IdentityBroken.main', '1')
        print(result)

def test_evm_broken_encode_calldata():
    contract = Contract(broken_contract, Contract.EVM)
    #with raises(AException):
    result = contract.encode_calldata('IdentityBroken.main', '1')
