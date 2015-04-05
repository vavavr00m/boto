# Create S3 Connection #

```
from boto.s3 import Connection
connection = Connection()
```

or if you do not have the Open SSL libraries installed with your Python installation, you'll need to use:

```
from boto.s3 import Connection
connection = Connection(is_secure=False)
```