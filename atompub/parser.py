# 
# django-atompub by James Tauber <http://jtauber.com/>
# http://code.google.com/p/django-atompub/
# An implementation of the Atom format and protocol for Django
# 
# 
# Copyright (c) 2007, James Tauber
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 



from xml.dom.minidom import parse
import re
from datetime import datetime, tzinfo


DATETIME = re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T"
r"(?P<hour>\d{2}):(?P<minute>\d{2})(:(?P<second>\d{2})(\.(?P<fraction>\d+))?)"
r"((?P<tzzulu>Z)|((?P<tzoffset>[\-+])(?P<tzhour>\d{2}):(?P<tzminute>\d{2})))$")


def parse_rfc3339(text):
    x = DATETIME.match(text).groupdict()
    
    class ZuluTZ(tzinfo):
        def utcoffset(self, dt):
            return timedelta(0)
    
    class OtherTZ(tzinfo):
        def __init__(self, tzoffset, tzhour, tzminute):
            minutes = int(tzhour) * 60 + int(tzminute)
            if tzoffset == "+":
                self.minutes = +minutes
            else:
                self.minutes = -minutes
            
        def utcoffset(self, dt):
            return timedelta(minutes=self.minutes)
    
    if x['tzzulu']:
        tz = ZuluTZ()
    else:
        tz = OtherTZ(x['tzoffset'], x['tzhour'], x['tzminute'])
        
    return datetime(int(x['year']), int(x['month']), int(x['day']), int(x['hour']), int(x['minute']), int(x['second']), 0, tz)



class AtomException(Exception):
    pass



def atom_name(element):
    if element.namespaceURI == 'http://www.w3.org/2005/Atom':
        return element.localName
    else:
        return None



def get_text(element):
    text = ""
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text += node.data
        else:
            raise AtomException("%s node not allowed here" % node.nodeName)
    return text



def get_xml(nodelist):
    text = ""
    for node in nodelist:
        text += node.toxml()
    return text



def get_elements(nodelist):
    for node in nodelist:
        if node.nodeType == node.ELEMENT_NODE:
            yield node
        elif node.nodeType == node.TEXT_NODE:
            # @@@ check for whitespace only
            continue
        else:
            raise AtomException("'%s' not allowed here" % node)


def parse_feed(element):
    
    feed_elements = {}
    entries = []
    
    for child in get_elements(element.childNodes):
        
        if entries:
            if atom_name(child) == 'entry':
                entries.append(parse_entry(child))
            else:
                raise AtomException("once entries start in feed, only further entries can follow, not '%s'" % child.nodeName)
        else:
            PARSE_TABLE = { # 'element': (function, multiple)
                'author': (parse_person, 'authors'),
                'category': (parse_category, 'categories'),
                'contributor': (parse_person, 'contributors'),
                'generator': (parse_generator, None),
                'icon': (parse_simple, None),
                'id': (parse_simple, None),
                'link': (parse_link, 'links'),
                'logo': (parse_simple, None),
                'rights': (parse_text, None),
                'subtitle': (parse_text, None),
                'title': (parse_text, None),
                'updated': (parse_date, None),
            }
            if atom_name(child) in PARSE_TABLE:
                function, multiple = PARSE_TABLE[atom_name(child)]
                if not multiple:
                    if atom_name(child) in feed_elements:
                        raise AtomException("feed cannot have more than one '%s'" % child.nodeName)
                    feed_elements[atom_name(child)] = function(child)
                else:
                    feed_elements.setdefault(multiple, []).append(function(child))
            elif atom_name(child) == 'entry':
                entries.append(parse_entry(child))
            else:
                raise AtomException("%s not allowed here" % child.nodeName)
    
    # @@@ check for id, title and updated
    return feed_elements, entries


def parse_person(element):
    
    person_elements = {}
    
    for child in get_elements(element.childNodes):
        
        PARSE_TABLE = {
            'name': (parse_simple, None),
            'uri': (parse_simple, None),
            'email': (parse_simple, None),
        }
        if atom_name(child) in PARSE_TABLE:
            function, multiple = PARSE_TABLE[atom_name(child)]
            if not multiple:
                if atom_name(child) in person_elements:
                    raise AtomException("person construct cannot have more than one '%s'" % child.nodeName)
                person_elements[atom_name(child)] = function(child)
            else:
                person_elements.setdefault(multiple, []).append(function(child))
        else:
            raise AtomException("%s not allowed here" % child.nodeName)
    
    # @@@ check for name
    return person_elements


