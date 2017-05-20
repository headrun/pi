import urllib
import urlparse
import robotparser

class URLGatekeeper:
    """a class to track robots.txt rules across multiple servers"""
    def __init__(self):
        self.rpcache = {} # a dictionary of RobotFileParser objects, by domain
        self.robotsurl = ''
        __version__ = "1.371"
        self.urlopener = urllib.FancyURLopener()
        self.urlopener.version = "feedfinder/" + __version__ + " " + self.urlopener.version + " +http://www.aaronsw.com/2002/feedfinder/"
        self.urlopener.addheaders = [('User-agent', self.urlopener.version)]
        robotparser.URLopener.version = self.urlopener.version
        robotparser.URLopener.addheaders = self.urlopener.addheaders

    def _getrp(self, url):
        protocol, domain = urlparse.urlparse(url)[:2]
        if self.rpcache.has_key(domain):
            return self.rpcache[domain], self.robotsurl
        baseurl = '%s://%s' % (protocol, domain)
        self.robotsurl = urlparse.urljoin(baseurl, 'robots.txt')
        rp = robotparser.RobotFileParser(self.robotsurl)
        try:
            rp.read()
        except:
            pass
        self.rpcache[domain] = rp
        return rp, self.robotsurl

def get_crawl_access(url):
    urlgatekeeper = URLGatekeeper()
    try:
        rp, robotsurl = urlgatekeeper._getrp(url)
        crawl_status = rp.can_fetch('*', url)
        return crawl_status, robotsurl
    except:
        return True, ''
