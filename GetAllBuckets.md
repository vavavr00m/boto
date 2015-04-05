# Get All Buckets #

```
from boto.s3 import Connection
connection = Connection()
buckets = connection.get_all_buckets()  # returns a list of bucket objects
```