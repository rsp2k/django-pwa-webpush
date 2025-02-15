import os

from django.conf import settings
from django.forms.models import model_to_dict
from django.templatetags.static import static
from django.urls import reverse

from pywebpush import WebPushException, webpush


def send_notification_to_user(user, payload, ttl=0):
    # Get all the push_info of the user

    errors = []
    push_infos = user.webpush_info.select_related("subscription")
    for push_info in push_infos:
        try:
            _send_notification(push_info.subscription, payload, ttl)

        except WebPushException as ex:
            errors.append(dict(subscription=push_info.subscription, exception=ex))

    if errors:
        raise WebPushException(f"Push failed: {errors}")


def send_notification_to_group(group_name, payload, ttl=0):
    from .models import Group
    # Get all the subscription related to the group

    errors = []
    push_infos = Group.objects.get(name=group_name).webpush_info.select_related("subscription")
    for push_info in push_infos:
        try:
            _send_notification(push_info.subscription, payload, ttl)

        except WebPushException as ex:
            errors.append(dict(subscription=push_info.subscription, exception=ex))

    if errors:
        raise WebPushException(f"Push failed: {errors}")


def send_to_subscription(subscription, payload, ttl=0):
    _send_notification(subscription, payload, ttl)


def _send_notification(subscription, payload, ttl):
    subscription_data = _process_subscription_info(subscription)
    vapid_data = {}

    webpush_settings = getattr(settings, "WEBPUSH_SETTINGS", {})
    vapid_private_key = webpush_settings.get("VAPID_PRIVATE_KEY")
    vapid_admin_email = webpush_settings.get("VAPID_ADMIN_EMAIL")

    # Vapid keys are optional, and mandatory only for Chrome.
    # If Vapid key is provided, include vapid key and claims
    if vapid_private_key:
        vapid_data = {
            "vapid_private_key": vapid_private_key,
            "vapid_claims": {"sub": "mailto:{}".format(vapid_admin_email)},
        }

    try:
        req = webpush(subscription_info=subscription_data, data=payload, ttl=ttl, **vapid_data)

    except WebPushException as e:
        # If the subscription is expired, delete it.
        if e.response.status_code == 410:
            subscription.delete()
        else:
            # Its other type of exception!
            raise e

    else:
        return req


def _process_subscription_info(subscription):
    subscription_data = model_to_dict(subscription, exclude=["browser", "id"])
    endpoint = subscription_data.pop("endpoint")
    p256dh = subscription_data.pop("p256dh")
    auth = subscription_data.pop("auth")

    return {"endpoint": endpoint, "keys": {"p256dh": p256dh, "auth": auth}}


def get_templatetag_context(context):
    vapid_public_key = getattr(settings, "WEBPUSH_SETTINGS", {}).get("VAPID_PUBLIC_KEY", "")
    user = None
    if request := context.get("request"):
        user = request.user

    data = {
        "group": context.get("webpush", {}).get("group"),
        "user": user,
        "vapid_public_key": vapid_public_key,
        "webpush_save_url": reverse("save_webpush_info"),
    }

    return data


def add_static_prefix_to_srcs(context):
    # Add static prefix to urls, cant do it in settings cause apps aren't initialized yet
    icon_static_urls = {}
    for size, static_file in getattr(settings, "PWA_APP_ICONS").items():
        icon_static_urls[size] = static(static_file)
    context["PWA_APP_ICONS"] = icon_static_urls

    # Add static prefix to urls, cant do it in settings cause apps aren't initialized yet
    splash_screens = []
    for splash_screen in context.get("PWA_APP_SPLASH_SCREEN"):
        static_file = splash_screen.get("src")
        src = static(static_file)
        media = splash_screen.get('media')
        splash_screens.append({
            "src": src,
            "media": media,
        })
    context["PWA_APP_SPLASH_SCREEN"] = splash_screens

    return context
