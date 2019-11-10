from selenium import webdriver

import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import re
from datetime import datetime, timedelta
import datefinder 

def main():

	list_of_events = [] #Contains events of deadlines of assignments foudn in classes

	url = "https://newclasses.nyu.edu/portal"

	chromedriver = "/Users/gautham/Downloads/chromedriver" #Location of chrome driver

	driver = webdriver.Chrome(chromedriver)
	driver.get(url)

	# try:
	element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "more-sites-menu"))) #waits for 100 secs until this ID is present in the webpage

	search = driver.find_elements_by_class_name('link-container') #link-container contains classes


	for i in range(1,len(search)):

		search = driver.find_elements_by_class_name('link-container')
		class_name = search[i].text
		search[i].click()
		driver.implicitly_wait(10)


		assignment = driver.find_element_by_link_text('Assignments') #menuitem contains assignments tab
		driver.implicitly_wait(10)
		assignment.click()

		assignment_names = driver.find_elements_by_name('asnActionLink') # contains assignment names
		deadlines = driver.find_elements_by_class_name('highlight') #contains deadlines for those assignments

		x = 0
		for j in range(len(assignment_names)):

			event,x = get_event(assignment_names,deadlines,j,x) 
			# print(event)
			
			list_of_events.append(event)

		driver.implicitly_wait(10)

	return list_of_events


def get_event(assignment_names, deadlines,j,x):

	event = {
				  'summary': 'Google I/O 2015',
				  'description': None,
				  'start': {
				    'dateTime': '2015-05-28T09:00:00',
				    'timeZone': 'Asia/Dubai',
				  },
				  'end': {
				    'dateTime': '2015-05-28T17:00:00',
				    'timeZone': 'Asia/Dubai',
				  },
				  'reminders': {
				    'useDefault': False,
				    'overrides': [
				      {'method': 'email', 'minutes': 24 * 60},
				      {'method': 'popup', 'minutes': 30},
				    ],
				  },
				}

	print(assignment_names[j].text)
	print(deadlines[j].text)
	print('')

	if deadlines[j].text == '- late':
					
		event['summary'] = assignment_names[j].text
		date_time = deadlines[x+1].text
		#Find format of darte from other formats
		matches = datefinder.find_dates(date_time)
		matches = list(matches)

		#Creating time format
		start_time = matches[0]
		end_time = start_time + timedelta(minutes = 30)

		event['start']['dateTime'] = start_time.strftime("%Y-%m-%dT%H:%M:%S")
	
		event['end']['dateTime'] = end_time.strftime("%Y-%m-%dT%H:%M:%S")

		x+=2

	else:
		
		event['summary'] = assignment_names[j].text
		date_time = deadlines[x].text
		#Find format of date from other formats
		matches = datefinder.find_dates(date_time)
		matches = list(matches)

		#Creating time format
		start_time = matches[0]
		end_time = start_time + timedelta(minutes = 30)

		event['start']['dateTime'] = start_time.strftime("%Y-%m-%dT%H:%M:%S")

		event['end']['dateTime'] = end_time.strftime("%Y-%m-%dT%H:%M:%S")

		x+=1

	return event,x

