# reboot #

The reboot method of the Instance object provides a way to reboot an EC2 instance.

## Method Description ##

### Name ###
reboot

### Parameters ###
**bold** indicates required parameter
_italics_ indicates an optional parameter

  * none

### Returns ###
Boolean True if successful or False if unsuccessful.

**Examples**
```
>>> rs = connection.get_all_instances()
>>> rs
[Reservation:r-7b57b212, Reservation:r-dd50b5b4, Reservation:r-d450b5bd]
>>> instance = rs[0].instances[0]
>>> instance
Instance:i-75b0571c
>>> instance.reboot()
True
```