# Introduction #

This example shows how to get a single key from a bucket and then write that key to a file.


# Details #
```
from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection('____________________', '________________________________________')
bucket = conn.get_bucket('bucketname')
key = bucket.get_key("picture.jpg")
fp = open ("picture.jpg", "w")
key.get_file (fp)
```