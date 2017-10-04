import argparse
import random
import requests
from bs4 import BeautifulSoup
from lxml import html
from openpyxl import Workbook


def get_course_content(course_uri):
    course_req = requests.get(course_uri)
    if not course_req.ok:
        return None
    else:
        return html.fromstring(course_req.content)


def get_course_info(content, course_uri):
    tree = content
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
    response = requests.get(xml_uri)
    soup = BeautifulSoup(response.content, 'lxml')
    rand_courses = random.sample(soup.find_all('loc'), courses_count)
    course_urls = map(lambda x: x.get_text(), rand_courses)

    return course_urls


def format_output_to_xlsx(courses):
    output_array = []
    for course in courses:
        output_array.append([course['title'],
                             course['start_date'],
                             course['language'],
                             course['commitment'],
                             course['rating'],
                             course['uri']])
    return output_array


def save_xlsx(formatted_courses, excel_name):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    for course_row in formatted_courses:
        ws.append(course_row)
    wb.save(excel_name)


def get_args():
    parser = argparse.ArgumentParser(description='this is a coursera random courses grabber.')
    parser.add_argument('-c', '--count',
                        help='How much courses do you want to scrape (default: 5)',
                        required=False,
                        default=5)
    parser.add_argument('-o', '--output',
                        help='Output excel file name (default: courses.xlsx)',
                        required=False,
                        default='courses.xlsx')
    args = parser.parse_args()
    return args


def process_all_courses(courses_count):
    xml_uri = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses = []
    for course_url in get_courses_list(xml_uri, courses_count):
        content = get_course_content(course_url)
        if content is not None:
            courses.append(get_course_info(content, course_url))
    return courses


if __name__ == '__main__':
    args = get_args()
    course_list = process_all_courses(args.count)
    save_xlsx(format_output_to_xlsx(course_list), args.output)
