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
import re

#********************************************************************
def gen_nogut(a,fil,db):
	
	second = True

	while second:
		dubl_a =[a[0]] # получим список сгенерированных  полей
		real_filds_name = list()
		rez = ''
		otv = '{'
		rez_err = ''
		pref = ''
		j = 1

		while j <= len(a[1:]):
			if (randint(1,10) > 5) and (j>1): # пропустим запись
				j+=1
				continue
			if (randint(1,10) > 4) and (j>1): #вставка лишней записи
				xa,xb = gen_el(fil) # получим имя поля и тип данных
				j = j-1
			else:
				xa = a[j][0]
				xb = a[j][1]

			if (randint(1,10) > 7): # заменим тип
				xb = fil[randint(0,len(fil)-1)]['name'][0]
				
			if (randint(1,10) > 7): # заменим поле
				xa,t = gen_el(fil)
				

			rez +=pref+xa+'='
			k = randint(0,1)
			if xb == 'text':
				rz = gen_text(' ',fil)
			elif xb == 'date':
				rz = gen_date(n = k)
			elif xb == 'phone':
				rz = gen_phone(n = k)
			elif xb == 'email':
				rz = gen_email(n = k)

			if k == 1:
				xb = 'text'

			pref = '&'
			rez +=rz
			otv += xa+':' + xb + ','
			
			

			if xa in real_filds_name: # если имя есть в списке
				continue
			j += 1
			dubl_a.append((xa,xb))
			real_filds_name.append(xa)
		second = check_db(db,dubl_a)
	
	return(rez + '--- error ---'+ otv[:len(otv) -1]+'}')
#*********************************************************************************************************

def gen_gut(a,fil):


	real_filds_name = list()
	for xa,xb in a[1:] :
		real_filds_name.append(xa)
	rez = ''
	
	pref = ''
	j = 1
	pos = 'direct'
	while j <= len(a[1:]):
		xa,xb = a[j]
		if randint(1,10) > 8: #вставка лишней записи
			while xa in real_filds_name: # получить имя поля, которого нет в списке
				xa,xb= gen_el(fil) # получим имя поля и тип данных
			real_filds_name.append(xa)
			pos = 'add'
		else:
			j +=1
					
		rez +=pref+xa+'='
		if xb == 'text':
			rz = gen_text(' ',fil)
		elif xb == 'date':
			rz = gen_date()
		elif xb == 'phone':
			rz = gen_phone()
		elif xb == 'email':
			rz = gen_email()

		pref = '&'
		rez +=rz
		
		
	return(rez + '---' + pos +'---'+a[0][1])
#*****************************************************
def gen_el(fil): # получим имя поля и тип данных
		b = fil[randint(0,len(fil)-1)]['name'] # list of words for names fild
		fild = b[0]
		fname = b[randint(1, len(fil)-1)]
		t= fild + '_' + fname
		return(t,fild)
#********************************************************************
def gen_text(post,fil):
	r = ''
	pst = ''
	l = randint(2,10)
	for i in range(l):
		a= fil[randint(0, len(fil)-1)] ['error']
		r += pst + a[randint(0, len(a)-1)]
		pst = post
	return(r)
#********************************************************************
def gen_date(n=0):
	sbl = ['%Y-%m-%d','%d.%m.%Y']
	if n == 0:
		forma = sbl[randint(0,1)]
	else:
		forma = '%m.%d.%y'
	
	a=time.time()-randint(1,30)*3600*24
	
	return(time.strftime(forma,time.gmtime(a)))

#********************************************************************
def gen_phone(n=0):
	m = '' 
	if n == 1:
		m = 'asdfghjklzxcvbnm'[randint(0,15)]
		
	return('+7 '+yy(3)+ ' ' + yy(3) + m + ' ' + yy(2) + ' ' + yy(2) )

#********************************************************************
def yy(x):
	return(str(randint(1,10**x-1)).zfill(x))
