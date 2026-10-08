import json
import pandas as pd
from pathlib import Path
from src.config import SETTINGS

def read_dataset(file_path: Path) -> pd.DataFrame:
    if not file_path.is_file():
        raise FileNotFoundError(f"Missing file: {file_path}")
    
    if file_path.suffix == ".csv":
        try:
           df = pd.read_csv(file_path , encoding="utf-8")
        except UnicodeDecodeError:
           df = pd.read_csv(file_path,encoding="utf-8-sig" )
    elif file_path.suffix == ".json":
        try:
            raw_data = json.loads(file_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            raise ValueError(f"error file:{file_path}")
        if isinstance(raw_data, list):
            df = pd.DataFrame(raw_data)
        elif isinstance(raw_data, dict) and "data" in raw_data:
             df = pd.DataFrame(raw_data["data"])
        else:
             raise ValueError(f"Unsupported file: {file_path}")
        
    else:
            raise ValueError(f"Unsupported file: {file_path}")
    if len(df) == 0:
         raise ValueError(f"Empty dataset: {file_path}")

    return df
  
def profile(df: pd.DataFrame) -> dict:
    rows = len(df)
    columns = list(df.columns)
    missing = df.isna().sum().to_dict()
    duplicates = int(df.duplicated().sum())
    return {
        'rows': rows, 
        'columns': columns, 
        'missing': missing, 
        'duplicates': duplicates
    }
if __name__ == "__main__":
    # 1. Khai báo danh sách các file cần test
    test_files = [
        "customers.csv",
        "products.csv",
        "orders.csv",
        "order_items.csv",
        "payments.json"
    ]
    
    print("--- BẮT ĐẦU CHẠY KIỂM THỬ ---")
    
    # 2. Dùng vòng lặp quét qua từng tên file
    for file_name in test_files:
        folder_path = Path("data/incremental/day_2026-07-01")
        full_path = folder_path / file_name
        
        try:
            df = read_dataset(full_path) 
            stats = profile(df)
            print(f"dataset={file_name} rows={stats['rows']} cols={len(stats['columns'])} missing={stats['missing']} duplicates={stats['duplicates']}")

        except Exception as e:
            print(f"[ERROR] {file_name} -> {type(e).__name__}")