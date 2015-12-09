#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# ---------------------------------------
# Created by: Jlfme<jlfgeek@gmail.com>
# Created on: 2015-12-08 19:48:18
# ---------------------------------------


import binascii
from Crypto.Cipher import AES


def aes_encryption(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(plaintext)
    text = binascii.b2a_hex(encrypted).decode()
    return text


def encrypt_password(password):
    key = bytes.fromhex('e8a50611815ef4b1a656ab08eee882e3')
    iv = bytes.fromhex("3336306c75796f7540696e7374616c6c")
    password = password.encode('utf-8')

    if not 8 <= len(password) <= 16:
        raise ValueError('The password must be 8-16 characters, yours: %s' % len(password))

    # 不够16字节,则填充b'\x08'补齐
    plaintext = password + b'\x08' * (16 - len(password))

    return aes_encryption(plaintext, key, iv)
