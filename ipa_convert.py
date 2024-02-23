import re
import pandas as pd

old_words = {
    'b': ["baaja", "baalia", "baaliar", "bajeri", "biibili", "biili", "biiler", "bussi"],
    'd': ["diaavulu", "decembari"],
    'f': ["farisiiari", "februaari", "feeria", "feeriar", "freer"],
    'g': ["gassi", "guuti"],
    'h': ["hiisti", "horaa", "horaartor", "huaa", "huaartor"],
    'j': ["januaari", "joorli", "joorlisior", "jorngoq", "juuli", "juulli", "juumooq", "juuni", "juuti"],
    'l': ["laaja", "lakker", "lakki", "lal'laaq", "lappi", "liimmer", "liimmi"],
    'r': ["raaja", "rinngi", "rommi", "russeq", "ruua", "ruujori", "ruusa", "ruusaar"],
    'v': ["viinnequt", "viinni"]
}

def is_upper(ch):
    return ch == ch.upper() and ch != ch.lower()

def ipa_kal_from(token):
    start = 0
    
    # Check for special words in dictionary
    first = token[0]
    if first in old_words:
        for word in old_words[first]:
            if token == word:
                return 0
        start = 1

    # Rules based on first letter
    if not first in 'aeikmnopqstu':
        start = max(start, 1)
    if re.match(r'^.[bcdwxyzæøå]', token):
        start = max(start, 2)

    # Additional rules
    if re.match(r'^.ai', token):
        start = max(start, 3)
    for match in re.finditer(r'[eo]+[^eorq]', token):
        start = max(start, match.start() + 2)

    last = token[-1]
    if not last in 'aikpqtu':
        start = max(start, len(token))

    # Consonant cluster handling
    for match in re.finditer(r'[^\wŋæøå]+', token):
        start = max(start, match.start() + 1)

    consonants_re = re.compile(r'([qwrtpsdfghjklzxcvbnmŋ])([qwrtpsdfghjklzxcvbnmŋ])')
    for match in consonants_re.finditer(token):
        if match.group(1) != match.group(2) and match.group(1) != 'r' and match.group(1) != 'n' and not (match.group(1) == 't' and match.group(2) == 's'):
            start = max(start, match.start() + 2)

    return start
'''
def ipa_kal_from(token):
    from_index = 0
    first = token[0]
    if first in old_words:
        if token in old_words[first]:
            return 0
        else:
            from_index = 1

    if not re.match(r'[aeikmnopqstu]', first):
        from_index = max(from_index, 1)

    if re.match(r'^[bcdwxyzæøå]', token):
        from_index = max(from_index, 2)

    if re.match(r'^.ai', token):
        from_index = max(from_index, 3)

    eorq = re.compile(r'[eo]+[^eorq]')
    match = eorq.search(token, from_index)
    while match:
        from_index = max(from_index, match.start() + 2)
        match = eorq.search(token, match.end())

    last = token[-1]
    if not re.match(r'[aikpqtu]', last):
        from_index = max(from_index, len(token))

    rf = re.search(r'[^aefgijklmnopqrstuvŋ][aefgijklmnopqrstuvŋ]+$', token)
    if rf:
        from_index = max(from_index, rf.start() + 1)

    cons = re.compile(r'([qwrtpsdfghjklzxcvbnmŋ])([qwrtpsdfghjklzxcvbnmŋ])')
    match = cons.search(token, from_index)
    while match:
        if match.group(1) == 'r':
            continue
        if match.group(1) == 'n' and match.group(2) == 'g':
            continue
        if match.group(1) == 't' and match.group(2) == 's':
            continue
        if match.group(1) != match.group(2):
            from_index = max(from_index, match.start() + 2)
        match = cons.search(token, match.end())

    return from_index
'''

