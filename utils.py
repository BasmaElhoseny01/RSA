import numpy as np
import math
import time
import random

from Crypto.Util import number
from sympy.ntheory import nextprime

def gcd(a, b):
    """
    returns gcd between two numbers a,b
    """

    while (True):
        temp = a % b
        if (temp == 0):
            return b
        a = b
        b = temp

def modInverse(a, n):
    """
    a*b = 1 mod n
    returns b which is multiplicative inverse of a module n
    """
    return pow(a, -1, n)