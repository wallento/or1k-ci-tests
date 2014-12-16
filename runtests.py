#!/usr/bin/python

from __future__ import print_function

import argparse
import os, sys
import subprocess
import re

class TargetBase:
    tests = []
    target = None
    objdir = None
    resultdir = None
    flags = ""
    def read_tests(self):
        self.objdir = "{0}_obj".format(self.target)
        if not os.path.isdir(self.objdir):
            os.mkdir(self.objdir)
        self.resultdir = "{0}_result".format(self.target)
        if not os.path.isdir(self.resultdir):
            os.mkdir(self.resultdir)

        f = open("{0}.tests".format(self.target))
        for l in f:
            self.tests.append(l.strip())
    def error(self, string):
        print("ERROR: ", string, file=sys.stderr)
        exit(1)

class Target_mor1kx_generic_verilator(TargetBase):
    exe = None
    def __init__(self):
        self.target = "mor1kx-generic_verilator"
        self.read_tests()
        self.exe = os.environ["MOR1KX_GENERIC_VERILATOR"]
        self.flags = "-mnewlib"

    def run_tests(self):
        for test in self.tests:
            outfile = "{0}/{1}.elf".format(self.objdir, test)
            execstr = "or1k-elf-gcc -o {0} {1} src/{2}.c".format(outfile, self.flags, test)
            print(execstr)
            if subprocess.call(execstr, shell=True) != 0:
                self.error("Cannot compile test {0}".format(test))
        
            execstr = "{0} --elf-load={1}".format(self.exe, outfile)
            print(execstr)
            ferr = open("{0}/{1}.stderr".format(self.resultdir, test), "w")
            try:
                out = subprocess.check_output(execstr, stderr=ferr, shell=True)
            except:
                self.error("Cannot run test {0}".format(test))
            glob = { "success": False, "output": out }
            execfile("{0}_golden/{1}.py".format(self.target,test), glob)
            print(glob["success"])


parser = argparse.ArgumentParser(description="Run automated tests")

parser.add_argument('target', type=str, help="target")


args = parser.parse_args()

if args.target == "mor1kx-generic_verilator":
    target = Target_mor1kx_generic_verilator()
    target.run_tests()
