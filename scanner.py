from flask import Flask, render_template, request, jsonify
import socket
import nmap
import whois
from datetime import datetime

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
        return {
            "domain": domain,
            "registrar": info.registrar,
            "organization": info.org,
            "country": info.country,
            "creation_date": str(info.creation_date),
            "expiration_date": str(info.expiration_date)
        }
    except:
        return {"error": "WHOIS lookup failed."}

def scan_ports(ip, mode):
    nm = nmap.PortScanner()

    if mode == "quick":
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    target = data.get("target")
    mode = data.get("mode", "quick")

    ip = resolve_target(target)
    if not ip:
        return jsonify({"error": "Invalid target"}), 400

    scan_results = scan_ports(ip, mode)
    whois_info = get_whois_info(target)

    return jsonify({
        "target": target,
        "ip": ip,
        "mode": mode,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "whois": whois_info,
        "scan_results": scan_results
    })

if __name__ == '__main__':
    app.run(debug=True)