from django.conf import settings
from django.core.exceptions import FieldError
from django.db import models

from .app_settings import PWA_APP_NAME


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "Push Group: %s" % self.name


class SubscriptionInfo(models.Model):
    """
    Stores the PushSubscription object returned by a browser
    """
    browser = models.CharField(max_length=100)
    user_agent = models.CharField(
        max_length=500, default="None"
    )
    endpoint = models.URLField(max_length=500)
    auth = models.CharField(max_length=100)
    p256dh = models.CharField(max_length=100)

    def __str__(self):
        return f"Subscription Information for {self.user_agent}"


class PushInformation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="webpush_info", blank=True, null=True, on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        SubscriptionInfo, related_name="webpush_info", on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, related_name="webpush_info", blank=True, null=True, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        # Check whether user or the group field is present
        # At least one field should be present there
        # Through from the functionality its not possible, just in case! ;)
        if self.user or self.group:
            super(PushInformation, self).save(*args, **kwargs)
        else:
            raise FieldError("At least user or group should be present")

    def __str__(self):

        return f"Push Subscription for: {self.user}"


class PushMessage(models.Model):
    active = models.BooleanField(default=True)
    send_on = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=200, null=False, default="Message from %s." % PWA_APP_NAME)
    message = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    icon = models.URLField(blank=True, null=True)
    send_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)

    def __str__(self):
        if self.sent:
            return f"{self.title}, sent on {self.send_on}"

        return f"{self.title}, to be sent on {self.send_on}"
