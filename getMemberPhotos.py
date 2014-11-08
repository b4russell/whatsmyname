from bs4 import BeautifulSoup as BS
import urllib
import re
import json
membersUrl = 'http://assembly.ca.gov/assemblymembers'
districtClass = 'views-field-field-member-district-value'
partyClass = 'views-field-field-member-party-value'
imageDir = 'static/images/'
jsonDir = 'static/'

class Member(object):
    def __init__(self, soup):
        self.name = soup.a.string.strip()
        nameParts = self.name.split(',')
        #Note a member might have no comma (Vacant) or two commas (Jr.)
        self.lastName = nameParts[0]
        self.firstName = nameParts[-1]
        self.district = int(soup.find(class_=districtClass).string.strip())
        self.party = soup.find(class_=partyClass).string.strip()[0]
        self.imageUrl = soup.img['src']
        self.dictionaryFields = ['district', 'lastName', 'firstName', 'name', 'party']
        self.dictionary = {attr: getattr(self, attr) for attr in self.dictionaryFields}

    def saveImage(self):
        filename = str(self.district) + ".jpg"
        urllib.urlretrieve(self.imageUrl, imageDir + filename)

class Members(object):
    def __init__(self, url):
        members = urllib.urlopen(url)
        html = members.read()
        self.soup = BS(html)
        self.cells = self.soup.find_all(class_=re.compile('odd|even'))
        self.elements = []
        for m in self.cells:
            try:
                self.elements.append(Member(m))
            except Exception as e:
                print 'a member could not be added because: ' + repr(e)

    def downloadImages(self):
        for m in self.elements:
            m.saveImage()

    def saveJSON(self):
        self.dictionary = [m.dictionary for m in self.elements]
        jsonDictionary = json.dumps(self.dictionary)
        jsonFile = open(jsonDir+'members.json', 'w')
        jsonFile.write(jsonDictionary)
        jsonFile.close()

if __name__ == '__main__':
    m = Members(membersUrl)
    m.saveJSON()
