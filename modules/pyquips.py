#!/usr/bin/python2.7

import os

# Global dirs should NOT have trailing slashes
scrape_dirs = ["/home/mark/ircbots/phenny/tmp/quips"]
resource_dir = "/etc/pyquips"
output_dir = "/var/www/quips"
quiplist = []

# Scrape folders for quips, deleting folder contents afterwards
def scrapeForQuips():
    global quiplist
    
    for folder in scrape_dirs:
        # Check if the folder exists
        if os.path.exists(folder) == False:
            print "WARN: Scrape path '" + folder + "' does not exist."
        
        # Check it's a folder
        if os.path.isdir(folder) == False:
            print "WARN: Scrape path '" + folder + "' is not a directory."
        
        # Get all quips from files, append them to a list and delete the file
        print "Scraping directories..."
        scrape_files = os.listdir(folder)
        for doc in scrape_files:
            f = open(folder + "/" + doc, 'r')
            quip = f.readline()
            quiplist.append(quip)
            f.close()
            os.remove(folder + "/" + doc)

# Append all quips in list to text file
def appendQuips():
    print "Saving quips..."
    print quiplist
    with open(resource_dir + "/quiplist.txt", "a") as f:
        for quip in quiplist:
            f.write(quip)

def phennyAppendQuips(quip):
    print "Saving quip..."
    with open(resource_dir + "/quiplist.txt", "a") as f:
        f.write(quip)

def compileHTMLQuiplist():
    print "Gathering resources..."
    with open(resource_dir + "/header.txt", "r") as f:
        headerFile = f.read()
    with open(resource_dir + "/quiplist.txt", "r") as f:
        txtFile = f.readlines()
    with open(resource_dir + "/footer.txt", "r") as f:
        footerFile = f.read()
        
    print "Writing HTML document..."
    with open(output_dir + "/index.html", "w") as f:
        f.write(headerFile)
        for quip in txtFile:
            f.write("<li>" + quip + "</li>\n")
        f.write(footerFile)
    
def run(quip):
    phennyAppendQuips(quip)
    compileHTMLQuiplist()

print "Script completed successfully."
