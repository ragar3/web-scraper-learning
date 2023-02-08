from bs4 import BeautifulSoup
from requests import get
import json

faculty = dict()

page = get('https://faculty.rpi.edu/departments')
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

main = soup.body.find(id='block-paperclip-content').find('ul')

for school_heading in main.find_all('li'):
	if not school_heading.find('h3') is None:
		school = school_heading.find('h3')
		faculty[school.string] = dict()

		dept_list = school_heading.find('ul')
		if not dept_list is None:
			for dept in dept_list.find_all('a'):
				faculty[school.string][dept.string] = dict()

				dept_url = 'https://faculty.rpi.edu' + dept.get('href')
				dept_page = get(dept_url)
				dept_soup = BeautifulSoup(dept_page.content, 'html.parser')



faculty_json = json.dumps(faculty, indent=2)
with open('faculty.json', 'w') as file:
	file.write(faculty_json)
