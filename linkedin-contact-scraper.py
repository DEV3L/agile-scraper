import csv
import os

from environs import Env
from selenium import webdriver

from app.page_objects.linkedin_contact_page_object import LinkedInContactPageObject
from app.page_objects.linkedin_feed_page_object import LinkedInFeedPageObject
from app.page_objects.linkedin_login_page_object import LinkedInLoginPageObject
from app.page_objects.linkedin_search_results_page_object import LinkedInSearchResultsPageObject

Env().read_env(path="./.env")

user_login_value = os.environ['USER_LOGIN']
user_password_value = os.environ['USER_PASS']

data_file = './data/justin_connections.csv'


class Contact:
    def __init__(self, row_data):
        self.first_name = row_data[0]
        self.last_name = row_data[1]
        self.email = row_data[2]
        self.phone = None
        self.company = row_data[3]
        self.position = row_data[4]
        self.connected_on = row_data[5]

    def dump(self):
        return [self.first_name, self.last_name, self.email, self.phone, self.company, self.position, self.connected_on]


with open(data_file) as csvfile:
    csv_data = csv.reader(csvfile)
    data_rows = [row for row in csv_data][1:]
    contacts = [Contact(row) for row in data_rows]

if __name__ == '__main__':
    browser = webdriver.Chrome()

    login_page = LinkedInLoginPageObject(browser, user_login_value, user_password_value)
    login_page.login()

    contact_count = 0

    for contact in contacts:
        linkedin_feed_page = LinkedInFeedPageObject(browser)
        linkedin_feed_page.search_contact(contact)

        linkedin_search_results = LinkedInSearchResultsPageObject(browser)
        contact_links = linkedin_search_results.scrape_contact_links()

        for link in contact_links:
            linkedin_contact_page = LinkedInContactPageObject(browser, link)
            contact_details = linkedin_contact_page.scrape_contact()

            if not contact_details:
                continue

            contact.email = contact_details['email'].replace('\n', '').replace('Email', '')
            contact.phone = contact_details['phone'].replace('\n', '').replace('Phone', '')

            contact_count += 1
            break

        if contact_count > 5:
            break

    browser.close()

    with open('results.csv', mode='w') as results:
        results_writer = csv.writer(results, delimiter=',')

        results_writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Title', 'Connected On'])
        for contact in contacts:
            results_writer.writerow(contact.dump())
