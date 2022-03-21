import logging

import africastalking
import phonenumbers
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Facility
from api.models import BroadcastMessage


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


@receiver(post_save, sender=BroadcastMessage)
def send_messages(sender, instance, created, **kwargs):
    if created:
        phones = instance.phones
        group = instance.group

        if group is not None:
            phones = [clean_phone(x.profile.phone) for x in User.objects.filter(profile__group=group)]
            logging.info(f"phones: {phones}")
            message = instance.message
            if phones:
                SMS('Appointment').send(phones, message)
                instance.completed = True
                instance.save()
                return
            return
        if instance.facilities:
            phones = [clean_phone(x.phone) for x in Facility.objects.all()]
            message = instance.message
            if phones:
                SMS('REPORTS').send(phones, message)
                instance.completed = True
                instance.save()
                return
