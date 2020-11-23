import locale, unicodedata
locale.setlocale(locale.LC_ALL, "")

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
