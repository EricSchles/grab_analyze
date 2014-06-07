# Grab from backpage, and classify according to ads I like.

import requests
import lxml.html
from text.classifiers import NaiveBayesClassifier

def grab_links(addr):
    r = requests.get(addr)
    html = lxml.html.fromstring(r.text)
    obj = html.xpath('//div[@class="cat"]/a')
    links = []
    link_objs = [elem.iterlinks() for elem in obj]
    for link_obj in link_objs:
        for j in link_obj:
            if 'href' in j:
                links.append(j[2])
    return links

classes = []
url = "http://manhattan.backpage.com/Classes/"
for i in xrange(5):
    if i == 0:
        tmp = grab_links(url)
        for j in tmp:
            classes.append(j)
    else:
        tmp = grab_links(url+"?page="+str(i))
        for j in tmp:
            classes.append(j)

train = []
test = []
with open("english.txt","r") as eng:
    for ind,val in enumerate(eng):
        try:
            val = val.encode("ascii","ignore")
            val = val.replace("\t","")
            val = val.replace("\n","")
            val = val.replace("\r","")
        except UnicodeDecodeError:
            continue
        
        train.append((val,"english"))

with open("spanish.txt","r") as span:
    for ind,val in enumerate(span):
        try:
            val = val.encode("ascii","ignore")
            val = val.replace("\t","")
            val = val.replace("\n","")
            val = val.replace("\r","")
        except UnicodeDecodeError:
            continue
        
        train.append((val,"spanish"))
    

cl = NaiveBayesClassifier(train)

english_links = open("english_links.txt","w")
spanish_links = open("spanish_links.txt","w")

for link in classes:
    r = requests.get(link)
    html = lxml.html.fromstring(r.text)
    obj = html.xpath('//div[@class="postingBody"]')
    post_body = [elem.text_content() for elem in obj]
    if post_body != []:
        text = post_body[0]
    try:
        text = text.encode("ascii","ignore")
        text = text.replace("\t","")
        text = text.replace("\n","")
        text = text.replace("\r","")
    except UnicodeDecodeError:
        continue
    
    if cl.classify(text) == "english":
        english_links.write("link= "+link+"\n\n")
        english_links.write("description= "+text+"\n\n")
    elif cl.classify(text) == "spanish":
        spanish_links.write("link= "+link+"\n\n")
        spanish_links.write("description= "+text+"\n\n")
    else:
        continue

english_links.close()
spanish_links.close()
