# -*- coding: utf-8 -*-
import scrapy


class AllcollegesSpider(scrapy.Spider):
    name = 'allcolleges'
    allowed_domains = ['careers360.com']
    start_urls = ['https://engineering.careers360.com/colleges/list-of-engineering-colleges-in-india/']

    def parse(self, response):
        colleges = response.xpath("//div[contains(@class, 'cardBlk')]")
        for college in colleges:
            yield{
                'College_name':college.xpath(".//h4/a/text()").extract_first(),
                'Fees': college.xpath(".//ul[@class='rank'][2]/li[1]/text()").extract_first(),
                'Ownership': college.xpath(".//ul[@class='rank'][1]/li[2]/a/text()").get(),
                'City': college.xpath(".//ul[@class='rank'][1]/li[1]/a[1]/text()").getall(),
                'State': college.xpath(".//ul[@class='rank'][1]/li[1]/a[2]/text()").getall(),
                'Ratings': college.xpath(".//div[@class='rating']/a/span/text()").get(),
                'Exams' :college.xpath(".//ul[contains(@class, 'rank')][2]/li[2]/a/text()").getall(),
                'View all courses' : college.xpath(".//div[@class='course']/span/a[@class='viewAll']/@href").get(),
                'Reviews' : college.xpath(".//ul[@class='rank'][1]/li[3]/a/@href").get()
            }

        #next page
        next_page= response.xpath("//a[@class='next']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback= self.parse)
