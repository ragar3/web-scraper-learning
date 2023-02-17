from bs4 import BeautifulSoup
from requests import get
import json

faculty = dict()
schools = []
departments = []

fields = ['title', 'email', 'phone']

page = get('https://directory.rpi.edu/organizations')
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

main = soup.body.find(class_='dirorg-list mt-5')

for child in main.children:
	if child.name == 'h2':
		school = child.find('a').string
		faculty[school] = dict()
		schools.append(school)

	if child.name == 'ul':
		school = schools[-1]

		for d in child.find_all('li'):
			dept = d.find('a').string
			faculty[school][dept] = dict()
			departments.append(dept)
			

			dept_page = get(d.find('a').get('href'))
			dept_soup = BeautifulSoup(dept_page.content, 'html.parser')

			table = dept_soup.find('tbody')
			for row in table.find_all('tr'):
				member = row.find('td')
				name = member.string.strip()
				faculty[school][dept][name] = dict()
				i = 0
				for field in member.next_siblings:
					if field.name == 'td':
						if not field.string is None:
							faculty[school][dept][name][fields[i]] = field.string.strip()
						else:
							faculty[school][dept][name][fields[i]] = field.find('a').string
						i += 1


faculty_json = json.dumps(faculty, indent=2)
with open('faculty.json', 'w') as file:
	file.write(faculty_json)
