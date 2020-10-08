#!/usr/bin/env python
"""
Packer wrapper script

Convert between JSON and YAML maintaining same order
Wrap packer execution, auto-translating YAML to JSON
"""

import argparse
import atexit
from collections import OrderedDict
import contextlib
import json
import os
import re
import subprocess
import tempfile
import time
import six
import sys
import yaml




class Exit(object):
    OK = 0
    CANCELLED = 1
    ERROR = 2

@contextlib.contextmanager
def smart_open(filename=None, mode='Ur'):
    if filename and filename != '-':
        fh = open(filename, mode)
    else:
        if mode is None or mode == '' or 'r' in mode:
            fh = sys.stdin
        else:
            fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdin and fh is not sys.stdout:
            fh.close()


# try to use LibYAML bindings if possible
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from yaml.representer import SafeRepresenter

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

Dumper.add_representer(OrderedDict, dict_representer)
Dumper.add_representer(str, SafeRepresenter.represent_str)
Loader.add_constructor(_mapping_tag, dict_constructor)
if six.PY3:
    Dumper.add_representer(str, SafeRepresenter.represent_str)
else:
    Dumper.add_representer(unicode, SafeRepresenter.represent_unicode)



if six.PY3:
    # Extending JSONEEncoder to support JSON dumping python3 bytes
    class FancyJSONEncoder(json.JSONEncoder):
        """
        Subclassing JSONEncoder to override default()
        Supports Python3 byte strings
        """
        def default(self, o):
            if isinstance(o, bytes):
                return o.decode('utf-8')
            # Let the base class default raise the TypeError
            return json.JSONEncoder.default(self, o)
else:
    FancyJSONEncoder = json.JSONEncoder


class ArgumentParserError(Exception): pass

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

g_tmp_files = []

@atexit.register
def goodbye():
    for filename in g_tmp_files:
        print("Deleting tmp file {}".format(filename))
        os.unlink(filename)

def launch_packer():
    """ Launch Packer but handle yaml """
    #import pdb; pdb.set_trace()
    #print "our args were {}".format(sys.argv)
    packer_args = []
    yaml_re = re.compile(r'.*\.ya?ml$')
    for arg in sys.argv:
        if yaml_re.search(arg):
            h, filename = tempfile.mkstemp(suffix='.json')
            new_arg = yaml_re.sub(filename, arg)
            packer_args.append(new_arg)
            #print "Created temp file {}, handle {}".format(filename, h)
            #print "src is {}".format(arg)
            to_json_file(arg, filename)
        else:
            packer_args.append(arg)
    packer_args = ['packer'] + packer_args[1:]
    #print "packer args are {}".format(packer_args)
    subprocess.call(packer_args)


def parse_args(args=None):
    parser = ThrowingArgumentParser(description='Packer wrapper')
    sub_parsers = parser.add_subparsers(dest='cmd', help='sub-command help')
    parser_convert = sub_parsers.add_parser('convert', help='Convert between JSON and YAML')
    parser_convert.add_argument('template', help='JSON or YAML file')
    parser_convert.add_argument('--out', '-o', help='Output file')
    conversion_grp = parser_convert.add_mutually_exclusive_group()
    conversion_grp.add_argument('--from-yaml-to-json', '--y-to-j', '--json', '-j',
            dest='json', action='store_true', help='src is YAML, dst is JSON')
    conversion_grp.add_argument('--from-json-to-yaml', '--j-to-y', '--yaml', '--yml', '-y',
            dest='yaml', action='store_true', help='src is YAML, dst is JSON')
    args = parser.parse_args(args)
    return args, parser_convert


def run_cmd(args, parser_convert):
    if args.cmd == 'convert':
        return convert(args, parser_convert)
    else:
        import pdb; pdb.set_trace()


def convert(args, parser_convert):
    ext = os.path.splitext(args.template)[1]
    if args.json or ext in ('.yml', '.yaml'):
        to_json_file(args.template, args.out)
    elif args.yaml or ext in ('.json'):
        to_yaml(args.template, args.out)
    else:
        parser_convert.error("Wazza")

def to_yaml(src, dst):
    with open(src) as f:
        template = f.read()
        f.close()
    with smart_open(dst, 'w') as out:
        yaml.dump(json.loads(template, object_pairs_hook=OrderedDict), out, indent=2, Dumper=Dumper, default_flow_style=False)

def to_json(src):
    #return json.dumps(yaml.load(src, Loader=Loader).decode('utf-8'), separators=(',',': '), indent=2)
    return json.dumps(yaml.load(src, Loader=Loader), separators=(',',': '), indent=2, cls=FancyJSONEncoder)
    #return yaml.load(src, Loader=Loader)

def to_json_file(src, dst):
    with open(src) as f:
        template = f.read()
        f.close()
    with smart_open(dst, 'w') as out:
        json.dump(yaml.load(template, Loader=Loader), out, separators=(',',': '), indent=2)

def main():
    try:
        try:
            args, parser_convert = parse_args()
            return run_cmd(args, parser_convert)
        except ArgumentParserError as e:
            launch_packer()
    except KeyboardInterrupt as e:
        return Exit.CANCELLED


if __name__ == "__main__":
    # execute only if run as a script
    sys.exit(main())
