# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import FormRequest


class TtMmSpider(scrapy.Spider):
    name = 'tt_mm'
    allowed_domains = ['betmarathon.com']
    start_urls = []
    list_range = list(range(1, 46))
    for i in list_range:
        x = 'https://www.betmarathon.com/en/popular/Football?page={}&pageAction=getPage&_'.format(i)
        start_urls.append(x)


    def parse(self, response):
        has_next_page = 'hasNextPage'
        req = response.text
        result = re.search(has_next_page, req)
        
        if result:
            _id = response.xpath("//div/@data-event-treeid").extract()
            for x in _id:
                x = x.replace('"', '')
                x = x.replace('\\', '')
        
                
                yield FormRequest(url='https://www.betmarathon.com/en/markets.htm', formdata={
                    'treeId': x,
                    'siteStyle': 'SIMPLE'
                }, callback=self.parse_odds)



    def parse_odds(self, response):
        home = response.xpath("//span[contains(@data-selection-key, 'Match_Result.1')]/parent::div/preceding-sibling::div/text()").extract_first()
        home = home.replace('To Win', '')
        home = home.strip()
        away = response.xpath("//span[contains(@data-selection-key, 'Match_Result.3')]/parent::div/preceding-sibling::div/text()").extract_first()
        away = away.replace('To Win', '')
        away = away.strip()



        yield {
            'home': home,
            'away': away,
            'F1': response.xpath("//span[contains(@data-selection-key, 'Match_Result.1')]/text()").extract_first(),
            'Fx': response.xpath("//span[contains(@data-selection-key, 'Match_Result.draw')]/text()").extract_first(),
            'F2': response.xpath("//span[contains(@data-selection-key, 'Match_Result.3')]/text()").extract_first(),
            'under2_5': response.xpath("//div[contains(@data-mutable-id, 'MG1_-569792649')]//span[contains(@data-selection-key, 'Under_2.5')]/text()").extract_first(),
            'over2_5': response.xpath("//div[contains(@data-mutable-id, 'MG1_-569792649')]//span[contains(@data-selection-key, 'Over_2.5')]/text()").extract_first(),
            'GM': response.xpath("//span[contains(@data-selection-key, 'First_Team_To_Score.yes')]/text()").extract_first(),
            'OM': response.xpath("//span[contains(@data-selection-key, 'Second_Team_To_Score.yes')]/text()").extract_first(),
            'GMPr1': response.xpath("//span[contains(@data-selection-key, 'First_Team_To_Score_-_1st_Half.yes')]/text()").extract_first(),
            'OMPr1': response.xpath("//span[contains(@data-selection-key, 'Second_Team_To_Score_-_1st_Half.yes')]/text()").extract_first(),
            'GMPr2': response.xpath("//span[contains(@data-selection-key, 'Total_Goals_(First_Team)_-_1st_Half0.Over_1.5')]/text()").extract_first(),
            'OMPr2': response.xpath("//span[contains(@data-selection-key, 'Total_Goals_(Second_Team)_-_1st_Half0.Over_1.5')]/text()").extract_first(),
            'GMDr1': response.xpath("//span[contains(@data-selection-key, 'First_Team_To_Score_-_2nd_Half.yes')]/text()").extract_first(),
            'OMDr1': response.xpath("//span[contains(@data-selection-key, 'Second_Team_To_Score_-_2nd_Half.yes')]/text()").extract_first(),
            'GMDr2': response.xpath("//span[contains(@data-selection-key, 'Total_Goals_(First_Team)_-_2nd_Half0.Over_1.5')]/text()").extract_first(),
            'OMDr2': response.xpath("//span[contains(@data-selection-key, 'Total_Goals_(Second_Team)_-_2nd_Half0.Over_1.5')]/text()").extract_first(),          
        }



