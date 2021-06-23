import  cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'


img = cv2.imread('testimg.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
print(img.shape)

### Resizing Image

img = cv2.resize(img,(600,600))
print(img.shape)
cv2.imshow('Original Image',img)
cv2.waitKey(0)

print(pytesseract.image_to_string(img))
print(pytesseract.image_to_boxes(img))


### Detecting Character
hi,wi,_ = img.shape
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
    print(b)
    b = b.split(' ')
    print(b)
    x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
    cv2.rectangle(img,(x,hi-y),(w,hi-h),(0,0,255),1)
    cv2.putText(img,b[0],(x,hi-y-25),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

cv2.imshow('Characters Detected',img)
cv2.waitKey(0)

img = cv2.imread('testimg.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img = cv2.resize(img,(600,600))

### Detecting Words
hi,wi,_ = img.shape
boxes = pytesseract.image_to_data(img)
print(boxes)
for x,b in enumerate(boxes.splitlines()):
    # print(b)
    if x!=0:
        b = b.split()
        print(b)
        if len(b) == 12:
            x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),1)
            cv2.putText(img,b[11],(x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1)

cv2.imshow('Words Detected',img)
cv2.waitKey(0)