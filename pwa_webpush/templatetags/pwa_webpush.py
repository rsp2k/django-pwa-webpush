import json

from django import template
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from .. import app_settings
from ..utils import get_templatetag_context, add_static_prefix_to_srcs

register = template.Library()


@register.filter(is_safe=True)
def js(obj):
    """ Transform a python object so it can be safely used in javascript/JSON. """
    return mark_safe(json.dumps(obj, cls=DjangoJSONEncoder))


@register.inclusion_tag("pwa.html", takes_context=True)
def progressive_web_app_meta(context):
    # Pass all PWA_* settings into the template
    context.update({
        setting_name: getattr(app_settings, setting_name)
        for setting_name in dir(app_settings)
        if setting_name.startswith("PWA_")
    })
    context['vapid_public_key'] = settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY']

    context = add_static_prefix_to_srcs(context)

    return context


@register.filter
@register.inclusion_tag("webpush_header.html", takes_context=True)
def webpush_header(context):
    template_context = get_templatetag_context(context)
    return template_context


@register.filter
@register.inclusion_tag("webpush_button.html", takes_context=True)
def webpush_button(context):
    template_context = get_templatetag_context(context)
    return template_context
