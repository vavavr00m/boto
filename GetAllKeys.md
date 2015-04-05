# Introduction #

Shows an example on how to get all the keys and print the name of each key


# Details #
```
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys

conn = S3Connection('____________________', '________________________________________')
bucket = conn.get_bucket('bucketname')

rs = bucket.list()

for key in rs:
   print key.name
```

If you have a directory called "FamilyPhotos" and only want pictures from that directory you can use the prefix parameter.  This is very useful when you have a very large number of keys.

```
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys

conn = S3Connection('____________________', '________________________________________')
bucket = conn.get_bucket('bucketname')

rs = bucket.list("FamilyPhotos")

for key in rs:
   print key.name
```