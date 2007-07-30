from django.conf.urls.defaults import *

from atompub.testmodel.feeds import TestFeed1

urlpatterns = patterns('',
    (r"^feeds/(.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": {
            "test_1": TestFeed1,
        }
    }),
)
