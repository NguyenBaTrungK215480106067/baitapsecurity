from datetime import datetime
from pyhanko.sign import signers, fields
from pyhanko.stamp.text import TextStampStyle
from pyhanko.pdf_utils import images
from pyhanko.pdf_utils.text import TextBoxStyle
from pyhanko.pdf_utils.layout import SimpleBoxLayoutRule, AxisAlignment, Margins
from pyhanko.sign.general import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec

# === PATHS (EDIT ACCORDING TO YOUR MACHINE) ===
PDF_IN = r"C:\Users\trung\OneDrive\Documents\BTVN-Sercurity\clean.pdf"
PDF_OUT = r"C:\Users\trung\OneDrive\Documents\BTVN-Sercurity\signed.pdf"
KEY_FILE = r"C:\Users\trung\OneDrive\Documents\BTVN-Sercurity\keys\signer_key.pem"
CERT_FILE = r"C:\Users\trung\OneDrive\Documents\BTVN-Sercurity\keys\signer_cert.pem"
SIG_IMG = r"C:\Users\trung\OneDrive\Documents\BTVN-Sercurity\assets\ten.jpg"

# ======================= PDF SIGNING PROCESS ===========================
print("=== PDF DIGITAL SIGNING PROCESS - LE QUOC TRUNG ===\n".encode('ascii', 'ignore').decode())

# Step 1: Prepare original PDF
print("Step 1: Prepare original PDF (clean.pdf).".encode('ascii', 'ignore').decode())

# Step 2: Create signature field (AcroForm)
print("Step 2: Create SigField1 and reserve /Contents (~8192 bytes).".encode('ascii', 'ignore').decode())

# Step 3: Define ByteRange (hash region excluding /Contents)
print("Step 3: Define ByteRange (hash region excluding /Contents).".encode('ascii', 'ignore').decode())

# Step 4: Compute SHA-256 hash
print("Step 4: Compute SHA-256 hash over ByteRange.".encode('ascii', 'ignore').decode())

# Step 5: Create PKCS#7 detached
print("Step 5: Create PKCS#7 detached (messageDigest, signingTime, cert chain).".encode('ascii', 'ignore').decode())

# === CREATE SIGNER & VALIDATION CONTEXT ===
signer = signers.SimpleSigner.load(KEY_FILE, CERT_FILE, key_passphrase=None)
vc = ValidationContext(trust_roots=[load_cert_from_pemder(CERT_FILE)])

# Step 6: Embed DER PKCS#7 into /Contents
print("Step 6: Embed DER PKCS#7 into /Contents offset (hex-encoded).".encode('ascii', 'ignore').decode())

# Step 7: Write incremental update
print("Step 7: Incremental update (append SigDict + cross-ref).".encode('ascii', 'ignore').decode())

# === OPEN ORIGINAL PDF ===
with open(PDF_IN, "rb") as inf:
    writer = IncrementalPdfFileWriter(inf)

    # Get last page number (to place signature)
    try:
        pages = writer.root["/Pages"]
        if "/Count" in pages:
            num_pages = int(pages["/Count"])
        else:
            num_pages = len(pages["/Kids"])
    except Exception:
        print("WARNING: Cannot read page count, default = 1.".encode('ascii', 'ignore').decode())
        num_pages = 1

    target_page = num_pages - 1  # sign on last page

    # Append signature field
    fields.append_signature_field(
        writer,
        SigFieldSpec(
            sig_field_name="SigField1",
            box=(240, 50, 550, 150),  # signature box (x, y coordinates)
            on_page=target_page
        )
    )

    # === Signature image ===
    background_img = images.PdfImage(SIG_IMG)

    # Layouts
    bg_layout = SimpleBoxLayoutRule(
        x_align=AxisAlignment.ALIGN_MIN,
        y_align=AxisAlignment.ALIGN_MID,
        margins=Margins(right=20)
    )

    text_layout = SimpleBoxLayoutRule(
        x_align=AxisAlignment.ALIGN_MIN,
        y_align=AxisAlignment.ALIGN_MID,
        margins=Margins(left=150)
    )

    text_style = TextBoxStyle(font_size=13)

    # Signature text
    sign_date = datetime.now().strftime("%d/%m/%Y")
    stamp_text = (
        "Le Quoc Trung"
        "\nPhone: 0968128503"
        "\nStudent ID: K225480106065"
        "\nDate: " + sign_date
    )

    stamp_style = TextStampStyle(
        stamp_text=stamp_text,
        background=background_img,
        background_layout=bg_layout,
        inner_content_layout=text_layout,
        text_box_style=text_style,
        border_width=1,
        background_opacity=1.0,
    )

    # Signature metadata
    meta = signers.PdfSignatureMetadata(
        field_name="SigField1",
        reason="Digital signature for Security Assignment",
        location="Thai Nguyen, VN",
        md_algorithm="sha256",
    )

    pdf_signer = signers.PdfSigner(
        signature_meta=meta,
        signer=signer,
        stamp_style=stamp_style,
    )

    # Perform signing and save
    with open(PDF_OUT, "wb") as outf:
        pdf_signer.sign_pdf(writer, output=outf)

# Step 8: LTV (DSS)
print("Step 8: LTV DSS - Append Certs/OCSP/CRLs/VRI (if available).".encode('ascii', 'ignore').decode())

print("\nPDF has been successfully signed!".encode('ascii', 'ignore').decode())
print("Signed file saved at:".encode('ascii', 'ignore').decode(), PDF_OUT)
