from bs4 import BeautifulSoup
import urllib
import operator
import math
import re
import synset_analyzer

class Bill:
    def __init__(self, t, amends, f):
        self.title = t
        self.amendments = amends
        self.features = f

class Amendment:
    def __init__(self, t, l, sec, s):
        self.title = t
        self.length = l
        self.sections = sec
        self.synset = s

def BuildBulkRemoval(soup, title):
    removed_secs = {}
    remove_divs = soup.find_all("div", id="strikediv")

    for sec in remove_divs:
        section = sec.find_all("div", style="margin:0 0 1em 0;")
        if len(section) > 0:
            for x in section:
                s = x.get_text()
                subsection = CheckSubSection(s)

                sec_title = str(title+subsection)
                removed_secs[sec_title] = 100.0
    return removed_secs

def get_removals(sections, title, prefix):
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
        sec_title = str(prefix+title+subsection)
        if len(s) > 0:
            removed_secs[sec_title] = round(float(remove_len)/float(len(s)), 2)

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
        if len(s) > 0:
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

def BuildAmendmentRemovals(soup, prefix):
    title = GetSectionTitle(soup)
    sections = soup.find_all("div", style="margin:0 0 1em 0;")
    remove = get_removals(sections, title, prefix)
    remove = dict(remove.items() + BuildBulkRemoval(soup, prefix+title).items())

    return remove

def GetSectionTitle(soup):
    section_title = soup.find("h6")
    try:
        return str(section_title.getText())
    except (UnicodeEncodeError, AttributeError):
        return "ERROR"

def BuildAmendmentSection(soup, prefix):
    title = GetSectionTitle(soup)
    additions = BuildAmendmentAdditions(soup, prefix+title)

    return additions

def cleanSection(sec):
    retVal = sec.replace(".SEC.", "")
    if retVal.endswith("."):
        retVal = retVal[0:-1]
    return retVal


def AmendmentSections(soup, title, s):
    sections = soup.find("div", id="bill_all")
    sectionTitles = set()
    tmpSec = ""
    txt = sections.get_text().split()
    secLock = False

    for y in txt:
        if secLock:
            sectionTitles.add(cleanSection(tmpSec+y))
            secLock = False
        if y == 'Section':
            tmpSec = y
            secLock = True
    amendment_vers = Amendment(title, len(sections.get_text()), sectionTitles, s)
    return amendment_vers

def scrape_versions(link):
    r = urllib.urlopen(link).read()
    soup = BeautifulSoup(r, 'lxml')
    s = synset_analyzer.compile_bill(soup)
    return AmendmentSections(soup, print_currentVersion(soup), s)

def compile_versions(versions, base):
    compAdd = "&cversion="
    version = 0
    amendments = []
    for x in versions:
        cmp_link = base+compAdd+x['value']
        #if version > 0:
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

def getFeatures(soup):
    vote = soup.find("span", id="vote")
    appropriation = soup.find("span", id="appropriation")
    fiscalcommittee = soup.find("span", id="fiscalcommittee")
    localprogram = soup.find("span", id="localprogram")

    vote_feature = str(vote.get_text().split()[1])
    if len(str(appropriation.get_text().split()[1])) > 3:
        appropriation_feature = "Changed"
    else:
        appropriation_feature = "Same"

    if len(str(fiscalcommittee.get_text().split()[2])) > 3:
        fiscal_feature = "Changed"
    else:
        fiscal_feature = "Same"

    if len(str(localprogram.get_text().split()[2])) > 3:
        local_feature = "Changed"
    else:
        local_feature = "Same"

    return (vote_feature, appropriation_feature, fiscal_feature, local_feature)

def open_url(link):
    r = urllib.urlopen(link).read()
    billFeatures = getFeatures(BeautifulSoup(r, "lxml"))
    comp = compare_section(BeautifulSoup(r, "lxml"))
    bill_title = GetBillTitle(BeautifulSoup(r, "lxml"))
    base = link[0:34]
    comp_link = base+comp
    amendments = compare_versions(comp_link)
    processed_bill = Bill(bill_title.strip(), amendments, billFeatures)

    return processed_bill

def compare_sets(billset1, billset2, title1, title2):
    bill_union = set()
    diff_score_add = 0
    diff_score_remove = 0
    if title1 == title2:
        return 0, 0, 0

    for y in billset2:
        if y in billset1:
            bill_union.add(y)
        else:
            diff_score_add += 1
    for z in billset1:
        if z not in billset2:
            diff_score_remove += 1

    diff_score_add = (float(diff_score_add) / len(billset1))*100
    diff_score_remove = (float(diff_score_remove) / len(billset1))*100

    if int(diff_score_remove) is 0:
        max_score = 0
    else:
        max_score = (float(abs(len(billset2) - len(bill_union)))/float(len(billset2)))*100

    return max_score


def converted_date(title):
    date_part = title[0:8]
    formatted_date = date_part[6:8]+"/"+date_part[0:3]+date_part[3:5]
    return formatted_date

def sort_amends(amendments):
    amends = []
    for x in amendments:
        for y in range(0, len(x)):
            converted_date(x[y].title)
            amends.append(x[y])

    return sorted(amends, key=lambda x: converted_date(x.title))

def compareAmendSections(sec1, sec2):
    secDiff = 0
    union = 0
    for x in sec2:
        if x not in sec1:
            secDiff += 1
        else:
            union += 1
    return (float(abs(secDiff-union))/len(sec1))*100

def process_bill(bill_link):
    bill = open_url(bill_link)
    max_synset_change = 0
    amends = sort_amends(bill.amendments)
    bills_json = open('bills.csv', 'a+')
    avgLenChange = 0
    changes = 0
    totalSecChange = 0

    for y in range(1, len(amends)-1):
            tmp_change = compare_sets(amends[y].synset, amends[y+1].synset, amends[y].title, amends[y+1].title)
            secChange = compareAmendSections(amends[y].sections, amends[y+1].sections)
            if tmp_change > max_synset_change:
                max_synset_change = tmp_change
            changes += tmp_change
            totalSecChange += secChange
            avgLenChange = (float(amends[y].length)/float(amends[y+1].length))*100
    avgLenChange = avgLenChange/(len(amends)-1)
    totalSecChange = float(totalSecChange)/(len(amends)-1)
    changes = float(changes)/(len(amends)-1)
    print(bill.title,changes,max_synset_change,avgLenChange, totalSecChange, bill.features)
    bills_json.write(bill.title+"|"+str(changes)+"|"+str(max_synset_change)+"|"+str(avgLenChange)+"|"+str(totalSecChange)+"|"+str(bill.features[0])+"|"+bill.features[1]+"|"+str(bill.features[2])+"|"+str(bill.features[3])+"\n")
    bills_json.close()
    return bill

def getTotalLinks(soup):
    table = soup.find("table", id="bill_results")
    links = []
    base = 'https://leginfo.legislature.ca.gov'
    link = table.find_all("a")
    for x in link:
        tmpLink = x
        links.append(base+tmpLink['href'])
    return links

def getBillList(search_link):
    r = urllib.urlopen(search_link).read()
    links = getTotalLinks(BeautifulSoup(r, "lxml"))
    return links
