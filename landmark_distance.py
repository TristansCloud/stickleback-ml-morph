# Input
#   - Two sets of landmarks to compare. Each set can contain one or more csv files.
#     The landmarks must refer to individuals present in both files. This script assumes
#     that the csv headers follow this format, the same as generated by create_csv.py: 
#       id,box_id,box_top,box_left,box_width,box_height,X0,Y0...XN,YN
#     

# Output
#   - The eculidian distance in pixels between the two landmark sets for each individual and each landmark. This is a N individual x N landmark csv file.

# Steps
#   1. Combine csv files for set one and two 
#   2. Quality control
#   3. Find the eculidian distance and angle in radians for each landmark and individual between the two landmark sets

import argparse
import pandas as pd
import sys
import math

ap = argparse.ArgumentParser()
ap.add_argument("-1", "--one", type=str, required=True, nargs='+',
    help="one or more csv files of landmarks generated by create_csv.py. For example, all of the test landmarks from n_fold_cv.py")
ap.add_argument("-2", "--two", type=str, required=True, nargs='+',
    help="one or more csv of landmarks to compare to set one. The individuals in this set must also be in set one, there can be no repeated individuals in either set, and there are the same amount of indivudals in both sets. The column names of csv files in set two must be the same as set one")
ap.add_argument("-i", "--id", type=str, default="id",
    help="the column name that contains the id for each individual. (default = id)")
ap.add_argument("-p", "--path", type=str, default="/",
    help="if the ID column contains a directory name, what character separates the filename and the directory? If there is no directory in the id leave this command blank. If the id contains a '/' that is not because of a directory, set this flag to 'n' (default = /)")
ap.add_argument("-l", "--landmarks", type=int, required=True,
    help="The number of landmarks.")
ap.add_argument("-o1", "--output1", type=str, default = "set1.csv",
    help="A csv file of the combined landmarks in set 1. Will only be produced if more than one csv was input for set 1. (default = set1.csv)")
ap.add_argument("-o2", "--output2", type=str, default = "set2.csv",
    help="A csv file of the combined landmarks in set 2. Will only be produced if more than one csv was input for set 2. (default = set2.csv)")
ap.add_argument("-d", "--distance", type=str, default = "distance.csv",
    help="filename of the distance csv file (default = distance.csv)")
ap.add_argument("-a", "--angle", type=str, default = "angle.csv",
    help="filename of the angle csv file (default = angle.csv)")
ap.add_argument("-df", "--difference", type=str, default = "difference.csv",
    help="filename of the set 1 - set 2 coordinates csv file (default = difference.csv)")
args = vars(ap.parse_args())


#   1. Combine csv files for set one and two
data = []
for csv in args["one"]:
    df = pd.read_csv(csv)
    data.append(df)
df1 = pd.concat(data, ignore_index=True)
data = []
for csv in args["two"]:
    df = pd.read_csv(csv)
    data.append(df)
df2 = pd.concat(data, ignore_index=True)


#   2. Quality control
if not df1[args["id"]].is_unique:
    sys.exit("duplicated values in the ID colum of set one, set two not checked")
if not df2[args["id"]].is_unique:
    sys.exit("duplicated values in the ID colum of set two, set one is ok")

# remove filepaths and just keep filenames
if args["path"] != "n":
    if df1[args["id"]].str.contains(args["path"]).any() or df2[args["id"]].str.contains(args["path"]).any(): # if the path character is in any of the id columns
        df1[args["id"]] = df1[args["id"]].str.split(args["path"])
        df1[args["id"]] = df1[args["id"]].str[-1]
        df2[args["id"]] = df2[args["id"]].str.split(args["path"])
        df2[args["id"]] = df2[args["id"]].str[-1]

# sort landmarks by id
df1 = df1.sort_values(by = args["id"])
df2 = df2.sort_values(by = args["id"])
df1 = df1.reset_index(drop = True)
df2 = df2.reset_index(drop = True)

