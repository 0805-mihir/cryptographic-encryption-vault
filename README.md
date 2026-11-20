# 🔐 Cryptographic Encryption Vault

A Python-based cybersecurity project designed to securely encrypt and decrypt multiple files using modern cryptographic algorithms.

## 📌 Project Overview

Cryptographic Encryption Vault is a Python-based file protection application that helps protect confidential files from unauthorized access.

The application uses AES-256-GCM encryption to protect file contents and PBKDF2-HMAC-SHA256 to generate a secure encryption key from the user's master password.

It also uses SHA-256 hashing to verify the integrity of restored files and creates an encrypted backup of the derived encryption key.

## 🎯 Project Objectives

- Secure multiple files using strong encryption.
- Generate encryption keys from a master password.
- Encrypt files inside a selected directory.
- Decrypt and restore encrypted files.
- Verify restored file integrity using SHA-256.
- Create an encrypted backup of the derived encryption key.
- Understand practical cryptography and cybersecurity concepts.

## ✨ Features

- **AES-256-GCM Encryption:** Protects file contents using authenticated encryption.
- **Password-Based Key Derivation:** Generates a 256-bit encryption key using PBKDF2-HMAC-SHA256.
- **Directory Scanning:** Identifies files inside the selected directory.
- **Multiple File Encryption:** Encrypts multiple files in a single operation.
- **File Decryption:** Restores encrypted files to their original readable format.
- **SHA-256 Integrity Verification:** Compares original and restored file hashes.
- **Encrypted Key Backup:** Creates an encrypted backup of the derived encryption key.
- **JSON Manifest:** Stores file paths, salt, and SHA-256 hashes.
- **Menu-Driven Interface:** Provides simple command-line options.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| AES-256-GCM | File encryption and decryption |
| PBKDF2-HMAC-SHA256 | Password-based key derivation |
| SHA-256 | File integrity verification |
| JSON | Metadata storage |
| Cryptography Library | Cryptographic operations |
| Visual Studio Code | Code development and execution |

## 📂 Project Structure

```text
Cryptographic-Encryption-Vault/
│
├── crypto_vault.py
├── requirements.txt
├── README.md
│
├── test_data/
│   ├── file1.txt
│   └── file2.txt
│
├── vault_data/
│   ├── encrypted/
│   │   ├── file1.txt.enc
│   │   └── file2.txt.enc
│   └── manifest.json
│
├── key_backup/
│   └── vault_key_backup.json
│
├── restored_data/
│   └── test_data/
│       ├── file1.txt
│       └── file2.txt
│
└── reports/
    └── Cryptographic_Encryption_Vault_Report.pdf
```

*Note: The folder structure above represents the intended project organization. Some folders are generated automatically when the application runs.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/0805-mihir/cryptographic-encryption-vault.git
```

### 2. Open the Project Directory

```bash
cd cryptographic-encryption-vault
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python crypto_vault.py
```

## ▶️ Application Menu

After running the application, the following menu is displayed:

```text
=========================================
     CRYPTOGRAPHIC ENCRYPTION VAULT
=========================================
1. Encrypt Directory
2. Decrypt Directory
3. Verify Key Backup
4. Exit
```

## 🔒 Encryption Process

1. Select the Encrypt Directory option.
2. Enter the directory path.
3. Enter the master password.
4. The application scans the selected directory.
5. PBKDF2-HMAC-SHA256 generates a 256-bit encryption key.
6. AES-256-GCM encrypts the selected files.
7. Encrypted files are stored inside the `vault_data` directory.
8. A JSON manifest and encrypted key backup are created.

The original files are not deleted during encryption.

## 🔓 Decryption Process

1. Select the Decrypt Directory option.
2. Enter the correct master password.
3. The application reads the JSON manifest.
4. The encryption key is derived again using PBKDF2-HMAC-SHA256.
5. AES-256-GCM decrypts the encrypted files.
6. Restored files are saved inside the `restored_data` directory.
7. SHA-256 hashes are compared to verify file integrity.

## 🧪 Testing and Results

The application was tested using a sample directory containing two text files.

**Testing Results:**

- Successfully encrypted two sample text files.
- Successfully generated encrypted files.
- Successfully created a JSON manifest.
- Successfully created an encrypted key backup.
- Successfully decrypted both encrypted files.
- Successfully restored both original files.
- Verified that restored file contents matched the original contents.

## 📸 Screenshots

Screenshots of the application execution, encryption output, encrypted files, and restored files are included in this repository.

## ⚠️ Security Notes and Limitations

- The correct master password is required for decryption.
- The current application uses a command-line interface.
- The encrypted key backup is created and can be verified, but it is not currently used for automatic key recovery during decryption.
- The JSON manifest is not cryptographically authenticated.
- The project is intended for educational and demonstration purposes.
- Do not use real confidential data without additional security testing and hardening.
- Never upload actual passwords, private keys, or confidential files to a public repository.

## 🚀 Future Improvements

- Develop a graphical user interface.
- Implement a secure key recovery mechanism.
- Add multi-factor authentication.
- Improve manifest authentication and tamper detection.
- Integrate secure cloud storage.
- Add detailed activity logging.
- Improve support for different file types.

## 🎓 Learning Outcomes

Through this project, I learned about:

- Practical implementation of cryptography.
- Symmetric encryption and decryption.
- Password-based key derivation.
- SHA-256 hashing and file integrity.
- Secure file handling using Python.
- Basic key management and encrypted backups.

## 👨‍💻 Author

**Mihir Koshti**

B.E. Computer Engineering

Cyber Security Project

## 🔗 GitHub Repository

[Cryptographic Encryption Vault](https://github.com/0805-mihir/cryptographic-encryption-vault)

---

**Developed as a practical cybersecurity project using Python and modern cryptographic techniques.**
