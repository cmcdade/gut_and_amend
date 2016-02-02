from bs4 import BeautifulSoup
import urllib

def get_removals(soup):
    removes = soup.find_all("strike")
    remove_divs = soup.find_all("div", id="strikediv")
    remove_len = 0

    for sec in removes:
        #print sec.get_text()
        remove_len += len(sec.get_text())

    for sec in remove_divs:
        #print sec.get_text()
        remove_len += len(sec.get_text())
    #print "\n"

    return remove_len

def get_additions(soup):
    adds = soup.find_all("font", class_="blue_text")
    add_len = 0
    for sec in adds:
        #print sec.get_text()
        add_len += len(sec.get_text())
    #print "\n"

    return add_len

def print_currentVersion(soup):
    version = soup.find("option", selected=True)
    print version.get_text()

def scrape_versions(link, bill_len):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, 'lxml')
    print_currentVersion(soup)
    print '----------------------------------'
    #print 'PRINTING ADDITIONS---------------\n'
    add = get_additions(soup)
    #print 'PRINT REMOVALS-------------------\n'
    remove = get_removals(soup)
    print 'add change: '+str((float(add)/float(bill_len)))
    print 'remove change: '+str((float(remove)/float(bill_len)))
    print '---------------------------------\n'

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
