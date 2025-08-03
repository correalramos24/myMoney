
from utils import utils_print as up
from utils import utils_files as uf

import pickle as pkl
import pandas as pd
from pathlib import Path

class PandasPersistance:
    """
    Persistance controller based on pandas dataframes.
    Dataframes are stored with an unique string identifier.
    """

    def __init__(self, path : Path):
        self.root : Path = path
        self.meta : Path = Path(self.root, "meta.data")
        self.files : dict[str, Path] = dict()
        #TODO: EXTEND THIS
        #self.cache : dict[str, pd.DataFrame] = dict()
        
        self.__info("INIT @", path)
    
        if uf.check_path_exists(path):
            self.__load()
            self.__info2("METADATA:", self.files)
        else:
            self.__info("Creating empty persitance structure!")
            self.__create_persistance()
    
    #========================INTERFACE METHODS==================================
    def store(self, df : pd.DataFrame, pers_id: str):
        self.__info(f"STORING {pers_id} ({id(df)})")
        p = Path(self.root, pers_id+".csv")
        if not self.exist(pers_id):
            self.__info("ADDING NEW ID:", pers_id)
            self.files[pers_id] = p
            self.__save_metadata()
        df.to_csv(p, index=True)            

    def load(self, pers_id: str) -> pd.DataFrame:
        path_df = self.files.get(pers_id)
        if path_df:
            self.__info("LOADING", pers_id)
            return pd.read_csv(path_df, index_col=0)
        else:
            self.__warn("Accesing non-found ID:", id)
            return None

    def exist(self, pers_id) -> bool:
        return pers_id in self.files
    
    def list_entities(self) -> list[str]:
        return list(self.files.keys())
    #==========================PRIVATE METHODS==================================
    def __load(self):
        self.__load_metadata()
    
    def __create_persistance(self):
        uf.create_dir(self.root, False)
        self.__save_metadata()

    def __load_metadata(self):
        with open(self.meta, "rb") as md_file:
            self.files = pkl.load(md_file)

    def __save_metadata(self):
        with open(self.meta, "wb") as md_file:
            pkl.dump(self.files, md_file)

    @staticmethod
    def __info(*args): up.info("DATABS:", *args)
    @staticmethod
    def __info2(*args): up.info2("DATABS:", *args)

if __name__ == "__main__":
    up.enable_info(True)
    up.info("TESTING PERSISTANCE CONTROLLER!")
    
    test_path =Path(Path(__file__).parent, "test_prt")
    
    p = PandasPersistance(test_path)
    df0 = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    })
    p.store(df0, "test1")
    assert(p.exist("test1"))
    assert(uf.check_file_exists(Path(test_path, "test1"+".csv")))
    df1 = p.load("test1")
    assert(df0.equals(df1))