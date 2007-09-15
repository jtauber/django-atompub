from django.conf.urls.defaults import *

from atompub.protocol.views import service

from atompub.testmodel.feeds import TestFeed1, TestFeed2, TestFeed3, TestFeed4

urlpatterns = patterns('',
    
    (r"^service/$", service),
    
    # for testing
    (r"^feeds/(.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": {
            "test_1": TestFeed1,
            "test_2": TestFeed2,
            "test_3": TestFeed3,
            "test_4": TestFeed4,
        }
    }),
    
    (r"^admin/", include("django.contrib.admin.urls")),
)
