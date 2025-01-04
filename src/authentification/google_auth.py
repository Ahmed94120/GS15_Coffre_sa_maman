import base64
import os
import pyotp
import qrcode

# Generate Google Authenticator Secret
def generate_google_authenticator_secret():
    """
    Generates a 16-character base32 secret key for Google Authenticator.
    """
    random_bytes = os.urandom(10)  # 10 bytes -> 16 Base32 characters
    secret = base64.b32encode(random_bytes).decode('utf-8').strip('=')
    return secret

# Generate QR Code for Google Authenticator
def generate_google_authenticator_qr(username, secret, issuer="SecureVaultByHackUTT"):
    """
    Generates a QR Code for Google Authenticator setup.
    """
    # Generate the otpauth URL
    otpauth_url = f"otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}"
    # Create QR Code
    qrcode.make(otpauth_url).show()

# Verify Google Authenticator Code
def verify_google_authenticator_code(secret, code):
    """
    Verifies a Google Authenticator code against the secret.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code)