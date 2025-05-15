#!/bin/bash

# -----------------------------
# nmap_parallel_aggregate_scan.sh
# Parallel Nmap scan with top-1000 ports, aggregate output to result.txt
# Input: hosts_alive.txt (format: "IP is alive")
# Created by Nazarii Zavada
# -----------------------------

INPUT="hosts_alive.txt"
TMPDIR="tmp_nmap_logs"
OUTFILE="result.txt"

mkdir -p "$TMPDIR"
rm -f "$OUTFILE"

echo "[*] Starting PARALLEL scan with aggregation to $OUTFILE..."

cat "$INPUT" | awk '{print $1}' | parallel -j 10 '
  sudo nmap -sS -sV -Pn -n --top-ports 1000 --host-timeout 60s --max-retries 2 {} -oN '"$TMPDIR"'/{}.txt
'

echo "[*] Aggregating results..."
cat "$TMPDIR"/*.txt > "$OUTFILE"

echo "[*] Cleaning up temporary files..."
rm -rf "$TMPDIR"

echo "[+] Scan complete. Aggregated results saved in $OUTFILE"
