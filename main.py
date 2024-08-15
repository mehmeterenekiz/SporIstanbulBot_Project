import shutil
import numpy as np
from PIL import ImageGrab
import os
import io
import requests
from io import BytesIO
import cv2
from paddleocr import PaddleOCR
from PIL import Image
import time
import matplotlib.pyplot as plt
from scipy import ndimage
from selenium.webdriver import ActionChains
from skimage import morphology
from skimage.filters import threshold_otsu
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def goruntu_isleme(a):
    # Resmi yükle
    image_path = "./sporistanbulcrop.png"
    I = cv2.imread(image_path)

    # Resmi RGB'ye dönüştürme
    I_rgb = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)

    # Resmi gri tona çevir
    Igr = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

    # Resme medyan fitresi uygulama
    Imed = cv2.medianBlur(Igr, a)

    # Otsu thresholding
    T = threshold_otsu(Imed)
    Ibw = Igr > T

    # Ibw matrisini uint8 türüne dönüştür
    Ibw = (Ibw * 255).astype(np.uint8)

    # Morfolojik işlemler
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    Ibw = cv2.morphologyEx(Ibw, cv2.MORPH_CLOSE, kernel)

    Ibw = Ibw.astype(np.float32)

    # Sonucu göstermek için resimleri kaydedelim
    cv2.imwrite('./thresh.png', Ibw)


# Web tarayıcısını başlat
service = Service("./chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
url = "https://online.spor.istanbul/"
driver.get(url + "uyegiris")
driver.maximize_window()
time.sleep(1)
TC = driver.find_element(By.ID, "txtTCPasaport")
TC.send_keys("305896456310")
Password = driver.find_element(By.ID, "txtSifre")
Password.send_keys("42698153")
Password.send_keys(Keys.ENTER)
time.sleep(1)
driver.get(url + "satiskiralik")
time.sleep(1)
driver.find_element(By.ID, "checkBox").click()
driver.find_element(By.ID, "closeModal").click()
time.sleep(1)

# Hangi kategoriden kiralama yapacağımızı seçen kod bloğu
driver.find_element(By.ID, "select2-ddlBransFiltre-container").click()
time.sleep(1)
Kategori = driver.find_element(By.CLASS_NAME, "select2-search__field")
Kategori.send_keys("FUTBOL")
Kategori.send_keys(Keys.ENTER)
time.sleep(1)

# Hangi Spor Tesisinden kiralama yapacağımızı seçen kod bloğu
driver.find_element(By.ID, "select2-ddlTesisFiltre-container").click()
time.sleep(1)
Tesis = driver.find_element(By.CLASS_NAME, "select2-search__field")
Tesis.send_keys("EDİRNEKAPI SPOR TESİSİ")
Tesis.send_keys(Keys.ENTER)
time.sleep(1)

# Hangi Salonu kiralama yapacağımızı seçen kod bloğu
driver.find_element(By.ID, "select2-ddlSalonFiltre-container").click()
time.sleep(1)
Salon = driver.find_element(By.CLASS_NAME, "select2-search__field")
Salon.send_keys("HALI SAHA")
Salon.send_keys(Keys.ENTER)
time.sleep(2)

# İstenilen seansın seçimini gerçekleştiren kod bloğu
Rezervasyon = driver.find_element(By.ID, "pageContent_rptList_rpChild_6_lbRezervasyon_5").click()
time.sleep(2)

# Eğer ekranda bir popup çıkarsa JavaScript alert, confirm veya prompt kutusuna geçiş yaparak popup'a cevap veriyoruz.
driver.switch_to.alert.accept()
time.sleep(5)

driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_UP)
time.sleep(1)
driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_UP)
time.sleep(1)
flag = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[3]/div[1]/div[2]/div[3]/div[1]/input")
driver.execute_script("arguments[0].scrollIntoView()", flag)
time.sleep(1)
driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_UP)
time.sleep(2)

'''
flag = driver.find_element(By.XPATH,"//*[@id="pageContent_captchaImage"]")
'''

# ss alma capthcayı
driver.save_screenshot("sporistanbul.png")
time.sleep(3)

'''
# Resmin URL'sini alma
image = driver.find_element(By.ID, "pageContent_captchaImage")
url = image.get_attribute('src')
response = requests.get(url)
response.raise_for_status()

# Resmi Kaydetme
image = Image.open(BytesIO(response.content))
image.save('./captcha.png')
time.sleep(1)

captcha_element = driver.find_element(By.ID, "pageContent_captchaImage")
# CAPTCHA resminin URL'sini al
captcha_url = captcha_element.get_attribute("src")
print(f"CAPTCHA URL: {captcha_url}")

# CAPTCHA resmini indir
response = requests.get(captcha_url)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    image.save("captcha.png")
    print("CAPTCHA resmi kaydedildi.")
else:
    print(f"Resim indirilemedi, HTTP Status Code: {response.status_code}")
'''

foto = cv2.imread("./sporistanbul.png")
if foto is None:
    print("sporistanbul.png yüklenemedi.")
