import scrapy
import re
import json
from urllib.parse import urlparse


class Content(scrapy.Spider):
    name = 'content'

    PRIORITY_PATHS = {
        'about', 'o-nas', 'o-firmie', 'kontakt', 'contact',
        'oferta', 'offer', 'uslugi', 'services', 'produkty',
        'products', 'team', 'zespol', 'cennik', 'pricing',
    }
    MAX_PAGES = 10

    def __init__(self, url=None, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domain = urlparse(url).netloc
        self.visited = set()

    def parse(self, response):
        if response.url in self.visited:
            return
        self.visited.add(response.url)

        yield {
            'page': response.url,
            # TODO: dodac pobieranie obrazow - uzyc ImagesPipeline + metoda extract_images()
            # potrzebne klucze wুitem: 'image_urls' (lista URL) i 'images' (wynik pipeline)
            'meta_data': self.meta_data(response),
            'schema_org': self.extract_schema_org(response),
            'content': self.get_text(response),
            'contact': self.extract_contact(response),
            'social_links': self.extract_social_links(response),
        }

        if len(self.visited) >= self.MAX_PAGES:
            return

        for href in response.css('a::attr(href)').getall():
            url = response.urljoin(href)
            parsed = urlparse(url)
            if parsed.netloc != self.allowed_domain or url in self.visited:
                continue
            path_parts = set(parsed.path.lower().strip('/').split('/'))
            if path_parts & self.PRIORITY_PATHS:
                yield response.follow(url, callback=self.parse)

    def meta_data(self, response):
        return {
            'title': response.css('title::text').get(),
            'description': response.css('meta[name="description"]::attr(content)').getall(),
            'keywords': response.css('meta[name="keywords"]::attr(content)').getall(),
            'og_title': response.css('meta[property="og:title"]::attr(content)').getall(),
            'og_description': response.css('meta[property="og:description"]::attr(content)').getall(),
            'og_image': response.css('meta[property="og:image"]::attr(content)').getall(),
            'og_url': response.css('meta[property="og:url"]::attr(content)').getall(),
            'canonical': response.css('link[rel="canonical"]::attr(href)').get(),
            'lang': response.css('html::attr(lang)').get(),
            'robots': response.css('meta[name="robots"]::attr(content)').get(),
        }

    def get_text(self, response):
        return {
            'h1': response.css('h1::text').getall(),
            'h2': response.css('h2::text').getall(),
            'h3': response.css('h3::text').getall(),
            'p': response.css('p::text').getall(),
            'a': response.css('a::text').getall(),
            'li': response.css('li::text').getall(),
            'nav': response.css('nav a::text').getall(),
            'footer': response.css('footer::text').getall(),
            'address': response.css('address::text').getall(),
        }

    def extract_schema_org(self, response):
        schemas = []
        for script in response.css('script[type="application/ld+json"]::text').getall():
            try:
                schemas.append(json.loads(script))
            except json.JSONDecodeError:
                pass
        return schemas

    def extract_contact(self, response):
        text = response.text
        emails = list(set(re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)))
        phones = list(set(re.findall(r'(?<!\d)(?:\+48[\s-]?)?(?:\d{3}[\s-]?\d{3}[\s-]?\d{3}|\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})(?!\d)', text)))
        return {'emails': emails, 'phones': phones}

    def extract_social_links(self, response):
        social_domains = [
            'facebook.com', 'instagram.com', 'linkedin.com',
            'twitter.com', 'x.com', 'youtube.com', 'tiktok.com',
        ]
        links = {}
        for href in response.css('a::attr(href)').getall():
            for domain in social_domains:
                if domain in href:
                    name = domain.split('.')[0]
                    links[name] = href
        return links
