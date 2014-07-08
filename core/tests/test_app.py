from rapidsms.tests.harness import TestScript
from core.utils import parse_text


class AppTest(TestScript):
    def test_message_parsing(self):
        result = parse_text('add', 'collywobbles')
        self.assertFalse(result)
