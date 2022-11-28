# Input:
#   - directory of all photos
#   - parameters for shape_trainer.py
#   - number of folds
#   - directory name for outputs to be placed in

# Output (one for each fold):
#   - predictor.dat
#   - test.xml
#   - parameters used for shape_trainer.py

# Steps:
#   1. copy all photos to a new directory called train in the output directory
#   2. move 1/n of photos to a test directory
#   3. generate train and test.xml
#   4. train model
#   5. move test photos back to train directory
#   6. repeat from step 2

import utils
import argparse
import os
import shutil

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", type=str, default='images',
    help="directory containing images", metavar='')
ap.add_argument("-l", "--landmark", type=str, default='landmarks',
    help="landmarks file (csv or tps)", metavar='')
ap.add_argument("-ct", "--csvtps", type=str, default='csv',
    help="csv or tps", metavar='')
ap.add_argument("-n", "--nfold", type=int, default=10,
    help="number of folds for cross validation", metavar='')
ap.add_argument("-o", "--out", type=str,
    help="output directory, defaults to 'output${n-folds}", metavar='')
# flags for shape_trainer.py
ap.add_argument("-th", "--threads", type=int, default=1,
    help="number of threads to be used (default = 1)", metavar='')
ap.add_argument("-dp", "--tree-depth", type=int, default=4,
    help="choice of tree depth (default = 4)", metavar='')
ap.add_argument("-c", "--cascade-depth", type=int, default=15,
    help="choice of cascade depth (default = 15)", metavar='')
ap.add_argument("-nu", "--nu", type=float, default=0.1,
    help="regularization parameter (default = 0.1)", metavar='')
ap.add_argument("-os", "--oversampling", type=int, default=10,
    help="oversampling amount (default = 10)", metavar='')
ap.add_argument("-s", "--test-splits", type=int, default=20,
    help="number of test splits (default = 20)", metavar='')
ap.add_argument("-f", "--feature-pool-size", type=int, default=500,
    help="choice of feature pool size (default = 500)", metavar='')
ap.add_argument("-nt", "--num-trees", type=int, default=500,
    help="number of regression trees (default = 500)", metavar='')
args = vars(ap.parse_args())

assert os.path.isdir(args['directory']), "Could not find the folder {}".format(args['directory'])
assert os.path.isfile(args['landmark']), "Could not find the file {}".format(args['landmarks'])
if args["out"]:
    out = args['out']
    assert not os.path.isdir(out), "Output directory already exists"
else:
    out = "output"+str(args['nfold'])
    assert not os.path.isdir(out), "Output directory already exists" 
os.mkdir(out)

#   1. copy all photos to a new directory called train in the output directory
shutil.copytree(args["directory"], out+"/train")

#   2. move 1/n of photos to a test directory
img = os.listdir(out + "/train")
img.sort()

for n in range(args["nfold"]):
    os.mkdir(out + "/test" + str(n))
    temp_img = [out + "/train/" + x for x in img[n::args["nfold"]]]
    for x in temp_img:
        shutil.move(x, out + "/test" + str(n))# , copy_function = shutil.copy(x, out + "/test" + str(n))

    #   3. generate train and test.xml
        # test
    cmd = "python3 train_on_subset.py -d " + out + "/train -o " + "train.xml"
    if args["csvtps"] == "csv":
        cmd = cmd + " -c " + args["landmark"]
    elif args["csvtps"] == "tps":
        cmd = cmd + " -t " + args["landmark"]
    print(cmd)
    os.system(cmd) # import train_on_subset.py? Nahh :)
        # train
    cmd = "python3 train_on_subset.py -d " + out + "/test" + str(n) + " -o " + "test" + str(n) + ".xml"
    if args["csvtps"] == "csv":
        cmd = cmd + " -c " + args["landmark"]
    elif args["csvtps"] == "tps":
        cmd = cmd + " -t " + args["landmark"]
    print(cmd)
    os.system(cmd)

    #   4. train model
    cmd  = "python3 shape_trainer.py -d " + "train.xml -t " + "test" + str(n) + ".xml -o " + "predictor" + str(n) + " -th " + str(args["threads"]) + " -dp " + str(args["tree_depth"]) + " -c " + str(args["cascade_depth"]) + " -nu " + str(args["nu"]) + " -os " + str(args["oversampling"]) + " -s " + str(args["test_splits"]) + " -f " + str(args["feature_pool_size"]) + " -n " + str(args["num_trees"])
    print(cmd)
    os.system(cmd)    

    #   5. move test photos back to train directory
    bck = os.listdir(out + "/test" + str(n))
    for x in bck:
        shutil.move(os.path.join(out + "/test" + str(n), x), out + "/train")

