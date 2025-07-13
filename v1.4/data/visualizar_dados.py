from decimal import Decimal
import pandas as pd
from sqlalchemy import select
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db import Session, vendas

def visualizer_data_db(df: pd.DataFrame) -> pd.DataFrame:
    print("DEBUG: Calling visualizer_data()")
    if not df.empty:
        print(df)
        return df
    else:
        with Session() as session:
            stmt = select(vendas)
            print(f"DEBUG: Executing SQL: {stmt}")
            records = session.execute(stmt).mappings().all()
            print(f"DEBUG: Retrieved {len(records)} rows")
        return pd.DataFrame(records)
    
    
def visualizer_data_local(df: pd.DataFrame) -> pd.DataFrame:
    print("DEBUG: Calling visualizer_data()")
    return df