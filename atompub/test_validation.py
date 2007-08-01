from datetime import datetime
import unittest

from atom import AtomFeed, ValidationError

class ValidationTests(unittest.TestCase):
    
    def test1(self): # minimal sunny day
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content='Some content.')
        feed.validate()
    
    def test2(self): # feed title type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title=('foo', 'test feed title'), updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test3(self): # feed subtitle type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', subtitle=('foo', 'test feed subtitle'), updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test4(self): # feed rights type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', rights=('foo', 'test feed rights'), updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test5(self): # entry title type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title=('foo', 'test entry title'), updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test6(self): # entry rights type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1))
        feed.add_item(atom_id='test_entry_id', title='test entry title', rights=('foo', 'test entry rights'), updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}], content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test7(self): # entry summary type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', summary=('foo', 'test entry summary'), updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test8(self): # source title type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', source={'title': ('foo', 'test source title')}, updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test9(self): # source subtitle type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', source={'subtitle': ('foo', 'test source title')}, updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test10(self): # source rights type one of text, html, xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', source={'rights': ('foo', 'test source title')}, updated=datetime(2007, 8, 1), content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test11(self): # feed can have author
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content='Some content.')
        feed.validate()
    
    def test12(self): # entry can have author
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1))
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}], content='Some content.')
        feed.validate()
    
    def test13(self): # an entry can override feed author
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry1_id', title='test entry1 title', updated=datetime(2007, 8, 1), content='Some content.')
        feed.add_item(atom_id='test_entry2_id', title='test entry2 title', updated=datetime(2007, 8, 1), authors=[{'name': 'Someone Else'}], content='Some content.')
        feed.validate()
    
    def test14(self): # if no feed author, all entries must have author
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1))
        feed.add_item(atom_id='test_entry1_id', title='test entry1 title', updated=datetime(2007, 8, 1), content='Some content.')
        feed.add_item(atom_id='test_entry2_id', title='test entry2 title', updated=datetime(2007, 8, 1), authors=[{'name': 'Someone Else'}], content='Some content.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test15(self): # if no feed author, all entries must have author, possibly in a source
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1))
        feed.add_item(atom_id='test_entry1_id', title='test entry1 title', updated=datetime(2007, 8, 1), source={'authors': [{'name': 'Someone Else'}]}, content='Some content.')
        feed.add_item(atom_id='test_entry2_id', title='test entry2 title', updated=datetime(2007, 8, 1), authors=[{'name': 'Someone Else'}], content='Some content.')
        feed.validate()
    
    def test16(self): # feeds must not contain more than one link rel="alternate" that has the same combination of type and hreflang values
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}],
            links=[{'rel': 'alternate', 'type': 'text/html', 'hreflang': 'en'}, {'rel': 'alternate', 'type': 'text/html', 'hreflang': 'fr'}])
        feed.validate()
    
    def test17(self): # feeds must not contain more than one link rel="alternate" that has the same combination of type and hreflang values
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}],
            links=[{'rel': 'alternate', 'type': 'text/html', 'hreflang': 'en'}, {'rel': 'alternate', 'type': 'text/html', 'hreflang': 'en'}])
        self.assertRaises(ValidationError, feed.validate)
    
    def test18(self): # entries without a content element must have a link rel="alternate"
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content='Test content.')
        feed.validate()
    
    def test19(self): # entries without a content element must have a link rel="alternate"
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1))
        self.assertRaises(ValidationError, feed.validate)
    
    def test20(self): # entries without a content element must have a link rel="alternate"
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), links=[{'rel': 'alternate', 'href': 'http://example.com/entry/1/'}])
        feed.validate()
    
    def test21(self): # entries must not contain more than one link rel="alternate" that has the same combination of type and hreflang values
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1),
            links=[{'rel': 'alternate', 'type': 'text/html', 'hreflang': 'en'}, {'rel': 'alternate', 'type': 'text/html', 'hreflang': 'fr'}])
        feed.validate()
    
    def test22(self): # entries must not contain more than one link rel="alternate" that has the same combination of type and hreflang values
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1),
            links=[{'rel': 'alternate', 'type': 'text/html', 'hreflang': 'en'}, {'rel': 'alternate', 'type': 'text/html', 'hreflang': 'en'}])
        self.assertRaises(ValidationError, feed.validate)
    
    def test23(self): # content with a src attribute must be empty
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'src': 'http://example.com/image.png' }, ''), summary='Some image.')
        feed.validate()
    
    def test24(self): # content with a src attribute must be empty
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'src': 'http://example.com/image.png' }, "Shouldn't' be here."), summary='Some image.')
        self.assertRaises(ValidationError, feed.validate)
    
    def test25(self): # content with a src attribute requires there be a summary element too
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'src': 'http://example.com/image.png' }, None))
        self.assertRaises(ValidationError, feed.validate)
    
    def test26(self): # content with a src attribute requires there be a summary element too
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'src': 'http://example.com/image.png' }, None), summary='Some Image.')
        feed.validate()
    
    def test27(self): # Base64 content requires there be a summary element too
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'type': 'image/png' }, '...some base64...'))
        self.assertRaises(ValidationError, feed.validate)
    
    def test28(self): # Base64 content requires there be a summary element too
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'type': 'text/plain' }, '...not base64...'))
        feed.validate()
    
    def test29(self): # Base64 content requires there be a summary element too
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'type': 'application/xml' }, '...not base64...'))
        feed.validate()
    
    def test30(self): # Base64 content requires there be a summary element too
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'type': 'image/png' }, '...some base64...'), summary='Some Image.')
        feed.validate()
    
    def test31(self): # invalid content type
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'type': 'foo' }, '...some foo content...'))
        self.assertRaises(ValidationError, feed.validate)
    
    def test32(self): # content with a src attribute can not have a type of text, html or xhtml
        feed = AtomFeed(atom_id='test_feed_id', title='test feed title', updated=datetime(2007, 8, 1), authors=[{'name': 'James Tauber'}])
        feed.add_item(atom_id='test_entry_id', title='test entry title', updated=datetime(2007, 8, 1), content=({'src': 'http://example.com/image.png', 'type': 'text'}, None), summary='Some Image.')
        self.assertRaises(ValidationError, feed.validate)

if __name__ == '__main__':
    unittest.main()