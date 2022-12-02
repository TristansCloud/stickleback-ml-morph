# Input:
#   - directory of all photos
#   - parameters for shape_trainer.py
#   - number of folds
#   - directory name for outputs to be placed in

# Output:
#   - predictor.dat (one for each fold)
#   - test.xml (one for each fold)
#   - parameters used for shape_trainer.py

# Steps:
#   1. Copy all photos to a train subdirectory of the output directory
#   2. Move 1/n of photos to a test subdirectory of the output directory
#   3. Generate train.xml and test.xml
#   4. Train model
#   5. Move test photos back to train directory
#   6. Repeat from step 2 for all n folds. Each fold is unique,
#      the images are lexicographically sorted and every nth file
#      is moved for a fold. The starting file for counting every
#      nth file shifts back by one after each fold.

import utils
import argparse
import os
import shutil

os.system("echo 'starting run' > log.txt")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
    help="directory containing images", metavar='')
ap.add_argument("-l", "--landmark", type=str, required=True,
    help="landmarks file (csv or tps files only)", metavar='')
ap.add_argument("-ct", "--csvtps", type=str, default='csv',
    help="filetype of landmarks (csv or tps, default = csv)", metavar='')
ap.add_argument("-n", "--nfold", type=int, default=5,
    help="number of folds for cross validation (default = 5)", metavar='')
ap.add_argument("-o", "--out", type=str,
    help="output directory (default = output${n-folds})", metavar='')
# flags for shape_trainer.py
ap.add_argument("-th", "--threads", type=int, default=2,
    help="number of threads to be used (default = 2)", metavar='')
ap.add_argument("-dp", "--tree-depth", type=int, default=4,
    help="choice of tree depth (default = 4)", metavar='')
ap.add_argument("-c", "--cascade-depth", type=int, default=30,
    help="choice of cascade depth (default = 30)", metavar='')
ap.add_argument("-nu", "--nu", type=float, default=0.1,
    help="regularization parameter (default = 0.1)", metavar='')
ap.add_argument("-os", "--oversampling", type=int, default=200,
    help="oversampling amount (default = 200)", metavar='')
ap.add_argument("-s", "--test-splits", type=int, default=30,
    help="number of test splits (default = 30)", metavar='')
ap.add_argument("-f", "--feature-pool-size", type=int, default=1000,
    help="choice of feature pool size (default = 1000)", metavar='')
ap.add_argument("-nt", "--num-trees", type=int, default=500,
    help="number of regression trees (default = 500)", metavar='')
args = vars(ap.parse_args())

assert os.path.isdir(args['data']), "Could not find the folder {}".format(args['data'])
assert os.path.isfile(args['landmark']), "Could not find the file {}".format(args['landmarks'])
if args["out"]:
    out = args['out']
    assert not os.path.isdir(out), "Output directory already exists"
else:
    out = "output"+str(args['nfold'])
    assert not os.path.isdir(out), "Output directory already exists" 
os.mkdir(out)

#   1. copy all photos to a new directory called train in the output directory
shutil.copytree(args["data"], out+"/train")
os.system("echo 'copied images to "+ out +"/train' >> log.txt")
    # rename to .jpg if the image extension is .JPG
jpg = set(x[-3:] for x in os.listdir(out + "/train"))
if jpg == {"JPG"}:
    for x in os.listdir(out + "/train"):
        os.rename(out + "/train/" + x, out + "/train/" + x[:-3]+"jpg")
    os.system("echo 'changed file extension from JPG to jpg' >> log.txt")

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
    os.system(cmd + ' >> log.txt')
        # train
    cmd = "python3 train_on_subset.py -d " + out + "/test" + str(n) + " -o " + "test" + str(n) + ".xml"
    if args["csvtps"] == "csv":
        cmd = cmd + " -c " + args["landmark"]
    elif args["csvtps"] == "tps":
        cmd = cmd + " -t " + args["landmark"]
    print(cmd)
    os.system(cmd + ' >> log.txt')

    #   4. train model
    cmd  = "python3 shape_trainer.py -d " + "train.xml -t " + "test" + str(n) + ".xml -o " + "predictor" + str(n) + " -th " + str(args["threads"]) + " -dp " + str(args["tree_depth"]) + " -c " + str(args["cascade_depth"]) + " -nu " + str(args["nu"]) + " -os " + str(args["oversampling"]) + " -s " + str(args["test_splits"]) + " -f " + str(args["feature_pool_size"]) + " -n " + str(args["num_trees"])
    print(cmd)
    os.system(cmd + ' >> log.txt')
       

    #   5. copy test photos back to train directory
    bck = os.listdir(out + "/test" + str(n))
    for x in bck:
        shutil.copy2(os.path.join(out + "/test" + str(n), x), out + "/train")

shutil.rmtree(out + "/train") 
