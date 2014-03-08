import requests
import json
import re

CRUNCHBASE_URL_1 = "http://api.crunchbase.com/v/1/person/"
CRUNCHBASE_URL_2 = ".js?api_key=emy48jd7q3k7kv6tx8ft6adb"

# Define list of people here
people = ['anne_wojcicki', 'bill_gates', 'brian_chesky', 'chris_anderson', \
        'drew_houston', 'elon_musk', 'jack_dorsey', 'jeff_bezos', \
        'larry_ellison', 'larry_page', 'marc_benioff', 'marissa_mayer', \
        'mark_zuckerberg', 'meg_whitman', 'michael_dell', 'nikola_tesla', \
        'peter_thiel', 'sergey_brin', 'shantau_narayen', 'sheryl_sandberg', \
        'steve_ballmer', 'steve_jobs', 'steve_wozniak', 'tim_cook'\
        ]
if __name__ == "__main__":
	for person in people:

		r = requests.get(CRUNCHBASE_URL_1 + person + CRUNCHBASE_URL_2)
		data_crunch = r.text

		try:
			changed_person = person.split('_')
			changed_person = person[0] + " " + person[1]
			changed_person = person.title()
			d2 = json.loads(data_crunch)
			overview = d2['overview']
			institution = d2['degrees'][0]['institution']
			companies = d2['relationships']
			associations = d2['tag_list']
			text_file = open(person + "_crunchbase.txt", "w")
			overview = re.sub('<[A-Za-z\/][^>]*>', '', overview)
			institution = re.sub('<[A-Za-z\/][^>]*>', '', institution)
			
			company_string = ""
			for company in companies:
				company_string += company['title'] + " at " + company['firm']['name']
				company_string += "\n"

			associations = re.sub('<[A-Za-z\/][^>]*>', '', associations)
			text_file.write("Overview:\n" + overview)
			text_file.write("\n\nEducation:\n" + institution)
			text_file.write("\n\nWork Experience:\n" + company_string)
			text_file.write("\nThings associated with " + changed_person + ":\n" + associations)
			text_file.close()

		except Exception as e:
			print person + " failed to be found on the crunchbase API"
