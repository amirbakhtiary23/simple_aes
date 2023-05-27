#!/usr/bin/env python3
from random import choice,randrange
alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def generate_keys(seed=11,min_size=3,max_size=15):
    """
    this function generates a tuple of keys for each itteration of aes
    in this implementation instead of using s-box matrix we use 
    vegenere cipher text which is unbreakable since we use random keys
    and hence cannot be attacked by frequency analysis
    """
    keys=[]
    for j in range (seed):
        key=""
        for i in range(randrange(min_size,max_size)):
            key=key+choice(alphabet)
        keys.append(key.lower())
    return keys



def gen_key(length=128):
    """
    this function produce the main key of algorithm so other keys can be derived by
    this one
    """
    key=""
    for j in range(length//8):
        key=key+choice(alphabet).lower()
    return key

def vigenere(
        text: str, 
        key: str, 
        alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        encrypt=True
):

    result = ''

    for i in range(len(text)):
        letter_n = alphabet.index(text[i])
        key_n = alphabet.index(key[i % len(key)])

        if encrypt:
            value = (letter_n + key_n) % len(alphabet)
        else:
            value = (letter_n - key_n) % len(alphabet)

        result += alphabet[value]

    return result
    

def vigenere_encrypt(text: str, key: str):
    return vigenere(text=text, key=key,alphabet=alphabet, encrypt=True)


def vigenere_decrypt(text: str, key: str):
    return vigenere(text=text, key=key,alphabet=alphabet, encrypt=False)
