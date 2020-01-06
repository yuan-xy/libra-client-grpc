from libra.transaction import *
import libra_client
from canoser import Uint64
import pytest


def test_invalid_signature():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    stx = SignedTransaction.gen_from_raw_txn(raw_tx, a0)
    stx.signature = [0]*64
    client = libra_client.Client("testnet")
    with pytest.raises(libra_client.client.VMError) as excinfo:
    	client.submit_signed_txn(stx)
    vm_error = excinfo.value
    assert vm_error.args == (1, 'INVALID_SIGNATURE')
    assert vm_error.error_code == 1
    assert vm_error.error_msg == 'INVALID_SIGNATURE'
