#!/usr/bin/env python3
"""
Simple Port Scanner
For ethical hacking, bug bounty, and authorized security testing only.
Only scan systems you own or have explicit permission to test.
"""

import socket
import sys
from datetime import datetime
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target, port, timeout=1):
    """
    Scan a single port on the target host.
    
    Args:
        target: IP address or hostname
        port: Port number to scan
        timeout: Connection timeout in seconds
    
    Returns:
        tuple: (port, status, service_name)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            sock.close()
            return (port, "open", service)
        else:
            sock.close()
            return (port, "closed", "")
    except socket.gaierror:
        return (port, "error", "Hostname could not be resolved")
    except socket.error:
        return (port, "error", "Could not connect")
    except KeyboardInterrupt:
        return (port, "interrupted", "")


def scan_ports(target, start_port, end_port, threads=100, timeout=1, show_closed=False):
    """
    Scan a range of ports on the target host.
    
    Args:
        target: IP address or hostname
        start_port: Starting port number
        end_port: Ending port number
        threads: Number of concurrent threads
        timeout: Connection timeout in seconds
        show_closed: Whether to display closed ports
    """
    print("-" * 50)
    print(f"Scanning target: {target}")
    print(f"Port range: {start_port}-{end_port}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    open_ports = []
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(scan_port, target, port, timeout): port 
                for port in range(start_port, end_port + 1)
            }
            
            for future in as_completed(futures):
                port, status, service = future.result()
                
                if status == "open":
                    open_ports.append(port)
                    print(f"[+] Port {port:5d} | OPEN    | {service}")
                elif status == "error":
                    print(f"[!] Port {port:5d} | ERROR   | {service}")
                elif show_closed and status == "closed":
                    print(f"[-] Port {port:5d} | CLOSED  |")
                elif status == "interrupted":
                    print("\n[!] Scan interrupted by user")
                    break
    
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(0)
    
    print("-" * 50)
    print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total open ports found: {len(open_ports)}")
    
    if open_ports:
        print(f"Open ports: {', '.join(map(str, sorted(open_ports)))}")
    print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Simple Port Scanner - For authorized security testing only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py 192.168.1.1 -p 1-1000
  python port_scanner.py example.com -p 80,443,8080
  python port_scanner.py 10.0.0.1 -p 1-65535 --threads 200
  python port_scanner.py scanme.nmap.org --common

LEGAL WARNING:
Only scan systems you own or have explicit written permission to test.
Unauthorized port scanning may be illegal in your jurisdiction.
        """
    )
    
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024", 
                        help="Port range (e.g., 1-1024, 80,443, or 1-65535)")
    parser.add_argument("--common", action="store_true",
                        help="Scan common ports (top 100)")
    parser.add_argument("--threads", type=int, default=100,
                        help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0,
                        help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--show-closed", action="store_true",
                        help="Show closed ports")
    
    args = parser.parse_args()
    
    # Common ports list (top 100)
    common_ports = [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
        1723, 3306, 3389, 5900, 8080, 8443, 8888, 20, 69, 88, 389, 636, 873,
        1433, 1521, 2049, 2375, 2376, 3000, 5432, 5555, 5601, 5985, 6379,
        6443, 8000, 8008, 8009, 8081, 8082, 8089, 8090, 8091, 8200, 9000,
        9001, 9090, 9091, 9092, 9200, 9300, 10000, 27017, 50000, 50070
    ]
    
    target = args.target
    
    # Parse port range
    if args.common:
        ports_to_scan = common_ports
        start_port = min(ports_to_scan)
        end_port = max(ports_to_scan)
        print(f"\n[*] Scanning {len(common_ports)} common ports...")
    elif "," in args.ports:
        # Individual ports
        ports_to_scan = [int(p.strip()) for p in args.ports.split(",")]
        start_port = min(ports_to_scan)
        end_port = max(ports_to_scan)
    elif "-" in args.ports:
        # Port range
        start_port, end_port = map(int, args.ports.split("-"))
        ports_to_scan = None
    else:
        # Single port
        start_port = end_port = int(args.ports)
        ports_to_scan = None
    
    # Validate port range
    if start_port < 1 or end_port > 65535:
        print("[!] Error: Port numbers must be between 1 and 65535")
        sys.exit(1)
    
    # Resolve hostname
    try:
        target_ip = socket.gethostbyname(target)
        if target != target_ip:
            print(f"[*] Resolved {target} to {target_ip}")
    except socket.gaierror:
        print(f"[!] Error: Could not resolve hostname {target}")
        sys.exit(1)
    
    # Run scan
    if ports_to_scan:
        # Scan specific ports
        for port_chunk in [ports_to_scan[i:i+args.threads] for i in range(0, len(ports_to_scan), args.threads)]:
            scan_ports(target_ip, min(port_chunk), max(port_chunk), 
                      args.threads, args.timeout, args.show_closed)
    else:
        # Scan port range
        scan_ports(target_ip, start_port, end_port, 
                  args.threads, args.timeout, args.show_closed)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(0)
