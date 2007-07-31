from django.utils.xmlutils import SimplerXMLGenerator

GENERATOR_TEXT = 'django-atompub'
GENERATOR_ATTR = {
    'uri': 'http://code.google.com/p/django-atompub/',
    'version': 'r5'
}

## based on django.utils.feedgenerator.rfc3339_date
def rfc3339_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')



## based on django.contrib.syndication.feeds.Feed
class Feed(object):
    
    
    def __init__(self, slug, feed_url):
        # @@@ slug and feed_url are not used yet
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
            subtitle = self.__get_dynamic_attr('feed_subtitle', None),
            rights = self.__get_dynamic_attr('feed_rights', None),
            authors = self.__get_dynamic_attr('feed_authors', None, default=[]),
            links = self.__get_dynamic_attr('feed_links', None, default=[]),
            hide_generator = self.__get_dynamic_attr('hide_generator', None, default=False)
        )
        
        for item in self.__get_dynamic_attr('items', None):
            feed.add_item(
                atom_id = self.__get_dynamic_attr('item_id', item), 
                title = self.__get_dynamic_attr('item_title', item),
                updated = self.__get_dynamic_attr('item_updated', item),
                published = self.__get_dynamic_attr('item_published', item),
                authors = self.__get_dynamic_attr('item_authors', item, default=[]),
                contributors = self.__get_dynamic_attr('item_contributors', item, default=[]),
                links = self.__get_dynamic_attr('item_links', item, default=[]),
                summary = self.__get_dynamic_attr('item_summary', item),
                content = self.__get_dynamic_attr('item_content', item),
            )
        
        return feed



## based on django.utils.feedgenerator.SyndicationFeed and django.utils.feedgenerator.Atom1Feed
class AtomFeed(object):
    
    mime_type = 'application/atom+xml'
    ns = u'http://www.w3.org/2005/Atom'
    
    
    def __init__(self, atom_id, title, updated, subtitle=None, rights=None, authors=[], links=[], hide_generator=False):
        self.feed = {
            'id': atom_id,
            'title': title,
            'updated': updated,
            'subtitle': subtitle,
            'rights': rights,
            'authors': authors,
            'links': links,
            'hide_generator': hide_generator,
        }
        self.items = []
    
    
    def add_item(self, atom_id, title, updated, published=None, authors=[], contributors=[], links=[], summary=None, content=None):
        self.items.append({
            'id': atom_id,
            'title': title,
            'updated': updated,
            'published': published,
            'authors': authors,
            'contributors': contributors,
            'links': links,
            'summary': summary,
            'content': content,
        })
    
    def write_text_construct(self, handler, element_name, data):
        if isinstance(data, tuple):
            text_type, text = data
            if text_type == 'xhtml':
                handler.startElement(element_name, {'type': text_type})
                handler._write(text) # write unescaped -- it had better be well-formed XML
                handler.endElement(element_name)
            else:
                handler.addQuickElement(element_name, text, {'type': text_type})
        else:
            handler.addQuickElement(element_name, data)
    
    def write_person_construct(self, handler, element_name, person):
        handler.startElement(element_name, {})
        handler.addQuickElement(u'name', person['name'])
        if 'uri' in person:
            handler.addQuickElement(u'uri', person['uri'])
        if 'email' in person:
            handler.addQuickElement(u'email', person['email'])
        handler.endElement(element_name)
    
    def write_content(self, handler, data):
        if isinstance(data, tuple):
            content_dict, text = data
            if content_dict.get('type') == 'xhtml':
                handler.startElement(u'content', content_dict)
                handler._write(text) # write unescaped -- it had better be well-formed XML
                handler.endElement(u'content')
            else:
                handler.addQuickElement(u'content', text, content_dict)
        else:
            handler.addQuickElement(u'content', data)
    
    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(u'feed', {u'xmlns': self.ns})
        handler.addQuickElement(u'id', self.feed['id'])
        self.write_text_construct(handler, u'title', self.feed['title'])
        if self.feed.get('subtitle'):
            self.write_text_construct(handler, u'subtitle', self.feed['subtitle'])
        handler.addQuickElement(u'updated', rfc3339_date(self.feed['updated']))
        for link in self.feed['links']:
            if 'length' in link:
                link['length'] = str(link['length'])
            handler.addQuickElement(u'link', '', link)
        for author in self.feed['authors']:
            self.write_person_construct(handler, u'author', author)
        if self.feed.get('rights'):
            self.write_text_construct(handler, u'rights', self.feed['rights'])
        if not self.feed.get('hide_generator'):
            handler.addQuickElement(u'generator', GENERATOR_TEXT, GENERATOR_ATTR)
        
        self.write_items(handler)
        
        handler.endElement(u'feed')
    
    def write_items(self, handler):
        for item in self.items:
            handler.startElement(u'entry', {})
            
            handler.addQuickElement(u'id', item['id'])
            handler.addQuickElement(u'title', item['title']) # @@@ doesn't handle text type yet
            handler.addQuickElement(u'updated', rfc3339_date(item['updated']))
            if item.get('published'):
                handler.addQuickElement(u'published', rfc3339_date(item['published']))
            
            for author in item['authors']:
                self.write_person_construct(handler, u'author', author)
            for contributor in item['contributors']:
                self.write_person_construct(handler, u'contributor', contributor)
            for link in item['links']:
                if 'length' in link:
                    link['length'] = str(link['length'])
                handler.addQuickElement(u'link', '', link)
            if item.get('summary'):
                handler.addQuickElement(u'summary', item['summary']) # @@@ doesn't handle text type yet
            if item.get('content'):
                self.write_content(handler, item['content'])
            
            handler.endElement(u'entry')