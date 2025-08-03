from persistance import PandasPersistance, KeyValuePersistance

from utils import utils_print as up
from utils import utils_files as uf

import pandas as pd
from pathlib import Path
from datetime import datetime

class Domain:
    
    movement_fields = ["concept", "amount", "tag", "date"]
    budget_fields   = ["concept", "tag", "amount", "date"]
    MOVMENTS = "movements_"
    BUDGET   = "budget_"
    INSTANCE_TYPE = [MOVMENTS, BUDGET]
        
    def __init__(self, root: Path):
        self.__info("INIT DOMAIN!")
        self.instances : dict[str, pd.DataFrame] = dict()
        self.db = PandasPersistance(root)
        #self.tags      : dict[str, tuple[str, str]] = dict()
        self.tags_db = KeyValuePersistance(Path(root, "tags"))
        
    def add_movement(self, **kwargs):
        self.__check_params_correct(kwargs, Domain.movement_fields)
        kwargs["date"] = datetime.strptime(kwargs["date"], "%d-%m-%Y")

        # build object:
        movement = pd.Series(kwargs).to_frame().T
        # Append data:
        mov_month = self.__get_month(kwargs["date"])
        df = self.__get_domain(Domain.MOVMENTS, mov_month, True)
        df = pd.concat([df, movement], ignore_index=True)
        self.__update_domain(Domain.MOVMENTS, mov_month, df)
        
        # Save to conclude Tx:
        self.__save_domain(Domain.MOVMENTS, mov_month)
    
    def del_movement(self, mov_id):
        pass
    
    def edit_movement(self, mov_id, **kwargs):
        pass
            
    def list_movement_month(self, month):
        df =  self.__get_domain(Domain.MOVMENTS, month)
        print(df)
    
    def get_movs(self, dom_id: str = None) -> pd.DataFrame:
        if dom_id:
            return self.__get_domain(Domain.MOVMENTS, dom_id)
        
        # If not dom_id -> return all
        ret = [self.__get_domain(Domain.MOVMENTS, m) 
               for m in self.list_avail_months()]

        if not ret: raise Exception("No movements found")
        return pd.concat(ret, ignore_index=True)
    
    def list_avail_months(self):
        return [month.removeprefix(Domain.MOVMENTS) 
                for month in self.db.list_entities() 
                if month.startswith(Domain.MOVMENTS)]
    
    
    def add_budget(self, **kwargs):
        self.__check_params_correct(kwargs, Domain.movement_fields)
    
    #==========================AGGREGATION METHODS==============================
    def monthly_per_tag(self, dom_id) -> pd.DataFrame:
        pass
    
    
    #==========================PRIVATE METHODS==================================           
    def __get_domain(self, instance_type : str, 
                     dom_id : str, crt=False) -> pd.DataFrame:
        if instance_type not in Domain.INSTANCE_TYPE:
            raise Exception(f"Invalid {instance_type} @ get_domain")
        
        real_id = instance_type + dom_id
        instance = self.instances.get(real_id)
        
        if instance is not None: 
            return instance
        else:
            self.__info("Unable to find", real_id, "@ DOM.")
            if self.db.exist(real_id):
                self.instances[real_id] = self.db.load(real_id)
            elif crt:
                self.__info("Unable to find", real_id, "@ DB.")
                self.instances[real_id] = pd.DataFrame()
            else:
                raise Exception("Trying to load invalid entity", dom_id)
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
    @staticmethod
    def __info2(*args): up.info2("DOMAIN:", *args)
    
    @staticmethod 
    def __check_params_correct(kwargs: dict[str, any], expected: list[str]):
        #TODO: Increase error management (throw which params are missing)
        if not (list(kwargs.keys()) == expected):
            raise Exception(f"Invalid args: {kwargs}!")
        

if __name__ == "__main__":
    up.enable_info(True)
    up.info("TESTING DOMAIN CONTROLLER!")
    
    test_path =Path(Path(__file__).parent, "test_domain")
    d = Domain(test_path)
    test_movement = {
        "concept": "SOPAR",
        "amount": -33,
        "tag_name": "CENA",
        "tag_color": "ORANGE",
        "date": "01-07-2025",
    }
    #d.add_movement(**test_movement)
    d.list_movement_month("08_25")
    d.list_movement_month("07_25")