# Data Privacy Notes

## Importance
Protects integrity, confidentiality, and availability of Test IO and customer systems.

## Threats
- **External:** Phishing, malware, ransomware, SQL injection, DDoS.
- **Internal:** Human error, intentional misuse, production data in test scripts.

## Data Categories
- **Personal (PII):** Identifiable living individuals.
- **Customer:** Belonging to customers.
- **Project/Program/Account:** Created during project lifecycle.
- **Company:** Owned by Test IO.

## Confidentiality Classes
- **Public:** Freely shared.
- **Confidential:** Non-public; leak causes harm (most Test IO info).
- **Strictly Confidential:** Leak causes significant harm; requires utmost care.

## PII Levels
- **Confidential PII:** Name, email, address, location, photo, marital status.
- **Strictly Confidential (Sensitive) PII:** Race, politics, religion, biometric/genetic data, health, sexual orientation, criminal proceedings, financial data, Gov ID.

## Special Strictly Confidential Categories
- **PHI (Personal Health Information):** Protected health/payment data.
- **PCI (Payment Card Information):** Cardholder data (CHD). Test IO is PCI DSS compliant; access via VPN only, no storage.
- **Intellectual Property:** Financial, Legal, Code, Marketing, sensitive photos.

## Reporting
Seek advice from Community Manager or Crowd Coordinator if unsure about handling data.
