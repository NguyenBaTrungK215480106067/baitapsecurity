BÀI TẬP VỀ NHÀ – MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN
Chủ đề: Chữ ký số trong file PDF
Giảng viên: Đỗ Duy Cốp
Thời điểm giao: 2025-10-24 11:45
Đối tượng áp dụng: Toàn bộ sv lớp học phần 58KTPM
Hạn nộp: Sv upload tất cả lên github trước 2025-10-31 23:59:59

Lê Quốc Trung - K225480106065
I. MÔ TẢ CHUNG
Sinh viên thực hiện báo cáo và thực hành: phân tích và hiện thực việc nhúng, xác thực chữ ký số trong file PDF.
Phải nêu rõ chuẩn tham chiếu (PDF 1.7 / PDF 2.0, PAdES/ETSI) và sử dụng công cụ thực thi (ví dụ iText7, OpenSSL, PyPDF, pdf-lib).

II. CÁC YÊU CẦU CỤ THỂ
1) Cấu trúc PDF liên quan chữ ký (Nghiên cứu)
PDF & Digital Signature Concepts (PAdES)

Catalog: Root object of a PDF, links to pages and document structure.

Pages tree: Hierarchical structure of all pages in the PDF.

Page object: Represents a single page, includes references to content, resources, and annotations.

Resources: Fonts, images, XObjects, and other objects used in page content.

Content streams: Instructions for drawing text, images, and graphics on a page.

XObject: External objects like images or forms that can be reused in pages.

AcroForm: Interactive form structure in PDF, contains fields like text boxes, checkboxes, and signature fields.

Signature field (widget): Form field that holds a digital signature.

Signature dictionary (/Sig): PDF object storing signature information such as signer, time, and certificate.

/ByteRange: Byte offsets indicating which parts of the PDF are signed.

/Contents: Placeholder for the actual digital signature (PKCS#7 or CMS).

Incremental updates: Appending changes to a PDF without rewriting the entire file, used for signing.

DSS (Document Security Store, PAdES): Optional structure storing certificates, OCSP responses, and CRLs for long-term validation.

2) Thời gian ký được lưu ở đâu?
/M trong Signature dictionary
Là thuộc tính Metadata của chữ ký (/Sig).

Dạng text, chỉ lưu thời điểm ký trên PDF.

Không có giá trị pháp lý, chỉ mang tính tham khảo.

Timestamp token (RFC 3161) trong PKCS#7

Là chứng chỉ thời gian được cấp bởi TSA (Time Stamping Authority).

Lưu trong attribute timeStampToken của chữ ký CMS/PKCS#7.

Có giá trị pháp lý, xác nhận chữ ký tồn tại tại thời điểm nhất định.

Document timestamp object (PAdES)

Là một signature object đặc biệt chỉ chứa timestamp, không chứa chữ ký người dùng.

Dùng cho Long Term Validation (LTV) theo PAdES.

DSS (Document Security Store)

Nếu PDF có DSS, có thể lưu timestamp và dữ liệu xác minh như chứng chỉ, OCSP, CRL.

Hỗ trợ xác minh chữ ký dài hạn (LTV) mà không cần kết nối Internet.

3) Các bước tạo và lưu chữ ký trong PDF (đã có private RSA)
Viết script/code thực hiện tuần tự:
Prepare original PDF
Chuẩn bị file PDF gốc cần ký.

File này sẽ là input cho quá trình ký số.

Create Signature field (AcroForm)
Tạo signature field (widget) trên PDF, thường tên là SigField1.

Reserve vùng /Contents (~8192 bytes) để lưu chữ ký sau này.

Define /ByteRange
Xác định vùng PDF sẽ tính hash, loại trừ vùng /Contents.

/ByteRange lưu các offset bắt đầu và kết thúc của vùng được ký.

Compute hash
Tính hash (SHA-256 hoặc SHA-512) trên vùng /ByteRange.

Hash này là cơ sở để tạo chữ ký số.

Create PKCS#7/CMS detached or CAdES
Bao gồm các attribute:

messageDigest (hash của PDF)

signingTime (thời điểm ký)

contentType (PDF)

Bao gồm certificate chain của signer.

Tùy chọn: thêm RFC3161 timestamp token để xác thực thời điểm ký.

Thông số bảo mật:

Hash algorithm: SHA-256 / SHA-512

RSA padding: PKCS#1 v1.5

Key size: ≥2048 bits

Các thông tin này lưu trong PKCS#7 ở phần signed attributes.

Embed DER PKCS#7 into /Contents
Chèn blob chữ ký DER vào vùng /Contents.

Lưu ý offset đúng theo /ByteRange.

Write incremental update
Ghi cập nhật bổ sung vào PDF, giữ nguyên nội dung gốc.

PDF vẫn hợp lệ, chữ ký được thêm mà không ghi đè file gốc.

(LTV) Update DSS
Nếu muốn Long Term Validation (LTV), cập nhật Document Security Store (DSS):

Chứng chỉ (Certs)

OCSP responses

CRLs

Validation-Related Information (VRI)

4) Các bước xác thực chữ ký trên PDF đã ký
Các bước kiểm tra:
Đọc Signature dictionary: /Contents, /ByteRange.
Tách PKCS#7, kiểm tra định dạng.
Tính hash và so sánh messageDigest.
Verify signature bằng public key trong cert.
Kiểm tra chain → root trusted CA.
Kiểm tra OCSP/CRL.
Kiểm tra timestamp token.
Kiểm tra incremental update (phát hiện sửa đổi).
Nộp kèm script verify + log kiểm thử.
III. YÊU CẦU NỘP BÀI
Báo cáo PDF ≤ 6 trang: mô tả cấu trúc, thời gian ký, rủi ro bảo mật.
Code + README (Git repo hoặc zip).
Demo files: original.pdf, signed.pdf, tampered.pdf.
(Tuỳ chọn) Video 3–5 phút demo kết quả.
IV. TIÊU CHÍ CHẤM
Lý thuyết & cấu trúc PDF/chữ ký: 25%
Quy trình tạo chữ ký đúng kỹ thuật: 30%
Xác thực đầy đủ (chain, OCSP, timestamp): 25%
Code & demo rõ ràng: 15%
Sáng tạo mở rộng (LTV, PAdES): 5%
V. GHI CHÚ AN TOÀN
Vẫn lưu private key (sinh random) trong repo. Tránh dùng private key thương mại.
Dùng RSA ≥ 2048-bit và SHA-256 hoặc mạnh hơn.
Có thể dùng RSA-PSS thay cho PKCS#1 v1.5.
Khuyến khích giải thích rủi ro: padding oracle, replay, key leak.
VI. GỢI Ý CÔNG CỤ
OpenSSL, iText7/BouncyCastle, pypdf/PyPDF2.
Tham khảo chuẩn PDF: ISO 32000-2 (PDF 2.0) và ETSI EN 319 142 (PAdES).
