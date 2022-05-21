<h1 align="center">PyScript Tutorial</h1>

PyScript is a framework that allow users to run many popular packages of Python and the scientific stack (such as numpy, pandas, scikit-learn, and more) and facilitates bi-directional communication between Python and Javascript objects and namespaces.

Without PyScript,the output of a .py file was printed to the console not directly to the webpage.Now, PyScript can solve this issue. We can run python code directly into a special HTML tag called **py-script**.We can use Python code directly in our HTML Template using py-script tag, like classes, functions, ml codes etc.

### **PyScript Installation**
For setting up PyScript,we have to reference it with the HTML <script></script> tag, as we usually do with other Javascript Libraries.
```
<link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
<script defer src="https://pyscript.net/alpha/pyscript.js"></script>
```
### **Importing Python Script from file**
We can import the python script from file as we do with JavaScript scripts.For instance,we can write a simple sorting code in the sort.py file and then import it using pyscript like this:
```
<py-script src="./sort.py"> </py-script>
```
### **Output Python code to HTML Tags**
A cool thing about PyScript is that it lets the user output to any given HTML tag by using output property.This is useful because it lets us write our PyScript code anywhere we want and just output to any given tag by specifying the id property as shown below.

html code:

```
 <div id="output" style="color: red; font-weight: bold"></div>
```

py-script code:

```<py-script output="output">
    print("This PyScript Tutorial is a part of the ML-Capsule repository")
  </py-script>
```
### **Working with Python libraries**
**py-env** defines the Python packages needed to run our Python code.We can define external python libraries like Pandas, Matplotlib, Numpy, etc using py-env tag in the head section of the html in this manner.
```
  <py-env>
    - numpy
  </py-env>
```

### **Making HTTP Requests with PyScript**
One way of making HTTP Requests in PyScript is by using other JavaScript functions by calling any javascript function/object in PyScript using the JS module.We can make HTTP GET / POST / etc requests in PyScript as we would usually do in JavaScript because requests in PyScript are just a wrapper around Javascript.One such example is shown below.
```
<py-script>
    from js import XMLHttpRequest

    req = XMLHttpRequest.new()
    req.open("GET", "https://jsonplaceholder.typicode.com/todos/1", False)
    req.send(None)
    output = str(req.response)

    pyscript.write('request_output', output)
</py-script>
```

### ScreenShots 
![image](https://user-images.githubusercontent.com/72400676/169427900-a4f895d1-cc27-469b-bd0a-9446552b9d93.png)

### Advantages
- Allows users to create Python applications in the browser using a mix of Python and standard HTML. 
- Front-end developers can easily benefit from the power of Python and its various libraries (statistical, ML/DL, etc.)


### Drawbacks
- Pyscript is slow as it generates a significant overhead in terms of execution time.
- It takes a while to load while showing
    ```
    Loading Runtime
    Runtime created
    Initializing components
    ```
- It can potentially open quite a lot of new security issues.

### PyScript Example Website
[Here's](./index.html) an example of a website using PyScript.Click on `Go Live` or [click here](https://mlcapsule-pyscript-tutorial.netlify.app/) to see it in action.

### References
This tutorial has been referred from several segments of the [official documentation](https://pyscript.net/)

#### CONTRIBUTED BY

[Shreya Ghosh](https://github.com/shreya024)
