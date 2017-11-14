# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import lxml.etree
import urllib
import os, csv 
import pandas
import linecache
import wikipedia

currentPath = os.getcwd()
csv_file = currentPath + "/updated_wik_billboard.csv"
ref_file = currentPath + "/billboard.csv" 

headers = []
reader = pandas.read_csv(ref_file)
count = 0
opposite = 0
current_index = 0

def scrape(artist, tries):
    
    global count
    global opposite
    
    title = artist
    
    #ny = wikipedia.page(artist)
    #print ny.content

    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    text = revs[-1].text[0:2500]
    
    index_genre = text.find("genre")
    index_start = text.find("[",index_genre)+2
    index_bar_1 = text.find("|", index_genre)+1
    index_bar_2 = text.find("|", index_bar_1)+1
    index_end =text.find("]",index_start)
    genre = ""
    
    if index_genre == -1 and tries == 0:
        opposite = opposite +1
        scrape(artist+" (singer)", 1)
    elif index_genre == -1:
        genre = ""
    else:
        if index_start < index_bar_1:
            if index_end < index_bar_1:
                count = count +1
                genre = text[index_start:index_end]
            else:
                count = count +1
                genre = text[index_bar_1:index_end]
        elif index_start > index_bar_1 and index_start < index_bar_2:
            if index_end < index_bar_2:
                count = count +1
                genre = text[index_start: index_end]
            else:
                count = count +1
                genre = text[index_bar_2:index_end]
    
    if genre.find("music") != -1:
        index_music = genre.find("music")
        genre = genre[:index_music-1]
    if genre.lower().find("pop") != -1:
        genre = "Pop"
    elif genre.lower().find("rock") != -1:
        genre = "Rock"  

    
    if genre == "" and tries == 1:
        opposite = opposite +1
        
    #print "count " + str(count)
    #print "opposite " + str(opposite)
    #print "artist "+artist
    #print "genre "+genre
    #print ""
    #print ""

    return genre
    
def create_headers():
    
    global headers
    
    try:
        with open(ref_file, 'rU') as csvfile:
            reader = csv.reader(csvfile, dialect='excel')            
            headers = reader.next()
            headers = headers[0:5]
            headers.append("Genre")
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))

def get_original(artist, current_index):

    line = linecache.getline(ref_file, current_index+2)   
    array = line.split(',')
    array = array[0:5]+array[6]
    artist = ""
    if current_index !=0:
        artist = reformat(array[2])
        array[2] = artist
    final = dict(zip(headers, array))
    return final

def reformat(artist):
    formatted = artist.strip()
    feature = artist.find(" featuring")
    if feature != -1:
        formatted = formatted[:feature]
    else:
        and_index = artist.find(" and")
        if and_index != -1:
            formatted = formatted[:and_index]
    
    if formatted.find("  ") != -1:
        space = formatted.find("  ")
        formatted = formatted[:space]
    
    formatted = formatted.title()
    return formatted

def create_csv():
    
    global header
    global ref_file
    global csv_file
    global current_index
    
    data = pandas.read_csv(ref_file)
    artists = data.Artist.tolist()
    
    try:
        with open(csv_file, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, dialect='excel')
            writer.writeheader()
            for artist in artists:
                general_dict = get_original(artist, current_index)
                artist = reformat(artist)
                genre = scrape(artist, 0);
                new_dict = {"Genre": genre}
                general_dict.update(new_dict)
                writer.writerow(general_dict)
                current_index = current_index+1
                if current_index%25 == 0:
                    print current_index
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))
        
def main():
    create_headers()
    create_csv()
    
if __name__ == '__main__':
    main()
           