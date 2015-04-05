# set\_as\_logging\_target #

The set\_as\_logging\_target method of the Bucket object provides a way to quickly set the correct permissions on a bucket to allow it to be a logging target for another bucket (see [Server Access Logging](http://docs.amazonwebservices.com/AmazonS3/2006-03-01/ServerLogs.html) for more details).  This logging provides web server style log files documenting all interactions with the bucket.

## Method Description ##

### Name ###
set\_as\_logging\_target

### Parameters ###
**bold** indicates required parameter
_italics_ indicates an optional parameter


**Examples**
```
>>> b1 = connection.get_bucket('my_public_bucket')
>>> b2 = connection.get_bucket('my_logging_bucket')
>>> b2.set_as_logging_target()
>>> b1.enable_logging(b2)
>>>
```

This example would enable logging on Bucket b1, sending the log files for b1 to Bucket b2.  See EnableLogging for more information about the enable\_logging method.