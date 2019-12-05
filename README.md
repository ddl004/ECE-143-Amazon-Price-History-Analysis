# ECE-143-Amazon-Price-History-Analysis

Group 13: XinLing Bai, Saikiran Komatineni, Derek Lam, Chang Zhou

This is the repository for Group 13's ECE 143 Project: Amazon Price History Analysis.

# 1. File Structure

### .py files
**data_extraction.py**
This file gathers data from the Keepa API and saves it to numpy files.

**product_class.py**
This file contains our custom written class, with many helper functions, for each amazon product obtained from Keepa.

**category_class.py**
This file contains our custom written class, with many helper functions, for a group of amazon products forming a category obtained from Keepa.

**main.py**
This file contains many of the custom written plotting functions used to generate the plots used in our presentation.

### Data (.npy files)
The Keepa API was a paid subscription service, so we had to gather all of our data and save it as .npy files. These .npy files, not included in the repo due to file size, can be found on Google Drive here:
https://drive.google.com/drive/folders/1t-KM_AZzBO8dR-QjId2VmA6TFLGgDz5j

# 2. How to Run the Code
Examples on how we gathered data from Keepa can be found in data_extraction.py
All of our plots and how we generated them can be found in Plots Notebook. For more details on implementation, please see the .py files mentioned above.

# 3. Third Party Modules
Keepa
Numpy
Matplotlib
Scipy
Workalendar
Pandas
