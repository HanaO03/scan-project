import cv2
import pytesseract
import re

def capture_image_from_camera():
    
    #التقاط صورة من الكاميرا مباشرةً.
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return None  # فشل فتح الكاميرا
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # فشل التقاط الصورة
        
        cv2.imshow("Camera", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # التقاط الصورة
            captured_image = frame
            break
        elif key == ord('q'):  # إلغاء العملية
            captured_image = None
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return captured_image

def preprocess_image(image):
    
    #معالجة الصورة لتحسين دقة OCR.
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(image):
    """
    استخراج النص من الصورة باستخدام Tesseract OCR.
    """
    custom_config = r'--oem 3 --psm 6 -l ara+eng'
    return pytesseract.image_to_string(image, config=custom_config)

def parse_id_info(text):
   
    #تحليل النص المستخرج لاستخراج المعلومات المطلوبة.
   
    patterns = {
        "arabic_name": r"الاسم:\s*([\u0600-\u06FF\s]+?)\s+([\u0600-\u06FF\s]+?)\s+([\u0600-\u06FF\s]+?)\s+([\u0600-\u06FF\s]+)",
        "english_name": r"Name:\s*([A-Za-z\s]+?)\s+([A-Za-z\s]+?)\s+([A-Za-z\s]+?)\s+([A-Za-z\s]+)",
        "national_id": r"الرقم الوطني:\s*(\d+)",
        "gender": r"الجنس:\s*([ذكرأنثى]+)",
        "dob": r"تاريخ الولادة:\s*(\d{2})/(\d{2})/(\d{4})"
    }

    info = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            info[key] = match.groups() if len(match.groups()) > 1 else match.group(1)
        else:
            info[key] = "غير معروف"
    
    return {
        "arabic_first_name": info["arabic_name"][0] if isinstance(info["arabic_name"], tuple) else "غير معروف",
        "arabic_father_name": info["arabic_name"][1] if isinstance(info["arabic_name"], tuple) else "غير معروف",
        "arabic_grandfather_name": info["arabic_name"][2] if isinstance(info["arabic_name"], tuple) else "غير معروف",
        "arabic_family_name": info["arabic_name"][3] if isinstance(info["arabic_name"], tuple) else "غير معروف",
        "english_first_name": info["english_name"][0] if isinstance(info["english_name"], tuple) else "غير معروف",
        "english_father_name": info["english_name"][1] if isinstance(info["english_name"], tuple) else "غير معروف",
        "english_grandfather_name": info["english_name"][2] if isinstance(info["english_name"], tuple) else "غير معروف",
        "english_family_name": info["english_name"][3] if isinstance(info["english_name"], tuple) else "غير معروف",
        "national_id": info["national_id"],
        "gender": info["gender"],
        "day": info["dob"][0] if isinstance(info["dob"], tuple) else "غير معروف",
        "month": info["dob"][1] if isinstance(info["dob"], tuple) else "غير معروف",
        "year": info["dob"][2] if isinstance(info["dob"], tuple) else "غير معروف",
    }

def main():
    """
    الوظيفة الرئيسية التي تقوم بالتقاط الصورة واستخراج البيانات فقط.
    """
    captured_image = capture_image_from_camera()
    
    if captured_image is None:
        return None  # فشل التقاط الصورة
    
    processed_image = preprocess_image(captured_image)
    extracted_text = extract_text(processed_image)
    info = parse_id_info(extracted_text)
    
    return info  # إرجاع المعلومات فقط بدون طباعة

if __name__ == "__main__":
    id_info = main()