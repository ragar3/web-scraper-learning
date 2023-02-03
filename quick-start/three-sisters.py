'''
author: Ria Agarwal
date: 2/3/23

This is my first attempt at using bs4, following the quick start guide found here:
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start
'''

from bs4 import BeautifulSoup

soup = BeautifulSoup(open("three-sisters.html"), "html.parser")

# print(soup.prettify())

print(soup.title)
print(soup.title.name)
print(soup.title.string) # this is the actual title
print(soup.title.parent.name) # title's parent is head

print(soup.p) # finds first paragraph?
print(soup.p) # yep, just finds first instance; not a file iterator
print(soup.p['class']) # class of first paragraph; in this case, 'title'

print(soup.a) # finds first <a> tag (hyperlink)
print(soup.find_all('a')) # returns list (?) of all hyperlinks in doc
print(type(soup.find_all('a'))) # nope, not exactly a list; bs4.element.ResultSet

print(soup.find(id='link3')) # finds a specific element

# looks useful: finds all URLs in a doc
for link in soup.find_all('a'):
	print(link.get('href'))
	# within hyperlink objects, find the href (link) attribute

# could be useful for instructions or reference pages?
print(soup.get_text()) 