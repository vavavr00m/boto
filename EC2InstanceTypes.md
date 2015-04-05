# Using the New EC2 Instance Types #

Amazon has now enabled different types of EC2 instances.  In addition to the original instance type (now called m1.small) there are two addition types of instances, m1.large and m1.xlarge (see [this](http://developer.amazonwebservices.com/connect/entry.jspa?externalID=993&categoryID=100)) for more details.

To accommodate this new feature, a new parameter has been added to the `run_instances` method of EC2Connection object in boto as well as to the `run` method of the Image object.  This new string parameter, called `instance_type` defaults to a value of `"m1.small"` for backward compatibility.  However, passing a value of `"m1.large"` or `"m1.xlarge"` will create instances of the new Instance Types.

Because the new Instance Types are 64-bit architectures, you need to be sure that the AMI you are using is compatible with the new instance.  AWS has provided some sample, public AMI's based on 64-bit Linux images and you can follow the same procedure as before to modify and rebundle these or create your own AMI from a loopback device on a local machine.

The 0.9c release of boto incorporates this initial support of Instance Types.  Future releases may refine the support.