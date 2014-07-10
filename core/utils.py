import re
from django.conf import settings


def parse_text(prefix, text):
    register_pattern = re.compile(
        r'^\s*(?:{})\s*reg\s*(?:[\s,;:]+(.+))?$'.format(prefix),
        re.IGNORECASE
    )
    report_pattern = re.compile(
        r'^\s*(?:{})\s*(?:[\s,;:]+(.+))?$'.format(prefix),
        re.IGNORECASE
    )

    text = unicode(text).translate(settings.CHARACTER_TRANSLATIONS)
    match = register_pattern.match(text)
    is_reg = is_help = False
    tokens = None

    if match:
        is_reg = True
        tokenset = match.groups()

        if tokenset[0] is None:
            # help request
            is_help = True
        else:
            tokens = tokenset[0].split()

        return is_reg, is_help, tokens

    match = report_pattern.match(text)

    if match:
        tokenset = match.groups()

        if tokenset[0] is None:
            # help request
            is_help = True
        else:
            tokens = parse_report_input(tokenset[0])

        return is_reg, is_help, tokens

    return False


def parse_report_input(value):
    pattern = re.compile(r'(?P<tag>[A-Z]+)\s*(?P<answer>\d+)', re.IGNORECASE)
    report_data = dict([(r.group('tag').upper(), r.group('answer')) for r in pattern.finditer(value)])
    return report_data
