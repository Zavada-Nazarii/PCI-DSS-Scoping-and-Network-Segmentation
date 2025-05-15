#!/bin/bash

# -----------------------------
# ⚡ nmap_parallel_service_scan.sh
# Parallel Nmap version scan for top 10000 ports
# Input: hosts_alive.txt (format: "IP is alive")
# Uses GNU parallel to accelerate scanning of multiple hosts
# created by Nazarii Zavada
# -----------------------------

INPUT="hosts_alive.txt"
OUTDIR="nmap_parallel_service_results"
mkdir -p "$OUTDIR"

echo "[*] Starting PARALLEL service scan on alive hosts..."

cat "$INPUT" | awk '{print $1}' | parallel -j 10 'echo "[*] Scanning {}..."; sudo nmap -sS -sV -Pn -n --top-ports 1000 --host-timeout 60s --max-retries 2 -oN "$OUTDIR/{}.txt" {}'

echo "[✔] Parallel scan complete. Results stored in $OUTDIR/"
