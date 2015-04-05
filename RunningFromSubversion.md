#How to install and use boto from subversion

# Introduction #

If you want to use the latest and greatest version of boto at all times, it's best to run from the subversion repository rather than using one of the packaged releases.  The packaged releases do, at least in theory, provide a more stable and consistent version and are easy to install.  Running out of subversion, however, always provides you with the latest features and bug fixes and since I run unit tests before any check-in you are still guaranteed a reasonable level of stability.  The choice is up to you.


# How to install boto from subversion #

The first step is to check out the latest version of boto from the subversion repository. Full instructions are provided [here](http://code.google.com/p/boto/source) but let's take the simple case of an anonymous checkout.  I'm going to assume you are using the command line version of subversion but you should be able to easily map this command to other subversion clients (change the path to suit your environment):

```
$ cd /home/mitch/Projects
$  svn checkout http://boto.googlecode.com/svn/trunk/ boto
```

This will create a directory called _boto_ in the current directory.  This directory will contain a complete copy of the latest files in the subversion repository.

The trick now is to get Python to include this directory in it's list of paths to search when you import a module.  There are really two ways to do this:

### Add the boto directory to the PYTHONPATH environment variable ###
In Linux or MacOS environments using bash-like shells this would be done like this:
```
$ export PYTHONPATH=$PYTHONPATH:/home/mitch/Projects/boto
```
You would probably want to add this to one of your startup scripts to make sure it gets set each time you login or start up a shell.  You may also need to add the PYTHONPATH environment variable to your IDE's settings.

### Add a symbolic link to your boto directory in the Python site ###
Let's assume that your Python is installed in /usr/local.  You will then find a directory called /usr/local/lib/python2.x/site-packages.  Note that you will have to adjust that path to your own installation and Python version number.  To create the symbolic link you would:
```
$ sudo ln -s /home/mitch/Projects/boto/boto /usr/local/lib/python2.4/site-packages
```
This approach would make the boto directory available to all users on the system but requires the ability to sudo or act as root on your system.

Once this is set up, you should be able to import boto just as you would if you had installed it with the Python setup.py installer.  Anytime you want to update your boto directory to the latest version, just:
```
$ cd /home/mitch/Projects/boto
$ svn update
```