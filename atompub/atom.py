from django.utils.xmlutils import SimplerXMLGenerator

GENERATOR_TEXT = 'django-atompub'
GENERATOR_ATTR = {
    'uri': 'http://code.google.com/p/django-atompub/',
    'version': 'r11'
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
            icon = self.__get_dynamic_attr('feed_icon', None),
            logo = self.__get_dynamic_attr('feed_logo', None),
            rights = self.__get_dynamic_attr('feed_rights', None),
            subtitle = self.__get_dynamic_attr('feed_subtitle', None),
            authors = self.__get_dynamic_attr('feed_authors', None, default=[]),
            categories = self.__get_dynamic_attr('feed_categories', None, default=[]),
            contributors = self.__get_dynamic_attr('feed_contributors', None, default=[]),
            links = self.__get_dynamic_attr('feed_links', None, default=[]),
            extra_attrs = self.__get_dynamic_attr('feed_extra_attrs', None),
            hide_generator = self.__get_dynamic_attr('hide_generator', None, default=False)
        )
        
        items = self.__get_dynamic_attr('items', None)
        if items is None:
            raise LookupError('Feed has no items field')
        
        for item in items:
            feed.add_item(
                atom_id = self.__get_dynamic_attr('item_id', item), 
                title = self.__get_dynamic_attr('item_title', item),
                updated = self.__get_dynamic_attr('item_updated', item),
                content = self.__get_dynamic_attr('item_content', item),
                published = self.__get_dynamic_attr('item_published', item),
                rights = self.__get_dynamic_attr('item_rights', item),
                source = self.__get_dynamic_attr('item_source', item),
                summary = self.__get_dynamic_attr('item_summary', item),
                authors = self.__get_dynamic_attr('item_authors', item, default=[]),
                categories = self.__get_dynamic_attr('item_categories', item, default=[]),
                contributors = self.__get_dynamic_attr('item_contributors', item, default=[]),
                links = self.__get_dynamic_attr('item_links', item, default=[]),
                extra_attrs = self.__get_dynamic_attr('item_extra_attrs', None, default={}),
            )
        
        return feed



