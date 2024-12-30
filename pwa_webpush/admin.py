import json
import threading

from django.conf.urls.static import static
from django.contrib import admin
from django.utils import timezone

from pwa_webpush import send_user_notification
from .models import PushInformation, PushMessage
from .utils import _send_notification


@admin.register(PushInformation)
class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "subscription", "group")
    actions = ("send_test_message",)

    def send_test_message(self, request, queryset):
        result = []
        payload = {"head": "Hey", "body": "Hello World"}
        for device in queryset:
            result.append(_send_notification(device, json.dumps(payload), 0))
        return



@admin.register(PushMessage)
class PwaPushMessageAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        # let's define this so there's no chance of AttributeErrors
        self._request_local = threading.local()
        self._request_local.request = None
        super().__init__(*args, **kwargs)

    def get_request(self):
        return self._request_local.request

    def set_request(self, request):
        self._request_local.request = request

    def add_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super().add_view(request, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()

        url = "/" if not obj.url else obj.url
        if url.startswith("/"):
            request = self.get_request()
            url = request.build_absolute_uri(url)

        icon_url = request.build_absolute_uri(
            static("pwa/icons/apple-icon-72x72.png")
            if not obj.icon
            else obj.icon
        )

        if not obj.sent and obj.active and obj.send_on <= timezone.now():
            payload = {
                "head": obj.title,
                "body": obj.message,
                "icon": icon_url,
                "url": url,
            }

            #  add some type of safety to this!
#            if not obj.send_to:
#                push_users = PushInformation.objects.all()

#            else:
            push_users = PushInformation.objects.filter(
                user=obj.send_to
            )

            for push_user in push_users:
                send_user_notification(user=push_user.user, payload=payload, ttl=1000)
                obj.sent = True
                obj.save()

        return

    list_display = (
        u"active",
        u"send_on",
        u"title",
        u"message",
        u"url",
        u"icon",
    )
    list_filter = (u"active", u"send_on")
