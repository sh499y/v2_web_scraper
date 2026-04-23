import scrapy


class Content(scrapy.Spider):
    name = 'content'

    #Dynamiczne wybieranie url
    def __init__(self, url=None, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        meta = self.meta_data(response)
        text = self.get_text(response)
        images = self.extract_images(response)

        yield {
            'page': response.url,
            'image_urls': images,
            'total_images': len(images),
            'meta_data': meta,
            'content': text
        }

    #Ekstrakcja Meta danych
    def meta_data(self, response):
        return {
            'title': response.css('title::text').get(),
            'description': response.css('meta[name="description"]::attr(content)').getall(),
            'keywords': response.css('meta[name="keywords"]::attr(content)').getall(),
            'og_title': response.css('meta[property="og:title"]::attr(content)').getall(),
        }

    #Eksrakcja Tekstu
    def get_text(self, response):
        return {
            'h1': response.css('h1::text').get(),
            'h2': response.css('h2::text').get(),
            'a': response.css('a::text').get(),
            'p': response.css('p::text').getall(),
        }

    #Ekstrakcja Obrazow
    def extract_images(self, response):
        # Zbierz wszystkie URLe obrazów
        image_urls = response.css('img::attr(src)').getall()

        # Konwertuj relatywne URLe na absolutne
        image_urls = [response.urljoin(url) for url in image_urls]
        return image_urls
