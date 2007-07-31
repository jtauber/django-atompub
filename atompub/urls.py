from django.conf.urls.defaults import *

from atompub.testmodel.feeds import TestFeed1, TestFeed2, TestFeed3

urlpatterns = patterns('',
    (r"^feeds/(.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": {
            "test_1": TestFeed1,
            "test_2": TestFeed2,
            "test_3": TestFeed3,
        }
    }),
)
