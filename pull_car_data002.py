# import libraries
import time
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime




def PullSpecificVehicleCarSalesData(url_st):
	
	headers = {'User-Agent': 'Mozilla/5.0'}
	
	print("requesting...")
	r = requests.get(url_st, headers=headers)
	#print(r.text)
	soup = BeautifulSoup(r.text, 'html.parser')
	print("responce recived!")

	print("prasing...")
	specifications = soup.findAll('div', class_= 'features-item')

	for feature in specifications:
		print(feature.find('div', attrs={'class':'features-item-name'}).text)
		print(feature.find('div', attrs={'class':'features-item-value'}).text.replace("\n", "").replace("\r", "").replace("  ", ""))


	



def PullCarSalesData(url_st, make, page_count):
	url_domain = "https://www.carsales.com.au"
	headers = {'User-Agent': 'Mozilla/5.0'}
	
	print("requesting...")
	r = requests.get(url_domain+url_st, headers=headers)
	#print(r.text)
	soup = BeautifulSoup(r.text, 'html.parser')
	cars = soup.findAll(class_= 'listing-item')
	print("responce recived!")

	print("prasing...")
	for car in cars:

		if car.find('h2'):

			car_title = car.find('h2').contents[0]
			car_price = car.find('div', attrs={'class':'price'}).text
			car_att = dict()
			car_link_url = car.find('a').attrs['href']

			
			car_title = car_title.replace("\n", "")
			car_title = car_title.replace("\r", "")
			car_title = car_title.replace("  ", "")

			car_year = car_title[:4]
			car_title = car_title.replace(car_year+" ", "")

			car_make = car_title[:car_title.index(" ",1)]
			car_title = car_title.replace(car_make+" ", "")

			car_model = car_title[:car_title.index(" ",1)]
			car_title = car_title.replace(car_model+" ", "")

		

			features = car.findAll(class_= 'listing-feature')
			for feature in features:
				car_att.update({feature.find('div', attrs={'class':'feature-title'}).text: feature.find('div', attrs={'class':'feature-text'}).text})

			with open('CarSalesData-'+make+'.csv', 'a', newline='') as csv_file:
	 			writer = csv.writer(csv_file)
	 			writer.writerow([car_make, car_model, car_year, car_title, car_price, car_att['Odometer'],car_att['Body'],car_att['Transmission'],car_att['Engine'],url_domain+car_link_url, datetime.now()])
			#print(car_title)
			#print(car_price)
			#print(car_att)

			PullSpecificVehicleCarSalesData(url_domain+car_link_url)


	if soup.find('a', attrs={'title':'Next'}).attrs['href']:
		next_50_link = soup.find('a', attrs={'title':'Next'}).attrs['href']
	else:
		next_50_link = None
	#print(next_50_link)

	pages = soup.findAll('div',attrs={"class":"pagination"})
	for x in pages:
		print("{} ".format(page_count)+x.find('p').text)

	page_number = page_count +1
	
	#sleep to limit the number of request per min so server dosent decide to block
	print("Sleep for 1 secs!")
	time.sleep(1)

	

	return [next_50_link, page_number]





Make = "Holden"
Model = "Captiva"
MinYear = "2013"

#starting_link = "/cars/dealer/private/demo/toyota/camry/?sortby=Year&offset=0&setype=sort&area=Stock&vertical=car&WT.z_srchsrcx=makemodel"

#starting_link = "/cars/results/?limit=24&setype=pagination&q=%28And.%28Or.SiloType.Dealer%20used%20cars._.SiloType.Demo%20and%20near%20new%20cars._.SiloType.Private%20seller%20cars.%29_.Make."+Make+"._.BodyStyle.Sedan._.Service.Carsales._.Year.range%282010..%29.%29&sortby=Year&offset=0&area=Stock&vertical=car&WT.z_srchsrcx=makemodel"




starting_link = "/cars/results/?sortby=Year&limit=50&q=%28And.Service.CARSALES._.%28C.Make."+Make+"._.Model."+Model+".%29_.%28Or.SiloType.Dealer+used+cars._.SiloType.Private+seller+cars._.SiloType.Demo+and+near+new+cars.%29_.Year.range%28"+MinYear+"..%29.%29"
page_count = 0
inprogress = True

nextURL = PullCarSalesData(starting_link, Make, page_count)

while inprogress:
	print("Page : {}".format(page_count))
	
	nextURL = PullCarSalesData(nextURL[0], Make, nextURL[1])
	if nextURL[0] is None:
		inprogress = False
		print("finished!")


#PullSpecificVehicleCarSalesData("https://www.carsales.com.au/cars/details/Holden-Captiva-2018/OAG-AD-16755914/?Cr=0")