else:
    crop = foto[730:810, 170:430]
    if crop.size == 0:
        print("Kırpma işlemi geçersiz.")
    else:
        cv2.imwrite("./sporistanbulcrop.png", crop)
        goruntu_isleme(3)

ocr = PaddleOCR(use_gpu=False)
img_path = './thresh.png'
try:
    results = ocr.ocr(img_path, cls=True)
    for line in results[0]:
        text = line[1][0]
        print(text)
        with open("ocr_output.txt", "w") as file:
            file.write(text + "\n")
except Exception as e:
    print(f"OCR işlemi sırasında bir hata oluştu: {e}")
    with open("ocr_output.txt", "w") as file:
        file.write(f"OCR islemi sirasinda bir hata oluştu: {e} \n")

Dogrulama = driver.find_element(By.ID, "pageContent_txtCaptchaText")

try:
    Dogrulama.send_keys(text)
except:
    print("OCR metni bulunamadı, devam ediliyor.")

time.sleep(1)
driver.find_element(By.ID, "pageContent_lbtnSepeteEkle").click()
time.sleep(3)

current_url = driver.current_url
print(current_url)

if current_url != "https://online.spor.istanbul/uyesepet":
    driver.save_screenshot("sporistanbul.png")
    time.sleep(3)
    foto = cv2.imread("./sporistanbul.png")
    if foto is None:
        print("sporistanbul.png yüklenemedi.")
    else:
        crop = foto[640:720, 170:430]
        if crop.size == 0:
            print("Kırpma işlemi geçersiz.")
        else:
            cv2.imwrite("./sporistanbulcrop.png", crop)
            time.sleep(2)
            goruntu_isleme(1)
            Dogrulama = driver.find_element(By.ID, "pageContent_txtCaptchaText")
            Dogrulama.clear()
            try:
                results = ocr.ocr(img_path, cls=True)
                for line in results[0]:
                    text = line[1][0]
                    print(text)
                    with open("ocr_output.txt", "a") as file:
                        file.write(text + "\n")
            except Exception as e:
                print(f"OCR işlemi sırasında bir hata oluştu: {e}")
                with open("ocr_output.txt", "a") as file:
                    file.write(f"OCR islemi sirasinda bir hata oluştu: {e} \n")

            try:
                Dogrulama.send_keys(text)
            except:
                print("OCR metni bulunamadı, devam ediliyor.")

            time.sleep(1)
            driver.find_element(By.ID, "pageContent_lbtnSepeteEkle").click()
            time.sleep(3)

if current_url != "https://online.spor.istanbul/uyesepet":
    driver.save_screenshot("sporistanbul.png")
    time.sleep(3)
    foto = cv2.imread("./sporistanbul.png")
    if foto is None:
        print("sporistanbul.png yüklenemedi.")
    else:
        crop = foto[640:720, 170:430]
        if crop.size == 0:
            print("Kırpma işlemi geçersiz.")
        else:
            cv2.imwrite("./sporistanbulcrop.png", crop)
            time.sleep(2)
            goruntu_isleme(5)
            Dogrulama = driver.find_element(By.ID, "pageContent_txtCaptchaText")
            Dogrulama.clear()
            try:
                results = ocr.ocr(img_path, cls=True)
                for line in results[0]:
                    text = line[1][0]
                    print(text)
                    with open("ocr_output.txt", "a") as file:
                        file.write(text + "\n")
            except Exception as e:
                print(f"OCR işlemi sırasında bir hata oluştu: {e}")
                with open("ocr_output.txt", "a") as file:
                    file.write(f"OCR islemi sirasinda bir hata oluştu: {e} \n")

            try:
                Dogrulama.send_keys(text)
            except:
                print("OCR metni bulunamadı, devam ediliyor.")

            time.sleep(1)
            driver.find_element(By.ID, "pageContent_lbtnSepeteEkle").click()
            time.sleep(3)

driver.find_element(By.ID, "pageContent_cbOnBilgilendirmeFormu").click()
driver.find_element(By.ID, "pageContent_cbMesafeliSatisSozlesmesi").click()
driver.find_element(By.ID, "pageContent_btnOdemeYap").click()

time.sleep(2)

İsim = driver.find_element(By.ID, "CardHoldersName")
İsim.send_keys("Mehmet Eren Ekiz")
Kartno = driver.find_element(By.ID, "PAN")
Kartno.send_keys("455529045865561")

DropdowmAy = driver.find_element(By.ID, "ExpiryMonth")
driver.find_element(By.ID, "CVV").click()
AySec = Select(DropdowmAy)
ay = AySec.options
time.sleep(1)
AySec.select_by_visible_text("9")
time.sleep(1)
AySec.select_by_index("8")
time.sleep(1)

DropdowmYıl = driver.find_element(By.ID, "ExpiryYear")
YılSec = Select(DropdowmYıl)
yıl = YılSec.options
time.sleep(1)
YılSec.select_by_visible_text("2027")
time.sleep(1)
YılSec.select_by_index("27")
time.sleep(1)

CVV = driver.find_element(By.ID, "CVV")
CVV.send_keys("203")
CVV.send_keys(Keys.ENTER)
time.sleep(1)

driver.find_element(By.ID, "SubmitButton").click()
time.sleep(1)
