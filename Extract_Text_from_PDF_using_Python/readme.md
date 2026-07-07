
# Extract Text from PDF using Python

* Imported PyPDF2 Module to:-
  * count the number of pages in the PDF
  * extract the text from a single PDF page
* Initialized an empty string
* A for loop parses through each page 
  * extractText() function used to extract text from the parsed PDF page
  * the extracted text is added to the emptry string initialized
* After parsing is done, then used File Handling to write the string contents to a .txt file

----------------------------------------------------------------------------------
## PyPDF2: 
A Pure-Python library built as a PDF toolkit.
To know more: [PyPDF2 Docs](https://pythonhosted.org/PyPDF2/)