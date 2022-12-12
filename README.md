# Welcome

This application is for automatically landmarking photos of threespine stickleback for the Stuart Lab at Loyola University Chicago. It builds off of simple-ml-morph from the github user agporto.

# Install

Follow the installation steps for [ML-morph](https://github.com/agporto/ml-morph):

## Python Dependencies

- numpy>=1.13.3
- pandas>=0.22.0
- dlib>=19.7.0
- opencv-python>=3.4.0.12

If their dependencies are satisfied, these modules can be installed using:

    pip install -r requirements.txt

Alternatively, the dependancies may be installed into a [Conda](https://docs.conda.io/en/latest/) environment. The companion paper for this project was run from a Python v3.7.11 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) environment running on an Ubuntu 20.04 server.

## Optional Dependencies
- imglab

For those who want to visualize the xml files produced by the pipeline, we recommend installing the [`imglab`](https://github.com/davisking/dlib/tree/master/tools/imglab) tool that is included in the `dlib 19.7.0` source code. 
Please refer to the [`original repository`](https://github.com/davisking/dlib/tree/master/tools/imglab) for installation details and basic usage.
An alternative [`version of imglab`](https://imglab.in/) is also available and can be used directly from the web browser. We reccomend using the browser version to verify the landmarks are properly placed on the images.

## Installation notes and general issues
For Mac users, a series of dependencies for `dlib>=19.7.0` will need to be installed before it can be used. A detailed protocol can be found [here](https://medium.com/@210/install-dlib-on-mac-ff9f4d03ad8).

For windows users, the `dlib>=19.7.0` installation will sometimes fail. An alternative way to install it is to use a `.whl`:
    
    pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f
    
Also note that while **ml-morph** can handle multiple image file formats, some care is needed with regards to the presence of special characters in image filenames. So far, we have only had problems with `&`, but it is possible that other special characters might lead the software to throw out an error. File extensions cannot be capitalized if running on Linux and if the xml files being generated are blank, check the file extension of your images.


# Usage

N-fold cross validation.
```
python3 n_fold_cv.py -d <data_directory_path> -l <landmark_path>
```
To generate a csv of the landmarking error for 5 folds
```
mv /output5/predictor[0-4].da
python3 prediction.py -i output5/test0/ -p output5/predictor0.dat -o output0.xml
python3 prediction.py -i output5/test1/ -p output5/predictor1.dat -o output1.xml
python3 prediction.py -i output5/test2/ -p output5/predictor2.dat -o output2.xml
python3 prediction.py -i output5/test3/ -p output5/predictor3.dat -o output3.xml
python3 prediction.py -i output5/test4/ -p output5/predictor4.dat -o output4.xml
```

# Options

```
python3 n_fold_cv.py --help

```


# Output

The progress of the run is recorded in `log.txt` which is in the git repository directory while the run is going but is moved into the output directory at the end of the run.

<!-- Because files are kept in the main directory and only moved to the output directory at the end of the run, this  -->

The `test<nfold>.xml` files can be converted to csv using the `csv.py` python script. Run this python script from the output directory.
```
python3 csv.py -n <nfold>
```
`csv.py` can convert the `output.xml` landmarks of `prediction.py` to `.csv`, allowing various data analysis platforms to better access the landmark coordinates. 
```
python3 csv.py -o output.xml
```