# This is used to create the test1 fixtures

from atompub.testmodel.models import *
from datetime import datetime

## first example from 1.1 of RFC 4287

feed_title = Text(text="Example Feed")
feed_title.save()

feed = AtomFeed(
    atom_id = "urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6",
    title = feed_title,
    updated = datetime.now(),
)
feed.save()

john_doe = Person(name="John Doe")
john_doe.save()

feed_link = Link(href="http://example.org/")
feed_link.save()

feed.authors.add(john_doe)
feed.links.add(feed_link)

feed.save()

entry_title = Text(text_type="text", text="Atom-Powered Robots Run Amok")
entry_title.save()

entry = AtomEntry(
    feed = feed,
    atom_id = "urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a",
    title = entry_title,
    updated = datetime.now(),
)

entry.save()

summary = Text(text="Some text.")
summary.save()

entry.summary = summary
entry.save()

entry_link = Link(href="http://example.org/2003/12/13/atom03")
entry_link.save()

entry.links.add(entry_link)

entry.save()


## second example from 1.1 of RFC 4287

feed_title = Text(text_type="text", text="dive into mark")
feed_title.save()

feed_subtitle = Text(
    text_type = "html",
    text = """
  A <em>lot</em> of effort
  went into making this effortless
""")
feed_subtitle.save()

feed = AtomFeed(
    atom_id = "tag:example.org,2003:3",
    title = feed_title,
    subtitle = feed_subtitle,
    updated = datetime.now(),
)

rights = Text(text="Copyright (c) 2003, Mark Pilgrim")
rights.save()

feed.rights = rights

feed.save()

feed_link1 = Link(rel="alternate", media_type="text/html", hreflang="en", href="http://example.org/")
feed_link2 = Link(rel="self", media_type="application/atom+xml", href="http://example.org/feed.atom")

feed_link1.save()
feed_link2.save()

feed.links.add(feed_link1)
feed.links.add(feed_link2)

entry_title = Text(text="Atom draft-07 snapshot")
entry_title.save()

entry = AtomEntry(
    feed = feed,
    atom_id = "tag:example.org,2003:3.2397",
    title = entry_title,
    updated = datetime.now(),
    published = datetime.now(),
)

entry.save()

entry_link1 = Link(rel="alternate", media_type="text/html", href="http://example.org/2005/04/02/atom")
entry_link2 = Link(rel="enclosure", media_type="audio/mpeg", length="1337", href="http://example.org/audio/ph34r_my_podcast.mp3")

entry_link1.save()
entry_link2.save()

entry.links.add(entry_link1)
entry.links.add(entry_link2)

mark = Person(name="Mark Pilgrim", uri="http://example.org/", email="f8dy@example.com")
sam = Person(name="Sam Ruby")
joe = Person(name="Joe Gregorio")

mark.save()
sam.save()
joe.save()

entry.authors.add(mark)
entry.contributors.add(sam)
entry.contributors.add(joe)

content = Content(
    text_type = "xhtml",
    xml_lang = "en",
    xml_base = "http//divintomark.org/",
    text = """
    <div xmlns="http://www.w3.org/1999/xhtml">
        <p><i>[Update: The Atom draft is finished.]</i></p>
    </div>
"""
)

content.save()

entry.content = content

entry.save()
