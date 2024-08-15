from django.contrib.sitemaps import Sitemap
from .models import *
from django.urls import reverse

"""
Sitemaps
    -> Are files which houses all URLs of a website and their metadata, which will be used by search engines to easily index any parts of that website
    -> A sitemap contains the following information
        1. URLs
        2. Last modified date (of each URLs)
        3. Frequency of change of content (of each URLs)
        4. Priority (of URLs)
    -> Methods and Attributes of Django's Sitemap class:
        1. items() - returns a queryset object (containing many items) that will be included in the sitemap
        2. location(item) - returns the absolute URL of the object/item
        3. lastmod(item) - returns the last modified date/time of the object/item
        4. changefreq(item) - returns the frequency of change of an object/item
        5. priority(item) - returns the priority of the object/item
        6. protocol - defines the protocol (HTTP/HTTPS) used by the object/item
        7. limit - defines the max no of items in the sitemap
"""


class BookSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "http"

    def items(self):
        return Book.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, item):
        return reverse("book_detail", args=[item.pk])
