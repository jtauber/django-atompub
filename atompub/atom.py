from django.utils.xmlutils import SimplerXMLGenerator



## based on django.utils.feedgenerator.rfc3339_date
def rfc3339_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')



## based on django.contrib.syndication.feeds.Feed
class Feed(object):
    
    
    def __init__(self, slug, feed_url):
        pass
    
    
    def __get_dynamic_attr(self, attname, obj, default=None):
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            # Check func_code.co_argcount rather than try/excepting the
            # function and catching the TypeError, because something inside
            # the function may raise the TypeError. This technique is more
            # accurate.
            if hasattr(attr, 'func_code'):
                argcount = attr.func_code.co_argcount
            else:
                argcount = attr.__call__.func_code.co_argcount
            if argcount == 2: # one argument is 'self'
                return attr(obj)
            else:
                return attr()
        return attr
    
    
    def get_feed(self, url=None):
        feed = AtomFeed(
            atom_id = self.__get_dynamic_attr('feed_id', None),
            title = self.__get_dynamic_attr('feed_title', None),
            updated = self.__get_dynamic_attr('feed_updated', None),
            authors = self.__get_dynamic_attr('feed_authors', None, default=[]),
            links = self.__get_dynamic_attr('feed_links', None, default=[]),
        )
        
        for item in self.__get_dynamic_attr('items', None):
            feed.add_item(
                atom_id = self.__get_dynamic_attr('item_id', item), 
                title = self.__get_dynamic_attr('item_title', item),
                updated = self.__get_dynamic_attr('item_updated', item),
                links = self.__get_dynamic_attr('item_links', item),
                summary = self.__get_dynamic_attr('item_summary', item),
            )
        
        return feed



## based on django.utils.feedgenerator.SyndicationFeed and django.utils.feedgenerator.Atom1Feed
class AtomFeed(object):
    
    mime_type = 'application/atom+xml'
    ns = u'http://www.w3.org/2005/Atom'
    
    
    def __init__(self, atom_id, title, updated, authors=[], links=[]):
        self.feed = {
            'id': atom_id,
            'title': title,
            'updated': updated,
            'authors': authors,
            'links': links,
        }
        self.items = []
    
    
    def add_item(self, atom_id, title, updated, links=[], summary=None):
        self.items.append({
            'id': atom_id,
            'title': title,
            'updated': updated,
            'links': links,
            'summary': summary,
        })
    
    
    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(u'feed', {u'xmlns': self.ns})
        handler.addQuickElement(u'id', self.feed['id'])
        handler.addQuickElement(u'title', self.feed['title']) # @@@ doesn't handle text type yet
        handler.addQuickElement(u'updated', rfc3339_date(self.feed['updated']))
        for link in self.feed['links']:
            handler.addQuickElement(u'link', '', link)
        for author in self.feed['authors']:
            handler.startElement(u'author', {})
            handler.addQuickElement(u'name', author['name'])
            if 'uri' in author:
                handler.addQuickElement(u'uri', author['uri'])
            if 'email' in author:
                handler.addQuickElement(u'email', author['email'])
            handler.endElement(u'author')
        
        self.write_items(handler)
        
        handler.endElement(u'feed')
    
    def write_items(self, handler):
        for item in self.items:
            handler.startElement(u'entry', {})
            
            handler.addQuickElement(u'id', item['id'])
            handler.addQuickElement(u'title', item['title']) # @@@ doesn't handle text type yet
            handler.addQuickElement(u'updated', rfc3339_date(item['updated']))
            
            for link in item['links']:
                handler.addQuickElement(u'link', '', link)
            if item.get('summary'):
                handler.addQuickElement(u'summary', item['summary']) # @@@ doesn't handle text type yet
            
            handler.endElement(u'entry')