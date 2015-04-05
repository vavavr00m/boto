# enable\_logging #

The enable\_logging method of the Bucket object provides a way to enable [Server Access Logging](http://docs.amazonwebservices.com/AmazonS3/2006-03-01/ServerLogs.html) on an S3 bucket.  This logging provides web server style log files documenting all interactions with the bucket.

## Method Description ##

### Name ###
enable\_logging

### Parameters ###
**bold** indicates required parameter
_italics_ indicates an optional parameter

  * **target\_bucket** - the bucket to which logging files will be written
  * _target\_prefix_ - a prefix for the keys that the delivered log files will be stored under

**Examples**
```
>>> b1 = connection.get_bucket('my_public_bucket')
>>> b2 = connection.get_bucket('my_logging_bucket')
>>> b1.enable_logging(b2)
>>>
```

This example would enable logging on Bucket b1, sending the log files for b1 to Bucket b2.  See SetAsLoggingTarget for information about how to set the permissions on the target bucket to allow log messages to be written.