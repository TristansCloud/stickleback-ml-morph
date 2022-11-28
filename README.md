## Welcome

This application is for automatically landmarking photos of threespine stickleback for the Stuart Lab at Loyola University Chicago using simple-ml-morph from the github user agporto. It includes features for formatting ObjectJ landmarks for MLmorph, predicting landmark locations using a pre-trained model, and calculating feature lengths from the resulting landmarks. 

## Output

The test${nfold}.xml files can be converted to csv using a python funtion in `utils.py`
```
from utils import *
df = dlib_xml_to_pandas('output.xml')
```
