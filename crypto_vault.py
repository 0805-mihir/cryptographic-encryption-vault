
import os
import json
import base64
import getpass
import hashlib
import secrets
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag


# ==========================================
# CONFIGURATION
# ==========================================

VAULT_FOLDER = Path("vault_data")
BACKUP_FOLDER = Path("key_backup")
RESTORE_FOLDER = Path("restored_data")

ITERATIONS = 600000
MAGIC = b"CVLT01"


# ==========================================
# PASSWORD INPUT
# ==========================================

def read_password(prompt, minimum_length=12):
    while True:
        # input() is used for compatibility with VS Code debugger.
        # Password will be visible while typing.
        password = input(prompt)

        if len(password) < minimum_length:
            print("[!] Password must contain at least 12 characters.")
            continue

        return password


# ==========================================
# KEY GENERATION
# ==========================================

def derive_key(password, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS
    )

    return kdf.derive(password.encode("utf-8"))


# ==========================================
# FILE ENCRYPTION
# ==========================================

def encrypt_file(source, destination, key):

    data = source.read_bytes()

    nonce = secrets.token_bytes(12)

    encrypted_data = AESGCM(key).encrypt(
        nonce,
        data,
        None
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    destination.write_bytes(
        MAGIC + nonce + encrypted_data
    )

    return hashlib.sha256(data).hexdigest()


# ==========================================
# FILE DECRYPTION
# ==========================================

def decrypt_file(source, destination, key):

    content = source.read_bytes()

    if len(content) < 34:
        raise ValueError("Invalid encrypted file.")

    if not content.startswith(MAGIC):
        raise ValueError("Invalid vault file format.")

    nonce = content[6:18]

    ciphertext = content[18:]

    decrypted_data = AESGCM(key).decrypt(
        nonce,
        ciphertext,
        None
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    destination.write_bytes(decrypted_data)

    return hashlib.sha256(
        decrypted_data
    ).hexdigest()


# ==========================================
# MANIFEST MANAGEMENT
# ==========================================

def save_manifest(manifest):

    VAULT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    manifest_path = VAULT_FOLDER / "manifest.json"

    manifest_path.write_text(
        json.dumps(manifest, indent=4),
        encoding="utf-8"
    )


def load_manifest():

    manifest_path = VAULT_FOLDER / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError("Vault manifest not found.")

    return json.loads(
        manifest_path.read_text(encoding="utf-8")
    )


# ==========================================
# ENCRYPTED KEY BACKUP
# ==========================================

def create_key_backup(key, password):

    BACKUP_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    salt = secrets.token_bytes(16)

    backup_key = derive_key(password, salt)

    nonce = secrets.token_bytes(12)

    encrypted_key = AESGCM(backup_key).encrypt(
        nonce,
        key,
        None
    )

    backup = {
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "iterations": ITERATIONS,
        "encrypted_key": base64.b64encode(
            encrypted_key
        ).decode()
    }

    backup_path = BACKUP_FOLDER / "vault_key_backup.json"

    backup_path.write_text(
        json.dumps(backup, indent=4),
        encoding="utf-8"
    )

    print("[+] Encrypted key backup created.")


# ==========================================
# RESTORE BACKUP KEY
# ==========================================

def restore_key(password):

    backup_path = BACKUP_FOLDER / "vault_key_backup.json"

    if not backup_path.exists():
        raise FileNotFoundError("Key backup not found.")

    backup = json.loads(
        backup_path.read_text(encoding="utf-8")
    )

    salt = base64.b64decode(backup["salt"])
    nonce = base64.b64decode(backup["nonce"])

    encrypted_key = base64.b64decode(
        backup["encrypted_key"]
    )

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=backup["iterations"]
    )

    backup_key = kdf.derive(
        password.encode("utf-8")
    )

    return AESGCM(backup_key).decrypt(
        nonce,
        encrypted_key,
        None
    )


# ==========================================
# DIRECTORY ENCRYPTION
# ==========================================

def encrypt_directory():

    folder_input = input(
        "Enter directory path to encrypt: "
    ).strip().strip('"')

    folder = Path(folder_input)

    if not folder.is_dir():
        print("[!] Directory not found.")
        return

    if VAULT_FOLDER.exists() and any(VAULT_FOLDER.iterdir()):
        print("[!] Vault already contains data.")
        print("[!] Use an empty vault folder.")
        return

    password = read_password(
        "Enter master password: "
    )

    salt = secrets.token_bytes(16)

    key = derive_key(password, salt)

    files = [
        file for file in folder.rglob("*")
        if file.is_file() and not file.is_symlink()
    ]

    if not files:
        print("[!] No files found in directory.")
        return

    manifest = {
        "version": 1,
        "source_directory": folder.name,
        "salt": base64.b64encode(salt).decode(),
        "files": []
    }

    print("\n========== ENCRYPTION STARTED ==========\n")

    for source in files:

        relative_path = source.relative_to(folder)

        destination = (
            VAULT_FOLDER
            / "encrypted"
            / (str(relative_path) + ".enc")
        )

        file_hash = encrypt_file(
            source,
            destination,
            key
        )

        manifest["files"].append({
            "path": relative_path.as_posix(),
            "sha256": file_hash
        })

        print("[+] Encrypted:", relative_path)

    save_manifest(manifest)

    create_key_backup(key, password)

    print("\n========== ENCRYPTION COMPLETED ==========")

    print("[+] Total files encrypted:", len(files))
    print("[+] Original files have NOT been deleted.")
    print("[+] Encrypted files stored in vault_data.")
    print("[+] Key backup stored in key_backup.")


# ==========================================
# DIRECTORY DECRYPTION
# ==========================================

def decrypt_directory():

    manifest = load_manifest()

    password = read_password(
        "Enter master password: "
    )

    salt = base64.b64decode(
        manifest["salt"]
    )

    key = derive_key(password, salt)

    output_folder = (
        RESTORE_FOLDER / manifest["source_directory"]
    )

    print("\n========== DECRYPTION STARTED ==========\n")

    restored_count = 0

    for item in manifest["files"]:

        relative_path = Path(item["path"])

        if (
            relative_path.is_absolute()
            or ".." in relative_path.parts
        ):
            raise ValueError("Unsafe file path detected.")

        source = (
            VAULT_FOLDER
            / "encrypted"
            / (str(relative_path) + ".enc")
        )

        destination = output_folder / relative_path

        if not source.is_file():
            raise FileNotFoundError(
                "Encrypted file missing: " + str(relative_path)
            )

        if destination.exists():
            raise FileExistsError(
                "Restored file already exists: " + str(destination)
            )

        file_hash = decrypt_file(
            source,
            destination,
            key
        )

        if file_hash != item["sha256"]:
            destination.unlink(missing_ok=True)
            raise ValueError(
                "Integrity verification failed: " + str(relative_path)
            )

        restored_count += 1

        print("[+] Restored and verified:", relative_path)

    print("\n========== DECRYPTION COMPLETED ==========")

    print("[+] Total files restored:", restored_count)
    print("[+] SHA-256 verification successful.")
    print("[+] Restored directory:", output_folder)


# ==========================================
# KEY BACKUP VERIFICATION
# ==========================================

def verify_backup():

    password = read_password(
        "Enter backup password: "
    )

    key = restore_key(password)

    print("\n[+] Key backup decrypted successfully.")
    print("[+] Key length:", len(key), "bytes")
    print("[+] AES-256 key backup verified.")


# ==========================================
# MAIN MENU
# ==========================================

def main():

    while True:

        print("\n=========================================")
        print("     CRYPTOGRAPHIC ENCRYPTION VAULT")
        print("=========================================")

        print("1. Encrypt Directory")
        print("2. Decrypt Directory")
        print("3. Verify Key Backup")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:

            if choice == "1":

                encrypt_directory()

            elif choice == "2":

                decrypt_directory()

            elif choice == "3":

                verify_backup()

            elif choice == "4":

                print("\nExiting Cryptographic Encryption Vault.")
                break

            else:

                print("[!] Invalid choice.")

        except InvalidTag:

            print("\n[!] Authentication failed.")
            print("[!] Wrong password or corrupted encrypted data.")

        except Exception as error:

            print("\n[!] Operation failed:", error)


# ==========================================
# PROGRAM EXECUTION
# ==========================================

if __name__ == "__main__":
    main()
