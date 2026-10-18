import os
import json
import re
import requests
import gspread
from google.oauth2.service_account import Credentials

def sync_salla_feed():
    # 1. إعداد الاتصال بجوجل شيت باستخدام بيانات الاعتماد
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds_json = json.loads(os.environ['GCP_CREDENTIALS'])
    creds = Credentials.from_service_account_info(creds_json, scopes=scope)
    client = gspread.authorize(creds)

    sheet_id = os.environ['SHEET_ID']
    sheet = client.open_by_key(sheet_id).sheet1

    # 2. جلب البيانات من ملف XML لمتجر مفاتيحي
    url = "https://mfatihy.com/ar/feeds/google-merchant/o15Iqwe1bKvSHzKRAV4KsZ7jP9VI6OpL"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        xml_content = response.text # قراءة النص الخام
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الرابط: {e}")
        return

    # 3. تحليل البيانات باستخدام التعابير النمطية (Regex) لتفادي أي أخطاء في الـ XML
    data = []
    # كتابة العناوين الأساسية
    data.append(["اسم المنتج", "وصف المنتج", "رابط المنتج", "رابط الصورة", "السعر", "التوفر", "نوع المنتج"])

    # تقسيم الملف إلى عناصر (items)
    items = re.findall(r'<item>(.*?)</item>', xml_content, re.DOTALL)
    
    for item in items:
        # استخراج الاسم
        title_match = re.search(r'<g:title>(.*?)</g:title>', item)
        if not title_match: title_match = re.search(r'<title>(.*?)</title>', item)
        title = title_match.group(1).strip() if title_match else ""
        
        # استخراج الوصف
        desc_match = re.search(r'<g:description>(.*?)</g:description>', item, re.DOTALL)
        if not desc_match: desc_match = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        description = desc_match.group(1) if desc_match else ""
        # تنظيف الوصف من أي أكواد برمجية (مثل CDATA أو HTML)
        description = description.replace('<![CDATA[', '').replace(']]>', '')
        description = re.sub(r'<[^>]+>', '', description).strip()
        
        # استخراج الرابط
        link_match = re.search(r'<g:link>(.*?)</g:link>', item)
        if not link_match: link_match = re.search(r'<link>(.*?)</link>', item)
        link = link_match.group(1).strip() if link_match else ""
        
        # استخراج الصورة
        image_match = re.search(r'<g:image_link>(.*?)</g:image_link>', item)
        image_link = image_match.group(1).strip() if image_match else ""
        
        # استخراج السعر
        price_match = re.search(r'<g:price>(.*?)</g:price>', item)
        price = price_match.group(1).strip() if price_match else ""
        
        # استخراج التوفر
        avail_match = re.search(r'<g:availability>(.*?)</g:availability>', item)
        availability = avail_match.group(1).strip() if avail_match else ""
        
        # استخراج نوع المنتج
        type_match = re.search(r'<g:product_type>(.*?)</g:product_type>', item)
        product_type = type_match.group(1).strip() if type_match else ""
        
        data.append([title, description, link, image_link, price, availability, product_type])

    # 4. تحديث الجدول
    if len(data) > 1:
        sheet.clear() # مسح البيانات القديمة بالكامل
        sheet.update(range_name='A1', values=data) # حقن البيانات الجديدة
        print(f"تم التحديث بنجاح! تم إدراج {len(data) - 1} منتج في الجدول بشكل دقيق.")
    else:
        print("لم يتم العثور على أي منتجات في الملف.")

if __name__ == "__main__":
    sync_salla_feed()
