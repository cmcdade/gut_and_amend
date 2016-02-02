from bs4 import BeautifulSoup
import urllib

def compare_versions(link):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, "lxml")

def compare_section(soup):
    comp_links = soup.find_all("a", id="nav_bar_top_version_compare")
    return comp_links[0]['href']

def open_url(link):
    r = urllib.urlopen(link).read()
    comp = compare_section(BeautifulSoup(r, "lxml"))
    base = link[0:34]
    comp_link = base+link
    compare_versions(comp_link)


def process_bill():
    bill_link = raw_input("Enter leginfo link to bill: ")
    print bill_link
    open_url(bill_link)

def main():
    process_bill()

if __name__ == '__main__':
    main()
