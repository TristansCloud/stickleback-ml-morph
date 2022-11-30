## Welcome

This application is for automatically landmarking photos of threespine stickleback for the Stuart Lab at Loyola University Chicago using simple-ml-morph from the github user agporto. It includes features for formatting ObjectJ landmarks for MLmorph, predicting landmark locations using a pre-trained model, and calculating feature lengths from the resulting landmarks. 

## Usage

N-fold cross validation. For more options run `python3 n_fold_cv.py --help`
```
python3 n_fold_cv.py -d <data_directory_path> -l <landmark_path>
```

## Output

The test${nfold}.xml files can be converted to csv using a python funtion in `utils.py`
```
from utils import *
df = dlib_xml_to_pandas('output.xml')
```
