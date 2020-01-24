import requests
from bs4 import BeautifulSoup
import lxml
import csv


def get_project_links():
    base_url = 'https://dff.dk/en/grants?b_start:int='
    list_pages = []
    num = 0
    # The number here (3110) refers to the number at the end of the url which increases by 10 when you go to the next page.
    # Click on the last page to see what the number is and change if needed
    while num <= 3110:
        page = base_url + str(num)
        num = num + 10
        list_pages.append(page)
    print(list_pages)
    return list_pages


def get_project_data():
    final_data = []
    for project_page in get_project_links():
        response = requests.get(project_page)
        soup = BeautifulSoup(response.text, 'lxml')

        for project in soup.find_all('div', {'class': 'result-item'}):
            project_data = []
            try:
                title = project.find('h2', {'class': 'result-title'})
                project_data.append(" ".join(title.text.split()))
                for other_info in project.find_all('ul', {'class': 'listing-horizontal'}):
                    for element in other_info.find_all('li'):
                        project_data.append(element.text.strip())
                for recipient_info in project.find_all('div', {'class': 'col-sm-3 result-person'}):
                    for person_host in recipient_info.find_all('div', {'class': 'col-xs-6 col-sm-12'}):
                        person = person_host.find('strong')
                        project_data.append(person.text.strip())
                        organisation = person_host.text.strip().replace(person.text.strip(), "")
                        project_data.append(" ".join(organisation.split()))
                for award_value_column in project.find_all('div', {'class': 'col-sm-2 text-right result-amount'}):
                    award_value = award_value_column.find('div', {'class': 'col-xs-6 col-sm-12'})
                    project_data.append(int(award_value.text.strip().replace('DKK\xa0', "").replace(',', '')))
                for abstract in project.find_all('p', {'class': 'col-md-11'}):
                    clean_abstract = " ".join(abstract.text.split())
                    project_data.append(clean_abstract)
            except TypeError:
                pass
            print(project_data)
            final_data.append(project_data)

    print("Length is: " + str(len(final_data)))
    return final_data


headers = ['project_title', 'funding_scheme', 'funding_area', 'award_year', 'PI', 'host_organisation', 'award_value',
           'abstract']
with open('dff_output.csv', encoding='utf-8', mode='w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(get_project_data())
