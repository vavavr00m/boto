# run #

The run method of the Instance object provides a way to reboot an EC2 instance.

## Method Description ##
[ec2 Tutorial](http://boto.googlecode.com/svn/trunk/doc/ec2-tut.txt)

### Name ###
run

### Parameters ###
**bold** indicates required parameter
_italics_ indicates an optional parameter

  * none

### Returns ###
Reservation of instances

**Examples**
```
>>> import boto
>>> ec2_conn = boto.connect_ec2(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
>>> images = ec2_conn.get_all_images(image_ids=['ami-b111f4d8'])
>>> images[0]
Image:ami-b111f4d8
>>> reservation = images[0].run(1,1, 'yourKeyPair')
>>> reservation
Reservation:r-c2dc2fab

```