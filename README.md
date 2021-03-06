# pushover
A wrapper to simplify use of the Pushover notification service API.

Visit https://pushover.net/ (an unaffiliated 3rd-party service) to see the details of the service and to
create an account. Free accounts currently (as of 2/21) allow a 30-day trial period with which to use 
and experiment with the service. A one-time fee of $5 allows perpetual use.

Steps to use:
<ol>
    <li>Create a pushover account at https://pushover.net/</li>
    <li>Sign in to your pushover account</li>
    <li>Use the site to generate an API KEY and a USER KEY for your application</li>
    <li>Place this pushover python package in your application's folder</li>
    <li>Insure the requests library is installed (pip install requests)</li>
    <li>Include "from pushover import PushoverNotificationService" in your code</li>
    <li>Create a PushoverNotificationService object using your API KEY and USER KEY</li>
    <li>Send notifications using this object
        <div>Example:</div>             
<pre>po = PushoverNotificationService(USER KEY, API KEY)
po.notify("This is a notification.")</pre>
    </li>    
</ol>
<hr>
Package Documentation:
<blockquote>
<pre>
class PushoverNotificationService(user_key, api_key)
    :param user_key: Pushover user key.
    :param api_key: Pushover api key.

        notify(message: str, *, title: Optional[str] = None, device_id: Optional[str] = None, sound: str = "persistent", priority: NotificationPriorityEnum = NotificationPriorityEnum.NORMAL)
            Make an API call to the Pushover notification service to send a notification.
            :param message: The text message body.  Max length is 1024 characters.
            :param title: A message title. May be None to use app name as title. Max length is 250 characters.
            :param device_id: Device identifier registered with Pushover. May be None to send to all registered devices.
            :param sound: Name of the notification sound to play.
            :param priority: PriorityEnum indicating message priority.
            :return: tuple (notify_successful:bool, return_msg: string description of return condition-for troubleshooting)

        class NotificationPriorityEnum(enum.IntEnum):
            Notification priority enumerations.           
</pre>
</blockquote>
