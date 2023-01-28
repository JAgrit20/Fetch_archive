
from sqlite3 import Cursor
import psycopg2
import requests
from bs4 import BeautifulSoup
import uuid
import random
import os

def connectSQL():
		try:
			connection = psycopg2.connect(user="doadmin",
										password="AVNS_rTB-YSzM3_a_wg5QVE2",
										host="dbaas-db-7476650-do-user-13222169-0.b.db.ondigitalocean.com",
										port="25060",
										database="library")
			cursor = connection.cursor()
			# postgres_insert_query = """INSERT INTO the_indegenous_backend_book (id,title,description,year,url) VALUES  (%s,%s,%s,%s,%s)"""
			postgres_insert_query = """SELECT * FROM the_indegenous_backend_book"""
			# record_to_insert = (ID,title,comp,2022,url)
			# cursor.execute(postgres_insert_query)

			cursor.execute(postgres_insert_query)
			connection.commit()
			results = cursor.fetchall()
			# results = cursor.fetchall()
			count = cursor.rowcount
			print(results)
			print(count, "Record inserted successfully into mobile table")

		except (Exception, psycopg2.Error) as error:
			print("Failed to insert record into mobile table", error)

connectSQL()
