# 🛡️ SmartScanner

**SmartScanner** is a web-based information gathering and network scanning tool developed in Python with Flask. It provides real-time WHOIS lookup, port scanning, subdomain enumeration using your own script, and professional PDF reporting — all in one dashboard.

> 👨‍💻 Made by **Ali Alwaili**

---

## 📁 Project Structure

```
SMARTSCANNER/
├── templates/
│   └── index.html        → Web UI (dashboard)
├── scanner.py            → Main Flask server
├── subdomain.py          → Your custom subdomain scanner
├── wordlist1.txt         → Wordlist used for brute-forcing subdomains
├── report.pdf            → Auto-generated PDF scan report
└── README.md             → Project documentation
```

---

## 🔧 Features

- 🔍 **Live Web Dashboard**
  - Enter domain/IP to scan
  - Select scan mode (Quick, Full, Fast, Aggressive)
  - Optional port range input (e.g., `20-1000`, `80,443`)
  - Enable/disable subdomain enumeration
  - Real-time scan results: WHOIS, open ports, subdomains
  - Searchable port scan table
  - Download PDF Report button

- 🧾 **WHOIS Lookup**
  - Auto extracts registrar, organization, country, creation and expiry dates

- 🌐 **Subdomain Enumeration**
  - Uses your own `subdomain.py`
  - Output is displayed directly on the dashboard
  - Brute-forces using `wordlist1.txt`

- 📡 **Port Scanning (via Nmap)**
  - `Quick`: Top 50 ports
  - `Full`: All ports
  - `Fast`: Top ports without detection
  - `Aggressive`: Includes OS & service detection
  - Works with custom ports (e.g., `21,22,443,8080`)

- 📄 **PDF Reporting**
  - Automatically generates `report.pdf` after scan
  - Contains:
    - Target details
    - Scan mode and time
    - WHOIS data
    - Port scan results
    - Subdomain list
  - Downloadable from dashboard

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/SmartScanner
cd SmartScanner
```

### 2. Install required Python packages

```bash
pip install flask nmap python-whois reportlab
```

### 3. Install Nmap

Make sure `nmap` is installed and accessible from the terminal:

```bash
# Linux
sudo apt install nmap

# Windows
https://nmap.org/download.html
```

---

## ▶️ Run the Application

```bash
python scanner.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📌 Notes

- Ensure `scanner.py` and `subdomain.py` are in the same folder.
- `subdomain.py` must accept a domain name as input and print subdomains (one per line).
- The `report.pdf` is overwritten each time a new scan is completed.
- You can replace `wordlist1.txt` with your custom wordlist.

---

## 🖼 Screenshot

![SmartScanner Screenshot](Screenshot%202025-04-02%20171958.png)

---

## 📜 License

This project is licensed under the MIT License.  
Free to use, customize, and distribute.

---

Made by **Ali Alwaili**
