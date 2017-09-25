import argparse
import random
import requests
from bs4 import BeautifulSoup
from lxml import html
from openpyxl import Workbook


def get_course_info(course_uri):
    course_req = requests.get(course_uri)
    if course_req.status_code != 200:
        return {}

    tree = html.fromstring(course_req.content)
    title = tree.xpath('//div[contains(@class,"header-container")]/h1[contains(@class,"title")]')
    start_date = tree.xpath('//div[contains(@class,"startdate")]/span')
    basic_info = tree.xpath('//div[@class="rc-BasicInfo"]/table/tbody/tr')
    commitment = language = rating = None
    for row in basic_info:
        data_class = row.xpath('.//i/@class')[0]
        if data_class == 'cif-clock':
            commitment = row.xpath('./td//text()')[1]
        elif data_class == 'cif-language':
            language = row.xpath('./td//text()')[1]
        elif data_class == 'cif-star-o':
            rating = row.xpath('./td//text()')[1]

    course_info = {'start_date': start_date[0].text,
                   'title': title[0].text,
                   'commitment': commitment,
                   'language': language,
                   'rating': rating,
                   'uri': course_uri
                   }
    return course_info


def get_courses_list(xml_uri, courses_count):
    request = requests.get(xml_uri)
    soup = BeautifulSoup(request.content, 'lxml')
    courses = map(lambda x: get_course_info(x.get_text()),
                  random.sample(soup.find_all('loc'),
                  courses_count))
    return courses


def output_courses_info_to_xlsx(courses, excel_name):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    for course in courses:
        ws.append([course['title'],
                   course['start_date'],
                   course['language'],
                   course['commitment'],
                   course['rating'],
                   course['uri']
                   ]
                  )
    wb.save(excel_name)


if __name__ == '__main__':
    xml_uri = 'https://www.coursera.org/sitemap~www~courses.xml'
    parser = argparse.ArgumentParser(description='this is a coursera random courses grabber.')
    parser.add_argument('-c', '--count', help='How much courses do you want to scrape (default: 5)', required=False)
    parser.add_argument('-o', '--output', help='Output excel file name (default: courses.xlsx)', required=False)
    args = parser.parse_args()
    courses_count = args.count or 5
    filename = args.output or 'courses.xlsx'
    courses = get_courses_list(xml_uri, courses_count)
    output_courses_info_to_xlsx(courses, filename)
