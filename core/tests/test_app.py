from rapidsms.tests.harness import TestScript
from core.utils import parse_text
from locations.models import Location, LocationType
from workers.models import Worker


class AppTest(TestScript):
    def test_message_parsing(self):
        result = parse_text('add', 'collywobbles')
        self.assertFalse(result)

    def test_registration(self):
        # self.runScript('''
        #     12345 > hfr reg fish
        #     12345 < Noin!
        # ''')
        l_type = LocationType.objects.create(name='State')
        Location.objects.create(name='Lagos', location_type=l_type, code='LAG')

        initial = Worker.objects.count()

        self.runScript('''
            12345 > hfr reg lag John Doe
            12345 < Thank you John Doe. You are now registered at Lagos State with the phone number 12345
            12345 > hfr reg lag Joe D. Blow
            12345 < Thank you Joe D. Blow. You are now registered at Lagos State with the phone number 12345
        ''')

        final = Worker.objects.count()

        self.assertEqual(initial + 1, final)
