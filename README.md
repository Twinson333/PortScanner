# Simple Port Scanner

A lightweight, multi-threaded port scanner written in Python for security research, penetration testing, and network diagnostics.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ⚠️ Legal Disclaimer

**This tool is for AUTHORIZED security testing ONLY.**

- Only scan systems you own or have **explicit written permission** to test
- Unauthorized port scanning may be **illegal** in your jurisdiction
- The authors assume **no liability** for misuse of this tool
- Always follow responsible disclosure practices
- Respect bug bounty program scopes and rules of engagement

## 🚀 Features

- **Multi-threaded scanning** - Fast concurrent port scanning
- **Flexible port selection** - Scan ranges, individual ports, or common ports
- **Service detection** - Identifies services running on open ports
- **Customizable parameters** - Adjust threads, timeouts, and output
- **Clean output** - Easy-to-read scan results
- **Hostname resolution** - Supports both IP addresses and hostnames
- **Keyboard interrupt handling** - Graceful exit with Ctrl+C

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses standard library only)

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/simple-port-scanner.git
cd simple-port-scanner

# Make the script executable (optional)
chmod +x port_scanner.py
```

## 💻 Usage

### Basic Usage

```bash
# Scan default ports (1-1024)
python port_scanner.py <target>

# Scan specific port range
python port_scanner.py 192.168.1.1 -p 1-1000

# Scan specific ports
python port_scanner.py example.com -p 80,443,8080,8443

# Scan common ports
python port_scanner.py scanme.nmap.org --common
```

### Advanced Options

```bash
# Full port scan with more threads
python port_scanner.py 10.0.0.1 -p 1-65535 --threads 200

# Scan with custom timeout
python port_scanner.py example.com -p 1-1000 --timeout 2.0

# Show closed ports (verbose)
python port_scanner.py 192.168.1.1 -p 80-100 --show-closed

# Help menu
python port_scanner.py -h
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `target` | Target IP address or hostname | Required |
| `-p, --ports` | Port range (e.g., 1-1024, 80,443, or 1-65535) | 1-1024 |
| `--common` | Scan common ports (top 100) | False |
| `--threads` | Number of concurrent threads | 100 |
| `--timeout` | Connection timeout in seconds | 1.0 |
| `--show-closed` | Display closed ports in output | False |

## 📊 Example Output

```
--------------------------------------------------
Scanning target: 192.168.1.1
Port range: 1-1000
Started at: 2024-02-17 10:30:45
--------------------------------------------------
[+] Port    22 | OPEN    | ssh
[+] Port    80 | OPEN    | http
[+] Port   443 | OPEN    | https
[+] Port  8080 | OPEN    | http-proxy
--------------------------------------------------
Scan completed at: 2024-02-17 10:31:02
Total open ports found: 4
Open ports: 22, 80, 443, 8080
--------------------------------------------------
```

## 🎯 Use Cases

### Bug Bounty Hunting
```bash
# Quick reconnaissance of web services
python port_scanner.py target.com -p 80,443,8080,8443

# Comprehensive scan for exposed services
python port_scanner.py target.com -p 1-10000 --threads 150
```

### Penetration Testing
```bash
# Initial enumeration phase
python port_scanner.py 10.0.0.0/24 --common

# Detailed service discovery
python port_scanner.py target.local -p 1-65535 --timeout 2
```

### Network Diagnostics
```bash
# Check if specific services are accessible
python port_scanner.py server.local -p 22,80,443,3306

# Verify firewall rules
python port_scanner.py internal-server -p 1-1000
```

## 🔍 Common Ports Scanned

The `--common` flag scans these frequently used ports:

- **Web**: 80, 443, 8080, 8443, 8888
- **Remote Access**: 22 (SSH), 23 (Telnet), 3389 (RDP), 5900 (VNC)
- **Databases**: 3306 (MySQL), 5432 (PostgreSQL), 27017 (MongoDB), 6379 (Redis)
- **Mail**: 25 (SMTP), 110 (POP3), 143 (IMAP), 993 (IMAPS), 995 (POP3S)
- **File Sharing**: 21 (FTP), 445 (SMB), 2049 (NFS)
- And many more...


### Recommended Test Targets

- **scanme.nmap.org** - Intentionally available for testing
- **Your own systems** - Virtual machines, local servers
- **Bug bounty programs** - Only within defined scope

## 🚧 Limitations

- TCP scanning only (no UDP support)
- Basic service detection (uses port number lookup)
- No OS fingerprinting
- No vulnerability detection
- Limited stealth capabilities

## 🔮 Future Enhancements

- [ ] UDP port scanning support
- [ ] Banner grabbing for detailed service identification
- [ ] Output to JSON/CSV formats
- [ ] Stealth scanning techniques
- [ ] IPv6 support
- [ ] Scanning multiple targets from a file
- [ ] Integration with vulnerability databases

---

**⚡ Remember**: With great power comes great responsibility. Happy (ethical) hacking!
