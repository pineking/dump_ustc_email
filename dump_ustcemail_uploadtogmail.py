#!/usr/bin/python


import imaplib
from pprint import pprint
import os
import email

def mkdirs(path):
 	if not os.path.exists(path):
 		os.makedirs(path)

def saveeml(c,dir):

	#make dir in local disk
	mkdirs(dir)
	
	print 'dump email to dir: '+dir
	c.select(dir)
	typ,data = c.search(None, 'ALL')


	total = len(data[0].split())

	for num in data[0].split():
		print "\r%s/%d"%(num,total),
		typ, data = c.fetch(num,'(RFC822)')
		f = open(dir+'/'+str(num)+'.eml','w')
		print >> f,data[0][1]
		f.close()


def uploademl(c,dir,label='ustc'):
	#upload
	print 'upload email from dir: '+dir+' to '+label

	#create label in your gmail
	c.create(label)
	for filename in os.listdir(dir):
		print "\r", filename,
		raw_eml = file(dir+'/'+filename).read()
		msg = email.message_from_string(raw_eml)
		date = email.utils.parsedate(msg['Date'])
		c.append(label, None, date, raw_eml)


	#mark as read
	c.select(label)
	typ,data = c.search(None,'Unseen')
	c.store(data[0].replace(' ',','),'+FLAGS','\Seen')


if __name__ == '__main__':
	ustcemailname = 'XXX@mail.ustc.edu.cn'
	ustcemailpasswd = 'your ustc email passwd'
	gmailname = 'XXXXX@gmail.com'
	gmailpasswd = 'your gmail passwd'

	print 'login ustc email: ',ustcemailname
	c1 = imaplib.IMAP4('202.38.64.8')
	c1.login(ustcemailname,ustcemailpasswd)

	typ, data = c1.list()
	print 'Response code:', typ
	print 'Response: '
	pprint(data)

	print 'login gmail: ',gmailname
	c2 = imaplib.IMAP4_SSL('imap.gmail.com')
	c2.login(gmailname,gmailpasswd)


	#run 
	saveeml(c1,'INBOX')
	uploademl(c2,'INBOX','ustc')

	c1.logout()
	c2.logout()