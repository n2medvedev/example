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
import server

#

if __name__ == '__main__':

	fz = open('zap.txt','r', encoding = "utf8")
	serv = server.Server('base.json')


	a=fz.read()
b= a.split('\n')
for i in b[:-1]:

	zapros,tip,otvet = i.split('---')
	print('\n-------------------------------------------------------------------------')

	print('запрос:', zapros)

	otv_serv = serv.post(zapros)
	print('ожидаемый ответ: ',otvet)
	
	print('тип запроса : ', tip)
	print('ответ    модуля: ',otv_serv )
	rez = (otv_serv == otvet)
	print('результат :',' НЕТ совпадения ' if not rez else ' Совпадение')
	b= ' '
	while True:

		b = input('Имя шаблона : ')
		if b == '':
			break
		print(serv.sea(b))

	
fz.close()

serv.stop()
print('The End')	

#return(0)








