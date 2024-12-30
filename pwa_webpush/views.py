import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from pwa_webpush.forms import SubscriptionForm, WebPushForm
from . import app_settings
from .utils import add_static_prefix_to_srcs


def manifest(request):
    """
    https://developer.mozilla.org/en-US/docs/Web/Manifest

    :param request:
    :return:
    """
    context = {
        setting_name: getattr(app_settings, setting_name)
        for setting_name in dir(app_settings)
        if setting_name.startswith("PWA_")
    }
    context = add_static_prefix_to_srcs(context)

    context['vapid_public_key'] = settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY']

    if request.scheme not in context.get("PWA_APP_START_URL"):
        context["PWA_APP_START_URL"] = request.build_absolute_uri(
            context.get("PWA_APP_START_URL")
        )

    if request.scheme not in context.get("PWA_APP_SCOPE"):
        context["PWA_APP_SCOPE"] = request.build_absolute_uri(
            context.get("PWA_APP_SCOPE")
        )

    return render(request, "manifest.json", context, content_type="application/json")


def offline(request):
    return render(request, "offline.html")


def process_subscription_data(post_data, request):
    """Process the subscription data according to out model"""
    subscription_data = post_data.pop("subscription", {})

    # As our database saves the auth and p256dh key in separate field,
    # we need to refactor it and insert the auth and p256dh keys in the same dictionary
    keys = subscription_data.pop("keys", {})
    subscription_data.update(keys)

    # Insert the browser name and user agent
    subscription_data["user_agent"] = request.META['HTTP_USER_AGENT']
    subscription_data["browser"] = post_data.pop("browser")
    return subscription_data


@require_POST
@csrf_exempt
def save_info(request):
    # Parse the  json object from post data. return 400 if the json encoding is wrong
    try:
        post_data = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return HttpResponse(status=400)

    # Process the subscription data to match with the model
    subscription_data = process_subscription_data(post_data, request=request)
    subscription_form = SubscriptionForm(subscription_data)
    # pass the data through WebPushForm for validation purpose
    web_push_form = WebPushForm(post_data)

    # Check if subscriptioninfo and the web push info are valid
    if subscription_form.is_valid() and web_push_form.is_valid():
        # Get the cleaned data in order to get status_type and group_name
        web_push_data = web_push_form.cleaned_data
        status_type = web_push_data.pop("status_type")
        group_name = web_push_data.pop("group")

        # We at least need the user or group to subscribe for a notification
        if request.user.is_authenticated or group_name:
            # Save the subscription info with subscription data
            # as the subscription data is a dictionary and its valid
            subscription = subscription_form.get_or_save()
            web_push_form.save_or_delete(
                subscription=subscription, user=request.user, status_type=status_type, group_name=group_name
            )

            # If subscribe is made, means object is created. So return 201
            if status_type == WebPushForm.SUBSCRIBE:
                return HttpResponse(status=201)

            # Unsubscribe is made, means object is deleted. So return 202
            elif WebPushForm.UNSUBSCRIBE:
                return HttpResponse(status=202)

    return HttpResponse(status=400)


class ServiceWorkerView(TemplateView):
    """
    Service Worker need to be loaded from same domain.
    Therefore, use TemplateView in order to server the webpush_serviceworker.js
    """

    template_name = "serviceworker.js"
    content_type = "application/javascript"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vapid_public_key'] = settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY']

        return context
