# get\_console\_output #

The get\_console\_output method of the Instance object provides a way to retrieves console output that has been posted for the specified EC2 instance.

## Method Description ##

### Name ###
get\_console\_output

### Parameters ###
**bold** indicates required parameter
_italics_ indicates an optional parameter

  * none

### Returns ###
ConsoleOutput object.

**Examples**
```
>>> rs = connection.get_all_instances()
>>> rs
[Reservation:r-7b57b212, Reservation:r-dd50b5b4, Reservation:r-d450b5bd]
>>> instance = rs[0].instances[0]
>>> instance
Instance:i-75b0571c
>>> output = instance.get_console_output()
>>> output.instance_id
u'i-75b0571c'
>>> output.timestamp
u'2007-02-08T08:16:01.000-08:00'
>>> print output.output
Linux version 2.6.16-xenU (builder@patchbat.amazonsa) (gcc version 4.0.1 20050727 (Red Hat 4.0.1-5)) #1 SMP Thu Oct 26 08:41:26 SAST 2006
BIOS-provided physical RAM map:
 Xen: 0000000000000000 - 000000006a400000 (usable)
980MB HIGHMEM available.
727MB LOWMEM available.
NX (Execute Disable) protection: active
IRQ lockup detection disabled
Built 1 zonelists
...
>>>
```