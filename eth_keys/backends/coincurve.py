from __future__ import absolute_import

from eth_keys.exceptions import (
    BadSignature,
)

from .base import BaseECCBackend


class CoinCurveECCBackend(BaseECCBackend):
    def __init__(self):
        try:
            import coincurve
        except ImportError:
            raise ImportError("The CoinCurveECCBackend requires the coincurve \
                               library which is not available for import.")
        self.keys = coincurve.keys
        self.ecdsa = coincurve.ecdsa
        super(CoinCurveECCBackend, self).__init__()

    def ecdsa_sign(self, msg_hash, private_key):
        private_key_bytes = bytes(private_key)
        signature_bytes = self.keys.PrivateKey(private_key_bytes).sign_recoverable(
            msg_hash,
            hasher=None,
        )
        signature = self.Signature(signature_bytes)
        return signature

    def ecdsa_recover(self, msg_hash, signature):
        signature_bytes = bytes(signature)
        try:
            public_key_bytes = self.keys.PublicKey.from_signature_and_message(
                signature_bytes,
                msg_hash,
                hasher=None,
            ).format(compressed=False)[1:]
        except (ValueError, Exception) as err:
            # `coincurve` can raise `ValueError` or `Exception` dependending on
            # how the signature is invalid.
            raise BadSignature(str(err))
        public_key = self.PublicKey(public_key_bytes)
        return public_key

    def private_key_to_public_key(self, private_key):
        public_key_bytes = self.keys.PrivateKey(bytes(private_key)).public_key.format(
            compressed=False,
        )[1:]
        return self.PublicKey(public_key_bytes)
