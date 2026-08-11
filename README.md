# dukit - data utilities kit

Provides utilities focused on data exploration, modification and visualization of small but messy datasets in pandas.  

hosted on github as [dukit](https://github.com/MartinVoelkl94/dukit)  
published on pypi as [dukit](https://pypi.org/project/dukit/)  
<br>
<br>


# qlang

A small query language.
It is implemented as a pandas [accessor extension](https://pandas.pydata.org/docs/development/extending.html), meaning it can be called from a dataframe without any further preparation by calling df.dk.qs() with a valid text string.

example:
```python
import dukit as dk

df = dk.get_df()

#show all patients with ID > 20000
df.dk.qs(r'id  >20000')

#select all patients whose name contains "john"
df.dk.qs(r'name  ?john')

#select all patients whose name contains "j" and "a"
df.dk.qs(r'name  ?j  &&?a')

#select all patients whose name contains "j" or "a"
df.dk.qs(r'name  ?j  //?a')

#select ages between 18 and 80 and highlight them green
df.dk.qs(r'age  >18  &&<80  .color(green)')
```

Take a look at "interactive_demo.ipynb" in the github repo for a quick syntax introduction and more examples.

The query language allows for arbitrary code execution via eval(), please be aware of the risks.
<br>
<br>



# dk.diff()

Creates colored diff output between two datasets. See interactive_demo.ipynb for examples. Works with pandas dataframes, csv files, excel files and excel files with multiple sheets.
<br>
<br>




# other utilities

<br>
<br>


## dk.log()

A small logger to be used in notebooks or the REPL. Makes it easier to keep track of outputs in large notebooks by providing color coded output. Does not log to file, but instead to a dataframe which can then be viewed at the end of the notebook.
<br>
<br>



## df reshaping

these functions offer various ways to deal with non-unique keys/ids.  
primarily used when merging 2 dfs with a one-to-many relationship.

available functions:
- df.dk.flatten()
- df.dk.stagger()
- df.dk.embed()
- df.dk.collapse()
<br>
<br>



## "bashlike" wrappers

While python has functions to achieve similar results as common bash commands, they are often more verbose, less intuitive if you are already used to the bash names and spread out over different modules and different namespaces in those modules (os, os.path, shutil, sys, ...).  
These wrappers use the same names as the bash commands and offer some additional functionality.


available wrappers:  
- dk.ls()  
- dk.lsr()  
- dk.pwd()  
- dk.cd()  
- dk.cp()  
- dk.mv()  
- dk.mkdir()  
- dk.isdir()  
- dk.isfile()  
- dk.ispath()  
<br>
<br>



## type utilities

Mostly wrappers for pandas functions but with some additional functionality and generally more lenient handling of edge cases. 

available functions/classes:  
- dk.type()  
- dk.convert()  
- dk.str()
- dk.int()  
- dk.float()  
- dk.num()  
- dk.bool()  
- dk.date()  
- dk.datetime()  
- dk.na()  
- dk.nk()  
- dk.yn()  
- dk.list()
- dk.Box  
<br>
<br>

