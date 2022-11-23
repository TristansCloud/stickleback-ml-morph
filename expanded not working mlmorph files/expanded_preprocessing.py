import argparse
import os
import utils


ap = argparse.ArgumentParser()
ap.add_argument('-i','--input-dir', type=str, default='images', help="input directory containing image files (default = images)", metavar='')
ap.add_argument('-c','--csv-file', type=str, default=None, help="(optional) XY coordinate file in csv format", metavar='')
ap.add_argument('-t','--tps-file', type=str, default=None, help="(optional) tps coordinate file", metavar='')
ap.add_argument('-s','--split', action="store_true", help="(optional) split images 80/20 into test and train? Default = yes", metavar='')
ap.add_argument('-p','--copy', action="store_true", help="(optional) copy images into a separate training folder (and test folder if --split)? Will write copied images as .jpg", metavar='')
ap.add_argument('-r','--random', action="store_false", help="(optional) use a different seed to generate train/test splits? Used for multiple runs. --random yes will give different splits each run", metavar='')
ap.add_argument('-o','--output', type=str, default='', help="string to prefix train.xml (and test.xml if --split yes) and dictionary to copy to if --copy", metavar='')

args = vars(ap.parse_args())

assert os.path.isdir(args['input_dir']), "Could not find the folder {}".format(args['input_dir'])


file_sizes=utils.split_train_test(args['input_dir'],random_seed=args['random'],copy_img=args['copy'],split_img=args['split'],out_file=args['output'])

if args['copy']:
    train_folder = args['output']+'train'
    test_folder = args['output']+'test'
else:
    train_folder = args['input-dir']
    test_folder = args['input-dir']

if args['csv_file'] is not None:
    dict_csv=utils.read_csv(args['csv_file'])
    utils.generate_dlib_xml(dict_csv,file_sizes['train'],folder=train_folder,copy_img=args['copy'],out_file=args['output']+'train.xml')
    utils.dlib_xml_to_tps(args['output']+'train.xml')
    if args['split'] == 'yes':
        utils.generate_dlib_xml(dict_csv,file_sizes['test'],folder=test_folder,copy_img=args['copy'],out_file=args['output']+'test.xml')
        utils.dlib_xml_to_tps(args['output']+'test.xml')
    
    
    
if args['tps_file'] is not None:
    dict_tps=utils.read_tps(args['tps_file'])
    utils.generate_dlib_xml(dict_tps,file_sizes['train'],folder=train_folder,copy_img=args['copy'],out_file=args['output']+'train.xml')
    utils.dlib_xml_to_tps(args['output']+'train.xml')
    if args['split'] == 'yes':
        utils.generate_dlib_xml(dict_tps,file_sizes['test'],folder=test_folder,copy_img=args['copy'],out_file=args['output']+'test.xml')
        utils.dlib_xml_to_tps(args['output']+'test.xml')
  