'''def kal_ipa(token):
    if not re.match(r'^[a-zæøåŋ]+$', token, re.IGNORECASE):
        return token

    token = token.replace('nng', 'ŋŋ').replace('ng', 'ŋ')

    V = re.compile(r'[aeiouyæøå]', re.IGNORECASE)

    i = 0
    split = ''
    while i < len(token) - 1:
        split += token[i]
        if V.match(token[i]) and token[i+1].lower() != 'r' and V.match(token[i+1]) and (i == len(token) - 2 or V.match(token[i+2])):
            split += ' '
        elif V.match(token[i]) and token[i+1].lower() != 'r' and not V.match(token[i+1]) and V.match(token[i+2]) and (i == len(token) - 3 or V.match(token[i+3])):
            i += 1
            split += token[i] + ' '
        elif token[i].lower() != token[i+1].lower() and V.match(token[i]) and V.match(token[i+1]):
            split += ' '
        i += 1
    split += token[i]
    token = split
    token = ' ' + token + '#'

    old = ''
    while old != token:
        old = token
        token = re.sub(r' ([bcdfghjklmnŋpqrstvwxz][aeiouyæøå][bcdfghjklmnŋpqrstvwxz] )', ' ¹\\1', token, flags=re.IGNORECASE)
        token = re.sub(r' ([aeiouyæøå][bcdfghjklmnŋpqrstvwxz] )', ' ¹\\1', token, flags=re.IGNORECASE)

    token = re.sub(r' ([bcdfghjklmnŋpqrstvwxz])([aeiouyæøå])(\\2)', ' ²\\1\\2\\3', token, flags=re.IGNORECASE)
    token = re.sub(r' ([aeiouyæøå])(\\1)', ' ²\\1\\2', token, flags=re.IGNORECASE)

    token = re.sub(r'(u) ([¹²]?)v([uo])', '\\1 \\2<sup>w</sup>\\3', token, flags=re.IGNORECASE)
    token = re.sub(r'(u) ([¹²]?)([aeiouyæøå])', '\\1 \\2<sup>w</sup>\\3', token, flags=re.IGNORECASE)
    token = re.sub(r'(i) ([¹²]?)([uoa])', '\\1 \\2<sup>j</sup>\\3', token, flags=re.IGNORECASE)

    token = re.sub(r' ([¹²]?)g', ' \\1ɣ', token, flags=re.IGNORECASE)
    token = re.sub(r'r ([¹²]?)r', 'χ \\1χ', token, flags=re.IGNORECASE)
    token = re.sub(r'g ([¹²]?)ɣ', 'x \\1x', token, flags=re.IGNORECASE)
    token = re.sub(r' ([¹²]?)r', ' \\1ʁ', token, flags=re.IGNORECASE)

    token = re.sub(r'ee( ?[¹²]?[ʁqrχ])', 'ɜ:\\1', token, flags=re.IGNORECASE)
    token = re.sub(r'e( ?[¹²]?[ʁqrχ])', 'ɜ\\1', token, flags=re.IGNORECASE)
    token = re.sub(r'oo( ?[¹²]?[ʁqrχ])', 'ɔ:\\1', token, flags=re.IGNORECASE)
    token = re.sub(r'o( ?[¹²]?[ʁqrχ])', 'ɔ\\1', token, flags=re.IGNORECASE)
    token = re.sub(r'aa( ?[¹²]?[ʁqrχ])', 'ɑ:\\1', token, flags=re.IGNORECASE)
    token = re.sub(r'a( ?[¹²]?[ʁqrχ])', 'ɑ\\1', token, flags=re.IGNORECASE)

    token = re.sub(r't( ?[iɜ])', 't<sup>s</sup>\\1', token, flags=re.IGNORECASE)
    token = re.sub(r't ([¹²]?)s', 't \\1t<sup>s</sup>', token, flags=re.IGNORECASE)
    token = re.sub(r'[bcdfghjklmnŋpqrstvwxz] ([¹²]?)([bcdfghjklmnŋpqrstvwxz])', '\\2 \\1\\2', token, flags=re.IGNORECASE)
    token = token.replace('l l', 'ɬ ɬ').replace('l ¹l', 'ɬ ¹ɬ').replace('l ²l', 'ɬ ²ɬ')
    token = token.replace('t<sup>s</sup>t<sup>s</sup>', 'tt<sup>s</sup>').replace(r'([aeiouyæøå])\1', '\\1:')

    token = re.sub(r' a( ?[tns])', ' ɛ\\1', token, flags=re.IGNORECASE)

    return token[1:-1]
'''

