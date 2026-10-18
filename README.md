# ProductsSheet
# 🚀 Automated E-Commerce Data Pipeline (Salla to Google Sheets)

## 📌 Project Overview
This project is an automated data pipeline designed to synchronize e-commerce product data from the **Salla platform** (via XML Merchant Feed) directly into a **Google Sheets** database. 

It was built to bypass advanced anti-bot firewalls (like Cloudflare) and ensure the product catalog is continuously updated. This database acts as the single source of truth for an AI-powered WhatsApp Chatbot (Meta AI), providing it with real-time product prices, descriptions, and direct purchase links.

## 🛠️ Technologies Used
* **Language:** Python 3.10
* **Libraries:** `requests`, `gspread`, `google-auth`, `re` (Regex for robust XML parsing)
* **Automation/CI-CD:** GitHub Actions
* **Cloud Infrastructure:** Google Cloud Platform (GCP) Service Accounts & Google Sheets API

## ⚙️ How It Works
1. **Data Ingestion:** The script uses a custom `User-Agent` to fetch the XML feed from the e-commerce store, bypassing strict firewall restrictions.
2. **Robust Parsing:** Instead of relying on standard XML parsers that may fail due to poorly formatted tags or special characters (like Emojis or CDATA), the script utilizes **Regex (Regular Expressions)** to accurately extract data fields (`title`, `description`, `price`, `link`, etc.) with a 100% success rate.
3. **Data Transformation:** It cleans up the product descriptions (stripping HTML tags) and shortens the URLs (removing tracking parameters) for a cleaner AI response format.
4. **Data Loading:** It authenticates securely with Google Sheets via a GCP Service Account and updates the entire catalog efficiently.
5. **Automation:** The process is fully automated using **GitHub Actions**, scheduled via a CRON job to run silently every night at 00:00 UTC.

## 🔒 Security Measures
Security is a top priority in this architecture. Following **Google Cloud Best Practices**:
* **Zero-Code Storage:** No credentials, API keys, or JSON files are hardcoded in the repository.
* **Environment Variables:** All sensitive data (GCP Credentials and Sheet IDs) are injected at runtime securely using **GitHub Secrets**.

## 👨‍💻 Author
* **Turki Alshaikh** - System Automation & Python Developer
