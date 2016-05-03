import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

def build_synset(text):
    bill_synset = {}
    for word in text:
        try:
            tmp_set = wn.synsets(word)
            if len(tmp_set) > 0:
                if str(tmp_set[0]) in bill_synset:
                    bill_synset[str(tmp_set[0])] += 1
                else:
                    bill_synset[str(tmp_set[0])] = 1
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return bill_synset
def compile_bill(soup):
    try:
        soup = soup.find("div", {"id": "bill_all"})
    # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
    except TypeError:
        pass

    try:
        text = soup.get_text()
    except AttributeError:
        return({})


# break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.split()
    text = [word.encode('utf-8') for word in text if word not in stopwords.words('english')]
    return build_synset(text)
