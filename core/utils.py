import re


def parse_text(prefix, text):
    register_pattern = re.compile(
        r'^\s*(?:{})\s*reg\s*(?:[\s,;:]+(.+))?$'.format(prefix),
        re.IGNORECASE
    )
    report_pattern = re.compile(
        r'^\s*(?:{})\s*(?:[\s,;:]+(.+))?$'.format(prefix),
        re.IGNORECASE
    )

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
            tokens = tokenset[0].split()

        return is_reg, is_help, tokens

    return False
