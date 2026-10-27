
from pathlib import Path

output_dir = Path("sample_documents")
output_dir.mkdir(exist_ok=True)

documents = {
    "employee_leave_policy.pdf": [
        ("Employee Leave Policy", 18),
        ("This is a fictional company policy for a learning project.", 12),
        ("Casual Leave", 14),
        ("Employees may take 12 casual leave days per calendar year.", 12),
        ("Sick Leave", 14),
        ("Employees may take 8 sick leave days per calendar year.", 12),
        ("Leave requests must be submitted to the reporting manager.", 12),
    ],
    "it_support_policy.pdf": [
        ("IT Support Policy", 18),
        ("This is a fictional company policy for a learning project.", 12),
        ("Password Reset", 14),
        ("Employees should use the company password reset portal.", 12),
        ("IT Support Hours", 14),
        ("The IT support team operates from 9 AM to 6 PM on weekdays.", 12),
        ("Critical incidents should be reported to the IT help desk.", 12),
    ],
    "expense_policy.pdf": [
        ("Expense Reimbursement Policy", 18),
        ("This is a fictional company policy for a learning project.", 12),
        ("Meal Expenses", 14),
        ("Employees may claim up to INR 500 per eligible business meal.", 12),
        ("Submission Deadline", 14),
        ("Expense claims must be submitted within 15 days of the expense.", 12),
        ("Receipts must be attached to every expense claim.", 12),
    ],
}


def escape_pdf_text(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def create_pdf(path, lines):
    commands = ["BT", "50 790 Td"]

    for index, (text, font_size) in enumerate(lines):
        if index > 0:
            commands.append("0 -35 Td")

        commands.append(f"/F1 {font_size} Tf")
        commands.append(f"({escape_pdf_text(text)}) Tj")

    commands.append("ET")
    stream = "\n".join(commands).encode("ascii", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode()
    )

    path.write_bytes(pdf)


for filename, lines in documents.items():
    create_pdf(output_dir / filename, lines)
    print(f"Created: {output_dir / filename}")

print("\nAll sample PDFs created.")
