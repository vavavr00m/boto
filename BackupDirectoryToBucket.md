#Take directory, Tar it, and backup

# Introduction #

This will take a directory, Tar it, and back the whole thing up to S3


# Details #
```
#!/usr/bin/python
"""
tarToS3 directoryName bucket keyName
if filename is a
"""
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys
import os
import time
import tarfile

def tarToS3(directoryName, s3Bucket, s3Key=None, s3AcctId=None, s3SecretAccess=None ):
	if s3Key==None:
		s3Key='backup.tar.gz'
	else:
		s3Key+='.tar.gz'
	contents = os.listdir(directoryName)
	if s3Key==None:
		s3Key="backup."+str(time.time())+".tar.gx"
		backupFile = "/tmp/"+s3Key
	else:
		backupFile = "/tmp/backup."+str(time.time())+".tar.gx"
	tar = tarfile.open(backupFile, "w:gz")
	for item in contents:
		tar.add(directoryName+'/'+item)
	tar.close()

	if s3SecretAccess==None:
		conn = S3Connection()
	else:
		conn = S3Connection(s3AcctId, s3SecretAccess)

	bucket = conn.get_bucket(s3Bucket)
	k = Key(bucket)
	k.key = s3Key
	k.set_contents_from_filename(backupFile)
```