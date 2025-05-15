
# 🔍 Nmap Ping Scan Examples with Full Functionality and Explanations

This README provides a set of targeted Nmap commands for discovering live hosts in hardened or segmented environments (e.g. CHE, SCADA, or isolated LANs). Each scan uses a specific "ping type" with full functionality, including reasons for state, and optimized for analysis/reporting.

---

## 🧪 ICMP Echo Ping (PE)
```bash
sudo nmap -sn -n -PE --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG icmp_pe.gnmap
```
**Description**: Sends ICMP Echo Request (like `ping`). Blocked on many networks, but very fast if allowed.

---

## 📡 ICMP Timestamp Ping (PP)
```bash
sudo nmap -sn -n -PP --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG icmp_pp.gnmap
```
**Description**: Sends ICMP Timestamp request. Less commonly blocked. Useful alternative to `-PE`.

---

## 📎 ICMP Address Mask Ping (PM)
```bash
sudo nmap -sn -n -PM --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG icmp_pm.gnmap
```
**Description**: Obsolete ICMP method, sometimes useful in legacy or misconfigured environments.

---

## 🔗 TCP SYN Ping (PS)
```bash
sudo nmap -sn -n -PS22,23,135,139,445,502,3389,5900,20000 --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG tcp_syn.gnmap
```
**Description**: Sends SYN packets to common ports. If SYN-ACK is received, host is considered up. Bypasses some ICMP filters.

---

## 🔓 TCP ACK Ping (PA)
```bash
sudo nmap -sn -n -PA22,135,445,502 --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG tcp_ack.gnmap
```
**Description**: Sends TCP ACK packets. Hosts with stateful firewalls may reply with RST.

---

## 🧬 UDP Ping (PU)
```bash
sudo nmap -sn -n -PU53,67,69,123,161,500 --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG udp_ping.gnmap
```
**Description**: Sends empty UDP packets. If port is closed, ICMP Port Unreachable is received. Slowest method, but useful when others fail.

---

## 🧰 Combined Efficient Discovery (Recommended)
```bash
sudo nmap -sn -n -PE -PS22,135,445 -PU161 --reason --max-retries 1 --host-timeout 10s 0.0.0.0/24 -oG discovery_combo.gnmap
```
**Description**: Combines the most effective ping types to discover live hosts across different configurations.

---

## 📄 Output Format
Each command saves output in **greppable format (`-oG`)**, suitable for easy parsing, reporting, and scripting.

---

## 📌 Notes
- `--reason`: shows why a host is marked up/down (e.g. no-response, echo-reply, reset).
- `--max-retries 1`: speeds up scanning by limiting retries.
- `--host-timeout 10s`: ensures scanning doesn’t hang on dead hosts.
- Adjust `0.0.0.0/24` to your network range as needed.

