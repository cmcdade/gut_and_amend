from bs4 import BeautifulSoup
import urllib
import re

class Bill:
    def __init__(self, t, amends):
        self.title = t
        self.amendments = amends

class Amendment:
    def __init__(self, t, adds, removs):
        self.title = t
        self.additions = adds
        self.removals = removs

def get_removals(sections, title):
    removed_secs = {}

    for sec in sections:
        remove_len = 0
        s = sec.get_text()

        removes = sec.find_all("strike")
        remove_divs = sec.find_all("div", id="strikediv")

        for small_remove in removes:
            remove_len += len(small_remove.get_text())

        for small_sec in remove_divs:
            remove_len += len(small_sec.get_text())

        subsection = CheckSubSection(s)
        removed_secs[str(title+subsection)] = round(float(remove_len)/float(len(s)), 2)

    return removed_secs

def print_currentVersion(soup):
    version = soup.find("option", selected=True)
    return version.get_text()

def CheckSubSection(s):
    if '(' in s:
        return s[s.index("(") + 1:s.index("(") + 2]
    else:
        return "1"

def PrintSubSection(title, add_len, total_len):
    change = (float(add_len)/float(total_len))*100.0
    if change > 0.0:
        print title+"\t"+str(change)+" %"

def BuildAmendmentSmallAdds(soup, title, add_secs):
    sections = soup.find_all("div", style="margin:0 0 1em 0;")

    for sec in sections:
        add_len = 0
        s = sec.get_text()
        adds = sec.find_all("font", class_="blue_text")
        subsection = CheckSubSection(s)
        for x in adds:
            add_len += len(x.get_text())
        add_secs[str(title+subsection)] = round(float(add_len)/float(len(s)), 2)

def BuildAmendmentAdditions(soup, title):
    tmp = soup.find_all("font", class_="blue_text")
    add_sections = {}
    BuildAmendmentSmallAdds(soup, title, add_sections)

    for y in tmp:
        divs = y.find_all("div", style="margin:0 0 1em 0;")
        if len(divs) > 0:
            for z in divs:
                subsection = CheckSubSection(z.get_text())
                add_sections[str(title+subsection)] = 100.0

    return add_sections

def BuildAmendmentRemovals(soup):
    title = GetSectionTitle(soup)
    sections = soup.find_all("div", style="margin:0 0 1em 0;")
    remove = get_removals(sections, title)

    return remove

def GetSectionTitle(soup):
    section_title = soup.find("h6")
    return str(section_title.getText())

def BuildAmendmentSection(soup):
    title = GetSectionTitle(soup)
    additions = BuildAmendmentAdditions(soup, title)

    return additions

def AmendmentSections(soup, title):
    sections = soup.find("div", id="bill_all")
    adds = {}
    removes = {}

    for x in sections:
        adds = dict(adds.items() + BuildAmendmentSection(x).items())
        removes = dict(removes.items() + BuildAmendmentRemovals(x).items())

    amendment_vers = Amendment(title, adds, removes)

    return amendment_vers

def scrape_versions(link):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, 'lxml')
    return AmendmentSections(soup, print_currentVersion(soup))

def compile_versions(versions, base):
    compAdd = "&cversion="
    version = 0
    amendments = []
    for x in versions:
        cmp_link = base+compAdd+x['value']
        if version > 0:
            amendments.append(scrape_versions(cmp_link))
        version += 1

    return amendments

def get_versions(soup, base):
    version_links = soup.find_all("select", id="version")
    amendments = []

    for x in version_links:
        val = x.find_all("option")
        amendments.append(compile_versions(val, base))

    return amendments

def compare_versions(link):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, "lxml")
    return get_versions(soup, link)

def GetBillTitle(soup):
    title = soup.find(id="bill_title")
    return title.get_text()

def compare_section(soup):
    comp_links = soup.find_all("a", id="nav_bar_top_version_compare")
    return comp_links[0]['href']

def open_url(link):
    r = urllib.urlopen(link).read()
    comp = compare_section(BeautifulSoup(r, "lxml"))
    bill_title = GetBillTitle(BeautifulSoup(r, "lxml"))
    base = link[0:34]
    comp_link = base+comp
    amendments = compare_versions(comp_link)
    processed_bill = Bill(bill_title, amendments)

    return processed_bill

def process_bill():
    bill_link = raw_input("Enter leginfo link to bill: ")
    bill = open_url(bill_link)
    print bill.title

def main():
    process_bill()

if __name__ == '__main__':
    main()
