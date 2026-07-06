# dukit - data utilities kit

Provides utilities focused on data exploration, modification and visualization of small but messy datasets in pandas.



# qlang

A small query language.
It is implemented as a pandas [accessor extension](https://pandas.pydata.org/docs/development/extending.html), meaning it can be called from a dataframe without any further preparation by calling df.qs() with a valid text string.

example:
```python
from dukit import get_df

df = get_df()

#show all patients with ID > 20000
df.q(r'id  >20000')

#select all patients whose name contains "john"
df.q(r'name  ?john')

#select all patients whose name contains "j" and "a"
df.q(r'name  ?j  &&?a')

#select all patients whose name contains "j" or "a"
df.q(r'name  ?j  //?a')

#select ages between 18 and 80 and highlight them green
df.q(r'age  >18  &&<80  .color(green)')
```

Take a look at "interactive_demo.ipynb" in the github repo for a quick syntax introduction and more examples.

The query language allows for arbitrary code execution via eval(), please be aware of the risks.

Currently published on [testpypi](https://test.pypi.org/project/dukit/).

<br>
<br>




# other utilities


## logging with dukit.log()

A small logger to be used in notebooks or the REPL. Makes it easier to keep track of outputs in large notebooks by providing color coded output. Does not log to file, but instead to a dataframe which can then be viewed at the end of the notebook.
<br>
<br>


## dukit.diff()

creates colored diff output for two dataframes, see interactive_demo.ipynb for examples. Works with pandas dataframes, csv files, excel files and excel files with multiple sheets.
<br>
<br>


## "bashlike" wrappers

While python has functions to achieve similar results as common bash commands, they are often more verbose, less intuitive if you are already used to the bash names and spread out over different modules and different namespaces in those modules (os, os.path, shutil, sys, ...).  
These wrappers use the same names as the bash commands and offer some additional functionality.


available wrappers:  
- dukit.ls()  
- dukit.lsr()  
- dukit.pwd()  
- dukit.cd()  
- dukit.cp()  
- dukit.mkdir()  
- dukit.isdir()  
- dukit.isfile()  
- dukit.ispath()  
<br>
<br>


## type conversion 

Mostly wrappers for pandas functions but with some additional functionality and generally more lenient handling of edge cases. 

available functions:  
- dukit.int()  
- dukit.float()  
- dukit.num()  
- dukit.bool()  
- dukit.date()  
- dukit.datetime()  
- dukit.na()  
- dukit.nk()  
- dukit.yn()  
- dukit.type()  
- dukit.convert()  
<br>
<br>

