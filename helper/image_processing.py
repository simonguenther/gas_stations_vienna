from PIL import Image, ImageEnhance 
import urllib
import pytesseract

class ImageProcessing():

    def __init__(self,url):
        self.TMP_DIRECTORY = '/Users/simon/python/gas_station_crawler/tmp/'
        self.ENHANCED =  self.TMP_DIRECTORY+"temp_enhanced.png"
        self.TEMP = self.TMP_DIRECTORY+"temp.png"
        self.URL = url
        print("New Instance with: ", self.URL)
        #self.process()
        
    def get_image_from_url(self):
        urllib.request.urlretrieve(self.URL, self.TEMP)
        print("Image saved as: ", self.TEMP)

    def enhance(self):
        im = Image.open(self.TEMP)
        enhancer = ImageEnhance.Sharpness (im.convert('RGB'))
        enhanced_im = enhancer.enhance(10.0)
        enhanced_im.save(self.ENHANCED)
        print("Image saved as: ", self.ENHANCED)

    def ocr(self):
         # Get Prices From Image
        im = Image.open(self.ENHANCED)
        width, height = im.size
        offset = 40
        pricelist = []
        while(offset + 25 <= height):
            cropped = im.crop((0,offset,width,offset+25))
            name = self.TMP_DIRECTORY+str(offset)+"__.png"
            print(name)
            cropped.save(name)
            offset += 25
            prices = pytesseract.image_to_string(name)
            prices = str(prices).replace("'","").replace("[","").replace("]","").replace(",",".")
            prices = prices.split()

            # len(prices) == EUR
            # len-1 == PRICE
            # 0-(len-1) == GASTYPE

            gastype = " ".join(prices[:-2])
            price = prices[-2]
            pricelist.append((gastype,price))

        return pricelist

    def process(self):
        print("Processing Image")
        self.get_image_from_url()
        self.enhance()
        return self.ocr()
        

      
    
        