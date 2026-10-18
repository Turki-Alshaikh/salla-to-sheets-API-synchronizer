import os
import json
import re
import requests
import gspread
from google.oauth2.service_account import Credentials
import xml.etree.ElementTree as ET

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
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الرابط: {e}")
        return

    # 3. تحليل الـ XML
    root = ET.fromstring(response.content)
    ns = {'g': 'http://base.google.com/ns/1.0'}
    
    data = []
    # كتابة العناوين الأساسية
    data.append(["اسم المنتج", "وصف المنتج", "رابط المنتج", "رابط الصورة", "السعر", "التوفر", "نوع المنتج"])

    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else ''
        
        # الوصف: استخراجه وتنظيفه من أكواد HTML
        desc_elem = item.find('g:description', ns)
        if desc_elem is None:
            desc_elem = item.find('description')
        description = desc_elem.text if desc_elem is not None else ''
        description = re.sub(r'<[^>]+>', '', description).strip()
        
        link = item.find('link').text if item.find('link') is not None else ''
        
        image_link = item.find('g:image_link', ns)
        image_link = image_link.text if image_link is not None else ''
        
        price = item.find('g:price', ns)
        price = price.text if price is not None else ''
        
        availability = item.find('g:availability', ns)
        availability = availability.text if availability is not None else ''
        
        product_type = item.find('g:product_type', ns)
        product_type = product_type.text if product_type is not None else ''
        
        data.append([title, description, link, image_link, price, availability, product_type])

    # 4. تحديث الجدول
    sheet.clear() # مسح البيانات القديمة بالكامل
    sheet.update(range_name='A1', values=data) # حقن البيانات الجديدة
    print(f"تم التحديث بنجاح! تم إدراج {len(data) - 1} منتج في الجدول.")

if __name__ == "__main__":
    sync_salla_feed()
