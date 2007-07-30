from django.db import models

# Normally you would use your existing models and generate Atom feeds from
# those but these models exist for testing purposes.



TEXT_TYPE_CHOICES = (
    ('T', 'text'),
    ('H', 'html'),
    ('X', 'xhtml'),
)



class Text(models.Model):
    
    text_type = models.CharField(maxlength=1, choices=TEXT_TYPE_CHOICES)
    text = models.TextField()



class Content(models.Model):
    
    # inline text|html: text_type=null|"text"|"html", media_type=null, src=null, text=text
    # inline xhtml: text_type="xhtml", media_type=null, src=null, text=xhtmlDiv
    # inline other: text_type=null, media_type=atomMediaType, src=null, text=text|anyElement
    # out of line: text_type=null, media_type=atomMediaType, src=atomUri, text=null
    
    text_type = models.CharField(maxlength=1, choices=TEXT_TYPE_CHOICES, null=True)
    media_type = models.CharField(maxlength=100, null=True)
    src = models.URLField(null=True)
    text = models.TextField()

    # atomCommonAttributes
    xml_lang = models.CharField(maxlength=20, null=True)
    xml_base = models.URLField(null=True)



class Person(models.Model):
    
    # atom:name
    name = models.CharField(maxlength=100)
    
    # atom:uri?
    uri = models.URLField(null=True)
    
    # atom:email?
    email = models.EmailField(null=True)



class Link(models.Model):
    
    # href
    href = models.URLField()
    
    # rel?
    rel = models.CharField(maxlength=20, null=True)
    
    # type?
    media_type = models.CharField(maxlength=100, null=True)
    
    # hreflang?
    hreflang = models.CharField(maxlength=20, null=True)
    
    # title?
    title = models.CharField(maxlength=100, null=True)
    
    # length?
    length = models.PositiveIntegerField(null=True)



class Category(models.Model):
    
    # term
    term = models.CharField(maxlength=100)
    
    # scheme?
    # @@@ not currently supported
    
    # label?
    # @@@ not currently supported



class AtomFeed(models.Model):
    
    # atomCommonAttributes
    xml_lang = models.CharField(maxlength=20, null=True)
    xml_base = models.URLField(null=True)
    
    # atomId
    atom_id = models.URLField(unique=True)
    
    # atomTitle
    title = models.ForeignKey(Text, related_name="feed_title_of")
    
    # atomUpdated
    updated = models.DateTimeField()
    
    # atomGenerator?
    # this is generated, not stored in the database
    
    # atomIcon?
    icon = models.URLField(null=True)
    
    # atomLogo?
    logo = models.URLField(null=True)
    
    # atomRights?
    rights = models.ForeignKey(Text, null=True, related_name="feed_rights_of")
    
    # atomSubtitle?
    subtitle = models.ForeignKey(Text, null=True, related_name="feed_subtitle_of")
    
    # atomAuthor*
    authors = models.ManyToManyField(Person, related_name="feeds_authored")
    
    # atomCategory*
    categories = models.ManyToManyField(Category, related_name="feeds")
    
    # atomContributor*
    contributors = models.ManyToManyField(Person, related_name="feeds_contributed_to")
    
    # atomLink*
    links = models.ManyToManyField(Link, related_name="feeds_linked_from")
    
    # extensionElement*
    # @@@ extension elements are not currently supported
    
    # atomEntry*
    # see AtomEntry below



class AtomEntry(models.Model):
    
    feed = models.ForeignKey(AtomFeed)
    
    # atomCommonAttributes
    xml_lang = models.CharField(maxlength=20, null=True)
    xml_base = models.URLField(null=True)
    
    # atomId
    atom_id = models.URLField(unique=True)
    
    # atomTitle
    title = models.ForeignKey(Text, related_name="entry_title_of")
    
    # atomUpdated
    updated = models.DateTimeField()
    
    # atomContent?
    content = models.ForeignKey(Content, null=True)
    
    # atomPublished?
    published = models.DateTimeField(null=True)
    
    # atomRights?
    rights = models.ForeignKey(Text, null=True, related_name="entry_rights_of")
    
    # atomSource?
    # @@@ source is not currently supported
    
    # atomSummary?
    summary = models.ForeignKey(Text, null=True, related_name="entry_summary_of")
    
    # atomAuthor*
    authors = models.ManyToManyField(Person, related_name="entries_authored")
    
    # atomCategory*
    categories = models.ManyToManyField(Category, related_name="entries")
    
    # atomContributor*
    contributors = models.ManyToManyField(Person, related_name="entries_contributed_to")
    
    # atomLink*
    links = models.ManyToManyField(Link, related_name="entries_linked_from")
    
    # extensionElement*
    # @@@ extension elements are not currently supported
