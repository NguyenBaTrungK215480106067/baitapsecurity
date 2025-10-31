from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os

# === Configure paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "keys")
os.makedirs(KEYS_DIR, exist_ok=True)

PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "signer_key.pem")
CERT_PATH = os.path.join(KEYS_DIR, "signer_cert.pem")

# === 1. Generate private RSA key (2048 bits) ===
print("Generating RSA 2048-bit private key...")
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# === 2. Create a self-signed certificate ===
print("Creating self-signed certificate...")

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Thai Nguyen"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Thai Nguyen"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "K58KTPM"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "MSSV: k225480106065"),
    x509.NameAttribute(NameOID.COMMON_NAME, "Lung Quoc Tre"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, "5276183490@example.invalid"),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow() - timedelta(minutes=1))
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    )
    .sign(private_key, hashes.SHA256())
)

# === 3. Write private key to file ===
with open(PRIVATE_KEY_PATH, "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
print(f"Private key saved at: {PRIVATE_KEY_PATH}")

# === 4. Write certificate to file ===
with open(CERT_PATH, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
print(f"Certificate saved at: {CERT_PATH}")

# === Done ===
print("\nKey pair and self-signed certificate created successfully.")
