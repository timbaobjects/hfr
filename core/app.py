from rapidsms.apps.base import AppBase
from .utils import parse_text


class App(AppBase):
    keyword = 'hfr'

    def handle(self, msg):
        parsed = parse_text(self.keyword, msg.text)

        if not parsed:
            return False

        is_reg, is_help, tokens = parsed

        if is_help:
            if is_reg:
                self.help_registration(msg)
            else:
                self.help_report(msg)
            return True

        if is_reg:
            self.process_registration(msg, tokens)
        else:
            self.process_report(msg, tokens)

        return True

    def help_registration(self, msg):
        pass

    def help_report(self, msg):
        pass

    def process_registration(self, msg, *reg_info):
        pass

    def process_report(self, msg, *tokens):
        pass
