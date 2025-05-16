import re
import sys
from pathlib import Path

def parse_nmap_file(file_path):
    """
    Парсить один .txt файл зі звітом nmap, навіть якщо там кілька звітів підряд.
    """
    report_data = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Розбиваємо на частини по кожному звіту nmap
    reports = re.split(r'Nmap scan report for ', content)
    for chunk in reports[1:]:  # перший елемент буде порожній
        lines = chunk.strip().splitlines()
        ip = lines[0].strip()
        text = "\n".join(lines)

        if "Host is up" not in text:
            report_data.append(f"[{ip}] 🔴 Host is down")
            continue

        if "Skipping host" in text:
            report_data.append(f"[{ip}] ⚠️ Host skipped due to timeout")
            continue

        ports_info = re.findall(r'(\d+/tcp)\s+open\s+([^\s]+)(?:\s+(.*))?', text)
        if ports_info:
            report_data.append(f"[{ip}] 🟢 Host is up with open ports:")
            for port, service, version in ports_info:
                line = f"    - {port:10} | {service:10} | {version.strip() if version else 'N/A'}"
                report_data.append(line)
        else:
            report_data.append(f"[{ip}] 🟢 Host is up, but no open ports detected")

    return report_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 nmap_parser.py <nmap_report.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = parse_nmap_file(file_path)

    output_file = "nmap_summary.txt"
    with open(output_file, "w") as f:
        f.write("\n".join(result))

    print(f"✔ Summary written to {output_file}")
