# GenList.py
# генерируем список POST- запросов  
# каждая запись списка содержит сам запрос и должный ответ сервера
#
#




# генерируем базу
from tinydb import TinyDB, Query, where
import os
from random import randint
import time
from datetime import datetime
import re

#********************************************************************
#----------------------------------------------------------------------------------------------
class Server():
	def __init__(self, namedb):
		self.db = TinyDB(namedb)
		self.fields = dict() # справочник для каждого имениполя и типа список имен шаблонов, в которых эта парочка есть
		db_all = self.db.all()
		for sabl in db_all:
			name = sabl['name']
			for name_field in sabl:
				if name_field == 'name':
					continue
				full_field = (name_field,sabl[name_field])
				if full_field in self.fields:
					self.fields[full_field].append(name)
				else:
					self.fields[full_field] = [name]
#		print(self.fields)
						
#----------------------------------------------------------------------------------------------
	def check_db(self,a):
		print('определили поля')
		print(a,'\n')
		name = dict() # считаем частоту нажождения имени
		for i in a: # смотрим каждое поле запроса
			if not (i in self.fields): # нет такого поля с таким именем в базе
				continue


			for j in self.fields[i]: #для каждого имени шаблона, в котором есть это поле с этим типом считаем количество
				if j in name:
					name[j] += 1
				else:
					name[j] = 1

		b = sorted(name.items(), key = lambda x: x[1], reverse = True)
#		print('список шаблонов')
#		print(b)




		#проверим полноту использования шаблона

		for i in b: # для каждого имени шаблона из списка

			sabl = self.db.search(where('name') == i[0])[0] # найдем этот шаблон
			ok = True
			for j in sabl: #для каждого поля этого шаблона
				if j == 'name':
					continue
				if not ((j,sabl[j]) in a):  # найдено поле шаблона, которого нет в запросе - не наш шаблон
					ok = False
					break
			if ok: # найден шаблон с наибольшей частотой, все поля которого есть в запросе
				return(i[0])


		return(False)
#----------------------------------------------------------------------------------------------
	def post(self, a):
		listDB = list()
		c = a.split('&')
		for i in c:
			xa,xb = i.split('=')
			xb = self.ftype(xb.strip())
			listDB.append((xa.strip(), xb))
		name =  self.check_db(listDB)
		if name:
			return(name)
		otv = '{'
		for i in listDB:
			otv += i[0] + ':' + i[1] + ','
		otv = otv[:len(otv)-1]+'}'
		return (otv)

#----------------------------------------------------------------------------------------------
	def ftype(self,a): # определяем тип данных в строке а
	# проверка на дату
		
		try:
			b = datetime.strptime(a,'%Y-%m-%d')
			return ('date')
		except:
			try:
				b = datetime.strptime(a,'%d.%m.%Y')
				return ('date')
			except:
				pass
	#проверка на телефон

		if re.fullmatch('\+7\d{10}',''.join(a.split(' '))) != None:
			return('phone')

	# проверка на email:

		if re.fullmatch("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",a) != None:
			return('email')


		return('text')
#-------------------------------------------------------------------
	def stop(self):
		self.db.close()
#-------------------------------------------------------------------
	def sea(self,b):
		print(self.db.search(where('name') == b))




