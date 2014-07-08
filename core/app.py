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
        name = ' '.join(names)
        worker = None
        location = Location.get_by_code(location_code)

        if location is None:
            msg.respond('Invalid location code: {}. You sent: {}'.format(
                location_code, msg.text))
            return

        connection = msg.connections[0]
        contact = connection.contact
        if contact:
            worker = contact.worker

            if worker:
                if worker.name == name and worker.location == location:
                    msg.respond('You are already registered.')
                    return
        else:
            contact = Contact.objects.create(name=name)
            connection.contact = contact
            connection.save()

        if worker is None:
            worker = Worker()

        worker.name = name
        worker.location = location
        worker.contact = contact
        worker.save()

        response = 'Thank you {}. You are now registered at {} ' \
            'with the phone number {}'.format(
                name,
                location,
                connection.identity
            )
        msg.respond(response)

    def process_report(self, msg, *tokens):
        pass
