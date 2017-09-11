# -*- coding: utf-8 -*-

import os
import time


CHARS_DFLT = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def randstr(length,
            prepend_time=False,
            chars=CHARS_DFLT):
    """Create pseudo-random string identifier.

    :param length: int, result identifier length
    :param prepend_time: bool, whether to prepend time string
    :param chars: str, chars options vector
    """
    scope = len(chars)
    result = ''

    for i in os.urandom(length):
        result += chars[ord(i) % scope]

    if prepend_time:
        return time.strftime('%Y%m%d%H%M%S') + result

    return result


SLUGIFY_TR = {
    # RUSSIAN
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'j',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ы': 'y',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',

    # UKRAINIAN
    'ґ': 'g',
    'є': 'e',
    'і': 'i',
    'ї': 'i',

    # NUMBERS
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',

    # ENGLISH
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'y': 'y',
    'z': 'z',
}

def slugify_cyr(string, min_length=3):
    """Convert Cyrillic string into slug."""
    slug = ''
    trig = 0

    for i in string:
        try:
            c = SLUGIFY_TR[unicode(i).lower().encode('utf-8')]
            if trig == 2:
                slug += '-'

            trig = 1
            slug += c

        except KeyError:
            if i in (' ', '-', '_') and trig != 0:
                trig = 2

    if len(slug) < min_length:
        raise ValueError("slug is too short: %s" % slug)

    return slug
