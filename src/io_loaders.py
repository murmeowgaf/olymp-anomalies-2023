import pandas as pd
import re
from typing import Dict

def load_excel_three_sheets(path: str, sheet_map: Dict[str, str]) -> pd.DataFrame:
    xl = pd.ExcelFile(path)
    frames = []
    for grade_key, sheet_name in sheet_map.items():
        if sheet_name not in xl.sheet_names:
            raise ValueError(f"Sheet '{sheet_name}' not found. Available: {xl.sheet_names}")
        df = pd.read_excel(path, sheet_name=sheet_name)
        num = re.findall(r'(\d+)', grade_key)
        df['grade'] = int(num[0]) if num else None
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    return out
