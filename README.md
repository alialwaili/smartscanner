# 🔍 SmartScanner

**By Ali Alwaili**

SmartScanner is a professional-grade, web-based port scanning and reconnaissance tool built with Python and Flask. It allows users to scan IP addresses and domains using multiple scanning strategies, visualize results in real-time on a beautiful dark-themed dashboard, and interactively search through open ports, services, and their states.

---

## 🚀 Features

- 🌐 Web-based interface (Flask + HTML/CSS/Vanilla JS)
- 🎨 Clean dark UI inspired by modern security dashboards
- 🧠 WHOIS lookup integration
- 🔍 Scan results displayed in interactive tables
- 🔎 Live search/filter through scan results
- 🕓 Scan time tracking
- ⚙️ Four scan modes for flexibility and performance

---

## 🧪 Scan Modes Explained

SmartScanner supports **4 powerful scan modes**, each designed for different levels of depth and performance:

| Mode        | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `quick`     | ✅ Scans **top 50 common ports** quickly. Good for everyday basic recon.     |
| `full`      | 📜 Scans **all 65,535 ports**. Thorough but takes more time.                 |
| `fast`      | ⚡ Scans **top ports only** with **no OS or version detection**. Fastest.     |
| `aggressive`| 🔥 Includes **service versioning + OS detection** on top 50 ports. Deepest.  |

You can choose your mode using the dropdown on the dashboard UI.

---

## 📂 Project Structure

```
SmartScanner/
├── scanner.py       # Flask backend logic
├── templates/
│   └── index.html             # Main UI with interactive dashboard
├── README.md                  # This documentation
```

---

## 🛠️ Requirements

- Python 3.7+
- Nmap (must be installed on your system)

### Install dependencies:
```bash
pip install flask python-nmap python-whois
```

### Make sure Nmap is installed:
```bash
nmap --version
```
If not, install via your package manager (e.g. `sudo apt install nmap` on Ubuntu).

---

## 🧑‍💻 Usage

1. Clone the repository
2. Navigate to the project folder
3. Run the Flask app:

```bash
python scanner.py
```

4. Open your browser and go to:
```
http://127.0.0.1:5000
```

---

## 📈 Output Example
- Displays all scan results in a live, interactive table
- Filter results by typing any keyword (port number, service name, etc.)

---

## 🧾 License
This project is provided for educational and ethical penetration testing purposes **only**. Unauthorized scanning is illegal.

**Created and maintained by Ali Alwaili** ✨

---

Feel free to contribute, customize, and expand SmartScanner!
# smartscanner
