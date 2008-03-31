# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import boto
from boto.pyami.scriptbase import ScriptBase
import os, StringIO

class CopyBot(ScriptBase):

    def __init__(self):
        ScriptBase.__init__(self)
        self.wdir = boto.config.get('Pyami', 'working_dir')
        self.log_file = '%s.log' % self.instance_id
        self.log_path = os.path.join(self.wdir, self.log_file)
        boto.set_file_logger(self.name, self.log_path)
        self.src_name = boto.config.get(self.name, 'src_bucket')
        self.dst_name = boto.config.get(self.name, 'dst_bucket')
        self.s3 = boto.connect_s3()
        self.src = self.s3.lookup(self.src_name)
        if not self.src:
            boto.log.error('Source bucket does not exist: %s' % self.src_name)
        self.dst = self.s3.lookup(self.dst_name)
        if not self.dst:
            self.dst = self.s3.create_bucket(self.dst_name)

    def copy_keys(self):
        boto.log.info('src=%s' % self.src.name)
        boto.log.info('dst=%s' % self.dst.name)
        try:
            for key in self.src:
                boto.log.info('copying %d bytes from key=%s' % (key.size, key.name))
                path = os.path.join(self.wdir, key.name)
                key.get_contents_to_filename(path)
                key.bucket = self.dst
                key.set_contents_from_filename(path)
                os.unlink(path)
        except:
            boto.log.exception('Error copying key: %s' % key.name)

    def copy_log(self):
        key = self.dst.new_key(self.log_file)
        key.set_contents_from_filename(self.log_path)
        
    def main(self):
        fp = StringIO.StringIO()
        boto.config.dump_safe(fp)
        self.notify('%s (%s) Starting' % (self.name, self.instance_id), fp.getvalue())
        if self.src and self.dst:
            self.copy_keys()
        if self.dst:
            self.copy_log()
        self.notify('%s (%s) Stopping' % (self.name, self.instance_id),
                    'Copy Operation Complete')
        if boto.config.getbool(self.name, 'exit_on_completion', True):
            ec2 = boto.connect_ec2()
            ec2.terminate_instances([self.instance_id])
        
