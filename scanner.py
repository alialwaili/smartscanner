from flask import Flask, render_template, request, jsonify, send_file
import socket
import nmap
import whois
import subprocess
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

TOP_50_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 465, 587, 993,
    995, 1433, 1521, 2049, 2375, 2376, 3000, 3306, 3389, 5432, 5500, 5601, 5900,
    6379, 8000, 8080, 8081, 8443, 8888, 9000, 9200, 9300, 11211, 27017, 28017,
    50000, 50030, 50070, 54321, 55555, 60000, 7547, 47808, 49152, 123
]

def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except Exception:
        return None

def get_whois_info(domain):
    try:
        info = whois.whois(domain)

        def safe(val):
            if isinstance(val, list):
                return str(val[0])
            return str(val)

        return {
            "Domain": domain,
            "Registrar": info.get("registrar"),
            "Organization": info.get("org"),
            "Country": info.get("country"),
            "Created On": safe(info.get("creation_date")),
            "Expires On": safe(info.get("expiration_date"))
        }
    except Exception as e:
        print("WHOIS lookup failed:", e)
        return {"Error": "WHOIS lookup failed."}

def enumerate_subdomains(domain):
    try:
        output = subprocess.check_output(
            ["python", "subdomain.py", domain],
            stderr=subprocess.DEVNULL
        )
        subdomains = output.decode().splitlines()
        return [s.strip() for s in subdomains if s.strip()]
    except Exception as e:
        print("Subdomain tool failed:", e)
        return []

def scan_ports(ip, mode, custom_ports=None):
    nm = nmap.PortScanner()

    if custom_ports:
        arguments = f"-T4 -p {custom_ports}"
    elif mode == "quick":
        arguments = f"-T4 -p {','.join(map(str, TOP_50_PORTS))}"
    elif mode == "full":
        arguments = "-T4 -p-"
    elif mode == "fast":
        arguments = "-T4 --top-ports 50"
    elif mode == "aggressive":
        arguments = f"-sV -O -T4 -p {','.join(map(str, TOP_50_PORTS))}"
    else:
        return []

    nm.scan(ip, arguments=arguments)
    results = []
    for proto in nm[ip].all_protocols():
        for port in nm[ip][proto].keys():
            service = nm[ip][proto][port]
            results.append({
                "port": port,
                "state": service.get('state', 'unknown'),
                "service": service.get('name', 'unknown'),
                "version": service.get('version', 'unknown')
            })
    return results

def generate_pdf_report(filename, target, ip, mode, timestamp, whois, ports, subdomains):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50

    def write_line(text, offset=15, bold=False):
        nonlocal y
        if y < 40:
            c.showPage()
            y = height - 50
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 10)
        c.drawString(50, y, text)
        y -= offset

    write_line("SmartScanner Report", 20, bold=True)
    write_line(f"Target: {target}")
    write_line(f"IP Address: {ip}")
    write_line(f"Scan Mode: {mode}")
    write_line(f"Timestamp: {timestamp}")
    write_line("")

    write_line("WHOIS Info", 20, bold=True)
    for key, value in whois.items():
        write_line(f"{key}: {value}")

    write_line("", 10)
    write_line("Open Ports", 20, bold=True)
    for p in ports:
        write_line(f"{p['port']}/{p['state']} - {p['service']} - {p['version']}")

    write_line("", 10)
    write_line("Subdomains", 20, bold=True)
    for sub in subdomains:
        write_line(sub)

    c.save()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    if not data or not data.get("target"):
        return "Missing target in request", 400

    target = data.get("target").strip()
    mode = data.get("mode", "quick")
    custom_ports = data.get("custom_ports", "").strip()
    run_subdomain = data.get("run_subdomain", False)

    ip = resolve_target(target)
    if not ip:
        return f"Could not resolve target '{target}'", 400

    try:
        scan_results = scan_ports(ip, mode, custom_ports if custom_ports else None)
    except Exception as e:
        return f"Scan failed: {str(e)}", 500

    whois_info = get_whois_info(target)
    subdomains = enumerate_subdomains(target) if run_subdomain else []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate PDF report
    generate_pdf_report(
        filename="report.pdf",
        target=target,
        ip=ip,
        mode=mode,
        timestamp=timestamp,
        whois=whois_info,
        ports=scan_results,
        subdomains=subdomains
    )

    return jsonify({
        "target": target,
        "ip": ip,
        "mode": mode,
        "timestamp": timestamp,
        "whois": whois_info,
        "subdomains": subdomains,
        "scan_results": scan_results
    })

@app.route("/download-report")
def download_report():
    return send_file("report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
