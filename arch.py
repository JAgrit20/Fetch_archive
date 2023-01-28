
from sqlite3 import Cursor
import psycopg2
import requests
from bs4 import BeautifulSoup
import uuid
import random
import os


from boto3 import session

from botocore.client import Config

ACCESS_ID = 'DO00VHKYNCQZJX6BTCTM'
SECRET_KEY = 'gZHIAtflZjq8QgY30f3IwUMoyIf9s1SduFf14rXlF0c'


def connectSQL(ID,title,comp,url):
		try:
			connection = psycopg2.connect(user="doadmin",
										password="AVNS_rTB-YSzM3_a_wg5QVE2",
										host="dbaas-db-7476650-do-user-13222169-0.b.db.ondigitalocean.com",
										port="25060",
										database="library")
			cursor = connection.cursor()
			postgres_insert_query = """INSERT INTO the_indegenous_backend_book (id,title,description,year,url) VALUES  (%s,%s,%s,%s,%s)"""
			record_to_insert = (ID,title,comp,2022,url)
			cursor.execute(postgres_insert_query, record_to_insert)
			# cursor.execute(postgres_insert_query)

			connection.commit()
			count = cursor.rowcount
			print(count, "Record inserted successfully into mobile table")

		except (Exception, psycopg2.Error) as error:
			print("Failed to insert record into mobile table", error)
		
# connectSQL()

# URL from which pdfs to be downloaded

for i in range(100):
	url = f"https://archive.org/details/books?and%5B%5D=lending___status%3A%22is_readable%22&and%5B%5D=collection%3A%22americana%22&sort=-week&page=5"


	session = session.Session()

	# Requests URL and get response object
	response = requests.get(url,timeout=15) 

	# Parse text obtained
	soup = BeautifulSoup(response.text, 'html.parser')



	# Find all hyperlinks present on webpage
	links = soup.find_all(class_ = "item-ttl C C2")

	i = 0

	# From all links check for pdf link and
	# if present download file
	for link in links:
		
		# print(link)
		try:
			ans = link.find('a')['href']
			print("ans",ans)
			filename = ans.split('/')[-1]
			print("filename",filename)

			comp_url =( "https://archive.org/"+ans)

			# data_type =link.get('data-category')
			response_2 = requests.get(comp_url,timeout=15) 
				# Parse text obtained
			soup = BeautifulSoup(response_2.text, 'html.parser')
			# Find all hyperlinks present on webpage
			links_2 = soup.find_all(class_ = "format-summary download-pill")
			title = soup.find(class_ = "breaker-breaker").text
			print("title",title)
		# except:
		# 	break
			for hit in links_2:
					
					i=i+1
					hit_detail = hit.text.strip()	
					if(hit_detail == "PDF              download"):
							try:
								# print("yes inside",hit['href'])
								
								comp_url =( "https://archive.org"+hit['href'])
								print("comp_url",comp_url)
								response = requests.get(comp_url,timeout=15) 
								path = "books3/"+filename+".pdf"
								name_book = filename+".pdf"
								
								idd = ''.join(str(random.randint(0,10)) for x in range(6))
								print("idd",idd)

								pdf = open("books3/"+name_book, 'wb')
								# print("response.content",response.content)
								pdf.write(response.content)

								pdf.close()
								print("File ", i, " downloaded")
								connectSQL(idd,title,comp_url,f'https://archivebooks.nyc3.digitaloceanspaces.com/{name_book}')

							# # Initiate session
								try:
									
									# client = session.client('s3',
									# 						region_name='nyc3',
									# 						endpoint_url='https://nyc3.digitaloceanspaces.com',
									# 						aws_access_key_id=ACCESS_ID,
									# 						aws_secret_access_key=SECRET_KEY)
															
									# client.upload_file(name)
									cmd = 's3cmd put'+name_book+'s3://archivebooks/'

									os.system(cmd)
									# client.upload_file(path,  # Path to local file
									# 'archivebooks',  # Name of Space
									# name_book)  # Name for remote file
									# connectSQL(idd,title,comp_url,f'https://archivebooks.nyc3.digitaloceanspaces.com/{name_book}')

									print("File ",filename , " uploaded")
								except Exception as ex:
									template = "An exception of type {0} occurred. Arguments:\n{1!r}"
									message = template.format(type(ex).__name__, ex.args)
									print (message)

								
							except Exception as ex:
								template = "An exception of type {0} occurred. Arguments:\n{1!r}"
								message = template.format(type(ex).__name__, ex.args)
								print (message)

		except Exception as ex:
			
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
