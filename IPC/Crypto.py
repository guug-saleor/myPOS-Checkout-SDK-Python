from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Cryptodome import Random
from base64 import b64encode, b64decode

def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private

def importKey(externKey):
    return RSA.importKey(externKey)

def getpublickey(priv_key):
    return priv_key.publickey()

def encrypt(message, pub_key):
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
    priv_key = importKey(priv_key)
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def sign(message, priv_key, hash="SHA256"):
    priv_key = importKey(priv_key)
    signer = PKCS1_v1_5.new(priv_key)

    if (hash == "SHA512"):
        digest = SHA512.new()
    elif (hash == "SHA384"):
        digest = SHA384.new()
    elif (hash == "SHA256"):
        digest = SHA256.new()
    elif (hash == "SHA1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, pub_key, hash="SHA256"):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA512"):
        digest = SHA512.new()
    elif (hash == "SHA384"):
        digest = SHA384.new()
    elif (hash == "SHA256"):
        digest = SHA256.new()
    elif (hash == "SHA1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)