def kal_ipa(token):
    
    if not re.match(r'^[a-zæøåŋ]+$', token, re.IGNORECASE):
        return token

    token = token.replace('nng', 'ŋŋ')
    token = token.replace('ng', 'ŋ')

    C = re.compile(r'[bcdfghjklmnŋpqrstvwxz]', re.IGNORECASE)
    V = re.compile(r'[aeiouyæøå]', re.IGNORECASE)

    i = 0
    split = ''
    
    while i < len(token) - 2:
        
        split += token[i]
        if V.match(token[i]) and C.match(token[i+1]) and V.match(token[i+2]):
            split += ' '
        elif V.match(token[i]) and C.match(token[i+1]) and C.match(token[i+2]) and V.match(token[i+3]):
            i += 1
            split += token[i]
            split += ' '
        elif token[i].lower() != token[i+1].lower() and V.match(token[i]) and V.match(token[i+1]):
            split += ' '
        i += 1
        
    split += token[i:]
    token = split
    
    token = ' ' + token + '#'

    old = ''

    while old != token:
        old = token
        token = re.sub(r' ([bcdfghjklmnŋpqrstvwxz][aeiouyæøå][bcdfghjklmnŋpqrstvwxz] )', r' ¹\1', token, flags=re.IGNORECASE)
        token = re.sub(r' ([aeiouyæøå][bcdfghjklmnŋpqrstvwxz] )', r' ¹\1', token, flags=re.IGNORECASE)

    token = re.sub(r' ([bcdfghjklmnŋpqrstvwxz])([aeiouyæøå])(\2)', r' ²\1\2\3', token, flags=re.IGNORECASE)
    token = re.sub(r' ([aeiouyæøå])(\1)', r' ²\1\2', token, flags=re.IGNORECASE)

    token = re.sub(r'(u) ([¹²]?)v([uo])', r'\1 \2<sup>w</sup>\3', token, flags=re.IGNORECASE)
    token = re.sub(r'(u) ([¹²]?)([aeiouyæøå])', r'\1 \2<sup>w</sup>\3', token, flags=re.IGNORECASE)
    token = re.sub(r'(i) ([¹²]?)([uoa])', r'\1 \2<sup>j</sup>\3', token, flags=re.IGNORECASE)

    token = re.sub(r' ([¹²]?)g', r' \1ɣ', token, flags=re.IGNORECASE)
    token = re.sub(r'r ([¹²]?)r', r'χ \1χ', token, flags=re.IGNORECASE)
    token = re.sub(r'g ([¹²]?)ɣ', r'x \1x', token, flags=re.IGNORECASE)
    token = re.sub(r' ([¹²]?)r', r' \1ʁ', token, flags=re.IGNORECASE)

    token = re.sub(r'ee( ?[¹²]?[ʁqrχ])', r'ɜ:\1', token, flags=re.IGNORECASE)
    token = re.sub(r'e( ?[¹²]?[ʁqrχ])', r'ɜ\1', token, flags=re.IGNORECASE)

    token = re.sub(r'oo( ?[¹²]?[ʁqrχ])', r'ɔ:\1', token, flags=re.IGNORECASE)
    token = re.sub(r'o( ?[¹²]?[ʁqrχ])', r'ɔ\1', token, flags=re.IGNORECASE)
    token = re.sub(r'aa( ?[¹²]?[ʁqrχ])', r'ɑ:\1', token, flags=re.IGNORECASE)
    token = re.sub(r'a( ?[¹²]?[ʁqrχ])', r'ɑ\1', token, flags=re.IGNORECASE)

    token = re.sub(r't( ?[iɜ])', r't<sup>s</sup>\1', token, flags=re.IGNORECASE)
    token = re.sub(r't ([¹²]?)s', r't \1t<sup>s</sup>', token, flags=re.IGNORECASE)
    token = re.sub(r'[bcdfghjklmnŋpqrstvwxz] ([¹²]?)([bcdfghjklmnŋpqrstvwxz])', r'\2 \1\2', token, flags=re.IGNORECASE)
    token = re.sub(r'l l', r'ɬ ɬ', token, flags=re.IGNORECASE)
    token = re.sub(r'l ¹l', r'ɬ ¹ɬ', token, flags=re.IGNORECASE)
    token = re.sub(r'l ²l', r'ɬ ²ɬ', token, flags=re.IGNORECASE)
    token = re.sub(r't<sup>s<\/sup>t<sup>s<\/sup>', r'tt<sup>s</sup>', token, flags=re.IGNORECASE)
    token = re.sub(r'([aeiouyæøå])\1', r'\1:', token, flags=re.IGNORECASE)

    token = token.replace(' a ', ' ɛ ')

    token = token[1:]
    
    return token

def kal_ipa_words(txt):
    ws = txt.split()
    ws = [kal_ipa(w)[:-1] for w in ws]
    return ' '.join(ws)

abbrs = [
    [r'\b([Ss])ap\.', r'\1apaatip']
]

def do_kal_ipa_raw(text):
    for abbr in abbrs:
        text = re.sub(abbr[0], abbr[1], text)
    sents = re.split(r'([.:!?]\s+)', text)
    
    detect = ''
    ipa = ''

    for sent in sents:
        tokens = re.split(r'([^a-zA-Zæøåŋ]+)', sent)
        
        for item in tokens:
            if item == '':
                tokens.remove(item)
        rvs = []
        
        for token in tokens:
            rv = ipa_kal_from(token.lower())
            
            rvs.append(rv)

        for i, token in enumerate(tokens):
            if not re.match(r'\w+', token) or rvs[i] == 0:
                ipa += kal_ipa(token.lower())
                detect += token
                continue

            ipa += token[:rvs[i]] + kal_ipa(token[rvs[i]:])
            detect += token[:rvs[i]] + token[rvs[i]:]

    return {'detect': detect, 'ipa': ipa}

if __name__ == "__main__":
    df = pd.DataFrame(columns=['input', 'output'])
    with open('input-ipa.txt', 'r') as file:
        for line in file:
            text= line.strip()
            rv = do_kal_ipa_raw(text)

            print("Detected: ", rv['detect'])
            #print("IPA: ", rv['ipa'])

            l = [x for x in rv['ipa'] if x!=' ']
            res = ' '.join(l)
            print("IPA: ", res)

            df.loc[len(df)] = {'input': text, 'output': res}
            print(df.head(10))

        df.to_csv('result.csv', index=False)
