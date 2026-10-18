# ProductsSheet
# 🚀 Automated E-Commerce Data Pipeline: Merchant Feed to Google Sheets

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-2088FF.svg)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-API-34A853.svg)
![Security](https://img.shields.io/badge/Security-Zero%20Code%20Storage-red.svg)

## 📌 Project Overview
This project is a fully automated Python-based data pipeline designed to bridge the gap between an e-commerce platform and an AI-powered customer service agent. 

It automatically extracts product data from a **Google Merchant Center XML Feed** (`/feeds/google-merchant/`), cleans and processes the data, and securely synchronizes it into a **Google Sheets database**. 

### 🤖 The Ultimate Goal: WhatsApp Business AI Integration
This automated Google Sheet serves as the **Single Source of Truth (Knowledge Base)** for a **WhatsApp Business AI Agent (Meta AI)**. By keeping the sheet updated daily, the AI can instantly and accurately answer customer queries with:
* Real-time product availability.
* Up-to-date pricing.
* Accurate product descriptions (e.g., Activation types, formatting support).
* Clean, direct purchase links.

---

## ⚙️ Architecture & Workflow

1. **Data Ingestion (Bypassing WAF):** The script sends a request to the e-commerce store's XML feed. It uses customized `User-Agent` headers to successfully bypass strict anti-bot firewalls (like Cloudflare) commonly used by platforms like Salla.
2. **Robust XML Parsing (Regex):** Standard XML parsers often crash when encountering raw emojis, messy HTML tags, or unescaped CDATA inside product descriptions. To guarantee a **100% success rate**, this script utilizes advanced **Regular Expressions (Regex)** to extract specific tags (`<g:title>`, `<g:price>`, `<g:link>`, etc.) directly from the raw text.
3. **Data Transformation:** 
   * Cleans product descriptions by stripping out messy HTML/CDATA tags.
   * Shortens and formats URLs by removing unnecessary tracking parameters (everything after `?`).
4. **Data Loading (GCP Integration):** The script connects to the Google Sheets API using a securely authenticated Google Cloud Service Account. It clears outdated data and pushes the freshly parsed catalog into the sheet.
5. **CI/CD Automation:** The entire pipeline is orchestrated via **GitHub Actions**. A CRON job is scheduled to run silently every day at 00:00 UTC (3:00 AM AST), ensuring the AI always has the latest catalog before morning business hours.

---

## 🛠️ Technology Stack
* **Language:** Python 3.10
* **Libraries:** `requests`, `re` (Regex), `gspread`, `google-auth`
* **Cloud Infrastructure:** Google Cloud Platform (GCP) - Service Accounts, Sheets API, Drive API
* **Automation:** GitHub Actions (`.yml` workflows)

---

## 🔒 Security Measures
Enterprise-grade security practices were implemented following Google Cloud guidelines:
* **Zero-Code Storage:** No passwords, API keys, or JSON credential files are hardcoded in the repository.
* **Environment Variables:** All sensitive credentials (`GCP_CREDENTIALS` and `SHEET_ID`) are securely stored as **GitHub Secrets** and injected into the workflow at runtime.
* **Least Privilege Access:** The GCP Service Account is only granted `Editor` access to the specific target spreadsheet, isolating it from the rest of the Google Drive workspace.

---

## 🚀 Setup & Execution

If you wish to replicate this pipeline:

1. **Google Cloud Platform:**
   * Enable the Google Sheets and Google Drive APIs.
   * Create a Service Account and download the `JSON` key.
   * Share your target Google Sheet with the Service Account email (as Editor).
2. **GitHub Secrets:**
   * Go to `Settings > Secrets and variables > Actions`.
   * Add `GCP_CREDENTIALS` (paste the entire JSON file content).
   * Add `SHEET_ID` (the long ID found in your Google Sheets URL).
3. **Run the Pipeline:**
   * The script runs automatically via the defined CRON schedule.
   * It can also be triggered manually from the **Actions** tab using the `workflow_dispatch` event.

---

## 👨‍💻 Author
**Turki Alshaikh**  
*Computer Science Graduate | IT & Automation Specialist*  
Focusing on building efficient, automated, and secure system integrations.
