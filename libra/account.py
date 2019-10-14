from nacl.signing import SigningKey
from libra.key_factory import new_sha3_256
from enum import Enum
from libra.account_config import AccountConfig

AccountStatus = Enum('AccountStatus', ('Local','Persisted','Unknown'))

class Account:
    def __init__(self, private_key, sequence_number=0):
        self._signing_key = SigningKey(private_key)
        self._verify_key = self._signing_key.verify_key
        shazer = new_sha3_256()
        shazer.update(self._verify_key.encode())
        self.address = shazer.digest()
        self.sequence_number = sequence_number
        self.status = AccountStatus.Local

    def json_print_fields(self):
        return ["address", "private_key", "public_key"]

    @classmethod
    def faucet_account(cls, private_key):
        ret = cls(private_key)
        ret.address = bytes.fromhex(AccountConfig.association_address())
        return ret

    def sign(self, message):
        return self._signing_key.sign(message)

    @property
    def address_hex(self):
        return self.address.hex()

    @property
    def public_key(self):
        return self._verify_key.encode()

    @property
    def private_key(self):
        return self._signing_key.encode()

    @property
    def public_key_hex(self):
        return self.public_key.hex()

    @property
    def private_key_hex(self):
        return self.private_key.hex()

