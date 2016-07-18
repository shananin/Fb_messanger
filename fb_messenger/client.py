from __future__ import unicode_literals
import logging
import requests
from fb_messenger import const
from fb_messenger.exceptions import RequestFailed, UnknownAction, MessengerAPIError
from fb_messenger import notification_type as nt
from fb_messenger import callbacks
from fb_messenger import callback_types
from fb_messenger import action_types


class FBMessenger(object):
    """
    client = FBMessenger(access_token='ADSD...')

    try:
        response = client.send_text('1231313', 'text')
    except MainException as e:
        logging.debug(e)

    attachment = attachments.Image(img_url='http://example.com/img.jpg')
    try:
        response = client.send_attachment('1231313', attachment)
    except MainException as e:
        logging.debug(e)
    """

    _callbacks = {}

    def __init__(self, access_token, logger=None, logger_level=None):
        if logger is not None:
            self.logger = logger
        else:
            # TODO: rewrite
            self.logger = logging.getLogger(__name__)

        if logger_level is not None:
            self.logger.setLevel(logger_level)

        self._access_token = access_token
        self._api_url = const.API_FB_MESSAGES_URL + self._access_token

    def send_attachment(self, recipient_id, attachment, notification_type=nt.REGULAR):
        payload = self._format_attachment_payload(recipient_id, attachment, notification_type)

        self.logger.debug(payload)

        request = requests.post(
            url='{}?access_token={}'.format(const.API_FB_MESSAGES_URL, self._access_token),
            json=payload,
        )

        if request.status_code >= 300:
            self.logger.warn(request.text)
            raise RequestFailed(request.text)

        return Response(response=request.json())

    def send_text(self, recipient_id, text, notification_type=nt.REGULAR):
        payload = self._format_text_payload(recipient_id, text, notification_type)

        self.logger.debug(payload)

        request = requests.post(
            url=const.API_FB_MESSAGES_URL + self._access_token,
            json=payload,
        )

        if request.status_code >= 300:
            self.logger.warn(request.text)
            raise RequestFailed(request.text)

        return Response(response=request.json())

    def send_action(self, recipient_id, sender_action):
        """
        Set typing indicators or send read receipts using the Send API,
        to let users know you are processing their request.


        :param recipient_id: user id
        :param sender_action: look fb_messenger.action_types
        :return Response:
        """
        if sender_action not in action_types.ALL_ACTIONS:
            raise UnknownAction

        response_dict = self._send_request(
            self._format_action_payload(recipient_id, sender_action)
        )

        return Response(response_dict)

    def process_message(self, body):
        self.logger.debug(body)

        if 'received' in self._callbacks:
            self._callbacks['received'](body)

    def callback(self, callback_name):
        def decorator(function):
            if callback_name not in callback_types.ALL_CALLBACKS:
                self.logger.warn('{} is not fb messenger callback'.format(callback_name))
                return function

            self.logger.info('{} callback has been added'.format(callback_name))
            self._callbacks[callback_name] = function
            return function

        return decorator

    def create_welcome_message(self, page_id, message):
        payload = self._format_welcome_message(message)

        request = requests.post(
            url='https://graph.facebook.com/v2.6/{}/thread_settings?access_token={}'.format(page_id,
                                                                                            self._access_token),
            json=payload,
        )

        return request.status_code, request.json()

    def _send_request(self, payload):
        request = requests.post(
            url=self._api_url,
            json=payload,
        )

        response_dict = request.json()

        if request.status_code >= 300:
            raise MessengerAPIError(response_dict)

        return response_dict

    @staticmethod
    def _format_action_payload(recipient_id, sender_action):
        return {
            'recipient': {
                'id': recipient_id,
            },
            'sender_action': sender_action,
        }

    @staticmethod
    def _format_text_payload(recipient_id, text, notification_type):
        return {
            'recipient': {
                'id': recipient_id,
            },
            'message': {
                'text': text,
            },
            'notification_type': notification_type,
        }

    @staticmethod
    def _format_attachment_payload(recipient_id, attachment, notification_type):
        return {
            'recipient': {
                'id': recipient_id,
            },
            'message': {
                'attachment': attachment,
            },
            'notification_type': notification_type,
        }

    @staticmethod
    def _format_welcome_message(attachment):
        return {
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [
                {
                    'message': {
                        attachment
                    }
                },
            ],
        }


class Response(object):
    def __init__(self, response_dict):
        self.recipient_id = response_dict.get('recipient_id', '')
        self.message_id = response_dict.get('message_id', '')

    def __str__(self):
        return self.message_id

    def __unicode__(self):
        return self.__str__()