if not df1[args["id"]].equals(df2[args["id"]]):
    print("attempting to filter out specimens not shared between sets")
    if any(df1[args["id"]].isin(df2[args["id"]])):
        df1 = df1[df1[args["id"]].isin(df2[args["id"]])]
        df2 = df2[df2[args["id"]].isin(df1[args["id"]])]
        df1 = df1.reset_index(drop = True)
        df2 = df2.reset_index(drop = True)
    else:
        sys.exit("none of the ID's are shared between the two sets, check the ID formatting")
    
    print("set 1")
    print(df1)
    print("set 2")
    print(df2)
    if not df1[args["id"]].equals(df2[args["id"]]):
        sys.exit("the id columns could not be made equal between the two sets")

# create a list of column names for the X and Y coordinates. Use to keep only ID and landmark columns
coordinate_names = ['X' + str(i) for i in range(args["landmarks"])] + ['Y' + str(i) for i in range(args["landmarks"])]
column_names = ["id"] + coordinate_names
print(column_names)
df1=df1[column_names]
df2=df2[column_names]

if df1.shape != df2.shape:
    sys.exit("the number of rows or columns of the landmark sets are not the same")

print("passed QA")

print("set 1")
print(df1)
print("set 2")
print(df2)

if len(args["one"]) > 1:
    df1.to_csv(args["output1"],index = False)
    print("saved " + args["output1"])
if len(args["two"]) > 1:
    df2.to_csv(args["output2"],index = False)
    print("saved " + args["output2"])


#   3. Find the eculidian distance and angle for each landmark and individual between the two landmark sets

# find the differences between the X and Y coordinates of the two dataframes
differences = df1[coordinate_names].subtract(df2[coordinate_names])

# square the differences
squared_differences = differences.pow(2)

# create seperate X and Y coord dataframes
X_coord = ['X' + str(i) for i in range(args["landmarks"])]
Y_coord = ['Y' + str(i) for i in range(args["landmarks"])]
sq_diff_X = squared_differences[X_coord]
sq_diff_Y = squared_differences[Y_coord]

# Landmark column names
landmark_id = ["LM" + str(i) for i in range(args["landmarks"])]

# Map old column names to landmark ID because the dataframe.add method wants the same column names
X_lm_id = dict(zip(X_coord, landmark_id))
Y_lm_id = dict(zip(Y_coord, landmark_id))
sq_diff_X = sq_diff_X.rename(columns = X_lm_id)
sq_diff_Y = sq_diff_Y.rename(columns = Y_lm_id)

# Euclidean calculation: A^2 + B^2 = C^2
squared_distance = sq_diff_X.add(sq_diff_Y)
distance = squared_distance.pow(0.5)

# angle calculation. original landmark is (0,0), reference is (0,1)
def angle_between(v1, v2):
  # Calculate the dot product of the two vectors
  dot_product = v1[0]*v2[0] + v1[1]*v2[1]
  # Calculate the magnitude of each vector
  v1_magnitude = math.sqrt(v1[0]**2 + v1[1]**2)
  v2_magnitude = math.sqrt(v2[0]**2 + v2[1]**2)
  # Calculate the angle between the vectors using the dot product and magnitudes
  angle = math.acos(dot_product / (v1_magnitude * v2_magnitude))
  return angle

tmpdf = []
for j, row in differences.iterrows():
    tmprow = [df1[args["id"]][j], df2[args["id"]][j]]
    for i in range(args["landmarks"]):
        v1 = (row['X' + str(i)], row['Y' + str(i)])
        if v1 == (0, 0):
            tmprow.append("NaN")
        else:
            v2 = (0, 1)
            angle = angle_between(v1, v2)
            if v1[0] < 0: # always report radians from counterclockwise
                angle = 2*math.pi - angle
            tmprow.append(angle)
    tmpdf.append(tmprow)

angles = pd.DataFrame(tmpdf)
angles.columns = ["id1", "id2"] + landmark_id
angles.to_csv(args["angle"], index = False)
print("saved " + args["angle"])

# add the two set's ID columns for distances
dout = pd.concat([df1[args["id"]], df2[args["id"]], distance], axis=1)
dout.columns = ["id1", "id2"] + landmark_id
dout.to_csv(args["distance"], index = False)
print("saved " + args["distance"])

# add the two set's ID columns for coordinate differences
dfout = pd.concat([df1[args["id"]], df2[args["id"]], differences], axis=1)
dfout.columns = ["id1", "id2"] + coordinate_names
dfout.to_csv(args["difference"], index = False)
print("saved " + args["difference"])