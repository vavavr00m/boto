# Introduction #

We are pleased to announce the availability of a new boto release; 0.9a.


# Highlights of 0.9a Release #

  * Boto now supports Amazon's Mechanical Turk service.  Many thanks to Ansel Halliburton for contributing this code.
  * Boto now supports the 2007-01-19 version of the EC2 API
  * SQS Queues now have methods to save and restore messages to/from S3
  * The S3 interface now allows you to iterate over all keys in a bucket, transparently handling the paged results returned by S3
  * The HTTPS connection has been parameterized within Boto to permit the use of the M2Crypto library which actually verifies the certificate of the server.  Many thanks to Jon Colverson for contributing this code as well as the contrib/m2helpers.py module.
  * The new SQS methods [GetQueueAttributes](http://docs.amazonwebservices.com/AWSSimpleQueueService/2007-05-01/SQSDeveloperGuide/Query_QueryGetQueueAttributes.html) and [SetQueueAttributes](http://docs.amazonwebservices.com/AWSSimpleQueueService/2007-05-01/SQSDeveloperGuide/Query_QuerySetQueueAttributes.html) are now supported.  This allows you to query a queue for the approximate number of messages in the queue.
  * The new SQS method [ChangeMessageVisibility](http://docs.amazonwebservices.com/AWSSimpleQueueService/2007-05-01/SQSDeveloperGuide/Query_QueryChangeMessageVisibility.html) is now supported.  This feature is most easily accessed via the Message.change\_visibility method.
  * The S3 library now fully supports the `delimiter` option.
  * The S3 library now allows a callback to be passed to the methods that get/put content to S3.  This enables feedback during large file transfers.  See [this](http://groups.google.com/group/boto-users/browse_frm/thread/76a8362d291ccc53/#) for more info.
  * Improved error reporting by including the XML response body as part of the exceptions
  * Cleaned up and improved the sending/receiving of files to/from S3, including addition of Expect header in PUT's to address issues with files > 2.1GB in size.  See [this](http://developer.amazonwebservices.com/connect/thread.jspa?threadID=15283&tstart=30) for more info.
  * Many smaller interface changes suggested by the boto community (see [this thread](http://groups.google.com/group/boto-users/browse_frm/thread/03e22359bc073d43) ) for details
  * Improved docstrings for classes and methods.  Still not perfect but better!

# Complete ChangeLog for 0.9a Release #

```
------------------------------------------------------------------------
r196 | Mitch.Garnaat | 2007-03-13 19:35:35 -0400 (Tue, 13 Mar 2007) | 1 line

First inklings of an mturk package.  Only supports one method so far but it does authenticate properly.
------------------------------------------------------------------------
r197 | Mitch.Garnaat | 2007-03-13 23:43:36 -0400 (Tue, 13 Mar 2007) | 1 line

Adding a tiny bit more to the nascent mturk module.  Also added ability to pass a list of target_elems into ResultSet.
------------------------------------------------------------------------
r198 | Mitch.Garnaat | 2007-03-13 23:44:19 -0400 (Tue, 13 Mar 2007) | 1 line

Adding an object to represent Price data in mturk.
------------------------------------------------------------------------
r199 | Mitch.Garnaat | 2007-03-19 18:22:22 -0400 (Mon, 19 Mar 2007) | 1 line

Trying out some interface enhancements to address Issue-52.
------------------------------------------------------------------------
r200 | Mitch.Garnaat | 2007-03-23 16:12:35 -0400 (Fri, 23 Mar 2007) | 1 line

Added a set_timeout method to Queue object.  Also added a test case for it.  Fixes Issue-53.
------------------------------------------------------------------------
r201 | Mitch.Garnaat | 2007-03-24 09:46:07 -0400 (Sat, 24 Mar 2007) | 1 line

lookup method now correctly sets key.size based on Content-Length header.  Fixes Issue-54.
------------------------------------------------------------------------
r202 | anseljh | 2007-03-27 13:44:42 -0400 (Tue, 27 Mar 2007) | 1 line

Added create_hit() and Question-related classes to mturk module.  AnswerSpecification class still needs to be fleshed out.  But - it actually works!  I created a hit, went to the MTurk website and found it, and completed it.
------------------------------------------------------------------------
r204 | anseljh | 2007-03-28 15:26:47 -0400 (Wed, 28 Mar 2007) | 1 line

mturk module: added AnswerSpecification and related classes (tested and works); fixed join() call re: keywords; added email notification (untested so far); cleaned up some whitespace that was causing problems with my IDE.
------------------------------------------------------------------------
r205 | anseljh | 2007-04-02 13:36:47 -0400 (Mon, 02 Apr 2007) | 1 line

fixed some oddly crufty indentation
------------------------------------------------------------------------
r206 | anseljh | 2007-04-02 13:37:52 -0400 (Mon, 02 Apr 2007) | 1 line

split out Question and QuestionForm; implemented SelectionAnswer; various housekeeping on mturk module
------------------------------------------------------------------------
r207 | anseljh | 2007-04-02 14:33:24 -0400 (Mon, 02 Apr 2007) | 1 line

first attempt at the Mechanical Turk Notification API; semi-confirmed to work with a simple TurboGears controller
------------------------------------------------------------------------
r208 | Mitch.Garnaat | 2007-04-02 15:24:18 -0400 (Mon, 02 Apr 2007) | 1 line

Added a -t option to specify visibility timeout.
------------------------------------------------------------------------
r209 | Mitch.Garnaat | 2007-04-02 15:25:31 -0400 (Mon, 02 Apr 2007) | 1 line

Adding support for newest EC2 api by incorporating patches from ps.spam.  Fixes Issue-55.
------------------------------------------------------------------------
r210 | Mitch.Garnaat | 2007-04-02 16:47:49 -0400 (Mon, 02 Apr 2007) | 1 line

Fixing a bug introduced in last commit.  Awrrr, beware the whitespace...
------------------------------------------------------------------------
r211 | anseljh | 2007-04-02 16:58:31 -0400 (Mon, 02 Apr 2007) | 1 line

fixed an oops on import line
------------------------------------------------------------------------
r212 | anseljh | 2007-04-09 19:30:35 -0400 (Mon, 09 Apr 2007) | 1 line

fix for setting reward in register_hit_type()
------------------------------------------------------------------------
r213 | Mitch.Garnaat | 2007-04-27 11:55:28 -0400 (Fri, 27 Apr 2007) | 1 line

Added two new methods to save messages to an S3 bucket and restore messages from an S3 bucket
------------------------------------------------------------------------
r214 | Mitch.Garnaat | 2007-04-27 11:57:38 -0400 (Fri, 27 Apr 2007) | 1 line

Added support for S3BucketListResultSet which transparently handles pages results from S3.  Added some docstrings.
------------------------------------------------------------------------
r215 | Mitch.Garnaat | 2007-04-27 12:05:58 -0400 (Fri, 27 Apr 2007) | 1 line

Tweaks to resultset
------------------------------------------------------------------------
r216 | Mitch.Garnaat | 2007-04-27 12:06:49 -0400 (Fri, 27 Apr 2007) | 1 line

Moved BucketListResultSet to s3 module.
------------------------------------------------------------------------
r217 | Mitch.Garnaat | 2007-04-27 22:40:19 -0400 (Fri, 27 Apr 2007) | 1 line

Adding support for https_connection_factory.  Fixes Issue-57.
------------------------------------------------------------------------
r218 | Mitch.Garnaat | 2007-04-27 22:40:32 -0400 (Fri, 27 Apr 2007) | 1 line

Adding support for https_connection_factory.  Fixes Issue-57.
------------------------------------------------------------------------
r219 | Mitch.Garnaat | 2007-04-27 22:40:46 -0400 (Fri, 27 Apr 2007) | 1 line

Adding support for https_connection_factory.  Fixes Issue-57.
------------------------------------------------------------------------
r220 | Mitch.Garnaat | 2007-04-27 22:41:08 -0400 (Fri, 27 Apr 2007) | 1 line

Adding support for https_connection_factory.  Fixes Issue-57.
------------------------------------------------------------------------
r221 | Mitch.Garnaat | 2007-04-27 22:41:27 -0400 (Fri, 27 Apr 2007) | 1 line

Adding support for https_connection_factory.  Fixes Issue-57.
------------------------------------------------------------------------
r222 | Mitch.Garnaat | 2007-04-27 22:42:00 -0400 (Fri, 27 Apr 2007) | 1 line

Adding support for https_connection_factory.  Fixes Issue-57.
------------------------------------------------------------------------
r223 | Mitch.Garnaat | 2007-04-28 23:05:03 -0400 (Sat, 28 Apr 2007) | 1 line

Forgot the __init__.py file for this module directory.
------------------------------------------------------------------------
r224 | Mitch.Garnaat | 2007-05-07 18:09:45 -0400 (Mon, 07 May 2007) | 1 line

Fixed a bug in get_results.py that prevented the result files from being downloaded.  Also changed the formats of some of the date-related headers in the messages.
------------------------------------------------------------------------
r225 | Mitch.Garnaat | 2007-05-07 19:34:39 -0400 (Mon, 07 May 2007) | 1 line

Fixed a bug that is triggered if there are no results in the queue.
------------------------------------------------------------------------
r226 | Mitch.Garnaat | 2007-05-07 20:01:40 -0400 (Mon, 07 May 2007) | 1 line

Added documentation of the -n option
------------------------------------------------------------------------
r227 | Mitch.Garnaat | 2007-05-16 14:48:11 -0400 (Wed, 16 May 2007) | 1 line

Fixed the __iter__ method of Bucket object.  Fixes Issue-60.
------------------------------------------------------------------------
r228 | Mitch.Garnaat | 2007-05-16 14:52:17 -0400 (Wed, 16 May 2007) | 1 line

Fixed a logic problem in handling of exception in key.send_file.  Fixes Issue-56.
------------------------------------------------------------------------
r229 | Mitch.Garnaat | 2007-05-16 15:06:03 -0400 (Wed, 16 May 2007) | 1 line

Fixed a logic problem in handling of exception in key.send_file.  Fixes Issue-56.
------------------------------------------------------------------------
r230 | Mitch.Garnaat | 2007-05-16 15:10:41 -0400 (Wed, 16 May 2007) | 1 line

Backing out bad commit
------------------------------------------------------------------------
r231 | Mitch.Garnaat | 2007-05-16 15:15:05 -0400 (Wed, 16 May 2007) | 1 line

Backing out a bad commit
------------------------------------------------------------------------
r232 | Mitch.Garnaat | 2007-05-20 21:39:57 -0400 (Sun, 20 May 2007) | 1 line

Added single-line patch from jjc1138 to update public_dns_name when update() is called.  Fixes Issue-58.
------------------------------------------------------------------------
r233 | Mitch.Garnaat | 2007-05-20 21:49:52 -0400 (Sun, 20 May 2007) | 1 line

Made a number of usability improvements.  Fixes Issue-61, Issue-62, Issue-63.
------------------------------------------------------------------------
r234 | Mitch.Garnaat | 2007-05-30 22:42:23 -0400 (Wed, 30 May 2007) | 1 line

Incorporates change in Key field name Key.key -> Key.name.  Should have been checked in before.
------------------------------------------------------------------------
r235 | Mitch.Garnaat | 2007-05-30 22:46:37 -0400 (Wed, 30 May 2007) | 1 line

Make the GetQueueAttributes and SetQueueAttributes available by transparently passing those commands off to a QueryConnection rather than using REST.  This allows you to get an approximate count of the number of messages in a queue; very useful.  Fixes Issue-43.
------------------------------------------------------------------------
r236 | Mitch.Garnaat | 2007-05-30 22:47:27 -0400 (Wed, 30 May 2007) | 1 line

Updated unit test to match new code
------------------------------------------------------------------------
r237 | Mitch.Garnaat | 2007-05-31 09:52:40 -0400 (Thu, 31 May 2007) | 1 line

Trying to create better log files for command line services
------------------------------------------------------------------------
r238 | Mitch.Garnaat | 2007-05-31 14:05:39 -0400 (Thu, 31 May 2007) | 1 line

trying out some new debug ideas.
------------------------------------------------------------------------
r239 | Mitch.Garnaat | 2007-05-31 15:57:16 -0400 (Thu, 31 May 2007) | 1 line

More work to try to debug services.
------------------------------------------------------------------------
r240 | Mitch.Garnaat | 2007-05-31 16:10:04 -0400 (Thu, 31 May 2007) | 1 line

fixed a bug in writing timestamp for log
------------------------------------------------------------------------
r241 | Mitch.Garnaat | 2007-06-01 09:51:33 -0400 (Fri, 01 Jun 2007) | 1 line

Added sorting of log messages
------------------------------------------------------------------------
r242 | Mitch.Garnaat | 2007-06-01 09:52:23 -0400 (Fri, 01 Jun 2007) | 1 line

Added a save method to save all messages in a queue to a file, deleting the messages in the process.
------------------------------------------------------------------------
r243 | Mitch.Garnaat | 2007-06-01 10:53:50 -0400 (Fri, 01 Jun 2007) | 1 line

Fixed Issue-57 by incorporating boto-connection_factory_exceptions.diff contributed by j. colverson
------------------------------------------------------------------------
r244 | Mitch.Garnaat | 2007-06-04 07:45:23 -0400 (Mon, 04 Jun 2007) | 1 line

Fixed a typo bug regarding http_exceptions
------------------------------------------------------------------------
r245 | Mitch.Garnaat | 2007-06-04 20:43:16 -0400 (Mon, 04 Jun 2007) | 1 line

Added support to s3 for delimiters.  Fixes Issue-65.  This required a change in resultset.py which percolated throughout the code.  Also added a simple unit test for delimiters.
------------------------------------------------------------------------
r246 | Mitch.Garnaat | 2007-06-05 13:47:31 -0400 (Tue, 05 Jun 2007) | 1 line

This file should have been committed in last changeset.
------------------------------------------------------------------------
r247 | Mitch.Garnaat | 2007-06-05 13:49:05 -0400 (Tue, 05 Jun 2007) | 1 line

Added callback to get_file and send_file methods.  Fixes Issue-66.
------------------------------------------------------------------------
r248 | Mitch.Garnaat | 2007-06-05 17:18:33 -0400 (Tue, 05 Jun 2007) | 1 line

Adding num_cb parameters to all get_ and set_ methods to control the number of times the callback function will be called.
------------------------------------------------------------------------
r249 | Mitch.Garnaat | 2007-06-05 22:04:31 -0400 (Tue, 05 Jun 2007) | 1 line

Simplified Key.get_file method by calling Connection.make_request to do the hard work.  Fixed bugs in the *_string methods.
------------------------------------------------------------------------
r250 | Mitch.Garnaat | 2007-06-06 06:52:44 -0400 (Wed, 06 Jun 2007) | 1 line

Removing old code from key.py.  Folding in another patch from j.colverson to connection.py
------------------------------------------------------------------------
r251 | Mitch.Garnaat | 2007-06-06 12:47:31 -0400 (Wed, 06 Jun 2007) | 1 line

Fixed a typo bug
------------------------------------------------------------------------
r252 | Mitch.Garnaat | 2007-06-08 02:03:42 -0400 (Fri, 08 Jun 2007) | 1 line

Body of error responses for S3 now included in S3ResponseError exception.  Fixes Issue-67.
------------------------------------------------------------------------
r254 | Mitch.Garnaat | 2007-06-08 17:19:08 -0400 (Fri, 08 Jun 2007) | 1 line

Added a -p option to submit_files.py that displays progress information for file transfers.
------------------------------------------------------------------------
r255 | Mitch.Garnaat | 2007-06-08 22:21:18 -0400 (Fri, 08 Jun 2007) | 1 line

Added some sanity around error checking the num_cb arg.
------------------------------------------------------------------------
r256 | Mitch.Garnaat | 2007-06-08 22:23:04 -0400 (Fri, 08 Jun 2007) | 1 line

Modified the -p option to submit_files.py to take a number which is then passed as num_cb
------------------------------------------------------------------------
r257 | Mitch.Garnaat | 2007-06-09 07:58:46 -0400 (Sat, 09 Jun 2007) | 1 line

Fixed a bug in submit_files.py and changed service.py to print all SQSErrors encountered so you can see the response body.
------------------------------------------------------------------------
r258 | Mitch.Garnaat | 2007-06-11 10:34:55 -0400 (Mon, 11 Jun 2007) | 1 line

Disabling debug printing of the actual request data unless debug is set to a value > 1.
------------------------------------------------------------------------
r259 | Mitch.Garnaat | 2007-06-12 14:03:19 -0400 (Tue, 12 Jun 2007) | 1 line

Added an Expect header to the send_file method.
------------------------------------------------------------------------
r260 | Mitch.Garnaat | 2007-06-12 22:49:59 -0400 (Tue, 12 Jun 2007) | 1 line

Removing unneeded class
------------------------------------------------------------------------
r265 | Mitch.Garnaat | 2007-06-21 17:58:19 -0400 (Thu, 21 Jun 2007) | 1 line

Making sure the URL's for instance data are terminated with / character
------------------------------------------------------------------------
r266 | Mitch.Garnaat | 2007-06-21 17:59:32 -0400 (Thu, 21 Jun 2007) | 1 line

Trying to make more sense of the exceptions.
------------------------------------------------------------------------
r267 | Mitch.Garnaat | 2007-06-21 18:59:46 -0400 (Thu, 21 Jun 2007) | 1 line

Adding error response body to exception
------------------------------------------------------------------------

```