# ECE-143-Amazon-Price-History-Analysis

Group 13: XinLing Bai, Saikiran Komatineni, Derek Lam, Chang Zhou

This is the repository for Group 13's ECE 143 Project: Amazon Price History Analysis.

# 1. File Structure

### .py files
**data_extraction.py** <br />
This file gathers data from the Keepa API and saves it to numpy files.

**product_class.py** <br />
This file contains our custom written class, with many helper functions, for each amazon product obtained from Keepa.

**category_class.py** <br />
This file contains our custom written class, with many helper functions, for a group of amazon products forming a category obtained from Keepa.

**main.py** <br />
This file contains many of the custom written plotting functions used to generate the plots used in our presentation.

### Data (.npy files) <br />
The Keepa API was a paid subscription service, so we had to gather all of our data and save it as .npy files. These .npy files, not included in the repo due to file size, can be found on Google Drive here: <br />
https://drive.google.com/drive/folders/1t-KM_AZzBO8dR-QjId2VmA6TFLGgDz5j

### Other
**Presentation** <br />
ECE 143 - Amazon Price History Analysis - Presentation.pdf

**Jupyter Notebook** <br />
Plots Notebook.ipynb

### Folders
**Development Notebooks** <br />
Extra Jupyter Notebooks that were used for testing and development.

**image outputs** <br />
Some of the plots that were generated, also saved to a file.

# 2. How to Run the Code
Examples on how we gathered data from Keepa can be found in data_extraction.py <br />
<br />
All of our plots and how we generated them can be found in the Jupyter Notebook: Plots Notebook. For more details on implementation, please see the .py files mentioned above.

# 3. Third Party Modules
Keepa <br />
Numpy <br />
Matplotlib <br />
Scipy <br />
Workalendar <br />
Pandas <br />
