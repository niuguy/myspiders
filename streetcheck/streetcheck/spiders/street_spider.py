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
            str(pcode) for pcode in pcodes[:1]
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for url in urls:
            time.sleep(0.1)
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        street = Street()
        postcode = response.url.split("/")[-1]
        print(response.url)
        soup = bf(response.text, 'lxml')
        culture_table = soup.find(id='culture').find("table")
        for row in culture_table.find('tbody').find_all('tr'):
            # print(row)
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols[0] == 'Chinese':
                street['street_code'] = postcode
                street['cn_count'] = cols[1]
                self.exporter.export_item(street)

        people_table = soup.find(id='people').find('table')
        total_people = people_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip()
        print(float(total_people))
        ab_people_title = people_table.find('td', {"data-chart-title": "AB"})
        ab_people = ab_people_title.nextSibling.text.strip()
        print(float(ab_people))
