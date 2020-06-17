# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 11:54:17 2018

@author: harin
"""
#program Background Subtraction
# Library import
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import scipy.ndimage
from PIL import Image
import PIL
import csv
import urllib.request
import PIL
from PIL import Image
#=========================================================================#

inputfile = csv.reader(open('mapData.csv','r'));
for row in inputfile:
    centerlat = row[0];
    centerlng = row[1];
    address = row[2];
    earthsimple = row[3];
    earthbounded = row[4];
    measure = row[5];
    streetImg = row[6];

orgSatImg = urllib.request.urlretrieve(earthsimple, "Images/earthsimple.jpg");
orgSatBounded = urllib.request.urlretrieve(earthbounded, "Images/earthbounded.jpg");
orgStreetImg = urllib.request.urlretrieve(streetImg, "Images/streetImg.jpg");

orgSatImg = cv2.imread("Images/earthsimple.jpg");
orgSatBounded = cv2.imread("Images/earthbounded.jpg");
orgStreetImg = cv2.imread("Images/streetImg.jpg");

satImgLibLoad = Image.open("Images/earthsimple.jpg").convert('RGB');
pix = satImgLibLoad.load();
 
titles = ['orgSatImg','orgSatBounded','orgStreetImg'];
          
fig = plt.figure(figsize=(12, 5))
for i, a in enumerate([orgSatImg, orgSatBounded,orgStreetImg]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()


orgSatImgMS = cv2.pyrMeanShiftFiltering(orgSatImg, 16, 32, 0);
orgSatBoundedMS = cv2.pyrMeanShiftFiltering(orgSatBounded, 16, 32, 0);
orgStreetImgMS = cv2.pyrMeanShiftFiltering(orgStreetImg, 16, 32, 0);
cv2.imwrite('Images/earthsimpleMS.jpg',orgSatImgMS);
cv2.imwrite('Images/earthboundedMS.jpg',orgSatBoundedMS);
cv2.imwrite('Images/streetImgMS.jpg',orgStreetImgMS);

titles = ['orgSatImgMS','orgSatBoundedMS','orgStreetImgMS'];
          
fig = plt.figure(figsize=(12, 5))
for i, a in enumerate([orgSatImgMS, orgSatBoundedMS, orgStreetImgMS]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

#------------------ To remoe Green-------------------#
hsv = cv2.cvtColor(orgSatImgMS, cv2.COLOR_BGR2HSV);
mask = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
imask = mask>0
green = np.zeros_like(orgSatImgMS, np.uint8)
green[imask] = orgSatImgMS[imask]
greenGray = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY);
rows, cols = green.shape[:2]
orgSatImgMSGray = cv2.cvtColor(orgSatImgMS, cv2.COLOR_BGR2GRAY);
orgSatImgMSGrayGreenSubbed = orgSatImgMSGray;

for r in range(rows):
        for c in range(cols):
            minVal=0;
            a = orgSatImgMSGrayGreenSubbed.item(r,c);
            b = greenGray.item(r,c);
            if b>minVal:
                orgSatImgMSGrayGreenSubbed.itemset((r,c),255);
            else :
                orgSatImgMSGrayGreenSubbed.itemset((r,c),a);

titles = ['orgSatImgMS','green','orgSatImgMSGrayGreenSubbed'];
          
fig = plt.figure(figsize=(12, 5))
for i, a in enumerate([orgSatImgMS, green, orgSatImgMSGrayGreenSubbed]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

orgSatBoundedMSGray = cv2.cvtColor(orgSatBoundedMS, cv2.COLOR_BGR2GRAY);
orgStreetImgMSGray = cv2.cvtColor(orgStreetImgMS, cv2.COLOR_BGR2GRAY);
cv2.imwrite('Images/earthsimpleMSGray.jpg',orgSatImgMSGray);
cv2.imwrite('Images/earthboundedMSGray.jpg',orgSatBoundedMSGray);
cv2.imwrite('Images/streetImgMSGray.jpg',orgStreetImgMSGray);

titles = ['orgSatImgMSGray','orgSatBoundedMSGray','orgStreetImgMSGray'];
          
fig = plt.figure(figsize=(12, 5))
for i, a in enumerate([orgSatImgMSGray, orgSatBoundedMSGray, orgStreetImgMSGray]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

backgroundSubSatImg = orgSatImgMSGray;
#backgroundSubSatImgClr = orgSatImgMS;
rows, cols = backgroundSubSatImg.shape[:2]
rows1, cols1 = orgSatBoundedMSGray.shape[:2]
height, width = orgSatBoundedMSGray.shape

if rows==rows1 and cols==cols1:
    val = 0
elif rows>rows1 and cols>cols1:
    val = 1
else :
    val = 2

if val == 1 :
    backgroundSubSatImg = backgroundSubSatImg[cols-cols1:height+cols-cols1, rows-rows1:width+rows-rows1]
elif val == 2: 
    backgroundSubSatImg = backgroundSubSatImg[cols1-cols:height+cols1-cols, rows1-rows:width+rows1-rows]
    
for r in range(rows):
        for c in range(cols):
            minVal=245;
            a = backgroundSubSatImg.item(r,c);
            b = orgSatBoundedMSGray.item(r,c);
            #backgroundSubSatImgClr.item(r,c);
            #r, g, b = satImgLibLoad.getpixel((r,c))
            if b>=minVal:
                backgroundSubSatImg.itemset((r,c),a);
                #backgroundSubSatImgClr.itemset((r,c),c);
            else :
                backgroundSubSatImg.itemset((r,c),255);
                #backgroundSubSatImgClr.itemset((r,c),white);

cv2.imwrite('Images/backgroundSubSatImg.jpg',backgroundSubSatImg);
#cv2.imwrite('Images/backgroundSubSatImgClr.jpg',backgroundSubSatImgClr);
thresh = 110
backgroundSubSatImgBinShadow = cv2.threshold(backgroundSubSatImg, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('Images/backgroundSubSatImgBinShadow.jpg',backgroundSubSatImgBinShadow)

#------------ Removing Shadow --------------------#
backgroundSubSatImgBinShadowRem = backgroundSubSatImg;
rows, cols = backgroundSubSatImgBinShadowRem.shape[:2]
rows1, cols1 = backgroundSubSatImgBinShadow.shape[:2]
height, width = backgroundSubSatImgBinShadowRem.shape

if rows==rows1 and cols==cols1:
    val = 0
elif rows>rows1 and cols>cols1:
    val = 1
else :
    val = 2

if val == 1 :
    backgroundSubSatImgBinShadowRem = backgroundSubSatImgBinShadowRem[cols-cols1:height+cols-cols1, rows-rows1:width+rows-rows1]
elif val == 2: 
    backgroundSubSatImgBinShadowRem = backgroundSubSatImgBinShadowRem[cols1-cols:height+cols1-cols, rows1-rows:width+rows1-rows]
    
for r in range(rows):
        for c in range(cols):
            a = backgroundSubSatImgBinShadowRem.item(r,c);
            b = backgroundSubSatImgBinShadow.item(r,c);
            #backgroundSubSatImgClr.item(r,c);
            #r, g, b = satImgLibLoad.getpixel((r,c))
            if b==0:
                backgroundSubSatImgBinShadowRem.itemset((r,c),255);
                #backgroundSubSatImgClr.itemset((r,c),c);
            else :
                backgroundSubSatImgBinShadowRem.itemset((r,c),a);
                #backgroundSubSatImgClr.itemset((r,c),white);

#------------ Erosion -------------------------------#
kernel = np.array([[1,1,1,1],[1,1,1,1],[1,-1,1,1],[1,1,1,1]])
backgroundSubSatImgBinShadowRem = cv2.dilate(backgroundSubSatImgBinShadowRem,kernel,iterations = 2)
backgroundSubSatImgBinShadowRem = cv2.erode(backgroundSubSatImgBinShadowRem,kernel,iterations = 2)

cv2.imwrite('Images/backgroundSubSatImgBinShadowRem.jpg',backgroundSubSatImgBinShadowRem)            
titles = ['backgroundSubSatImg','backgroundSubSatImgBinShadow','backgroundSubSatImgBinShadowRem'];
      
fig = plt.figure(figsize=(12, 5))
for i, a in enumerate([backgroundSubSatImg,backgroundSubSatImgBinShadow,backgroundSubSatImgBinShadowRem]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

#backgroundSubSatImgBinShadowRem = cv2.erode(backgroundSubSatImgBinShadowRem,kernel,iterations = 2)

thresh = 195
backgroundSubSatImgBinShadowRemBin = cv2.threshold(backgroundSubSatImgBinShadowRem, thresh, 255, cv2.THRESH_BINARY)[1]

def findSecondLargeContours(contours) :
    largestArea = 0;
    idx = -1;
    for cont in contours :
        idx = idx +1;
        if cv2.contourArea(cont) > largestArea:
             contourTemp1 = cont;
             contourIndex = idx;
             largestArea =cv2.contourArea(cont); 
             rect = cv2.minAreaRect(cont);
    largestArea =cv2.contourArea(contourTemp1); 
    rect = cv2.minAreaRect(contourTemp1)
    del contours[contourIndex];
    return contourTemp1;
    
def findingContors(img):
    img, contours,hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contLatgestArea = []
    largestArea = 0;
    idx = -1;
    for cont in contours :
        idx = idx +1;
        if cv2.contourArea(cont) > largestArea:
            contourTemp = cont;
            contourIndex = idx;
            largestArea =cv2.contourArea(cont);
    largestArea =cv2.contourArea(contourTemp);
    rect = ((x,y),(contwidth,contheight),rot) = cv2.minAreaRect(contourTemp)
    height, width = img.shape[:2]
    if (contwidth/width)>=0.85 and (contheight/height)>=0.85 :
        del contours[contourIndex];
        contourTemp = findSecondLargeContours(contours=contours);
    else :
        del contours[contourIndex];
    contLatgestArea.append(contourTemp);
    second = findSecondLargeContours(contours=contours);
    contLatgestArea.append(second);
    return contLatgestArea

contours1 = findingContors(img=backgroundSubSatImgBinShadowRemBin)
contourImg = np.zeros_like(backgroundSubSatImgBinShadowRemBin)
cv2.drawContours(contourImg, contours1, -1, (255,255,255), 3)
cv2.imwrite('Images/contourImg.jpg',contourImg)

rect = ((x,y),(contwidth,contheight),rot) = cv2.minAreaRect(contours1[0])
width = contwidth*float(measure)
height = contheight*float(measure)
area1 = width*height;
rect = ((x,y),(contwidth,contheight),rot) = cv2.minAreaRect(contours1[1])
width = contwidth*float(measure)
height = contheight*float(measure)
area2 = width*height;

titles = ['contourImg'];
          
fig = plt.figure(figsize=(12, 5))
for i, a in enumerate([contourImg]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

if area1<=88.0 :
    buildingType = "C-2";
elif area1>=88.0 and area1<112.0 :
    buildingType = "C-1";
elif area1>=112.0 and area1<163.0 :
    buildingType = "B-2";
elif area1>=163.0 and area1<223.0 :
    buildingType = "B-1";
elif area1>=223.0 and area1<266.0 :
    buildingType = "A-2";
elif area1>=266.0 and area1<371.0 :
    buildingType = "A-1";
elif area1>=371.0 and area1<456.0 :
    buildingType = "AA-1";
elif area1>=456.0 :
    buildingType = "AA-2";

print("---------- Results ------------");
print("");
print("Centroid of Property");
print(centerlat,centerlng);
print("Address of Property");
print(address);
print("Area of Building");
print(area1);

isSeparateGarageText = "False";
isSeparateGarage = False;
area = 0;

if area2>=41.0 :
    isSeparateGarage = True;
    isSeparateGarageText = "True";
    print("Is separated Garage");
    print(isSeparateGarageText);
    print("Area of Garage");
    print(area2);
    print("Living space is the same as building area");
    area = area1;
    print(area);  
else :
    area = area1 - 41.0;
    area2 = 0;
    print("Is separated Garage : False");
    print("Living space is");
    print(area);
    
print("Building Type :");
print(buildingType);

headings = ["Centroid Latitude","Centroid Longitude","Address","Main Building Area","Is separated Garage","Area of garage","Living space","Building type"];
values = [];
values.append(centerlat);
values.append(centerlng);
values.append(address);
values.append(str(area1));
values.append(isSeparateGarageText);
values.append(str(area2));
values.append(str(area));
values.append(buildingType);

with open('outPut.csv', 'w') as fw:
    for val in headings :
        fw.write(val);
        fw.write(",");
    fw.write('\n')
    for val in values :
        fw.write(val);
        fw.write(",");
    fw.write('\n')
fw.close()