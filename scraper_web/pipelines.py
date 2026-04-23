from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse


class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        page_url = item.get('page', '') if item else ''
        domain = urlparse(page_url).netloc
        folder_name = domain.replace('.', '_').replace(':', '_')
        image_name = request.url.split('?')[0].split('/')[-1]
        return f'{folder_name}/{image_name}'

    def convert_image(self, image, size=None, *, response_body):
        if size is None:
            return image, response_body
        return super().convert_image(image, size, response_body=response_body)
