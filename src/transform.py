import pandas as pd
import json
from src.config import SETTINGS
from pathlib import Path

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]
    
    for col in out.columns:
        if out[col].dtype == 'object':
          
            out[col] = out[col].str.strip()

    enum_columns = ['email', 'status', 'payment_status', 'payment_method', 'channel']
    for col in enum_columns:
        if col in out.columns:
            out[col] = out[col].str.lower()

    numeric_columns = ['unit_price', 'cost_price', 'order_total', 'discount_amount', 'amount', 'quantity']
    for col in numeric_columns:
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors='coerce')
    
    for col in out.columns:
            if col.endswith(('_at', '_date')):
                out[col] = pd.to_datetime(out[col], errors='coerce', utc=True)
                
    return out

if __name__ == "__main__":
    # Trỏ đến file customers.csv trong thư mục raw
    sample_file = SETTINGS.raw_dir / "customers.csv"
    
    if sample_file.is_file():
        # Đọc dữ liệu gốc (Before)
        df_raw = pd.read_csv(sample_file, encoding="utf-8")
        df_clean = normalize(df_raw)
        evidence_content = "=== BEFORE (5 rows) ===\n" + str(df_raw.head(5)) + "\n\n=== AFTER (5 rows) ===\n" + str(df_clean.head(5))
        # Lưu đúng vào thư mục docs/evidence ở gốc project
        output_dir = Path("docx/evidence")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "05-normalize.txt"
        output_file.write_text(evidence_content, encoding="utf-8")
        
        print(f"[SUCCESS] Đã ghi log chuẩn hóa thành công vào: {output_file.resolve()}")
    else:
        print(f"Không tìm thấy file mẫu tại: {sample_file}")