import scrapy
from ..items import ElectricbargainstoresItem
import requests
import os
# from os.path import splitext
# from urllib.parse import urlparse
import mimetypes


class StoreScraperSpider(scrapy.Spider):
    name = 'store_scraper'
    allowed_domains = ['www.electricbargainstores.com']
    start_urls = ['https://www.electricbargainstores.com/brands-s/3361.htm']

    def parse(self, response):

        sub_links = response.xpath('//*[@class="subcategory_link"]/@href').extract()
        for link in sub_links:
            yield response.follow(link, self.parseSubCategory)

    def parseSubCategory(self, response):
        sub_links = response.xpath('//*[@class="subcategory_link"]/@href').extract()
        if sub_links:
            for link in sub_links:
                yield response.follow(link, self.parseSubCategory)
        else:

            product_links = response.xpath('//*[@class="v-product__title productnamecolor colors_productname"]/@href').extract()
            if product_links:
                cat = response.url.rsplit('/', 1)[1]
                cat = cat.rsplit('.', 1)[0]
                yield response.follow(response.url + '?&cat='+cat+'&show=300')
                product_links = response.xpath('//*[@class="v-product__title productnamecolor colors_productname"]/@href').extract()
                for product_link in product_links:
                    yield response.follow(product_link, self.parseProduct)
    

    def parseProduct(self, response):
        product = ElectricbargainstoresItem()
        product['Name'] = response.xpath('//title/text()').extract_first()
        product['ProductCode'] = response.xpath('//*[@class="product_code"]/text()').extract_first()
        product['Price'] = '$'+response.xpath('//*[@itemprop="price"]/text()').extract_first()
        desc = response.xpath('//*[@id="ProductDetail_ProductDetails_div2"]//tr/descendant::*/text()').extract()
        descrip = ""
        for l in desc:
            descrip = descrip + " " + l.strip()
        product['TechSpecs'] = descrip.strip().replace('\n',' ')
        photo_links = response.xpath('//*[@id="altviews"]/a/@href').extract()
        if photo_links:
            for j in range(len(photo_links)):
                if photo_links[j][1]=='/':
                   photo_links[j] = "http://"+photo_links[j][2:]
                if photo_links[j][1]=='v':
                    photo_links[j]= 'https://www.electricbargainstores.com'+photo_links[j]

        else:
            photo_links= response.xpath('//*[@property="og:image"]/@content').extract()
            for j in range(len(photo_links)):
                if photo_links[j][1]=='/':
                   photo_links[j] = "http://"+photo_links[j][2:]
                if photo_links[j][1]=='v':
                    photo_links[j]= 'https://www.electricbargainstores.com'+photo_links[j]
                
        product['ProductPhoto']  = photo_links 
        pdf_links =  response.xpath('//*[(@id = "ProductDetail_TechSpecs_div")]//a/@href').extract()
        for j in range(len(pdf_links)):
                if pdf_links[j][1]=='/':
                   pdf_links[j] = "http://www."+pdf_links[j][2:]
                if pdf_links[j][1]=='v':
                    pdf_links[j]= 'https://www.electricbargainstores.com'+pdf_links[j]
                

        product['PDFlink'] = pdf_links
        dl_links = product['ProductPhoto'] + product['PDFlink']
        paths  = []
        # use your own path for output folder
        dir = r'C:\Users\karti\Desktop\projects\electricbargainstores\electricbargainstores\output'
        os.chdir(dir)
        dir =  product['ProductCode']
        os.mkdir(dir)
        os.chdir(os.getcwd() +'\\'+dir)
        i=1
        for lnk in dl_links:

            r = requests.get(lnk,allow_redirects=True)
            content_type = r.headers['content-type']
            ext = mimetypes.guess_extension(content_type)
            fname = product['ProductCode'] + '-'+ str(i) + ext
            open(fname, 'wb').write(r.content)
            paths.append('output/'+ product['ProductCode']+'/'+fname)
            i=i+1

            
            
  
        product['PhotoPath'] = paths[:len(product['ProductPhoto'])]
        product['PDFPath'] = paths[len(product['ProductPhoto']):]
        product['Link'] = response.url
        yield product
