#!/usr/bin/env python


import os, sys
import urllib, bs4, zipfile

if len(sys.argv) < 2:
    raise ValueError("Please specify output dir")

outdir = os.path.abspath(sys.argv[1])

if not os.path.exists(outdir):
    os.makedirs(outdir)

# download html file
htmlfile = os.path.join(outdir, 'twic.html')
if not os.path.exists(htmlfile):
    url = "http://theweekinchess.com/twic"
    f = urllib.urlopen(url)
    text = f.read()
    open(htmlfile, 'wt').write(text)
    text = open(htmlfile, 'rU').read()
    open(htmlfile, 'wt').write(text)
else:
    text = open(htmlfile).read()


import bs4
soup = bs4.BeautifulSoup(text)


# table with results
tables = soup.find_all('table', class_='results-table')
assert len(tables) == 1
table = tables[0]

# all rows with data
trs = table.find_all('tr', class_='')
print len(trs), 'records'

for tr in trs:
    tds = tr.find_all('td')
    # first cell is index
    ind = tds[0].text
    sys.stdout.write("%s: " % ind); sys.stdout.flush()
    # find pgn link in one of the cells
    found = False
    for td in tds[1:]:
        if td.text == 'PGN': 
            found = True
            break
    if not found: 
        print >> sys.stderr, "PGN for %s not found" % ind
        continue
    a = td.a
    href = a['href']
    fn = os.path.basename(href)
    # download
    sys.stdout.write("Downloading... "); sys.stdout.flush()
    urllib.urlretrieve(href, fn)
    bn, ext = os.path.splitext(fn)
    # extract
    sys.stdout.write("Extracting... "); sys.stdout.flush()
    zip_ref = zipfile.ZipFile(fn, 'r')
    zip_ref.extractall(outdir)
    zip_ref.close()
    os.remove(fn)
    # check output
    pgnfile = 'twic%s.pgn' % ind
    assert os.path.exists(os.path.join(outdir, pgnfile))
    sys.stdout.write("\n"); sys.stdout.flush()
    continue
