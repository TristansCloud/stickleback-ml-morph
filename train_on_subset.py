# This function takes as input a folder of images
# and a csv or tps file that contains the image landmarks and outputs "train.xml".
# The csv/tps can have more images than what are in the folder, only images in the folder 
# will be included in train.xml. The image filename in the csv/tps should only include
# the file, nothing about the path, eg fish.JPG, not /home/fish.JPG.

import utils
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('-d','--directory', type=str, default='images', help="input directory containing image files (default = images)", metavar='')
ap.add_argument('-c','--csv-file', type=str, default=None, help="(optional) XY coordinate file in csv format", metavar='')
ap.add_argument('-t','--tps-file', type=str, default=None, help="(optional) tps coordinate file", metavar='')
ap.add_argument('-o','--output-file', type=str, default='train.xml', help="(optional) output file name (default = train.xml", metavar='')

args = vars(ap.parse_args())

assert os.path.isdir(args['directory']), "Could not find the folder {}".format(args['directory'])

files=utils.train_on_subset_img_prep(args['directory']) # this seems to be working

# print(files) # shows that the image file names are 'directory/filename', which gives problems for utils.generate_dlib_xml
# which seems to want just the filename. Not sure why directory is needed, preprocessing.py works with the same options
# that train_on_subset.py throws the filename error.

# need to make sure only the photos in directory are being written the the train.xml
# get directory directory name (not full path) and have out_file={dirname}.xml
if args['csv_file'] is not None:
    dict_csv=utils.read_csv(args['csv_file'])
    utils.subset_generate_dlib_xml(dict_csv,files,folder=args['directory'],out_file=args['output_file']) # subset_generate_dlib_xml is a copy of generate_dlib_xml for working with the train_on_subset.py function. It pastes the directory path to the name variable

if args['tps_file'] is not None:
    dict_tps=utils.read_tps(args['tps_file'])
    utils.subset_generate_dlib_xml(dict_tps,files,folder=args['directory'],out_file=args['output_file']) # subset_generate_dlib_xml is a copy of generate_dlib_xml for working with the train_on_subset.py function. It pastes the directory path to the name variable
