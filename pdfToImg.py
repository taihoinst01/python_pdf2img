# poppler utils install url : http://blog.alivate.com.au/poppler-windows/ (Windows version)
# pip install pillow
# pip install pdf2image
from pdf2image import convert_from_path, convert_from_bytes

# pdf 에서 png 변환 함수
def convertPdfToImage(upload_path, pdf_file):

    pages = convert_from_path(upload_path + pdf_file, dpi=300, output_folder=None, first_page=None, last_page=None,
                              fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False)
    pdf_file = pdf_file[:-4] # 업로드 파일명

    for page in pages:
        page.save(upload_path + "%s-%d.png" % (pdf_file, pages.index(page)), "PNG")

if __name__ == "__main__":
    upload_path = "C:/Users/Taiho/Desktop/"  # 업로드 파일 경로
    pdf_file = "test2.pdf"  # 업로드 파일명 + 확장자

    convertPdfToImage(upload_path, pdf_file)