from pathlib import Path
import pandas as pd

class FileSystem:
    
    def __init__(self, finance_dir_path: Path, username: str) -> None:
        self.username = username
        self.finance_dir_path = finance_dir_path
        self.receipts_dir_path = finance_dir_path / Path("receipts") / Path(username)
        self.receipts_tmp_path = self.receipts_dir_path / Path("tmp")

    
    def receipts_to_dataframe(self) -> pd.DataFrame:
        pass




    
