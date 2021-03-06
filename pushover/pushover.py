#!/usr/bin/env python
# Pushover Notification Service Interface Module
#
# Pushover is an online notification service that provides an API to allow posting notifications to user devices.
# https://pushover.net
#
# David Smith
# 6/6/2020

import enum
import time
from typing import Optional, Tuple

import requests


class PushoverNotificationService:
    """
    Class to simplify use of the Pushover notification service API.
    """

    version = "1.0"

    # URL of the pushover service
    PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

    # Valid notification sounds
    NOTIFICATION_SOUNDS = ["pushover", "bike", "bugle", "cashregister", "classical", "cosmic", "falling", "gamelan",
                           "incoming", "intermission", "magic", "mechanical", "pianobar", "siren", "spacealarm",
                           "tugboat", "alien", "climb", "persistent", "echo", "updown", "vibrate", "none"]

    # Max number of attempts if notify api call fails
    NOTIFY_ATTEMPTS_MAX = 3
    # If notify fails, wait this long before attempting an automatic retry
    NOTIFY_RETRY_INTERVAL_SECS = 1


    class NotificationPriorityEnum(enum.IntEnum):
        """
        Notification priority.
        Note: EMERGENCY is not yet supported
        """
        LOWEST = -2,    # Won't generate a notification (app badge is incremented)
        LOW = -1,       # No sound/vibrate, but will generate a popup notification
        NORMAL = 0,     # Generate sound/vibrate and popup notification (depending on device's settings)
        HIGH = 1,       # Bypass user's Pushover-configured quiet hours - generate sound/vibrate and popup
        EMERGENCY = 2   # Notify repeatedly with sound/vibrate regardless of device's do-not-disturb settings


    def __init__(self, user_key: str, api_key: str):
        """
        :param user_key: Pushover user key.
        :param api_key: Pushover api key.
        """
        if not isinstance(api_key, str):
            raise TypeError("'api_key' must be a string.")
        if not isinstance(user_key, str):
            raise TypeError("'user_key' must be a string.")

        # Copy keys
        self.api_key = api_key[:]
        self.user_key = user_key[:]


    def notify(self, message: str, *, title: Optional[str] = None, device_id: Optional[str] = None, sound: str = "persistent",
               priority: NotificationPriorityEnum = NotificationPriorityEnum.NORMAL) -> Tuple[bool, str]:
        """
        Make an API call to the Pushover notification service to send a notification.
        :param message: The text message body.  Max length is 1024 characters.
        :param title: A message title. May be None to use app name as title. Max length is 250 characters.
        :param device_id: Device identifier registered with Pushover. May be None to send to all registered devices.
        :param sound: Name of the notification sound to play.
        :param priority: PriorityEnum indicating message priority.
        :return: tuple (notify_successful:bool, return_msg: string description of return condition-for troubleshooting)
        """
        if sound not in self.NOTIFICATION_SOUNDS:
            raise ValueError("Invalid value for 'sound'.")
        if not isinstance(priority, self.NotificationPriorityEnum):
            raise ValueError("Invalid value for 'msg_priority'.")
        if priority == self.NotificationPriorityEnum.EMERGENCY:
            raise NotImplementedError("Emergency priority notifications not supported.")

        # API required parameters: token, user, message
        data = {"token": self.api_key,
                "user": self.user_key,
                "message": message,
                "priority": priority.value}

        # API optional parameters
        # 'device': If none specified, it sends to all registered devices
        if device_id:
            data["device"] = device_id
        # 'title': If none specified, it uses the app name as the default
        if title:
            data["title"] = title
        # 'sound'
        if sound:
            data["sound"] = sound

        # Attempt to send with retry in the event of failure
        for retry_count in range(self.NOTIFY_ATTEMPTS_MAX):
            # default values
            ret_val = True
            ret_msg = "success"

            rsp = None
            try:
                # Send notification
                rsp = requests.post(self.PUSHOVER_API_URL, json=data)

            except Exception as ex:
                # Handle exceptions that occur during attempt that prevent connection/send-receive from occurring.
                # (Doesn't include HTTPError that can be raised by 'raise_for_status' call below)
                # Set return values
                ret_val = False
                ret_msg = "error: " + str(ex)

            if rsp:
                # Test for success
                try:
                    # Evaluate if successful
                    rsp.raise_for_status()

                    # Success
                    return ret_val, ret_msg

                except requests.HTTPError:
                    # Failed - attempt to get returned error message
                    try:
                        error_msg = rsp.json()["errors"]        # Returns a list
                        error_msg = "error: " + str(error_msg)

                        # Set return values
                        ret_val = False
                        ret_msg = error_msg

                    except (ValueError, KeyError):
                        # (No data returned or problem decoding)
                        # Set return values
                        ret_val = False
                        ret_msg = "error"

            # Attempt failed - delay before retry
            time.sleep(self.NOTIFY_RETRY_INTERVAL_SECS)

        return ret_val, ret_msg
