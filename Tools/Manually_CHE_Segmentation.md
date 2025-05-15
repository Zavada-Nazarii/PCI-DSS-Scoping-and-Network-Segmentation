
# PCI DSS Segmentation Testing – Manual Techniques (Non-Nmap/Masscan)

This README documents the commands and techniques used to verify network segmentation boundaries, specifically aimed at identifying any unauthorized access paths to the Cardholder Data Environment (CHE - 0.0.0.0/16) from non-CHE zones.

## 1. IP Route Verification

Check the default routing path to understand the outbound network flow.

```bash
ip route show
```

Expected:
- Only a default route via external or perimeter gateway (e.g., `1.1.1.1`).
- No specific route to `0.0.0.0/16` is expected.

---

## 2. ICMP Reachability Test (Ping)

Attempt to ping CHE segment IPs to check for basic network-level access.

```bash
ping -c 3 0.0.0.1
ping -c 3 0.0.255.254
```

Expected: 100% packet loss (filtered or unreachable).

---

## 3. ICMP Sweep using fping

A fast ping sweep to detect live hosts across the CHE range.

```bash
fping -g 0.0.0.0/16 2>/dev/null
```

Expected: All responses should be `unreachable`.

---

## 4. Traceroute to CHE Segment

Trace the route to the CHE subnet to detect if any routing path exists.

```bash
traceroute 0.0.0.1
```

Expected: All hops timeout (`* * *`), indicating either no route or firewall blocking.

---

## 5. TCP Connectivity Checks using Netcat

Attempt direct TCP connections to common ports on CHE IPs.

```bash
nc -vz 0.0.0.1 80
nc -vz 0.0.1.1 443
```

Expected: Either `connection refused` or `connection timed out`.

---

## 6. TCP SYN Probing via hping3

Manually test if TCP ports on CHE segment respond to SYN packets.

```bash
sudo hping3 -S -p 80 -c 1 0.0.1.1
sudo hping3 -S -p 443 -c 1 0.0.0.1
```

Expected: `no reply` (firewall drop) or `RA` (RST/ACK = port closed); `SA` (SYN/ACK) would indicate segmentation failure.

---

## Conclusion

All of the above tests are designed to detect unauthorized access routes to the CHE without using automated port scanners like Nmap or Masscan. Proper segmentation should yield no responses across all methods.

Ensure to document exact responses and retain evidence (e.g., output screenshots or logs) for audit and reporting.
