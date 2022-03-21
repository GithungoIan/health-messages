import logging
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'health.settings'

logger = logging.getLogger(__name__)
import django

django.setup()
logger.info("[*] setting up django...")


from datetime import timedelta

import phonenumbers
import schedule
from django.utils import timezone

from api.models import Appointment

import africastalking


logger = logging.getLogger(__name__)


def clean_phone(phone):
    try:
        number = phonenumbers.format_number(
            phonenumbers.parse(phone, 'KE'),
            phonenumbers.PhoneNumberFormat.E164
        )
        return number
    except phonenumbers.NumberParseException:
        return None


class SMS:
    def __init__(self, sender_id):
        self.sender_id = sender_id
        self.username = "sandbox"
        self.api_key = "f40eda4358d8ea23ecc2a68274f36473137ab9dc9c4ab975a687f43f26dc7b2f"

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, recipients, message):
        sender = self.sender_id
        try:
            response = self.sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            logger.info('Encountered an error while sending: %s' % str(e))


class BackgroundAppointments:
    def __init__(self):
        self.AppSMS = SMS('Appointments')
        self.repSMS = SMS('HealthInfo')

    def get_to_be_notified(self):
        return Appointment.objects.filter(visited=False) \
            .filter(notified=False) \
            .filter(date__lt=timezone.now() + timedelta(days=1))

    def get_to_be_reminded(self):
        return Appointment.objects.filter(visited=False). \
            filter(date__lt=timezone.now() - timedelta(days=1)). \
            filter(reminded=False)

    def mark_reminded(self, appointment: Appointment):
        appointment.reminded = True
        appointment.save()

    def mark_notified(self, appointment: Appointment):
        appointment.notified = True
        appointment.save()

    def remind(self):
        items = self.get_to_be_reminded()
        if items.count() == 0:
            return
        logger.info("Sending remind messages")
        for item in items:
            message = f"Hello, {item.user.username}, did you forget about your appointment? You had a {item.type} " \
                      f"appointment on {item.date.time} in the {item.department}. Kindly attend"
            cleaned_phone = clean_phone(item.user.profile.phone)
            if cleaned_phone is None:
                continue
            self.repSMS.send([cleaned_phone], message)
            self.mark_reminded(item)
        logger.info("DONE")

    def notify(self):
        items = self.get_to_be_notified()
        if items.count() == 0:
            return
        logger.info("Sending notify messages...")
        for item in items:
            message = f"Hello {item.user.username}, You have a {item.type} appointment on {item.date} " \
                      f" in {item.department}. Please observe time "
            cleaned_phone = clean_phone(item.user.profile.phone)
            if cleaned_phone is None:
                continue
            self.AppSMS.send([cleaned_phone], message)
            self.mark_notified(item)
        logger.info("Done")

    def run_notify(self):
        schedule.every(5).seconds.do(self.notify)
        logger.info("Starting appointment background job")
        while True:
            schedule.run_pending()

    def run_remind(self):
        schedule.every(5).seconds.do(self.remind)
        logger.info("Starting reminder background job")
        while True:
            schedule.run_pending()
