import feedparser

class RssAggregator():
    feedurl = ''

    def __init__(self, rss_url):
        print(rss_url)
        self.feedurl = rss_url

    def parse(self):
        newfeed = feedparser.parse(self.feedurl)
        return newfeed