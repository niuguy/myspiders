import scrapy
import time
from bs4 import BeautifulSoup as bf
import pandas as pd
from streetcheck.items import Street
from scrapy.exporters import CsvItemExporter


class StreetSpider(scrapy.Spider):
    name = "street"

    def __init__(self, kw='', pn=10, **kwargs):

        file_name = 'streetcheck/resources/streets.csv'
        self.file = open(file_name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def start_requests(self):
        codes_df = pd.read_csv('streetcheck/resources/first_postcodes.csv')
        pcodes = codes_df['first_postcode'].to_list()
        urls = [
            'https://www.streetcheck.co.uk/postcodedistrict/' +
            str(pcode) for pcode in pcodes
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for url in urls:
            time.sleep(0.1)
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    # def parse(self, response):
    #     street = Street()
    #     postcode = response.url.split("/")[-1]
    #     print(response.url)
    #     soup = bf(response.text, 'lxml')
    #     culture_table = soup.find(id='culture').find("table")
    #     for row in culture_table.find('tbody').find_all('tr'):
    #         # print(row)
    #         cols = row.find_all('td')
    #         cols = [ele.text.strip() for ele in cols]
    #         if cols[0] == 'Chinese':
    #             street['street_code'] = postcode
    #             street['cn_count'] = cols[1]
    #             self.exporter.export_item(street)

    #     people_table = soup.find(id='people').find('table')
    #     total_people = people_table.find('tfoot').find(
    #         'tr').find_all('td')[1].text.strip()
    #     print(float(total_people))
    #     ab_people_title = people_table.find('td', {"data-chart-title": "AB"})
    #     ab_people = ab_people_title.nextSibling.text.strip()
    #     print(float(ab_people))

    def parse(self, response):
        street = Street()
        postcode = response.url.split("/")[-1]
        street['street_code'] = postcode
        print(response.url)
        soup = bf(response.text, 'lxml')

        culture_table = soup.find(id='culture').find("table")
        total_ethics = float(culture_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip())
        for row in culture_table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols[0] == 'Chinese':
                street['cn_count'] = cols[1]
                street['cn_rate'] = round(float(cols[1])/total_ethics, 3)

            if cols[0] == 'White':
                street['white_rate'] = round(float(cols[1])/total_ethics, 3)
                # self.exporter.export_item(street)

        people_table = soup.find(id='people').find('table')
        total_people = float(people_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip())
        ab_people = float(people_table.find(
            'td', {"data-chart-title": "AB"})
            .parent
            .findAll('td')[1].text.strip())
        street['ab_people_rate'] = round(ab_people/total_people, 3)

        employ_table = soup.find(id='employment').find('table')
        total_economic = float(employ_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip())
        fe_people = float(employ_table.find('tbody')
                          .find_all('tr')[0].find_all('td')[1].text.strip())
        street['fulltime_rate'] = round(fe_people/total_economic, 3)
        # ab_people = ab_people_title.nextSibling.text.strip()
        # print(float(ab_people))
        print(street)
        self.exporter.export_item(street)
        yield street
