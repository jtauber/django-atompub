from atompub.testmodel.models import AtomFeed as AtomFeedModel
from atompub.atom import Feed

feed_1 = AtomFeedModel.objects.get(pk=1)

class TestFeed1(Feed):
    
    hide_generator = True
    
    def feed_id(self):
        return feed_1.atom_id
    
    def feed_title(self):
        return feed_1.title.text # @@@ doesn't yet take into account text type
    
    def feed_updated(self):
        return feed_1.updated
    
    def feed_authors(self):
        for author in feed_1.authors.all():
            yield {'name': author.name}
    
    def feed_links(self):
        for link in feed_1.links.all():
            yield {'href': link.href}
    
    def items(self):
        return feed_1.atomentry_set.order_by('-updated')
    
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
            yield {'href': link.href}
    


feed_2 = AtomFeedModel.objects.get(pk=2)

class TestFeed2(Feed):
    
    def feed_id(self):
        return feed_2.atom_id
    
    def feed_title(self):
        return (feed_2.title.text_type, feed_2.title.text)
    
    def feed_updated(self):
        return feed_2.updated
    
    def feed_subtitle(self):
        return (feed_2.subtitle.text_type, feed_2.subtitle.text)
    
    def feed_rights(self):
        if feed_2.rights.text_type:
            return (feed_2.rights.text_type, feed_2.rights.text)
        else:
            return feed_2.rights.text
    
    def feed_authors(self):
        for author in feed_2.authors.all():
            yield {'name': author.name}
    
    def feed_links(self):
        for link in feed_2.links.all():
            link_dict = {'href': link.href}
            if link.rel:
                link_dict['rel'] = link.rel
            if link.media_type:
                link_dict['type'] = link.media_type
            if link.hreflang:
                link_dict['hreflang'] = link.hreflang
            if link.length:
                link_dict['length'] = link.length
            yield link_dict
    
    def items(self):
        return feed_2.atomentry_set.order_by('-updated')
    
    def item_id(self, item):
        return item.atom_id
    
    def item_title(self, item):
        return item.title.text # @@@ doesn't yet take into account text type
    
    def item_updated(self, item):
        return item.updated

    def item_published(self, item):
        return item.published
    
    def item_summary(self, item):
        if item.summary:
            return item.summary.text # @@@ doesn't yet take into account text type
        else:
            return None
    
    def item_content(self, item):
        content_dict = {}
        if item.content.text_type:
            content_dict['type'] = item.content.text_type
        elif item.content.media_type:
            content_dict['type'] = item.content.media_type
        if item.content.src:
            content_dict['src'] = item.content.src
        if item.content.text:
            content_text = item.content.text
        if item.content.xml_lang:
            content_dict['xml:lang'] = item.content.xml_lang
        if item.content.xml_base:
            content_dict['xml:base'] = item.content.xml_base
        return (content_dict, content_text)
    
    def item_links(self, item):
        for link in item.links.all():
            link_dict = {'href': link.href}
            if link.rel:
                link_dict['rel'] = link.rel
            if link.media_type:
                link_dict['type'] = link.media_type
            if link.hreflang:
                link_dict['hreflang'] = link.hreflang
            if link.length:
                link_dict['length'] = link.length
            yield link_dict
    
    def item_authors(self, item):
        for author in item.authors.all():
            person_dict = {'name': author.name}
            if author.uri:
                person_dict['uri'] = author.uri
            if author.email:
                person_dict['email'] = author.email
            yield person_dict
    
    def item_contributors(self, item):
        for contributor in item.contributors.all():
            person_dict = {'name': contributor.name}
            if contributor.uri:
                person_dict['uri'] = contributor.uri
            if contributor.email:
                person_dict['email'] = contributor.email
            yield person_dict


## test feed that isn't database-backed but tests some features not used by feeds above

from datetime import datetime

class TestFeed3(Feed):
    
    feed_id = "my_id"
    feed_title = "My Blog"
    feed_updated = datetime.now()
    
    feed_extra_attrs = {"foo": "bar"}
    
    feed_icon = "icon_url"
    feed_logo = "logo_url"
    
    feed_contributors = [{"name" : "James Tauber"}]
    
    feed_categories = [{"term": "test"}]
    
    items = [None] # dummy entry
    
    def item_id(self, item):
        return "item_id"
    
    def item_title(self, item):
        return "html", "<b>My</b> Entry"
    
    def item_updated(self, item):
        return datetime.now()
    
    def item_summary(self, item):
        return "This is a summary."
    
    def item_rights(self, item):
        return "Do what you will. This is just a test."

    def item_categories(self, item):
        return [
            {"term": "test"},
            {"term": "test", "scheme": "http://example.com/", "label": "test label"}
        ]
    
    def item_extra_attrs(self, item):
        return {"foo": "baz"}
