# Introduction #

There are quite a few people using boto.  We average 50+ downloads a week and there are well over 200 people on the discussion list.  I'd love to know what the heck all of you people are doing with it.  If you are able to share some info, please add it to the list below.


# Cool Stuff #

### **[ivan\_d](http://twitter.com/ivan_d)** ###
I used #boto to store Twitter social graph on simple db. I had written a simple python crawler. Thanks for #boto!

### **Nate Aune** ###
I just gave a talk at PyCon about using Boto as a component for PondCMS, a hosted and supported Plone service on EC2. You can download the slides here to learn more about the project: http://us.pycon.org/media/2009/talkdata/PyCon2009/066/PyCon_2009_-_Plone_in_the_Cloud.pdf

### **Eric Evans** ###
I use boto with duplicity[1](1.md) for backups. I follow that list as well, and anecdotally there seems to be a lot of other people who do as well.

### **Nikolaus Rath** ###
I'm using it for backups:
  * Start an EC2 instance
  * Mount an EBS volume
  * rsync local disk to EBS
  * Shutdown the instance again
Not particularly sophisticated I guess, but it works very well :-).


### **Elias Torres of Lookery** ###
I'm using boto for doing uploading large amounts of files to S3 from Apache Hadoop.

### **mARK bLOORE** ###
i do batch processing on EC2.  i use boto to fire up 20 or 30
instances, check that they started properly, transfer some files to
them, and start a script.  (actually, i use ssh to start the script.)
when done they use boto to save their results to S3.  the
batch-controller script waits til those instances have gotten fairly
started, and then fires up more...  i don't do them all at once
because S3 can't keep up with loading data to them.

i also use boto a lot indirectly, through s3funnel
(http://s3funnel.googlecode.com/), which makes using S3 on the command
line easy.

i haven't used boto for other AWS stuff, except to find that SDB can't
provide the data rate i needed.

### **dp** ###
At my previous employer, I used boto for automated daily database
backups to S3 and for a dynamic EC2 deployment system that allowed us
on-demand scalability.

Hooray for boto!

### **Mike Cariaso** ###
http://www.snpedia.com/index.php/Promethease
allows people to analyze their DNA, and pay $2 for improved performance. It uses boto for the FPS interface.

http://www.RunBlast.com
is a slightly neglected attempt to build a simplified interface to
http://en.wikipedia.org/wiki/BLAST
as well as the necessary databases and a parallelized implementation. It uses boto all over.

### **Blair Bethwaite** ###
We (www.messagelab.monash.edu.au) have been using boto to interface
our grid computing middleware Nimrod/G with the cloud - more info
about the project here: www.messagelab.monash.edu.au/NimrodInTheCloud.
Nimrod is really a family of tools (where Nimrod/G provides the
execution services) and there are higher level tools for optimisation,
experimental design and workflows built on top. Boto has been very
useful to us, if not for it we probably would have written an ugly
wrapper interface around the Amazon client tools. Thanks!

### DartWare ###
Thanks to the boto developers, DartWare was able to quickly throw
together an Amazon CloudWatch plugin for their interactive monitoring
suite InterMapper.

Check it out for yourself:

http://www.intermapper.com/products/ec2-monitoring

### [botoweb](http://bitbucket.org/cmoyer/botoweb) ###
After working with Mitch, I developed a quick Framework designed to create your own web-services built inside of the Cloud called [botoweb](http://bitbucket.org/cmoyer/botoweb). Within a matter of moments you can quickly create a fully-featured REST interface with your own Authorization and Application logic.

### **WikiTrans** ###
A few of us at Johns Hopkins University use boto to farm out translation tasks to Mechanical Turk. We send sentences in one language and ask users to translate them to another language. We then use the data collected to train statistical machine translation tools. The tool we're building isn't ready for the public yet, but we call it wikitrans, because while we're collecting data we are also translating documents from wikipedia into other languages as a way of giving back (beyond the micropayment via mturk).

