
import utils.utils_print as up
import utils.utils_files as uf
from utils.utils_controllers import AbstractPersistance

import pandas as pd
from pathlib import Path

class KeyValuePersistance(AbstractPersistance):
    def store(self, content : str, pers_id : str):
        self._info(f"STORING {pers_id} {content}")
        self.entities[pers_id] = content
        self._save_metadata()
        
    def load(self, pers_id : str) -> str:
        ret = self.entities.get(pers_id)
        if ret:
            return ret
        else:
            self._warn("Accesing non-found ID:", id)
            return None       


class PandasPersistance(AbstractPersistance):
    """
    Persistance controller based on pandas dataframes.
    Dataframes are stored with an unique string identifier.
    """
    
    #========================INTERFACE METHODS==================================
    def store(self, content: any, pers_id : str):
        self._dbg(f"STORING {pers_id} ({id(content)})")
        p = Path(self.root, pers_id+".csv")
        if not self.exist(pers_id):
            self._dbg("ADDING NEW ID:", pers_id)
            self.entities[pers_id] = p
            self._save_metadata()
        content.to_csv(p, index=True)            

    def load(self, pers_id: str) -> pd.DataFrame:
        path_df = self.entities.get(pers_id)
        if path_df:
            self._info("LOADING", pers_id)
            return pd.read_csv(path_df, index_col=0)
        else:
            self._warn("Accesing non-found ID:", id)
            return None


if __name__ == "__main__":
    up.enable_info(True)
    up.info("TESTING PERSISTANCE CONTROLLER!")
    
    test_path =Path(Path(__file__).parent, "test_prt")
    
    p = PandasPersistance(test_path)
    pt = KeyValuePersistance(Path(test_path, "tags"))
    df0 = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    })
    p.store(df0, "test1")
    pt.store("BLUE", "MATERIAL")
    pt.store("RED", "PARTY")
    print(pt.list_entities())
    assert(p.exist("test1"))
    assert(uf.check_file_exists(Path(test_path, "test1"+".csv")))
    df1 = p.load("test1")
    assert(df0.equals(df1))