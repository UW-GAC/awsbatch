import json
import os
import sys

class jobdef(object):
    def __init__(self,jobdef_file=None, jobdef_version="1.0", verbose = False):
        self.verbose = verbose
        self.jobdef_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                                     "jobdef.json")
        if self.verbose:
            print(">>>jobdef: ctx file is: " + self.jobdef_file)
        if jobdef_file != None:
            self.jobdef_file = jobdef_file
        # open the json ctx file
        with open(self.jobdef_file) as cfh:
            self.jbd = json.load(cfh)

    def GetJobdef(self):
        return self.jbd