#********************************************************************
def gen_name_adr(l=0,k=0):
	er = '~`?><}{][$%^:;/\\'
	find_err = False
	b = '"-_+.'+"'"
	
	r=''
	if l == 0:
		c = randint(2,11)
	elif k== 0 :
		c = randint(2,6)
	else:
		c = randint(2,10)
	while (not find_err) : # будем генерировать пока не получим ошибочный адрес
		i = 1
		r=''
		while i< c:
			a= chr(randint(39,122))
			if ((a in b) and (len(r) >0) and (l == 0)) or ((a>='a') and (a<='z')) or ((a>='A') and (a<='Z')):
				i +=1
				r +=a
				if (k > 0) and (randint(1,10) > 8):
					r += er[randint(0,len(er)-1)] + r
					find_err = True
		if k == 0:
			find_err = True

	return(r)
#********************************************************************
def gen_email(n = 0):
	name = ' '
	while re.fullmatch("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",name) == None:
		a= gen_name_adr(k = n)
		b = gen_name_adr(k = n)
		c= gen_name_adr(l=2,k =n)
		name = a + '@' + b + '.' + c
		if n > 0:
			break
	return(name)		
#********************************************************************

def genel(fil,name,db):
	q = Query()

	element1 = []
	# generating name
	while True: 
		
		
		name_name = name[randint(0,len(name)-1)]+'-'+name[randint(0,len(name)-1)]
		if len(db.search(q.name == name_name)) == 0:
			break
		
	
	element1.append(('name',name_name))
	## generating count filds
	count_fields = randint(2,6)
	j = 0
	temp_list = list()
	while j<count_fields:
		t,fild = gen_el(fil) # получим имя поля и тип данных
		if t in temp_list:
			continue
		j += 1
		temp_list.append(t)
		element1.append((t,fild)) 


	return(element1)
#***************************************************************
	# проверка на уникальность набора
def check_db(db,a):
	b = db.search(where(a[1][0]) == a[1][1]) #создадим список записе(справочников), у которых есть первый, кроме имени, элемент 
	
	for i in b: #   берем каждый справочник из списка
		if len(i) != len(a): #не совпадает количество элементов
			continue
		eq = True
		for j in a[2::] :
			try:
				if i[j[0]] == j[1]: #есть такой элемент(имя поля есть в шаблоне и значение этого поля совпадает со значением списка)
					continue
			except:
				pass
			eq = False # хотя бы один элемент не совпадает
			break
		if eq: # нашелся справочник, который совпадает по набору со сгенерированным набором
			return(i['name'])
	return(False)
#***********************************************************************	

def gen_err(listBase,fil):
	#не хватает правильного поля - неправильный один из типов - неправильное имя поля    
	type_error = [[]]
	return()





if __name__ == '__main__':
	data = {'name': ['date', 'create','born', 'validation','verification','death'],'error':['aaa','drop','del','form'],'type':['DD.MM.YYYY','YYYY-MM-DD'], 'reg':[]} 
	tel =  {'name':['phone','personal','office','mobile','work','home'],'error': ['form','group','match','hh'],'type':['+7 xxx xxx xx xx']}
	email = {'name':['email','personal','office','mobile','work','home'],'error': ['form','group','match','hh'],'type':['x*@x*.ru']}
	name = ['name','Form','My','Order','personal','office','mobile','work','home','in','out']
	text = {'name':['text','name','comment','progeny','address','ancestors'], 'error':['Raya','Butiful','Graf','Markiz','King','Czar','Vova','best','Nikola','ok','jonior','men','Katya']}

	fz = open('zap.txt','w', encoding = "utf8")
	os.remove('base.json')
	db = TinyDB('base.json')
	listBase = list()
	j = 0
	i = 0
	fil = [data,tel,email,text]
	# герерируем базу
	while i<100:
		a= genel(fil,name,db)
		
		n = check_db(db,a)
		if n: #eсть такой набор
			j += 1
			print(n,j)
			continue
		db.insert(dict(a))
		listBase.append(a)

		i += 1

	# генерируем запросы
	print('записей в базе ',len(listBase))

	i=[0,0]
	for a in listBase:

		if randint(1,10)>6: # генерируем правильную запись
			fz.write(gen_gut(a,fil)+'\n')
			i[0] +=1
		if randint(1,10)>6: # генерируем неправильную запись
			fz.write(gen_nogut(a,fil,db)+'\n')
			i[1] +=1

		
	print('сгенерировано запросов :', end = ' ')
	print('правильных',i[0],'   неправильных',i[1])


	db.close()
	fz.close()
	print('The End')	

#return(0)








