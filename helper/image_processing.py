from PIL import Image, ImageEnhance 
import urllib
import pytesseract
import time
import logging

class ImageProcessing():

    def __init__(self,url):
        logging.basicConfig(filename='error.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        self.TMP_DIRECTORY = '/Users/simon/python/gas_station_crawler/tmp/'
        self.ENHANCED =  self.TMP_DIRECTORY+"temp_enhanced.png"
        self.TEMP = self.TMP_DIRECTORY+"temp.png"
        self.ERROR_DIRECTORY = '/Users/simon/python/gas_station_crawler/error/'
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

    def transform(self, _in):
        #isascii = lambda s: len(s) == len(s.encode())
        #print("is Ascii? ", isascii(_in))

        if("Wasser" in _in):
            print("Wasserstoff detected")
            _in = "Wasserstoff"
        elif ("Maxx" in _in) and ("Super100" in _in):
            print("MaxxMotion Super 100 plus detected")
            _in = "MaxxMotion Super 100plus"
        elif ("Maxx" in _in) and ("Diesel" in _in):
            _in = "MaxxMotion Diesel"
            print("MaxxMotion Diesel detected")
        else:
            print("No unicode found, keeping string")
        return _in
        
    def ocr(self):
         # Get Prices From Image
        im = Image.open(self.ENHANCED)
        width, height = im.size
        offset = 40
        pricelist = []
        while(offset + 25 <= height):
            cropped = im.crop((0,offset,width,offset+25))
            name = self.TMP_DIRECTORY+str(offset)+"__.png"
            print("Tempfile saved to: ", name)
            cropped.save(name)
            offset += 25
            prices = pytesseract.image_to_string(name)
            print("Prices after OCR: ", prices)
            prices = str(prices).replace("'","").replace("[","").replace("]","").replace(",",".").replace("EUR","").replace("/100g","")
            prices = prices.split()
            print("Prices after processing: ", prices)

            # len(prices) == EUR
            # len-1 == PRICE
            # 0-(len-1) == GASTYPE

            if(len(prices) >= 2):
                
                gastype = " ".join(prices[:-1])
                gastype = self.transform(gastype)

                price = prices[-1]
                pricelist.append((gastype,price))
            else:
                print("Not enough price splits to continue")
                error_id = str(int(time.time()))
                error_path = self.ERROR_DIRECTORY+error_id+".png"
                logging.error("ERROR with: %s", error_id)
                im.save(error_path)

        return pricelist

    def process(self):
        print("Processing Image")
        self.get_image_from_url()
        self.enhance()
        return self.ocr()
        

      
    
        