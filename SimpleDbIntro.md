# Introduction #

This page will give you a quick overview of the current boto SimpleDB library.  Before reading this it would probably be a good idea to check out these resources from Amazon:

  * [SimpleDB Developer's Guide](http://docs.amazonwebservices.com/AmazonSimpleDB/2007-11-07/DeveloperGuide/)
  * [SimpleDB Getting Started Guide](http://docs.amazonwebservices.com/AmazonSimpleDB/2007-11-07/GettingStartedGuide/)

# Let's Get Started #

To begin with SimpleDB, you need to create a connection to the SimpleDB service just like you do with all other boto interfaces.

```
>>> import boto
>>> sdb = boto.connect_sdb('<your aws access key>', '<your aws secret key'>)
```

## Create a Domain ##

Once you have a connection, you can create a new domain.  According to the AWS docs:

> All Amazon SimpleDB information is stored in domains. Domains are similar to tables that contain similar data. You can execute queries against a domain, but cannot execute joins between domains.

To create a new domain:

```
>>> domain = sdb.create_domain('my_domain')
```

To list the all of the items in the domain, you could do this:

```
>>> for item in domain:
...     print item.name
... 
```

Of course, this is a brand new domain so there are no items contained within it yet.  However, the above construct would cycle through **ALL** items within the domain.  The paging of results is handled automatically by boto via a Python generator function.

## Adding Items to the Domain ##

To create a new item within our new domain:

```
>>> item = domain.new_item('item1')
```

Because this item has no attribute name/value pairs associated with it, it really doesn't exist yet in SimpleDB.  It won't get persisted to SimpleDB until we call the .save() method on it.  But first, let's add some key/value pairs to it:

```
>>> item['key1'] = 'value1'
>>> item['key2'] = 'value2'
```

In addition to storing scalar string values, you can also store lists of values like this:

```
>>> item['key3'] = ['one', 'two', 'three']
```

Or you can append values to existing attribute names using the add\_value method like this:

```
>>> item.add_value('key2', 'value2_1')
```

With add\_value, the value you add is to the attribute name ('key2') in addition to any existing values.  So, it's like appending to a list.

Time to save it to SimpleDB:

```
>>> item.save()
```

## Getting Items from the Domain ##
retrievedItem
If we now go and ask the domain object to retrieve the Item called 'item1' from SimpleDB, we can see our values have, in fact, been stored:

```
>>> retrievedItem = domain.get_item('item1')
>>> retrievedItem
{u'key2': [u'value2', u'value2_1'], u'key1': u'value1', 'u'key3': [u'one', u'two', u'three']}
>>> 
```

If we now go back and iterate over the items in the domain, we can see our new item, 'item1' show up.

```
>>> for item in domain:
...     print item.name
... 
item1
```

Note that item object returned by the query resultset iterator is a live Item object.  When returned by the resultset object, it contains only the name of the item because SimpleDB does not allow attribute values to be returned as part of a query, only item names.  However, if you access an attribute of the Item object, it will automatically retrieve all attributes for the item from SimpleDB.  So, in our above example we could also do something like this:

```
>>> for item in domain:
...     print item.name, item['key1']
...
item1, value1
```

## Querying SimpleDB ##

We can also query our domain, like this:

```
>>> rs = domain.query("['key1' = 'value1']")
>>> for item in rs:
...     print item.name
... 
item1
>>> 
```

Here again, the paging of search results will be handled transparently by boto.  If there are 10,000 items matching the query you will eventually pull all of those results over (unless SimpleDB cuts you off for taking up too much compute time!).

If you already created your domain, and you want to reconnect to it:

```
>>> retrievedDomain = sdb.get_domain('my_domain')
>>> for item in retrievedDomain:
...     print item.name
... 
item1
>>> 
```

More examples and good stuff to follow.  Enjoy and don't be shy with those comments!

Mitch