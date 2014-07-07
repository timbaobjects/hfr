import re
from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler


class BaseHandler(KeywordHandler):
    prefix = 'hfr'

    @classmethod
    def _keyword(cls):
        if hasattr(cls, 'keyword') and cls.keyword:
            pattern = r"^\s*(?:{})\s*(?:{})(?:[\s,;:]+(.+))?$".format(
                cls.prefix,
                cls.keyword
            )
        else:
            pattern = r"^\s*(?:%s)(\s*?)$" % cls.prefix
        return re.compile(pattern, re.IGNORECASE)
