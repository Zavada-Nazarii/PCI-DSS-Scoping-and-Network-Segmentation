
## 🚫 TC4: Активне тестування сегментації з позаобласних сегментів

### 🎯 Мета:
Перевірити відсутність несанкціонованого доступу до CDE з мережевих сегментів, які визначені як out-of-scope. Виконати активне тестування згідно з вимогою PCI DSS 11.3.4.

---

### 🧰 Інструменти:
- `nmap` — портове сканування TCP/UDP
- `ping` / `hping3` — ICMP/UDP тестування
- `netcat` / `telnet` — тестування доступності сервісів вручну
- `curl` / `wget` — HTTP(s)-тестування
- DNS-утиліти: `nslookup`, `dig`

---

### 🔄 Технічна послідовність дій (Step-by-Step)

#### ✅ 1. Підготовка:
- Визначити сегменти, які документовані як out-of-scope
- Отримати список IP-адрес/інтерфейсів CDE для перевірки
- Підготувати систему для запуску сканувань (окремий хост з правами адміністратора)

#### ✅ 2. ICMP Ping Test:
```bash
ping -c 4 <CDE_IP>
hping3 -1 <CDE_IP> -c 4
```
- Перевірка реакції на Echo Request
- Очікувано: **timeout / unreachable**

#### ✅ 3. TCP Port Scan:
```bash
nmap -Pn -p- <CDE_IP>
```
- Перевірити відкриті порти, наприклад 22, 80, 443, 3389
- Очікувано: **всі порти фільтровані або закриті**

#### ✅ 4. UDP Port Scan:
```bash
nmap -sU -Pn -p 53,123,161,500 <CDE_IP>
```
- Перевірка критичних UDP сервісів
- Очікувано: **немає відкритих UDP портів**

#### ✅ 5. DNS Resolution Test:
```bash
nslookup internal-cde-host.local
dig @dns-server internal-cde-host.local
```
- Тестуємо можливість резолвити CDE-хости з out-of-scope мереж
- Очікувано: **NXDOMAIN / REFUSED**

#### ✅ 6. Application Layer Access Test:
```bash
curl -v http://<CDE_IP>:80
telnet <CDE_IP> 443
nc -zv <CDE_IP> 445
```
- Спроба з’єднатися з додатками (веб, SMB, RDP)
- Очікувано: **connection refused / timeout**

#### ✅ 7. Повноцінне Penetration Testing:
- Ініціювати спроби обійти мережеві контролі через:
  - Відкриті маршрути (`traceroute`)
  - Несанкціоновані proxy або jump-хости
  - Внутрішні DNS або NAT викривлення
- Застосувати комбіновані атаки:
  - DNS tunneling
  - Port Knocking

#### ✅ 8. Тест на обхід через наявність адмін-доступу:
- З хостів, де є локальний root/administrator:
  - Спробувати змінити маршрут
  - Forwarding через SSH тунелі
  - Встановлення додаткових служб (proxy, VPN)
- Очікувано: **неможливість досягти CDE навіть з адмін-доступом у out-of-scope**

---

### 📌 Очікуваний результат:
- Жоден тип трафіку (ICMP, TCP, UDP, DNS, HTTP) з позаобласних сегментів **не дозволений**
- Всі спроби обійти сегментацію — **блокуються на мережевому або прикладному рівні**
- CDE ізольований та не досяжний згідно з PCI DSS 11.3.4

---

### ⚠️ Типові вразливості:
- Неповна фільтрація ICMP або внутрішніх портів
- Відсутність міжмережевого екрану між trusted ↔ out-of-scope зон
- DNS leaks
- Необмежений outbound доступ з out-of-scope у CDE
