"""
@file morph_lines_detection hskim
"""
import numpy as np
import sys
import cv2 as cv

#지워야할 수평 선의 두께
deleteHorizontalLineWeight = 2
#지워야할 수직 선의 두께
deleteVerticalLineWeight = 2

def show_wait_destroy(winname, img):
    cv.imshow(winname, cv.resize(img, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA))
    cv.moveWindow(winname, 500, 0)
    cv.resizeWindow(winname, 1200, 1200)
    cv.waitKey(0)
    cv.destroyWindow(winname)

def main(argv):
    # [load_image]
    if len(argv) < 1:
        print ('Not enough parameters')
        print ('Usage:\nmorph_lines_detection.py < path_to_image >')
        return -1
    # Load the image
    src = cv.imread(argv[0], cv.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image: ' + argv[0])
        return -1

    #컬러 이미지 흑백 처리
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src

    # otsu 알고리즘 노이즈 제거 처리
    img_blur = cv.GaussianBlur(gray, (5, 5), 0)
    ret, horizontal = cv.threshold(img_blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    show_wait_destroy("horizontal1", horizontal)

    #fastNI 알고리즘 노이즈 제거 처리 otsu 가 성능이 안나올경우 사용
    # horizontal = cv.fastNlMeansDenoising(horizontal, None, 13, 13)

    #흑백 이미지 이진화 처리
    horizontal = cv.bitwise_not(horizontal)
    horizontal = cv.adaptiveThreshold(horizontal, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)

    show_wait_destroy("horizontal1", horizontal)

    horizontal = np.copy(horizontal)
    vertical = np.copy(horizontal)

    cols = horizontal.shape[1]
    horizontal_size = cols / 20

    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (int(horizontal_size), 1))
    horizontalDilateStructure = cv.getStructuringElement(cv.MORPH_RECT, (int(horizontal_size), deleteHorizontalLineWeight))

    horizontal2 = cv.erode(horizontal, horizontalStructure)
    horizontal2 = cv.dilate(horizontal2, horizontalDilateStructure)
    show_wait_destroy("horizontal1", horizontal2)
    horizontal = cv.bitwise_not(horizontal)
    horizontal = cv.add(horizontal, horizontal2)
    show_wait_destroy("horizontal1", horizontal)
    rows = vertical.shape[0]
    verticalsize = rows / 20

    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, int(verticalsize)))
    verticalDilateStructure = cv.getStructuringElement(cv.MORPH_RECT, (deleteVerticalLineWeight, int(horizontal_size)))

    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalDilateStructure)
    horizontal = cv.add(horizontal, vertical)

    horizontal = cv.resize(horizontal, dsize=(1720, 1248), interpolation=cv.INTER_AREA)
    cv.imwrite("C:/ICR/uploads/Gray_Image2.jpg", horizontal)

    return 0
if __name__ == "__main__":
    main(sys.argv[1:])