from bs4 import BeautifulSoup
import urllib
import re

def get_removals(sections):
    remove_len = 0
    for sec in sections:
        removes = sec.find_all("strike")
        remove_divs = sec.find_all("div", id="strikediv")
        for small_remove in removes:
            remove_len = remove_len + 1
        for small_sec in remove_divs:
            remove_len = remove_len + 1

    return remove_len

def get_additions(sections):
    additions = 0
    num_sections = 0
    for sec in sections:
        adds = sec.find_all("font", class_="blue_text")
        for add in adds:
            additions = additions + 1

    return additions

def print_currentVersion(soup):
    version = soup.find("option", selected=True)
    print version.get_text()

def get_sections(soup):
    sections = soup.find_all("div", style="margin:0 0 1em 0;")
    add = get_additions(sections)
    remove = get_removals(sections)
    x = 1
    for sec in sections:
        x = x + 1
    print '----------------------------------'        
    print "Total number of sections: "+str(x)
    print "Number of sections with additions: "+str(add)
    print "Number of sections with removals: "+str(remove)
    print '---------------------------------\n'

def scrape_versions(link, bill_len):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, 'lxml')
    print_currentVersion(soup)
    get_sections(soup)
    #print 'PRINTING ADDITIONS---------------\n'
    #print 'PRINT REMOVALS-------------------\n'

def get_bill_length(link):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r ,'lxml')
    body = soup.find("div", id="bill_all")

    return len(body.get_text())

def compile_versions(versions, base):
    compAdd = "&cversion="
    version = 0
    current_bill_len = 0
    for x in versions:
        cmp_link = base+compAdd+x['value']
        if version == 0:
            current_bill_len = get_bill_length(cmp_link)
        else:
            scrape_versions(cmp_link, current_bill_len)
        version += 1

def get_versions(soup, base):
    version_links = soup.find_all("select", id="version")
    for x in version_links:
        val = x.find_all("option")
        compile_versions(val, base)

def compare_versions(link):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, "lxml")
    get_versions(soup, link)

def compare_section(soup):
    comp_links = soup.find_all("a", id="nav_bar_top_version_compare")
    print_billTitle(soup)
    print "\n"
    return comp_links[0]['href']

def print_billTitle(soup):
    title = soup.find(id="bill_title")
    print title.get_text()

def open_url(link):
    r = urllib.urlopen(link).read()
    comp = compare_section(BeautifulSoup(r, "lxml"))
    base = link[0:34]
    comp_link = base+comp
    compare_versions(comp_link)

def process_bill():
    bill_link = raw_input("Enter leginfo link to bill: ")
    print bill_link
    open_url(bill_link)

def main():
    process_bill()

if __name__ == '__main__':
    main()
