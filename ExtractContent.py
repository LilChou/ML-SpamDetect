#!/usr/bin/python
# FileName: Subsampling.py 
# Version 1.0 by Tao Ban, 2010.5.26
# This function extract all the contents, ie subject and first part from the .eml file 
# and store it in a new file with the same name in the dst dir. 

import email.parser 
import os, sys, stat
import shutil
#-------------------------------------------
import re
#-------------------------------------------

def ExtractSubPayload (filename):
	''' Extract the subject and payload from the .eml file.
	
	'''
	if not os.path.exists(filename): # dest path doesnot exist
		print "ERROR: input file does not exist:", filename
		os.exit(1)
	fp = open(filename)
	msg = email.message_from_file(fp)
	payload = msg.get_payload()
	if type(payload) == type(list()) :
		payload = payload[0] # only use the first part of payload
	sub = msg.get('subject')
	sub = str(sub)
	if type(payload) != type('') :
		payload = str(payload)
#-------------------------------------------
	payload = payload.lower()
	start = 0

	if payload.find('<head>') >=0:
		# print("Found HEAD")
		# print(filename)
		start = payload.find('<head>')
		end = payload.find('</head>')
		payload = payload[:start] + payload[(end+7):]
	
	payload = re.sub(r'https?:\/\/.*[\s]*', '', payload, 0, flags=re.MULTILINE)
	payload = re.sub(r'http?:\/\/.*[\s]*', '', payload, 0, flags=re.MULTILINE)
	payload = re.sub(r'<.*?>', '', payload, 0, flags=re.MULTILINE)
	
	if payload.find('Content-Type', 0) >= 0:
		if payload.find('Content-Transfer-Encoding', 0) >= 0:
			start = payload.find('Content-Transfer-Encoding', 0)
		start = payload.find('\n\n', start)
	payload = payload[start:]

	start = 0
	while payload.find('<', start) >= 0:
		start = payload.find('<', start)+1
		end = payload.find('>', start)
		if end != -1:
			payload = payload[:(start-1)] + payload[(end+1):]
		else: break
	# while payload.find('{', start) >= 0:
	# 	start = payload.find('{', start)+1
	# 	end = payload.find('}', start)
	# 	if end != -1:
	# 		payload = payload[:(start-1)] + payload[(end+1):]
	# 	else: break
	
	payload = re.sub(r'>', '', payload, 0, flags=re.MULTILINE)
	# cleanr = re.compile('<.*?>')
	# payload = re.sub(cleanr, '', payload)
#-------------------------------------------
	return sub.lower() + "\n" + payload.lower()

def ExtractBodyFromDir ( srcdir, dstdir ):
	'''Extract the body information from all .eml files in the srcdir and 
	
	save the file to the dstdir with the same name.'''
	if not os.path.exists(dstdir): # dest path doesnot exist
		os.makedirs(dstdir)  
	files = os.listdir(srcdir)
	for file in files:
		srcpath = os.path.join(srcdir, file)
		dstpath = os.path.join(dstdir, file)
		src_info = os.stat(srcpath)
		if stat.S_ISDIR(src_info.st_mode): # for subfolders, recurse
			ExtractBodyFromDir(srcpath, dstpath)
		else:  # copy the file
			body = ExtractSubPayload (srcpath)
			dstfile = open(dstpath, 'w')
			dstfile.write(body)
			dstfile.close()


###################################################################
# main function start here
# srcdir is the directory where the .eml are stored
print 'Input source directory: ' #ask for source and dest dirs
srcdir = raw_input()
if not os.path.exists(srcdir):
	print 'The source directory %s does not exist, exit...' % (srcdir)
	sys.exit()
# dstdir is the directory where the content .eml are stored
print 'Input destination directory: ' #ask for source and dest dirs
dstdir = raw_input()
if not os.path.exists(dstdir):
	print 'The destination directory is newly created.'
	os.makedirs(dstdir)

###################################################################
ExtractBodyFromDir ( srcdir, dstdir ) 

