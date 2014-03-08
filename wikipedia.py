#!/usr/bin/env python

import re
import yaml
import urllib
import urllib2

# Define list of people here
people = ['anthony_foxx', 'chuck_hagel', 'eric_holder', 'ernest_moniz'\
        'hilda_solis', 'hillary_clinton', 'jack_lew', 'janet_napolitano'\
        'jeh_johnson', 'joe_biden', 'john_kerry', 'ken_salazar'\
        'leon_panetta', 'ray_lahood', 'robert_gates', 'sally_jewell'\
        'steven_chu', 'thomas_perez', 'tim_geithner']

class WikipediaError(Exception):
    pass

class Wikipedia:
    url_article = 'http://%s.wikipedia.org/w/index.php?action=raw&title=%s'
    url_image = 'http://%s.wikipedia.org/w/index.php?title=Special:FilePath&file=%s'
    url_search = 'http://%s.wikipedia.org/w/api.php?action=query&list=search&srsearch=%s&sroffset=%d&srlimit=%d&format=yaml'
    
    def __init__(self, lang):
        self.lang = lang
    
    def __fetch(self, url):
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            result = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            raise WikipediaError(e.code)
        except urllib2.URLError, e:
            raise WikipediaError(e.reason)
        
        return result
    
    def article(self, article):
        url = self.url_article % (self.lang, urllib.quote_plus(article))
        content = self.__fetch(url).read()
        
        if content.upper().startswith('#REDIRECT'):
            match = re.match('(?i)#REDIRECT \[\[([^\[\]]+)\]\]', content)
            
            if not match == None:
                return self.article(match.group(1))
            
            raise WikipediaError('Can\'t found redirect article.')
        
        return content
    
    def image(self, image, thumb=None):
        url = self.url_image % (self.lang, image)
        result = self.__fetch(url)
        content = result.read()
        
        if thumb:
            url = result.geturl() + '/' + thumb + 'px-' + image
            url = url.replace('/commons/', '/commons/thumb/')
            url = url.replace('/' + self.lang + '/', '/' + self.lang + '/thumb/')
            
            return self.__fetch(url).read()
        
        return content
    
    def search(self, query, page=1, limit=10):
        offset = (page - 1) * limit
        url = self.url_search % (self.lang, urllib.quote_plus(query), offset, limit)
        content = self.__fetch(url).read()
        
        parsed = yaml.load(content)
        search = parsed['query']['search']
        
        results = []
        
        if search:
            for article in search:
                title = article['title'].strip()
                
                snippet = article['snippet']
                snippet = re.sub(r'(?m)<.*?>', '', snippet)
                snippet = re.sub(r'\s+', ' ', snippet)
                snippet = snippet.replace(' . ', '. ')
                snippet = snippet.replace(' , ', ', ')
                snippet = snippet.strip()
                
                wordcount = article['wordcount']
                
                results.append({
                    'title' : title,
                    'snippet' : snippet,
                    'wordcount' : wordcount
                })
        
        # yaml.dump(results, default_style='', default_flow_style=False,
        #     allow_unicode=True)
        return results

if __name__ == '__main__':
    for person in people:
        try:
            wiki = Wikipedia('simple')
            changed_person = person.split('_')
            changed_person = person[0] + " " + person[1]
            changed_person = person.title()
            overview = re.sub('<[A-Za-z\/][^>]*>', '', wiki.article(changed_person))
            # overview = re.sub('^\[\[ .* \]\]$', '', overview)
            overview = overview.replace("[[", "");
            overview = overview.replace("]]", "");
            overview = overview.replace("{{", "");
            overview = overview.replace("}}", "");
            overview = overview.replace("| ", "");
            overview = overview.replace("|", "");

            text_file = open(person + "_wikipedia.txt", "w")
            text_file.write("Overview:\n" + overview)
            text_file.close()
        except Exception as e:
            print changed_person + " failed to be found on Wikipedia"





