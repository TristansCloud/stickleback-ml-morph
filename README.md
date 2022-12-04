## Welcome

This application is for automatically landmarking photos of threespine stickleback for the Stuart Lab at Loyola University Chicago using simple-ml-morph from the github user agporto. It includes features for formatting ObjectJ landmarks for MLmorph, predicting landmark locations using a pre-trained model, and calculating feature lengths from the resulting landmarks. 

## Usage

N-fold cross validation. For more options run `python3 n_fold_cv.py --help`
```
python3 n_fold_cv.py -d <data_directory_path> -l <landmark_path>
```

## Output

The progress of the run is recorded in `log.txt` which is in the `sticklebac-ml-morph` directory while the run is going but is moved into the output directory during the end of the run.

The `test<nfold>.xml` files can be converted to csv using the `csv.py` python script. Run this python script from the output directory.
```
python3 csv.py -n <nfold>
```
`csv.py` can convert the `output.xml` landmarks of `prediction.py` to `.csv`, allowing various data analysis platforms to better access the landmark coordinates. 
```
python3 csv.py -o output.xml
```

