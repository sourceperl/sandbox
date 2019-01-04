#!/usr/bin/env python3

from collections import namedtuple
from difflib import get_close_matches
import re
import string
from unicodedata import normalize

# some type
Token = namedtuple("Token", ["type", "value"])

# some const
TOKS = [r"(?P<WORD>[a-zA-Z][a-zA-Z_0-9]*)",
        r"(?P<NB>\d+)",
        r"(?P<WS>\s+)",
        r"(?P<PCT>[%s]+)" % string.punctuation]
SENTENCE_PAT = re.compile("|".join(TOKS))

ACT_LIST = {"allume": None, "donne": None}
WHAT_LIST = {"lumiere": None, "heure": None}
WHERE_LIST = {"salon": None}


# some functions
def gen_tokens(pat, text):
    # replace accent
    text = normalize('NFD', text).encode('ascii', 'ignore').decode()
    # tokenize
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

if __name__ == "__main__":
    txts = """Allume la lumière dans le salon.
              Donne  moi l'heure."""

    for txt in map(str.strip, txts.split(".")):
        # ignore null sentence
        if not txt:
            continue
        # debug
        print("#" * 20)
        print(txt)
        # tokenize sentence
        for token in gen_tokens(SENTENCE_PAT, txt):
            # parse word
            if token.type == "WORD":
                # search action/what/where
                id_act = get_close_matches(token.value, ACT_LIST, cutoff=0.8)
                id_what = get_close_matches(token.value, WHAT_LIST, cutoff=0.8)
                id_where = get_close_matches(token.value, WHERE_LIST, cutoff=0.8)
                if id_act:
                    print("ACT_LIST %s" % token.value)
                if id_what:
                    print("WHAT_LIST %s" % token.value)
                if id_where:
                    print("WHERE_LIST %s" % token.value)
