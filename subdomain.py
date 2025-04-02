import argparse
import requests
import dns.resolver
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def get_crt_subdomains(domain):
    """Query certificate transparency logs from crt.sh"""
    subdomains = set()
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=10)
        if response.ok:
            data = response.json()
            for entry in data:
                name_value = entry['name_value']
                if '\n' in name_value:
                    names = name_value.split('\n')
                    for name in names:
                        subdomains.add(name.strip().lower())
                else:
                    subdomains.add(name_value.lower())
    except Exception as e:
        print(f"Error querying crt.sh: {e}")
    return subdomains

def attempt_zone_transfer(domain):
    """Attempt DNS zone transfer"""
    subdomains = set()
    try:
        ns_query = dns.resolver.resolve(domain, 'NS')
        nameservers = [str(ns) for ns in ns_query]
        
        for ns in nameservers:
            try:
                axfr = dns.query.xfr(ns, domain, timeout=5)
                zone = []
                for message in axfr:
                    zone.extend(message.answer)
                for record in zone:
                    if record.rdtype == dns.rdatatype.A:
                        subdomains.add(str(record.name).lower())
            except Exception as e:
                continue
    except Exception as e:
        pass
    return subdomains

def resolve_subdomain(subdomain):
    """Check if subdomain exists by resolving DNS"""
    try:
        answers = dns.resolver.resolve(subdomain, 'A')
        if answers:
            return subdomain
    except:
        return None

def brute_force_subdomains(domain, wordlist):
    """Brute-force subdomains using a wordlist"""
    found = set()
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        with open(wordlist, 'r') as f:
            for line in f:
                word = line.strip()
                if word:
                    subdomain = f"{word}.{domain}"
                    futures.append(executor.submit(resolve_subdomain, subdomain))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found.add(result)
    return found

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration Tool")
    parser.add_argument("domain", help="Domain to enumerate subdomains for")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist for brute-forcing")
    args = parser.parse_args()

    domain = args.domain.lower()
    subdomains = set()

    print(f"[*] Checking crt.sh for subdomains...")
    crt_subs = get_crt_subdomains(domain)
    subdomains.update(crt_subs)

    print(f"[*] Attempting DNS zone transfer...")
    zone_subs = attempt_zone_transfer(domain)
    subdomains.update(zone_subs)

    if args.wordlist:
        print(f"[*] Brute-forcing subdomains...")
        brute_subs = brute_force_subdomains(domain, args.wordlist)
        subdomains.update(brute_subs)

    # Clean and filter results
    clean_subs = set()
    target_domain = f".{domain}"
    for sub in subdomains:
        if sub.endswith(target_domain) or sub == domain:
            clean_subs.add(sub)

    print(f"\n[+] Found {len(clean_subs)} unique subdomains:")
    for subdomain in sorted(clean_subs):
        print(subdomain)

print("This Tool Was Created By Ali ALwaili")

if __name__ == "__main__":
    main()