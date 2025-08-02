from persistance import PandasPersistance

from utils import utils_print as up
from utils import utils_files as uf

import pandas as pd
from pathlib import Path
from datetime import datetime

class Domain:
    
    movement_fields = ["concept", "amount", "tag_name", "tag_color", "date"]
        
    def __init__(self, root: Path):
        self.instances : dict[str, pd.DataFrame] = dict()
        self.__info("INIT DOMAIN!")
        self.db = PandasPersistance(root)
    
    def add_movement(self, **kwargs):
        self.__check_params_correct(kwargs, Domain.movement_fields)
        kwargs["date"] = datetime.strptime(kwargs["date"], "%d-%m-%Y")

        # build object:
        movement = pd.Series(kwargs).to_frame().T
        # Append data:
        mov_month = self.__get_month(kwargs["date"])
        df = self.__get_domain("movements", mov_month)
        df = pd.concat([df, movement], ignore_index=True)
        self.__update_domain("movements", mov_month, df)
        
        # Save to conclude Tx:
        self.__save_domain("movements", mov_month)
        
    def list_movement_month(self, month):
        df =  self.__get_domain("movements", month)
        print(df)
    
    def list__movements_all(self):
        pass
    
    #==========================PRIVATE METHODS==================================
    def __get_domain(self, instance_type : str, dom_id : str) -> pd.DataFrame:
        if instance_type != "movements" and instance_type != "budget":
            raise Exception(f"Invalid {instance_type} @ get_instance")
        
        real_id = instance_type + "_" + dom_id
        instance = self.instances.get(real_id)
        
        if instance is not None: 
            return instance
        else:
            self.__info("Unable to find", real_id, "@ DOM.")
            if self.db.exist(real_id):
                self.instances[real_id] = self.db.load(real_id)
            else:
                self.__info("Unable to find", real_id, "@ DB.")
                self.instances[real_id] = pd.DataFrame()
            return self.instances[real_id]
    
    def __update_domain(self, isnt_type : str, dom_id : str, df: pd.DataFrame):
        if isnt_type != "movements" and isnt_type != "budget":
            raise Exception(f"Invalid type {isnt_type} @ get_instance")
        
        real_id = isnt_type + "_" + dom_id
        self.__info2(real_id, "->", id(df))
        self.instances[real_id] = df
    
    def __save_domain(self, isnt_type, dom_id) -> None:
        if isnt_type != "movements" and isnt_type != "budget":
            raise Exception(f"Invalid type {isnt_type} @ get_instance")
        
        real_id = isnt_type + "_" + dom_id
        self.__info(f"SAVE {real_id} ({id(self.instances[real_id])})")
        
        self.db.store(self.instances[real_id], real_id)

    @staticmethod
    def __get_month(dt: datetime):
        "Return a string with format month-year"
        return dt.strftime("%m_%y")
    
    @staticmethod
    def __info(*args): up.info("DOMAIN:", *args)
    def __info2(*args): up.info2("DOMAIN:", *args)
    
    @staticmethod 
    def __check_params_correct(kwargs: dict[str, any], expected: list[str]):
        #TODO: Increase error management (throw which params are missing)
        if not (list(kwargs.keys()) == expected):
            raise Exception("Invalid args!")
        

if __name__ == "__main__":
    up.enable_info(True)
    up.info("TESTING DOMAIN CONTROLLER!")
    
    test_path =Path(Path(__file__).parent, "test_domain")
    d = Domain(test_path)
    test_movement = {
        "concept": "ABACUS",
        "amount": -10,
        "tag_name": "MATERIAL",
        "tag_color": "RED",
        "date": "01-08-2025",
    }
    d.add_movement(**test_movement)
    d.list_movement_month("08_25")