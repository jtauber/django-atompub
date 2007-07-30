from atompub.testmodel.models import AtomFeed as AtomFeedModel
from atompub.atom import Feed

feed_1 = AtomFeedModel.objects.get(pk=1)

class TestFeed1(Feed):
    
    def feed_id(self):
        return feed_1.atom_id
    
    def feed_title(self):
        return feed_1.title.text # @@@ doesn't yet take into account text type
    
    def feed_updated(self):
        return feed_1.updated
    
    def feed_authors(self):
        for author in feed_1.authors.all():
            yield {"name": author.name}
    
    def feed_links(self):
        for link in feed_1.links.all():
            yield {"href": link.href}
    
    def items(self):
        return feed_1.atomentry_set.order_by("-updated")
    
    def item_id(self, item):
        return item.atom_id
    
    def item_title(self, item):
        return item.title.text # @@@ doesn't yet take into account text type
    
    def item_updated(self, item):
        return item.updated
    
    def item_summary(self, item):
        if item.summary:
            return item.summary.text # @@@ doesn't yet take into account text type
        else:
            return None
    
    def item_links(self, item):
        for link in item.links.all():
            yield {"href": link.href}
    
