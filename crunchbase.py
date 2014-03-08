import requests
import json
import re

CRUNCHBASE_URL_1 = "http://api.crunchbase.com/v/1/person/"
CRUNCHBASE_URL_2 = ".js?api_key=emy48jd7q3k7kv6tx8ft6adb"

# Define list of people here
people = ['anthony_foxx', 'chuck_hagel', 'eric_holder', 'ernest_moniz'\
        'hilda_solis', 'hillary_clinton', 'jack_lew', 'janet_napolitano'\
        'jeh_johnson', 'joe_biden', 'john_kerry', 'ken_salazar'\
        'leon_panetta', 'ray_lahood', 'robert_gates', 'sally_jewell'\
        'steven_chu', 'thomas_perez', 'tim_geithner']
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
			overview = re.sub('<[A-Za-z\/][^>]*>', '', overview)
			institution = re.sub('<[A-Za-z\/][^>]*>', '', institution)
			
			company_string = ""
			for company in companies:
				company_string += company['title'] + " at " + company['firm']['name']
				company_string += "\n"

			associations = re.sub('<[A-Za-z\/][^>]*>', '', associations)
			text_file = open(person + "_crunchbase.txt", "w")
			text_file.write("Overview:\n" + overview)
			text_file.write("\n\nEducation:\n" + institution)
			text_file.write("\n\nWork Experience:\n" + company_string)
			text_file.write("\nThings associated with " + changed_person + ":\n" + associations)
			text_file.close()

		except Exception as e:
			print person + " failed to be found on the crunchbase API"
