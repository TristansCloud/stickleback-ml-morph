# Welcome

This application is for automatically landmarking photos of threespine stickleback for the Stuart Lab at Loyola University Chicago, but can be applied to any images containing a single specimen that needs to be landmarked. It builds off of simple-ml-morph from the github user agporto.

# Install

The companion paper for this project was run from a Python v3.7.11 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) environment running on an Ubuntu 20.04 server.
  
If you have conda installed on your machine open your terminal (MacOS or Linux) or Anaconda prompt shell (Windows). The following script will create a conda environment and install all the needed dependancies
```
conda create --name mlmorph python=3.7
conda activate mlmorph
conda install -c conda-forge dlib numpy pandas opencv
```
Whenever you want to run the automated landmarking program, don't forget to run 
```
conda activate mlmorph
```

If you don't want to use conda, you can follow the installation steps for [ML-morph](https://github.com/agporto/ml-morph):

## Python Dependencies

- numpy>=1.13.3
- pandas>=0.22.0
- dlib>=19.7.0
- opencv-python>=3.4.0.12

If their dependencies are satisfied, these modules can be installed using:
```
pip install -r requirements.txt
```

Once the dependancies are installed, the program can be downloaded:
```
git clone https://github.com/TristansCloud/stickleback-ml-morph.git
cd stickleback-ml-morph
```

## Optional Dependencies
- imglab

We reccomend using the [`browser version of imglab`](https://imglab.in/) to verify the .xml files of landmarks are properly placed on the images as a quality assurance step in your analysis. Low accuracy models may be training on improperly formatted landmarks. The [`imglab`](https://github.com/davisking/dlib/tree/master/tools/imglab) tool is included in the `dlib 19.7.0` source code and can be installed locally. 
Please refer to the [`original repository`](https://github.com/davisking/dlib/tree/master/tools/imglab) for installation details and basic usage.

## Installation notes and general issues
For Mac users, a series of dependencies for `dlib>=19.7.0` will need to be installed before it can be used. A detailed protocol can be found [here](https://medium.com/@210/install-dlib-on-mac-ff9f4d03ad8).

For windows users, the `dlib>=19.7.0` installation will sometimes fail. An alternative way to install it is to use a `.whl`:
    
    pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f
    
Also note that while **ml-morph** can handle multiple image file formats, some care is needed with regards to the presence of special characters in image filenames. So far, we have only had problems with `&`, but it is possible that other special characters might lead the software to throw out an error. File extensions cannot be capitalized if running on Linux and if the xml files being generated are blank, check the file extension of your images.


# Usage

To learn more about each python script run
```
python3 <script_name>.py --help
```
*** WARNING *** The program currently changes the landmarks to be 0 indexed, i.e. landmark 1 will be landmark 0 in all output files. This does not affect your input landmark file. Remember this when reassigning landmark IDs.

## Vignette for N-fold cross validation.
Cross validation can be done through `n_fold_cv.py`, 5 fold cross validation is the default. The basic usage is
```
python3 n_fold_cv.py -i <image_directory_path> -l <landmark_path>
```
To run the n-fold cross validation using the example images, run:
```
python3 n_fold_cv.py -i images/image-examples/ -l landmarks/landmark-examples/csv-example.csv
```
  
Generate xml and tps landmarks using the predictors from each fold. The nth predictor were not trained with the nth test directory, i.e. predictor0 was not trained with test0/ images.
```
python3 prediction.py -i output5/test0/ -p output5/predictor0.dat -o output5/output0.xml
python3 prediction.py -i output5/test1/ -p output5/predictor1.dat -o output5/output1.xml
python3 prediction.py -i output5/test2/ -p output5/predictor2.dat -o output5/output2.xml
python3 prediction.py -i output5/test3/ -p output5/predictor3.dat -o output5/output3.xml
python3 prediction.py -i output5/test4/ -p output5/predictor4.dat -o output5/output4.xml
```
Make csv files of of the predicted and training landmarks
```
python3 create_csv.py -o output5/output0.csv -i output5/output0.xml
python3 create_csv.py -o output5/output1.csv -i output5/output1.xml
python3 create_csv.py -o output5/output2.csv -i output5/output2.xml
python3 create_csv.py -o output5/output3.csv -i output5/output3.xml
python3 create_csv.py -o output5/output4.csv -i output5/output4.xml
python3 create_csv.py -o output5/test0.csv -i output5/test0.xml
python3 create_csv.py -o output5/test1.csv -i output5/test1.xml
python3 create_csv.py -o output5/test2.csv -i output5/test2.xml
python3 create_csv.py -o output5/test3.csv -i output5/test3.xml
python3 create_csv.py -o output5/test4.csv -i output5/test4.xml
```
The script `landmark_distance.py` takes two sets of the same landmarks and provides this data for each landmark and individual between the two sets:
- The distance between the landmarks
- The angle between the first landmark, the point (0,1) relative to the first landmark, and the second landmark.
- The difference in X and Y coordinates (X1,Y1) - (X2, Y2).
It can accept more than one csv file per set of landmarks. You will likely want to compare the true landmark position to where the model placed the landmark to get a finer understanding of you're model's performance. To do this using the csv files created in the previous step:
```
python3 landmark_distance.py -1 output5/output[0-4].csv -2 output5/test[0-4].csv -l 40 -o1 mlmorph.csv -o2 manual.csv
```
<!-- For the manually relandmarked points
```
python3 landmark_distance.py -1 output5/manual.csv -2 30_relandmarked_ml_format.csv -l 40 -a 30_relm_angle.csv -d 30_relm_distance.csv
``` -->

`landmark_distance.py` outputs three files; two csv files of landmarks for set 1 and 2, and a csv file of the distance in pixels between the two sets of landmarks. You can use this distance file to explore how error varies among landmarks and individuals. Certain landmarks may be placed less accurately than others. Some features may be present in a small subset of individuals and the model may not handle these outliers well. Check for these conditions using the distance csv and your favorite data analysis software. There are Rscripts from the companion paper to to this for the Stuart Lab's stickleback images. These files are created in the main `stickleback-ml-morph` directory. To cleanup and move these files to the output folder, run:
```
mv distance.csv mlmorph.csv manual.csv angle.csv output5/
```
Once you are satified with the model's performance, you can retrain it using all available images (no cross validation):
```
python3 train_on_subset.py -d images/image-examples/ -c landmarks/landmark-examples/csv-example.csv -o all_images.xml
python3 shape_trainer.py -d all_images.xml # all_images.xml must be in the same folder as shape_trainer.py
mv all_images.xml predictor.dat output5/ # cleanup
```
`predictor.dat` is the model trained on all images. You can use the `prediction.py` python script to landmark new images using your trained model. The model will likely perform better if these images were taken under the same conditions as the images used to train your model. Make a csv of landmarks from the resulting `output.xml` using `create_csv.py` as was demonstrated earlier
```
python3 prediction.py -i /path/to/unlandmarkedimages -p predictor.dat
python3 create_csv.py -i output.xml -o new_landmarks.csv
```