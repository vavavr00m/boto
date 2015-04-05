# Introduction #

Two situations have arisen lately to inspire this extension functionality.

The first is the new 20080101 release of the SQS API.  This is a significantly new API that not only changes basic SQS functionality but also brings with it a whole new pricing model.  Unfortunately, the new API also loses a couple of key features that some boto users are relying such as grants and message visibility.  Amazon has agreed to support both API's for an extended period of time so it makes sense that boto should also support both API's.

In addition, the S3 service introduced bucket locality in late 2007.  This allows users to create buckets in specific locations (currently US or EU).  This is also a very useful feature but to enable this AWS had to make some very significant changes in their API's.

In both of these cases, there is a desire to support the new exciting functionality provided by AWS but that needs to balanced with an equally strong desire to not break existing code.  There are really two main ways to address this:

  1. Merge both API's into single API that supports both features.  This is good in that all users would automatically gain access to all functionality.  The downside is that it makes the code much more complex and ugly and still introduces significant risk of breaking existing code.

  1. Provide a way to allow multiple versions of code to co-exist and provide a way for boto users to select which version they wish to use.

The new boto extension capability introduced in [Change Set 523](http://code.google.com/p/boto/source/detail?r=523) takes the second approach.  Here's how it works.


# Details #

Let's take the SQS module as our example.  The current boto release supports API version 2007-05-01.  Our goal is to introduce the 2008-01-01 functionality with as little disruption or modification to the existing code as possible.

The way this has been addressed is to create a new sub module, boto.sqs.20080101, in the subversion repository.  This sub module contains all of the code from the main module which needed to be modified to support the new API.  So, all new code is in boto.sqs.20080101 and all of the code in boto.sqs is unchanged.  In addition, the code in boto.sqs.20080101 only supports the new API and doesn't attempt to support the old API.  This makes the code much more clean.

The trick now is to allow the user to easily select which version they want to use and not have to modify their code (other than the modifications required by actual API changes) to use one version or the other.  To enable that, a new function has been added to the boto module called `check_extensions`.  The code is shown below:

```
def check_extensions(module_name, module_path):
    """
    This function checks for extensions to boto modules.  It should be called in the
    __init__.py file of all boto modules.  See:
    http://code.google.com/p/boto/wiki/ExtendModules

    for details.
    """
    option_name = '%s_extend' % module_name
    version = config.get('Boto', option_name, None)
    if version:
        dirname = module_path[0]
        path = os.path.join(dirname, version)
        if os.path.isdir(path):
            if config.getint('Boto', 'debug', 0):
                print 'extending module %s with: %s' % (module_name, path)
            module_path.insert(0, path)
```

This function needs to be called from the `__init__.py` file contained in boto.sqs, like this:

```
import boto

boto.check_extensions(__name__, __path__)
```

This will cause `check_extensions` to be called with the name of the module (boto.sqs) and the [\_\_path\_\_](http://docs.python.org/tut/node8.html#SECTION008430000000000000000) variable for the module.  The `check_extensions` function then looks in the BotoConfig for an option in the Boto section called `boto.sqs_extend`.  If it finds a value for that option, it tries to append a directory to the modules `__path__` based on name found in BotoConfig.

So, if I wanted to use the new SQS API rather than the old one, I would add this to my `~/.boto` or `/etc/boto.cfg` file:

```
[Boto]
boto.sqs_extend = 20080101
```

Now, when I start up boto it and access anything in `boto.sqs` Python will first search the boto.sqs.20080101 module and then, if it's not found, will look in `boto.sqs`