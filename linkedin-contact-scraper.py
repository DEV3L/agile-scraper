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

write_records_buffer = 10

file_prefix = user_login_value.split('@')[0]
data_file = f'./data/{file_prefix}_connections.csv'
results_file = f'./output/{file_prefix}_results.csv'


def run():
    print(f'Begin LinkedIn Contact Scraper - For {user_login_value}')
    print("- for the modern Jew on the go, now at MedaSync")

    contact_results = read_results_file(results_file)
    mapped_contacts = {contact.key: contact for contact in contact_results}

    contacts = read_data_file(data_file)
    print(f'Starting to Process {len(contacts)} contacts')

    browser = webdriver.Chrome()

    login_page = LinkedInLoginPageObject(browser, user_login_value, user_password_value)
    login_page.login()

    print(f'Logged into LinkedIn with user {user_login_value}')

    contact_count = 0
    for contact in contacts:
        mapped_contact = mapped_contacts.get(contact.key)

        if mapped_contact and (mapped_contact.email or mapped_contact.phone):
            continue

        print(f'Looking for contact: {contact.first_name} {contact.last_name}')
        contact_count = scrape_contact(contact, contact_count, contacts, browser)

    browser.close()
    write_records(contacts, contact_count)

    print(f'Finished LinkedIn Contact Scraper - For {user_login_value}')


def filter_contacts(contacts):
    results = read_results_file(result_file)
    results = [result for result in results if result.email or result.phone]
    filtered_contacts = []
    for contact in contacts:
        is_found = False

        for result_contact in results:
            if result_contact.key == contact.key:
                is_found = True
                break

        if not is_found:
            filtered_contacts.append(contact)

    return filtered_contacts


def read_data_file(data_file: str):
    data_rows = _read_file(data_file)
    return [Contact.from_row_data(row) for row in data_rows]


def read_results_file(results_file: str):
    try:
        results = _read_file(results_file)
        return [Contact.from_result_data(result) for result in results]
    except Exception as e:
        return []


def _read_file(file_name: str):
    with open(file_name) as csvfile:
        csv_data = csv.reader(csvfile)
        data_rows = [row for row in csv_data][1:]
    return data_rows


def scrape_contact(contact, contact_count: int, contacts, browser):
    linkedin_feed_page = LinkedInFeedPageObject(browser)
    if not linkedin_feed_page.search_contact(contact):
        return contact_count

    linkedin_search_results = LinkedInSearchResultsPageObject(browser)
    contact_links = linkedin_search_results.scrape_contact_links()

    for link in contact_links:
        linkedin_contact_page = LinkedInContactPageObject(browser, link)
        contact_details = linkedin_contact_page.scrape_contact()

        if not contact_details:
            continue

        contact.email = contact_details['email'].replace('\n', '').replace('Email', '')
        contact.phone = contact_details['phone'].replace('\n', '').replace('Phone', '')

        if should_write(contact_count):
            write_records(contacts, contact_count)

        return contact_count + 1

    return contact_count


def write_records(contacts, contact_count):
    with open(results_file, mode='w') as results:
        print(f'Writing records: {contact_count} of {len(contacts)}')

        results_writer = csv.writer(results, delimiter=',')

        results_writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Title', 'Connected On'])
        for contact in contacts:
            results_writer.writerow(contact.dump())


def should_write(contact_count):
    return contact_count and contact_count % write_records_buffer == 0


class Contact:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.phone = None
        self.company = None
        self.position = None
        self.connected_on = None

    @property
    def key(self):
        return self.first_name + self.last_name + self.position

    def dump(self):
        return [self.first_name, self.last_name, self.email, self.phone, self.company, self.position, self.connected_on]

    @staticmethod
    def from_row_data(row_data):
        contact = Contact()

        contact.first_name = row_data[0]
        contact.last_name = row_data[1]
        contact.email = row_data[2]
        contact.phone = None
        contact.company = row_data[3]
        contact.position = row_data[4]
        contact.connected_on = row_data[5]

        return contact

    @staticmethod
    def from_result_data(result_data):
        contact = Contact()

        contact.first_name = result_data[0]
        contact.last_name = result_data[1]
        contact.email = result_data[2]
        contact.phone = result_data[3]
        contact.company = result_data[4]
        contact.position = result_data[5]
        contact.connected_on = result_data[6]

        return contact


if __name__ == '__main__':
    run()
