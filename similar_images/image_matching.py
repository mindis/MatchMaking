'''
----------------
Pre-requisites
----------------

install python 3

install PIP module -
	sudo apt install python3-pip

install imagehash module- 
	sudo pip3 install imagehash

install Pillow module- 
	sudo pip3 install Pillow

install requests module- 
sudo pip3 install requests

'''

import sys

from PIL import Image
import requests
from io import BytesIO
import imagehash



def match_images(p_img_url1, p_img_url2):
    response1 = requests.get(p_img_url1)
    if response1.status_code!= 200:
    	#return "Argument 1 URL is invalid - "+p_img_url1
    	return response1.content

    #img1 = Image.open(BytesIO(response1.content))
    
    response2 = requests.get(p_img_url2)
    if response2.status_code!= 200:
    	#return "Argument 2 URL is invalid - "+p_img_url2
    	return response2.content
    #i1mg2 = Image.open(BytesIO(response2.content))

    hash_1 = imagehash.phash(Image.open(BytesIO(response1.content)))
    hash_2 = imagehash.phash(Image.open(BytesIO(response2.content)))
    
    val= hash_1 - hash_2
    
    return 1 if val==0 else 0


#img_url1 = "https://storage.googleapis.com/nr-production-api-listing-images/24ecf799d08f3dd220806cb9c8221240.jpeg"
if __name__ == '__main__':
	img_url1 = sys.argv[1]
	img_url2 = sys.argv[2] 
	result = match_images(img_url1,img_url2)
	print(result)


