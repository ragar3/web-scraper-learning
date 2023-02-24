import pandas
from bs4 import BeautifulSoup
from requests import get
import json
from time import time


class professor(object):
	def __init__(self, prof_soup):
		self.soup = prof_soup
		self.prof = {
		'Name' : self.name(),
		'Title' : self.title()
		}
		self.contact()
		self.position()

	def name(self):
		return self.soup.find('h3').string.strip()

	def title(self):
		return self.soup.find('h4').string.strip()

	def contact(self):
		s = self.soup.find_all(class_='col-12 col-md-4')[0]
		for line in s.find_all('p'):
			c = line.text.split(':')
			if "Email" in c[0]:
				self.prof['Email'] = c[1].strip()
			elif "RCS" in c[0]:
				self.prof['RCS'] = c[1].strip().replace('RCS id: ', '')
			elif "Phone" in c[0]:
				self.prof['Phone'] = c[1].strip().replace('Phone: ', '')

	def position(self):
		s = self.soup.find_all(class_='col-12 col-md-4')[1]
		for line in s.find_all('p'):
			c = line.text.split(':')
			self.prof[c[0]] = c[1].strip()

	def __str__(self):
		return str(self.prof)



def find_matches(url):
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser').body
	soup = soup.find(class_='pplsearch-results-people container')

	if not soup:
		print("Sorry, nothing found.")
		return []

	matches = []
	for p in soup.find_all(class_='row p-3 odd'):
		matches.append(professor(p))
	for p in soup.find_all(class_='row p-3 even'):
		matches.append(professor(p))

	return matches





if __name__ == '__main__':
	start = time()

	df = pandas.read_csv('spring-2021.csv')

	instructors = set()

	for i in set(df['course_instructor']):
		profs = i.split('/')
		for p in profs:
			instructors.add(p)

	matches = []
	for i in list(instructors):
		url = 'https://directory.rpi.edu/pplsearch/NULL/' + i
		matches += find_matches(url)

	faculty = []
	for m in matches:
		faculty.append(m.prof)

	faculty_json = json.dumps(faculty, indent=2)
	with open('faculty.json', 'w') as file:
		file.write(faculty_json)

	end = time()

	print(end-start, 'seconds')