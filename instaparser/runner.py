from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from instaparser import settings
from instaparser.spiders.instagramcom import InstagramcomSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramcomSpider)

    process.start()
