#/bin/python
import os,math
from sys import argv
import argparse
from shutil import copyfile,make_archive,rmtree
import xml.etree.ElementTree

def ensure_dir(s):
	if not os.path.exists(s):
		os.makedirs(s)


PACKAGE_DIR='poly/'
OUTPUT_PATH='.'
OUTPUT_DIR=OUTPUT_PATH+'/domjudge/'
EXTENSION_FOR_OUTPUT = '.a'
sample_tests = ['01']
PROBCODE = "PROB1"
PROBCOLOR = "#000000"
nodelete = False
#PARSING COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description='Process Polygon Package to Domjudge Package.')
parser.add_argument('package', type=str, help='path of the polygon package')
parser.add_argument('--code',  type=str, help='problem code for domjudge')
parser.add_argument('--sample',type=str, help='Specify the filename for sample test. Defaults to \'01\'')
parser.add_argument('--color', type=str, help='problem color for domjudge (in #XXXXXX format)')
parser.add_argument('-o','--output', type=str, help='Output Package directory')
parser.add_argument('--no-delete', action='store_true', help='Don\'t delete the output directory')
parser.add_argument('--ext', type=str, help='Set extension for the OUTPUT files in testset')
args = parser.parse_args()
if args.code:
	PROBCODE = args.code

if args.color:
	PROBCODE = args.color

if args.sample:
	sample_tests = [args.sample]

if args.output:
	OUTPUT_PATH = args.output
	OUTPUT_DIR=OUTPUT_PATH+'/domjudge/'

if args.ext:
	EXTENSION_FOR_OUTPUT = args.ext

if args.no_delete:
	nodelete = True


#Extracting the package
import zipfile
if not os.path.isfile(args.package):
	print "[ERROR] PACKAGE ZIP NOT FOUND"
	exit(1)
zip_ref = zipfile.ZipFile(args.package, 'r')
zip_ref.extractall(PACKAGE_DIR)
zip_ref.close()

#Create the OUTPUT DIR
ensure_dir(OUTPUT_DIR)

#Create Sub DIRS for tests
ensure_dir(OUTPUT_DIR+'/data')
ensure_dir(OUTPUT_DIR+'/data/sample')
ensure_dir(OUTPUT_DIR+'/data/secret')

#Parse XML for Problem Data
root = xml.etree.ElementTree.parse(PACKAGE_DIR+'problem.xml').getroot()
problem_name = root.find('names').find('name').attrib['value']
timelimit = int(math.ceil(float(root.find('judging').find('testset').find('time-limit').text)/1000.0))


desc = open(OUTPUT_DIR+'domjudge-problem.ini','w+')
desc.write("probid='"+PROBCODE+"'\n")
desc.write("name='"+problem_name+"'\n")
desc.write("timelimit='"+str(timelimit)+"'\n")
desc.write("color='"+PROBCOLOR+"'\n")
desc.close()

tests = filter(lambda x:not x.endswith(EXTENSION_FOR_OUTPUT),os.listdir(PACKAGE_DIR+'/tests'))
for test in tests:
	if test in sample_tests:
		copyfile(PACKAGE_DIR+'/tests/'+test,OUTPUT_DIR+'/data/sample/'+test+'.in')
		copyfile(PACKAGE_DIR+'/tests/'+test+EXTENSION_FOR_OUTPUT,OUTPUT_DIR+'/data/sample/'+test+'.ans')
	else:
		copyfile(PACKAGE_DIR+'/tests/'+test,OUTPUT_DIR+'/data/secret/'+test+'.in')
		copyfile(PACKAGE_DIR+'/tests/'+test+EXTENSION_FOR_OUTPUT,OUTPUT_DIR+'/data/secret/'+test+'.ans')

#ZIP the OUTPUT and DELETE Temp
#Assuming last four chars = .zip
make_archive(OUTPUT_PATH+'/domjudge', 'zip', OUTPUT_DIR)
rmtree(PACKAGE_DIR)
if nodelete == False:
	rmtree(OUTPUT_DIR)
