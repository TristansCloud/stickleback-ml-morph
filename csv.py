from utils import *
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--nfold", type=int,
    help="Number of folds. This flag can only be used for the test.xml landmarks of n_fold_cv.py", metavar='')
ap.add_argument("-o", "--output", type=str,
    help="Convert any .xml landmark file to .csv", metavar='')
args = vars(ap.parse_args())

if args["nfold"]:
    for n in range(args["nfold"]):
        df = dlib_xml_to_pandas("test" + str(args["nfold"]) + ".xml")
        df.to_csv("test" + str(args["nfold"]) + ".csv")
elif args["output"]:
    df = dlib_xml_to_pandas(args["output"])
    df.to_csv(args["output"])