## based on django.utils.feedgenerator.SyndicationFeed and django.utils.feedgenerator.Atom1Feed
class AtomFeed(object):
    
    mime_type = 'application/atom+xml'
    ns = u'http://www.w3.org/2005/Atom'
    
    
    def __init__(self, atom_id, title, updated, icon=None, logo=None, rights=None, subtitle=None,
        authors=[], categories=[], contributors=[], links=[], extra_attrs={}, hide_generator=False):
        if atom_id is None:
            raise LookupError('Feed has no feed_id field')
        if title is None:
            raise LookupError('Feed has no feed_title field')
        if updated is None:
            raise LookupError('Feed has no feed_updated field')
        self.feed = {
            'id': atom_id,
            'title': title,
            'updated': updated,
            'icon': icon,
            'logo': logo,
            'rights': rights,
            'subtitle': subtitle,
            'authors': authors,
            'categories': categories,
            'contributors': contributors,
            'links': links,
            'extra_attrs': extra_attrs,
            'hide_generator': hide_generator,
        }
        self.items = []
    
    
    def add_item(self, atom_id, title, updated, content=None, published=None, rights=None, source=None, summary=None,
        authors=[], categories=[], contributors=[], links=[], extra_attrs={}):
        if atom_id is None:
            raise LookupError('Feed has no item_id method')
        if title is None:
            raise LookupError('Feed has no item_title method')
        if updated is None:
            raise LookupError('Feed has no item_updated method')
        self.items.append({
            'id': atom_id,
            'title': title,
            'updated': updated,
            'content': content,
            'published': published,
            'rights': rights,
            'source': source,
            'summary': summary,
            'authors': authors,
            'categories': categories,
            'contributors': contributors,
            'links': links,
            'extra_attrs': extra_attrs,
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
    
    def write_link_construct(self, handler, link):
        if 'length' in link:
            link['length'] = str(link['length'])
        handler.addQuickElement(u'link', '', link)
    
    def write_category_construct(self, handler, category):
        handler.addQuickElement(u'category', '', category)
    
    def write_source(self, handler, data):
        handler.startElement(u'source', {})
        if data.get('id'):
            handler.addQuickElement(u'id', data['id'])
        if data.get('title'):
            self.write_text_construct(handler, u'title', data['title'])
        if data.get('subtitle'):
            self.write_text_construct(handler, u'subtitle', data['subtitle'])
        if data.get('icon'):
            handler.addQuickElement(u'icon', data['icon'])
        if data.get('logo'):
            handler.addQuickElement(u'logo', data['logo'])
        if data.get('updated'):
            handler.addQuickElement(u'updated', rfc3339_date(data['updated']))
        for category in data.get('categories', []):
            self.write_category_construct(handler, category)
        for link in data.get('links', []):
            self.write_link_construct(handler, link)
        for author in data.get('authors', []):
            self.write_person_construct(handler, u'author', author)
        for contributor in data.get('contributors', []):
            self.write_person_construct(handler, u'contributor', contributor)
        if data.get('rights'):
            self.write_text_construct(handler, u'rights', data['rights'])
        handler.endElement(u'source')
    
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
        feed_attrs = {u'xmlns': self.ns}
        if self.feed.get('extra_attrs'):
            feed_attrs.update(self.feed['extra_attrs'])
        handler.startElement(u'feed', feed_attrs)
        handler.addQuickElement(u'id', self.feed['id'])
        self.write_text_construct(handler, u'title', self.feed['title'])
        if self.feed.get('subtitle'):
            self.write_text_construct(handler, u'subtitle', self.feed['subtitle'])
        if self.feed.get('icon'):
            handler.addQuickElement(u'icon', self.feed['icon'])
        if self.feed.get('logo'):
            handler.addQuickElement(u'logo', self.feed['logo'])
        handler.addQuickElement(u'updated', rfc3339_date(self.feed['updated']))
        for category in self.feed['categories']:
            self.write_category_construct(handler, category)
        for link in self.feed['links']:
            self.write_link_construct(handler, link)
        for author in self.feed['authors']:
            self.write_person_construct(handler, u'author', author)
        for contributor in self.feed['contributors']:
            self.write_person_construct(handler, u'contributor', contributor)
        if self.feed.get('rights'):
            self.write_text_construct(handler, u'rights', self.feed['rights'])
        if not self.feed.get('hide_generator'):
            handler.addQuickElement(u'generator', GENERATOR_TEXT, GENERATOR_ATTR)
        
        self.write_items(handler)
        
        handler.endElement(u'feed')
    
    def write_items(self, handler):
        for item in self.items:
            entry_attrs = item.get('extra_attrs', {})
            handler.startElement(u'entry', entry_attrs)
            
            handler.addQuickElement(u'id', item['id'])
            self.write_text_construct(handler, u'title', item['title'])
            handler.addQuickElement(u'updated', rfc3339_date(item['updated']))
            if item.get('published'):
                handler.addQuickElement(u'published', rfc3339_date(item['published']))
            if item.get('rights'):
                self.write_text_construct(handler, u'rights', item['rights'])
            if item.get('source'):
                self.write_source(handler, item['source'])
            
            for author in item['authors']:
                self.write_person_construct(handler, u'author', author)
            for contributor in item['contributors']:
                self.write_person_construct(handler, u'contributor', contributor)
            for category in item['categories']:
                self.write_category_construct(handler, category)
            for link in item['links']:
                self.write_link_construct(handler, link)
            if item.get('summary'):
                self.write_text_construct(handler, u'summary', item['summary'])
            if item.get('content'):
                self.write_content(handler, item['content'])
            
            handler.endElement(u'entry')