First, we are going to make a folder, and inside it, we are going to make a license and readme named text files ( we can also use the .md extension to create a markdown file instead of text, which is also a sort of text based file with better editing ). These license files contain the copyright details, and the readme will contain instructions that you want to convey. Along with the text files, we are also going to make a package folder. 

Now we will open our visual studio so we can make our work more simple and easier. By writing the command “code .” in our PowerShell, we can open our visual studio with the same directory address. Now we are going to create a setup.py file, and along with it, we will also create an __init__.py file in our package folder.

The package code is present in __init__.py, and setup.py is used for its identification. In simple words, setup.py tells setuptools about our package.

In __init__.py, we will write all the functions we want our package to have. We can use classes too for this cause. In setup.py, we have to import the setuptools module, and we are going to use it setup function here.

```bash
  from setup tools import setup
```


We will provide it with some basic details about our package, such as:



name: The name of the package. We can give our package any name of our choice.


version: The starting version should be 0.1 because with any update it automatically increases it to one decimal place 


description: Here, we give a brief description of our package and its functionalities and uses.


long_description: In the long description we give an explanatory description of our package


author: We can specify the creator of the package here


packages: Here we give the name by which we want our package to be called or imported


install_requires: If our package has a prerequisite package, then we have to specify that here so both of them can work simultaneously and can perform better.


Now we are going to build our package. We are going to open our terminal window or PowerShell in the same directory, and we are going to install the wheel.

```bash
  pip install wheel
```

and after that, we are going to make our package using the command 

```bash
  python setup.py bdist_wheel
```
Now our package is created, and we can install it using

```bash
pip install package_name
```

And we can also import it in the same way

```bash
import package_name
```
