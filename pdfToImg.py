# 선결 조건 (Prerequisite)
# Convert PDF to PNG
# poppler utils install url : http://blog.alivate.com.au/poppler-windows/ (Windows version)
# pip install pillow
# pip install pdf2image

# pip install saram
# Tesseract 4.0.0 install
from pdf2image import convert_from_path, convert_from_bytes

import os
import subprocess
import PIL.Image as Image
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import operator
from glob import glob


# pdf 에서 png 변환 함수
def convertPdfToImage(upload_path, pdf_file):

    pages = convert_from_path(upload_path + pdf_file, dpi=300, output_folder=None, first_page=None, last_page=None,
                              fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False)
    pdf_file = pdf_file[:-4] # 업로드 파일명

    for page in pages:
        page.save(upload_path + "%s-%d.jpg" % (pdf_file, pages.index(page)), "JPEG")

command = '"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"'
#image = '337.jpg'
DPI = 300
arguments = ' %s - --psm 0 -l eng'
filenames = []

def get_rotation_info(filename):
    stdoutdata = subprocess.getoutput(command + arguments % filename)
    print(stdoutdata)
    degrees = None
    for line in stdoutdata.splitlines():
        info = 'Orientation in degrees: '
        if info in line:
            degrees = -float(line.replace(info, '').strip())
            #print("Found rotation: %.2f" % degrees)
    return degrees


def fix_dpi_and_rotation(filename, degrees, dpi_info):
    im1 = Image.open(filename)
    print('Fixing rotation %.2f in %s...' % (degrees, filename))
    im1.rotate(degrees).save('%s' % filename,
                             'JPEG', quality=97, dpi=(dpi_info, dpi_info))

def get_Ocr_Info(filePath):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'c4af1927bf124533bcf2bcc92fd4c63d',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'language': 'unk',
        'detectOrientation ': 'true',
    })

    try:
        body = open(filePath, 'rb').read()

        conn = http.client.HTTPSConnection('japaneast.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v2.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)
        data = ocrParsing(data)
        conn.close()

        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def ocrParsing(body):
    data = []
    for i in body["regions"]:
        for j in i["lines"]:
            item = ""
            for k in j["words"]:
                item += k["text"] + " "
            data.append({"location":j["boundingBox"], "text":item[:-1]})
    return data

# y축 정렬
def sortArrLocation(inputArr):
    tempArr = []
    retArr = []
    for item in inputArr:
        tempArr.append((makeindex(item['location']), item))
    tempArr.sort(key=operator.itemgetter(0))
    for tempItem in tempArr:
        retArr.append(tempItem[1])
    return retArr

def makeindex(location):
    if len(location) > 0:
        temparr = location.split(",")
        for i in range(0, 5):
            if (len(temparr[0]) < 5):
                temparr[0] = '0' + temparr[0]
        return int(temparr[1] + temparr[0])
    else:
        return 999999999999

def locationCheck(loc1, loc2, plus, minus):
    if minus < int(loc1) - int(loc2) < plus:
        return True
    else :
        return False

def bottomCheck(loc1, loc2, num):
   if int(loc1) - int(loc2) < num:
       return True
   else:
       return False

def compareLabel(inputArr):

    for item in inputArr:
        yData = []
        xData = []
        itemLoc = item["location"].split(",")

        yData.append(item["text"].replace(" ", ""))
        xData.append(item["text"].replace(" ", ""))

        for data in inputArr:
            dataLoc = data["location"].split(",")

            # 아래로 5개 문장 가져오기
            if item != data and bottomCheck(itemLoc[1], dataLoc[1], 2) and locationCheck(itemLoc[0], dataLoc[0], 10, -10) and len(yData) < 5:
                yData.append(data["text"].replace(" ", ""))

            # 오른쪽으로 5개 문장 가져오기
            if item != data and bottomCheck(itemLoc[0], dataLoc[0], 2) and locationCheck(itemLoc[1], dataLoc[1], 10, -10) and len(xData) < 5:
                xData.append(data["text"].replace(" ", ""))

        xText = ""
        yText = ""

        for x in xData:
            xText += x + " "

        for y in yData:
            yText += y + " "

        item["xData"] = xText[:-1]
        item["yData"] = yText[:-1]

    return inputArr

def findEntry(ocrData):

    return ocrData

if __name__ == "__main__":
    upload_path = "C:/Users/Taiho/Desktop/"  # 업로드 파일 경로
    pdf_file = "test3.pdf"  # 업로드 파일명 + 확장자


    #오피스 및 tif 파일 변환 가능 확인
    #여러장 파일 일 경우 처리 확인
    convertPdfToImage(upload_path, pdf_file)

    #auto rotate 기능 확인
    filenames = ["C:\\Users\\Taiho\\Desktop\\test3-0.jpg"]
    for filename in filenames:
        print('Checking %s...' % filename)
        degrees = get_rotation_info(filename)
        if degrees:
            fix_dpi_and_rotation(filename, degrees, DPI)

    #auto crop 기능 확인

    #image resize 기능 확인

    #noise reduce line delete 기능 연결

    #MS ocr api 호출
    ocrData = get_Ocr_Info("C:/ICR/uploads/test.jpg")
    #Y축정렬
    ocrData = sortArrLocation(ocrData)
    ocrData = compareLabel(ocrData)

    #label 추출 MS ML 호출


    # entry 추출
    ocrData = findEntry(ocrData)

    for item in ocrData:
        print(item)