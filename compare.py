# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import ssdeep
import os
import json


def get_item(name):
    # link
    path = "output/" + name + ".html"
    
    # file
    file = open(path, "r", encoding="utf-8")

    # read file
    html = BeautifulSoup(file.read())
    
    # the content of the page
    content = html.find("div", {"id": "content"})

    # we want the Erwägung
    erw = content.find('h1', text="Erwägungen")

    data = {}

    # we take the paragraphs
    paragraphs = []
    
    while erw:
        if erw.find('strong') is not None:
            paragraph = {}
            
            # the index of the paragraph
            index = erw.find('strong').extract().text
            paragraph["index"] = index
            
            # we want the original text
            paragraph["original"] = str(erw.text)[1:]
            
            # we find the links
            links = erw.findChildren("a", {"class": "LexLink"})
            hrefs = []
            for link in links:
                hrefs.append(link["href"][1:])
                link.extract()
            paragraph["links"] = hrefs
            
            # we remove to get text
            thinsp = erw.findChildren("span", {"class": "thinsp"})
            for t in thinsp:
                t.extract()
            notes = erw.findChildren("span", {"class": "note"})
            for note in notes:
                note.extract()
            pagebk = erw.findChildren("span", {"class": "pagebreak"})
            for bk in pagebk:
                bk.extract()
            
            # we save only the text
            paragraph["content"] = erw.text
            
            # we hash the text
            paragraph["hash"] = ssdeep.hash(bytes(erw.text, "utf-8"))
            
            # check that we have a big enough text
            if len(paragraph["content"]) > 10:
                paragraphs.append(paragraph)
                
    
        # next paragraph
        erw = erw.findNext("p")
    
    # save the paragraphs and return
    data["paragraphs"] = paragraphs
    return data

  def compare_all_paragraphs(data):

     
    number_of_paragraphs = 0
    #for decision in data:
    #    for paragraph in decision:
    #        number_of_paragraphs = number_of_paragraphs+1
    
    cmpmatrix = {}
    hashlink = {}
    
    #compare_score_matrix = [[0 for _ in range(number_of_paragraphs)] for _ in range(number_of_paragraphs)]
    for name1,decision1 in data.items():
        for name2,decision2 in data.items():
            if name1 == name2 or decision1 == decision2:
                break
            else:
                for paragraph1 in data[name1]["paragraphs"]:
                    x = paragraph1["hash"]
                    for paragraph2 in data[name2]["paragraphs"]:
                        y = paragraph2["hash"]
                        compare = ssdeep.compare(x,y)
                        
                        if compare:
                            #print("\n")
                            #print(compare)
                            #print(paragraph1["content"])
                            #print(paragraph2["content"])
                            xint = int.from_bytes(bytes(x,'ascii'),byteorder="big") # big/small, this is arbitrary but MUST be constant
                            yint = int.from_bytes(bytes(y,'ascii'),byteorder="big") # big/small, this is arbitrary but MUST be constant
                            if xint < yint:
                                try:
                                    cmpmatrix[x][y] = compare ## ordre correct!
                                except KeyError:
                                    cmpmatrix[x] = {y: compare}
                            else:
                                try:
                                    cmpmatrix[y][x] = compare ## ordre correct!
                                except KeyError:
                                    cmpmatrix[y] = {x: compare}
                            try:
                                hashlink[x].append( ( name1, paragraph1['index']) )
                            except KeyError:
                                hashlink[x] = [( name1, paragraph1['index']) ]
                            try:
                                hashlink[y].append( ( name2, paragraph2['index']) )
                            except KeyError:
                                hashlink[y] = [( name2, paragraph2['index']) ]

                        
    return cmpmatrix
                

path = "entscheide.txt"
with open(path, "r") as file:
    names = file.read().splitlines()
    
output = {}
for name in names:
    output[name] = get_item(name)


with open('json_data.json', 'w', encoding="utf-8") as outfile:
    content = json.dumps(output, indent=4, ensure_ascii=False)
    outfile.write(content)
    
with open('/home/ilya/openlegal/json_data.json', 'r') as inputfile:
    data = json.loads(inputfile.read())

comparison_values = compare_all_paragraphs(data)

with open('comparison_values.json', 'w', encoding="utf-8") as outfile:
    content = json.dumps(comparison_values, indent=4, ensure_ascii=False)
    outfile.write(content)

