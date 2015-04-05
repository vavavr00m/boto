# Introduction #

There is a growing list of configuration options for the boto library.  Many of these options can be passed into the constructors for top-level objects such as connections.  Some options, such as credentials, can also be read from environment variables (e.g. `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).  But there is no central place to manage these options.  So, the development version of boto has now introduced the notion of boto config files.


# Details #

A boto config file is simply a .ini format configuration file that specifies values for options that control the behavior of the boto library.  Upon startup, the boto library looks for configuration files in the following locations and in the following order:

  1. /etc/boto.cfg - for site-wide settings that all users on this machine will use
  1. ~/.boto - for user-specific settings

The options are merged into a single, in-memory configuration that is available as `boto.config`.  The `boto.pyami.config` class is a subclass of the standard Python [SafeConfigParser](http://docs.python.org/lib/module-ConfigParser.html) object and inherits all of the methods of that object.  In addition, the `boto.pyami.config` class defines additional methods that are described on the PyamiConfigMethods page.

# Sections #

The following sections and options are currently recognized within the boto config file.

## Credentials ##

The `Credentials` section is used to specify the AWS credentials used for all boto requests.  The order of precedence for authentication credentials is:

  1. Credentials passed into Connection class constructor.
  1. Credentials specified by environment variables
  1. Credentials specified as options in the config file.

This section defines the following options:

**aws\_access\_key\_id**

> Your AWS access key

**aws\_secret\_access\_key**

> Your AWS secret access key

### Example ###

```
[Credentials]
aws_access_key_id = <your access key>
aws_secret_access_key = <your secret key>
```

## Boto ##

The `Boto` section is used to specify options that control the operaton of boto itself.  This section defines the following options:

**debug**

> Controls the level of debug messages that will be printed by the boto library.
> The following values are defined:
```
        0 - no debug messages are printed
        1 - basic debug messages from boto are printed
        2 - all boto debugging messages plus request/response messages from httplib
```

**proxy**

> The name of the proxy host to use for connecting to AWS.

**proxy\_port**

> The port number to use to connect to the proxy host.

**proxy\_user**

> The user name to use when authenticating with proxy host.

**proxy\_pass**

> The password to use when authenticating with proxy host.

**num\_retries**

> The number of times to retry failed requests to an AWS server.  If boto
> receives an error from AWS, it will attempt to recover and retry the request.
> The default number of retries is 5 but you can change the default with this option.

### Examples ###

```
[Boto]
debug = 0
num_retries = 10

proxy = myproxy.com
proxy_port = 8080
proxy_user = foo
proxy_pass = bar
```