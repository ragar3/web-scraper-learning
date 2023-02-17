import pandas
from bs4 import BeautifulSoup
from requests import get
from webbrowser import open
import json


class professor(object):
	def __init__(self, prof_soup):
		self.soup = prof_soup
		self.info = {
		'name' : '',
		'title' : '',
		'email' : '',
		'rcs' : '',
		'phone' : '',
		'department' : '',
		'school' : ''
		}

	def name(self):
		self.info['name'] = self.soup.find('h3').string

	def title(self):
		self.info['title'] = self.soup.find('h4').string

	def email(self):
		pass

	def rcs(self):
		pass

	def phone(self):
		pass

	def department(self):
		pass

	def school(self):
		pass

	def form_dict(self):
		for k in self.info:
			if self.info[k] == '':
				del self.info[k]
		return self.info



def find_matches(url):
	page = get(url)
	soup = BeautifulSoup(page.content, 'html.parser').body
	soup = soup.find(class_='pplsearch-results-people container')

	if not soup:
		print("Sorry, nothing found.")
		return []

	matches = []
	for p in soup.find_all('h3'):
		matches.append(professor(p))
	return matches


df = pandas.read_csv('spring-2021.csv')

instructors = set(df['course_instructor'])

for i in set(df['course_instructor']):
	profs = i.split('/')
	instructors.remove(i)
	for p in profs:
		instructors.add(p)

matches = []
for i in instructors:
	url = 'https://directory.rpi.edu/pplsearch/NULL/' + i
	matches += find_matches(url)

faculty = []
for m in matches:
	faculty.append(m.form_dict())

faculty_json = json.dumps(faculty, indent=4)
with open('faculty.json', 'w') as file:
	file.write(faculty_json)