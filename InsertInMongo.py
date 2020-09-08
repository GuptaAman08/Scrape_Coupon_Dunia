#!python3
try:
	from pymongo import MongoClient
	from pprint import pprint
except Exception as e:
	raise e

import bs4, requests, datetime, time
from selenium import webdriver
import json

#Activating the selenium module for use in chrome headless browser
#so that the module can run in background

#getting the page as soup module using request and bs4
def getRequestSoup(url):
	return bs4.BeautifulSoup(requests.get(url).text,'html.parser')

#getting the page as soup module using selenium and bs4
def getDriverSoup(url):
	driver.get(url)
	return bs4.BeautifulSoup(driver.page_source, 'html.parser')

def getCode(url, offerId):
	url = url+'?modal=getCodeModal&offer={0}'.format(offerId)
	couponCodePage = getDriverSoup(url)
	return couponCodePage.find(class_= 'code-txt').text

def appendRow(row):
	workSheet.append_row(values=row)
	print('row saved!')

def loadMorePage(url):
	driver.get(url)
	loadMoreButton = driver.find_element_by_class_name('load-more-offers')
	print('Wait while loading all the offer in the page.....', end='')
	while True:
		print('.', end='')
		try:
			loadMoreButton.click()
		except Exception as e:
			break
		time.sleep(2)
	print('\nOffer loaded....')
	return bs4.BeautifulSoup(driver.page_source, 'html.parser')


def getCategory(url):
	offerCategory = ' '.join(url.split('/')[-1].split('-'))
	print('Extracting from  : ' + offerCategory)

	categoryPage = loadMorePage(url)  

	#get the all the offers
	offers = categoryPage.find_all(class_='offer-card-holder')
	for offer in offers:
		#extract the title, store, code, offerDetails
		storeName = offer.find(class_='store-name').text.strip()
		offerTitle = offer.find(class_='offer-title offer-get-code-link').get('data-offer-value')
		print('Extracting the offer : ' + offerTitle)

		offerDetail = []
		for li in offer.find_all('li'):
			offerDetail.append((li.text).strip())
		# offerDetail = '\n'.join(offerDetail)

		offerId = offer.find(class_='get-offer-code').get('data-offer-value')

		print("Offer Id : " + str(offerId))
		#Getting the offer code
		# offerCode = getCode(url, offerId)

		if not offerId:
			offerId = "Not Available"


		row = {
			"StoreName": storeName,
			"OfferTitle": offerTitle,
			"OfferDetail": offerDetail,
			"CouponCode": offerId,
			"OfferCategory": offerCategory
		}

		print('Appending offer {0} to the sheet couponScrapper'.format(offerTitle))
		try:
			collection.insert(row)
			print("record inserted")
		except:
			print("Insertion Failed !!!!!")
			exit(1)

		pprint(row)



def start():
	startTime = datetime.datetime.now()
	
	url = 'https://www.coupondunia.in/categories'
	categoriesPage = getRequestSoup(url)
	
	categoriesUrl = [ 'https://www.coupondunia.in' + category.parent.get('href') for category in categoriesPage.find_all(class_='sub-category')]

	for url in categoriesUrl:
		getCategory(url)
	
	print("Done!")
	endTime = datetime.datetime.now()
	print('Total time taken for scrapping' + str((startTime - endTime).total_seconds()))






try:
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)
except:
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		driver = webdriver.Chrome(options=options)
	except Exception as e:
		raise e


try: 
	conn = MongoClient("mongodb://localhost:27017/")
	db = conn["couponDunia"]
	collection = db["scrapeData"]
except Exception as e:
	print("First Create a database!!")


start()