import os.path
import os
import sys
import traceback
import argparse

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import jinja2.exceptions

BASE_PATH=os.path.dirname(os.path.abspath(__file__))


production_flag_set = '--tls --http-auth'

# Command ine options
parser = argparse.ArgumentParser(description='Generate Dockerfile from Jinja2 template')

# Template
parser.add_argument('--template', dest='template_file', action='store', default='Dockerfile.j2',
                   help='Template file to process')

# Template
parser.add_argument('--templates-dir', dest='templates_dir', action='store', default=os.path.join(BASE_PATH, 'templates'),
                   help='Template file to process')


parser.add_argument('--requirements', dest='requirements_file', action='store', default='requirements.txt',
                   help="PIP's requirements file")

parser.add_argument('--output', dest='output', action='store', default='Dockerfile',
                   help="Destination filename")


args = parser.parse_args()

TEMPLATE_DIR=args.templates_dir

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), undefined = StrictUndefined)

template = env.get_template(args.template_file)

req_file = open(args.requirements_file, 'r')

def stip_line(l):
    return l.translate(None, '\r\n')

vars = {
    'requirements_filename': args.requirements_file,
    'deps': ' \\\n'.join([stip_line(r) for r in req_file if r[0] != '#' and len(stip_line(r)) > 0])
    }

o = open(args.output, 'w')

try:
    o.write('''
# Achtung!!! Attention!!! Huomio!!! Pozor!!!
# This is a generated file. Avoid to edit manually

''')

    # print "# Generated from %s by the magic of Jinja2\n" % (os.path.join(TEMPLATE_DIR,'nginx.conf.j2'))

    o.write(template.render(vars))

except jinja2.exceptions.UndefinedError,e:
    print "Failed to process template: %s" % (e)
    raise
