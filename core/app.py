from rapidsms.apps.base import AppBase
from rapidsms.models import Contact
from locations.models import Location
from workers.models import Worker
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
            self.process_registration(msg, *tokens)
        else:
            self.process_report(msg, *tokens)

        return True

    def help_registration(self, msg):
        pass

    def help_report(self, msg):
        pass

    def process_registration(self, msg, *tokens):
        location_code = tokens[0]
        names = tokens[1:]
        location = Location.get_by_code(location_code)

        connection = msg.connections[0]
        contact = connection.contact
        if contact:
            msg.respond('You are already registered!')
            return

        if location is None:
            msg.respond('Invalid location code: {}. You sent: {}'.format(
                location_code, msg.text))
            return

        contact = Contact.objects.create(name=' '.join(names))
        connection.contact = contact
        connection.save()

        Worker.objects.create(name=contact.name, location=location,
                              contact=contact)

        response = 'Thank you {}. You are now registered in {} with the phone number {}'.format(contact.name, location.name, connection.identity)
        msg.respond(response)

    def process_report(self, msg, *tokens):
        pass
