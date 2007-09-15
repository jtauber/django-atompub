from atompub.atom import Feed

from atompub.protocol.models import Collection


class CollectionFeed(Feed):
    
    def get_object(self, params):
        if len(params) != 1:
            raise LookupError
        return Collection.objects.get(id=params[0])
    
    def feed_id(self, obj):
        return obj.href()
    
    def feed_title(self, obj):
        return obj.title
    
    def items(self, obj):
        # @@@ returns all for now
        return obj.memberentry_set.order_by("-edited")
    
    def item_id(self, item):
        return item.href()
    
    def item_title(self, item):
        return item.title
    
    def item_updated(self, item):
        return item.edited # @@@ for now
    
    def item_authors(self, item):
        return [{"name": item.creator.get_full_name()}]
    
    def item_links(self, item):
        return [
            {"href": item.href()},
            {"rel": "edit", "href": item.href()}
        ]