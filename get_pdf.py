from requests import get
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
from os import path, getcwd
import sys

url = input("Enter the url")
#url = "http://www-inst.eecs.berkeley.edu/~cs70/fa16/"

req = get(url)
if req.status_code == 200:
    html = req.text

bs = soup(html, 'html.parser')
links = bs.findAll('a')

n_pdfs = 0
n_saved_pdfs = 0

for link in links:
    current_link = link.get('href')
    if current_link is not None and current_link.endswith('pdf'):
        weblink = urljoin(url, current_link)
        print("pdf file found at: " + weblink)
        n_pdfs+=1

        file_address = str(current_link).split('/')[-1]

        if path.exists(file_address) == False:
            content = get(weblink, stream = True)

            if content.status_code == 200 and content.headers['content-type'] == 'application/pdf':
                print('File size(mb)', round(float(content.headers['Content-length'])/1000000), 2, sep=',')
                with open(file_address, 'wb') as pdf:
                    print('saving pdf to', file_address)
                    pdf.write(content.content)
                    print('COMPLETE!')

                    n_saved_pdfs+=1
                    print()
            else:
                print('content.status_code: ' + str(content.status_code))
                print('''content.headers['content-type']:''',content.headers['content-type'])
                print()
        else:
            print('Already Saved!')
            n_saved_pdfs+=1
            print()
if n_pdfs == 0:
    raise Exception('No pdfs found on page')

print("{0} pdfs found, {1} saved ".format(n_pdfs,n_saved_pdfs))

print(n_pdfs)
