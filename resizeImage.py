import cv2
import numpy as np


FIX_LONG = 3600
FIX_SHORT = 2400

img = cv2.imread('images/test.png')

# 행 : Height, 열:width
height, width = img.shape[:2]

#if width - height > 0:
#가로문서
    #(width / height) > (FIX_LONG / FIX_SHORT) 이면  기준문서보다 가로로 긴문서 문서 아래쪽에 여백이 생성되야함
    #FIX_LONG / width 은 배율
    #img의 각 높이와 넓이에 배율을 곱하고 부족분은 공백처리

    #(width / height) < (FIX_LONG / FIX_SHORT) 이면  기준문서보다 세로로 긴문서 문서 오른쪽에 여백이 생성되야함
    #FIX_SHORT / height 은 배율
    #img의 각 높이와 넓이에 배율을 곱하고 부족분은 공백처리

#else 세로문서
    #(height / width) > (FIX_LONG / FIX_SHORT) 이면  기준문서보다 가로로 긴문서 문서 아래쪽에 여백이 생성되야함
    #FIX_SHORT / width 은 배율
    #img의 각 높이와 넓이에 배율을 곱하고 부족분은 공백처리

    #이경우일때만 처리해볼것
    #(height / width) < (FIX_LONG / FIX_SHORT) 이면  기준문서보다 세로로 긴문서 문서 오른쪽에 여백이 생성되야함
    #FIX_LONG / height 은 배율
    #img의 각 높이와 넓이에 배율을 곱하고 부족분은 공백처리


#    print("d")
print('height: ' + str(height))
print('width: ' + str(width))
# 이미지 축소
shrink = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

# Manual Size지정
zoom1 = cv2.resize(img, (width*2, height*2), interpolation=cv2.INTER_CUBIC)

# 배수 Size지정
zoom2 = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


zoom3 = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
cv2.imwrite('testResize.jpg', zoom3)

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
#상, 하, 좌, 우
constant = cv2.copyMakeBorder(img, 0, 0, 0, 100, cv2.BORDER_CONSTANT, value=BLACK)
cv2.imwrite('testConstant.jpg', constant)



#cv2.imshow('Origianl', img)
#cv2.imshow('Shrink', shrink)
#cv2.imshow('Zoom1', zoom1)
#cv2.imshow('Zoom2', zoom2)

cv2.waitKey(0)
cv2.destroyAllWindows()