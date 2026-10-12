import socket
import ipaddress
from datetime import datetime


def scan_ports(target, ports, services):
    print("=" * 55)
    print("           NETWORK PORT SCANNER")
    print("=" * 55)
    print("Target IP:", target)
    print("-" * 55)
    print(f"{'PORT':<10}{'SERVICE':<25}{'STATUS':<15}")
    print("-" * 55)

    open_count = 0
    closed_count = 0
    other_count = 0
    results=[]

    for port in ports:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        sock.settimeout(1)

        try:
            result = sock.connect_ex((target, port))

            if result == 0:
                status = "OPEN"
                open_count += 1
            elif result == 111:
                status = "CLOSED"
                closed_count += 1
            else:
                status = "OTHER/ERROR"
                other_count += 1

            print(
                f"{port:<10}"
                f"{services[port]:<25}"
                f"{status:<15}"
            )
            results.append(f"{port:<10}{services[port]:<25}{status:<15}")

        except OSError as error:
            print(f"Port {port}: Error - {error}")
            other_count += 1

        finally:
            sock.close()

    print("-" * 55)
    print("Scan completed!")
    print("Open ports:", open_count)
    print("Closed ports:", closed_count)
    print("Other results:", other_count)
    with open("scan_report.txt", "w") as report:
        report.write(f"Scan Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("NETWORK PORT SCANNER REPORT\n")
        report.write(f"Target IP: {target}\n\n")
        report.write("PORT      SERVICE                  STATUS\n")
        report.write("-" * 55 + "\n")

        for result in results:
            report.write(result + "\n")

        report.write("\nScan completed!\n")
        report.write(f"Open ports: {open_count}\n")
        report.write(f"Closed ports: {closed_count}\n")
        report.write(f"Other results: {other_count}\n")

    print("Report saved to scan_report.txt")
    print("=" * 55)


target = input("Enter target IPv4 address: ").strip()

try:
    ipaddress.IPv4Address(target)
except ipaddress.AddressValueError:
    print("Invalid IPv4 address!")
    raise SystemExit

ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8000]

services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8000: "HTTP (test server)"
}

scan_ports(target, ports, services)
