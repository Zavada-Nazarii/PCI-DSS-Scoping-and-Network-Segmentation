import re
import sys
from pathlib import Path

def parse_nmap_file(file_path, mode="all", debug=False):
    """
    Парсить один .txt файл зі звітом nmap (у тому числі об'єднані).
    mode: "up" | "down" | "timeout" | "all"
    debug: True для виводу проміжної інформації
    """
    report_data = []

    with open(file_path, 'r') as f:
        content = f.read()

    reports = re.split(r'Nmap scan report for ', content)
    for chunk in reports[1:]:
        lines = chunk.strip().splitlines()
        ip = lines[0].strip()
        text = "\n".join(lines)

        if "Host is up" not in text:
            if mode in ("all", "down"):
                report_data.append(f"[{ip}] 🔴 Host is down")
            continue

        if "Skipping host" in text:
            if mode in ("all", "timeout"):
                report_data.append(f"[{ip}] ⚠️ Host skipped due to timeout")
            continue

        if mode in ("all", "up"):
            report_data.append(f"[{ip}] 🟢 Host is up with open ports:")
            for line in lines:
                # Знайдемо всі відкриті порти: <port>/tcp  open  <service> [version (optional)]
                port_match = re.match(r'^(\d+/tcp)\s+open\s+([\w\-\?]+)(\s+.+)?$', line.strip())
                if port_match:
                    port = port_match.group(1)
                    service = port_match.group(2)
                    version = port_match.group(3).strip() if port_match.group(3) else "N/A"
                    report_data.append(f"    - {port:10} | {service:10} | {version}")
                elif debug and line.strip().startswith(tuple(str(p) for p in range(10))):
                    report_data.append(f"[DEBUG] Не вдалося розпарсити: {line.strip()}")

    return report_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 nmap_parser.py <nmap_report.txt> [mode] [--debug]")
        print("Modes: all (default), up, down, timeout")
        sys.exit(1)

    file_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "all"
    debug = "--debug" in sys.argv

    if mode not in ("all", "up", "down", "timeout"):
        print(f"[!] Invalid mode: {mode}")
        sys.exit(1)

    result = parse_nmap_file(file_path, mode, debug)

    output_file = "nmap_summary.txt"
    with open(output_file, "w") as f:
        f.write("\n".join(result))

    print(f"✔ Summary written to {output_file}")