def parse_category(element):
    category_dict = {}
    for name, value in element.attributes.items():
        category_dict[name] = value
    
    # @@@ check for term
    return category_dict


def parse_generator(element):
    generator_attr = {}
    for name, value in element.attributes.items():
        generator_attr[name] = value
    generator_text = get_text(element)
    return generator_attr, generator_text


def parse_simple(element):
    return get_text(element)


def parse_link(element):
    link_dict = {}
    for name, value in element.attributes.items():
        link_dict[name] = value
    
    # @@@ check for href
    return link_dict


def parse_text(element):
    if element.hasAttribute('type'):
        text_type = element.getAttribute('type')
        if text_type in ['text', 'html']:
            return (text_type, get_text(element))
        elif text_type == 'xhtml':
            pass # @@@
        else:
            raise AtomException("text construct of type '%s' not allowed" % text_type)
    else:
        return get_text(element)


def parse_date(element):
    text = get_text(element)
    return parse_rfc3339(text)


def parse_content(element):
    if element.hasAttribute('type'):
        text_type = element.getAttribute('type')
        if text_type == 'xhtml':
            return get_xml(element.childNodes)
        elif text_type in ['text', 'html']:
            return (text_type, get_text(element))
        elif "/" in text_type:
            # @@@ should really check for Base64
            return (text_type, get_text(element))
        else:
            return (text_type, get_text(element))
        
    else:
        return get_text(element)


def parse_source(element):
    source = {}
    
    for child in get_elements(element.childNodes):
        
        PARSE_TABLE = { # 'element': (function, multiple)
            'author': (parse_person, 'authors'),
            'category': (parse_category, 'categories'),
            'contributor': (parse_person, 'contributors'),
            'generator': (parse_generator, None),
            'icon': (parse_simple, None),
            'id': (parse_simple, None),
            'link': (parse_link, 'links'),
            'logo': (parse_simple, None),
            'rights': (parse_text, None),
            'subtitle': (parse_text, None),
            'title': (parse_text, None),
            'updated': (parse_date, None),
        }
        if atom_name(child) in PARSE_TABLE:
            function, multiple = PARSE_TABLE[atom_name(child)]
            if not multiple:
                if atom_name(child) in source:
                    raise AtomException("feed cannot have more than one '%s'" % child.nodeName)
                source[atom_name(child)] = function(child)
            else:
                source.setdefault(multiple, []).append(function(child))
        else:
            # @@@ allow extension elements
            raise AtomException("%s not allowed here" % child.nodeName)


def parse_entry(element):
    entry = {}
    
    for child in get_elements(element.childNodes):
        
        PARSE_TABLE = { # 'element': (function, multiple)
            'author': (parse_person, 'authors'),
            'category': (parse_category, 'categories'),
            'content': (parse_content, None),
            'contributor': (parse_person, 'contributors'),
            'id': (parse_simple, None),
            'link': (parse_link, 'links'),
            'published': (parse_date, None),
            'rights': (parse_text, None),
            'source': (parse_source, None),
            'summary': (parse_text, None),
            'title': (parse_text, None),
            'updated': (parse_date, None),
        }
        if atom_name(child) in PARSE_TABLE:
            function, multiple = PARSE_TABLE[atom_name(child)]
            if not multiple:
                if atom_name(child) in entry:
                    raise AtomException("entry cannot have more than one '%s'" % child.nodeName)
                entry[atom_name(child)] = function(child)
            else:
                entry.setdefault(multiple, []).append(function(child))
        else:
            raise AtomException("%s not allowed here" % child.nodeName)
    
    return entry



if __name__ == "__main__":
    import sys
    doc = parse(sys.argv[1])

    root = doc.firstChild

    if atom_name(root) == "feed":
        print parse_feed(root)
    elif atom_name(root) == "entry":
        print parse_entry(root)
    else:
        print "root must be 'feed' or 'entry'"