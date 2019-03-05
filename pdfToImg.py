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