[![Build Status](https://travis-ci.org/avryhof/django-pwa-webpush.svg)](https://travis-ci.org/avryhof/django-pwa-webpush)
[![CodeFactor](https://www.codefactor.io/repository/github/avryhof/django-pwa-webpush/badge)](https://www.codefactor.io/repository/github/avryhof/django-pwa-webpush)
[![codecov](https://codecov.io/gh/avryhof/django-pwa-webpush/branch/master/graph/badge.svg)](https://codecov.io/gh/avryhof/django-pwa-webpush)
[![PyPI - Downloads](https://img.shields.io/pypi/v/django-pwa-webpush.svg)](https://pypi.org/project/django-pwa-webpush)
[![PyPI - Downloads](https://img.shields.io/pypi/djversions/django-pwa-webpush.svg)](https://pypi.org/project/django-pwa-webpush)


Django-PWA-Webpush
===================

This package is a pretty simple merge of [django-pwa](https://github.com/silviolleite/django-pwa), and [django-webpush](https://github.com/safwanrahman/django-webpush).

django-pwa
=====
This Django app turns your project into a [progressive web app](https://developers.google.com/web/progressive-web-apps/).  Navigating to your site on an Android phone will prompt you to add the app to your home screen.

Launching the app from your home screen will display your app [without browser chrome](https://github.com/silviolleite/django-pwa/raw/master/images/screenshot2.png).  As such, it's critical that your application provides all navigation within the HTML (no reliance on the browser back or forward button).

django-webpush
=====
Django-PWA-Webpush is a Package made for integrating and sending [Web Push Notification](https://developer.mozilla.org/en/docs/Web/API/Push_API) in Django Application.

Currently, it Supports Sending Push Notification to **Firefox 46+ and Chrome 52+**.

More at [Can I use...](https://caniuse.com/#feat=push-api)

This README
=====
This readme is a sloppy copy and paste job from the READMEs of the two packages I combined. So I have also included their own README files, since they are very informative.

. [django-pwa](https://github.com/avryhof/django-pwa-webpush/DJANGO-PWA-README.md)
. [django-webpush](https://github.com/avryhof/django-pwa-webpush/DJANGO-WEBPUSH-README.md)


Requirements
=====
Progressive Web Apps require HTTPS unless being served from localhost.  If you're not already using HTTPS on your site, check out [Let's Encrypt](https://letsencrypt.org/) and [ZeroSSL](https://zerossl.com/).

----------
Installation and Setup
-------------

You can install it easily from pypi by running

    pip install django-pwa-webpush

After installing the package, add `pwa_webpush` in in your `INSTALLED_APPS` settings

```python
INSTALLED_APPS = (
    ...
    'pwa_webpush',
)
```

You also need these settings:

```python

PWA_APP_NAME = 'My App'
PWA_APP_DESCRIPTION = "My app description"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/',
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'

PWA_APP_ICONS = [
    {"src": "pwa/icon-72x72.png", "size": "72x72"},
    {"src": "pwa/icon-96x96.png", "size": "96x96"},
    {"src": "pwa/icon-128x128.png", "size": "128x128"},
    {"src": "pwa/icon-144x144.png", "size": "144x144"},
    {"src": "pwa/icon-152x152.png", "size": "152x152"},
    {"src": "pwa/icon-192x192.png", "size": "192x192"},
    {"src": "pwa/icon-384x384.png", "size": "384x384"},
    {"src": "pwa/icon-512x512.png", "size": "512x512"},
]

PWA_APP_SPLASH_SCREEN = [
    {
        "src": "pwa/splash_screen-640x1136.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    },
    {
        "src": "pwa/splash_screen-750x1334.png",
        "media": "(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)",
    },
    {
        "src": "pwa/splash_screen-1242x2208.png",
        "media": "(device-width: 621px) and (device-height: 1104px) and (-webkit-device-pixel-ratio: 3)",
    },
    {
        "src": "pwa/splash_screen-1125x2436.png",
        "media": "(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)",
    },
    {
        "src": "pwa/splash_screen-828x1792.png",
        "media": "(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)",
    },
    {
        "src": "pwa/splash_screen-1242x2688.png",
        "media": "(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)",
    },
    {
        "src": "pwa/splash_screen-1536x2048.png",
        "media": "(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)",
    },
    {
        "src": "pwa/splash_screen-1668x2224.png",
        "media": "(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2)",
    },
    {
        "src": "pwa/splash_screen-1668x2388.png",
        "media": "(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)",
    },
    {
        "src": "pwa/splash_screen-2048x2732.png",
        "media": "(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)",
    },
]

PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

```

All PWA_ settings are optional, and the app will work fine with its internal defaults.  Highly recommend setting at least `PWA_APP_NAME`, `PWA_APP_DESCRIPTION`, `PWA_APP_ICONS` and `PWA_APP_SPLASH_SCREEN`.

For Webpush, you also need

```python

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "Vapid Public Key",
    "VAPID_PRIVATE_KEY":"Vapid Private Key",
    "VAPID_ADMIN_EMAIL": "admin@example.com"
}
```
**Replace ``"Vapid Public Key"`` and ``"Vapid Private Key"`` with your Vapid Keys. Also replace ``admin@example.com`` with your email so that the push server of browser can reach to you if anything goes wrong.**

> **To know how to obtain Vapid Keys please see this [`py_vapid`](https://github.com/web-push-libs/vapid/tree/master/python) and [Google Developer Documentation](https://developers.google.com/web/fundamentals/push-notifications/subscribing-a-user#how_to_create_application_server_keys). You can obtain one easily from [web-push-codelab.glitch.me](https://web-push-codelab.glitch.me/). ``Application Server Keys`` and ``Vapid Keys`` both are same.**

Then include `pwa_webpush` in the `urls.py`

```python
urlpatterns =  [
    url(r'', include('pwa_webpush.urls')) # You MUST use an empty string as the URL prefix
]
```

Add PWA Information to your template.
-------------------
Inject the required meta tags in your base.html (or wherever your HTML &lt;head&gt; is defined):
```html
{% load pwa_webpush %}

<head>
    ...
    {% progressive_web_app_meta %}
    ...
</head>
```

Add Web Push Information to your template.
-------------------

So in template, you need to load `webpush_notifications` custom template tag by following:
- If you are using built in templating engine, add `{% load webpush_notifications %}` in the template
- If you are using **jinja** templating engine, you do not need to load anything.

Next, inside the `<head></head>` tag add `webpush_header` according to your templating engine:

```html
<head>
  # For django templating engine
  {% webpush_header %}
  # For jinja templating engine
  {{ webpush_header() }}
</head>
```
Next, inside the `<body></body>` tag, insert `webush_button` where you would like to see the **Subscribe to Push Messaging** Button. Like following

```html
<body>
  <p> Hello World! </p>
  # For django templating engine
  {% webpush_button %}
  # For jinja templating engine
  {{ webpush_button() }}
</body>
```

 >**Note:** The Push Notification Button will show only if the user is logged in or any `group` named is passed through `webpush` context

 ***If you would like to mark the subscription as a group, like all person subscribe for push notification from the template should be marked as group and would get same notification, you should pass a `webpush` context to the template through views. The `webpush` context should have a dictionary like `{"group": group_name}`*** . Like following

```python
 webpush = {"group": group_name } # The group_name should be the name you would define.

return render(request, 'template.html',  {"webpush":webpush})
```
> **Note:** If you dont pass `group` through the `webpush` context, only logged in users can see the button for subscription and able to get notification.

----------

Troubleshooting
=====
While running the Django test server:

1. Verify that `/manifest.json` is being served
1. Verify that `/serviceworker.js` is being served
1. Verify that `/offline` is being served
1. Use the Application tab in the Chrome Developer Tools to verify the progressive web app is configured correctly.
1. Use the "Add to homescreen" link on the Application Tab to verify you can add the app successfully.

Adding Your Own Service Worker
=====
To add service worker functionality, you'll want to create a `serviceworker.js` or similarly named template in a template directory, and then point at it using the PWA_SERVICE_WORKER_PATH variable (PWA_APP_FETCH_URL is passed through).

```python
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'my_app', 'serviceworker.js')

```

The offline view
=====
By default, the offline view is implemented in `templates/offline.html`
You can overwrite it in a template directory if you continue using the default `serviceworker.js`.



Links
=====
* [Push API (mdn.org)](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
* [How Push Works (web.dev)](https://web.dev/articles/push-notifications-how-push-works)

