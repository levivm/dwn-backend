import base64
import hashlib
import hmac

from passlib.hash import bcrypt


def get_hmac(password):
    """Returns a Base64 encoded HMAC+SHA512 of the password signed with the salt specified
    by ``SECURITY_PASSWORD_SALT``.
    :param password: The password to sign
    """
    salt = u'\xc3e\x1f[i\'W\x06\x1a\xcd7\x18^"W\xe6\xaaE#\xf0\x8d\xf9s\xa7'

    h = hmac.new(
        salt.encode('utf-8'),
        password.encode('utf-8'),
        hashlib.sha512
    )
    return base64.b64encode(h.digest())


def encrypt_password(password):
    """Encrypts the specified plaintext password using the configured encryption options.
    :param password: The plaintext password to encrypt
    """
    signed = get_hmac(password).decode('ascii')
    return bcrypt.encrypt(signed)
