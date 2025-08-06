from persistance import PandasPersistance
from utils.utils_controllers import AbstractDomain
from utils import utils_py as upy

import pandas as pd
from datetime import datetime

class domainMovements(AbstractDomain):
    
    fields = ["concept", "amount", "tag", "date"]
    mov_types  = ["str", "float64", "str", "datetime"]
    
    def init_database(self, db_root): return PandasPersistance(db_root)
    def _create_new_instance(self): return pd.DataFrame()
    
    def add_mov(self, **kwargs):
        self._log(f"Adding movement")
        self.__check_params_correct(kwargs)
        kwargs["date"] = datetime.strptime(kwargs["date"], "%d-%m-%Y")
        
        movs = pd.DataFrame(kwargs,index=[0])
        self._dbg(movs)
        #movs = movs.astype(dict(zip(movDomain.mov_fields,movDomain.mov_types)))
        
        mov_month = self.__get_month(kwargs["date"])
        df = self._get_instance(mov_month, True)
        df = pd.concat([df, movs], ignore_index=True)
        self._update_instance(mov_month, df, True)
        self._ok("DONE")
    
    def del_mov(self, mov_id, unique_id):
        self._log(f"Deleting {mov_id}.{unique_id}!")
    
    def edit_mov(self, mov_id, unique_id, **kwargs):
        self._log(f"Editing {mov_id}.{unique_id}!")
        
    def get_movs(self, dom_id: str | list[str] | None = None) -> pd.DataFrame:
        if upy.is_a_list(dom_id) or dom_id is None:
            dom_id = self.get_avail_instances() if dom_id is None else dom_id
            info = [self._get_instance(m) for m in dom_id]
            if not info: 
                raise Exception("NO DATA FOUND!")
            else: 
                return pd.concat(info, ignore_index=True)                
        elif dom_id:
            return self._get_instance(dom_id)
        else:
            raise Exception(f"UNRECOGNISED PARAMETER {dom_id}")
    
    
    #==========================AGGREGATION METHODS==============================
    def monthly_per_tag(self, dom_id) -> pd.DataFrame:
        return None
    
    #===========================PRIVATE METHODS=================================
    @staticmethod
    def __get_month(dt: datetime):
        "Return a string with format month-year"
        return dt.strftime("%m_%y")
        
    @staticmethod 
    def __check_params_correct(kwargs: dict[str, any]):
        if not (list(kwargs.keys()) == domainMovements.fields):
            raise Exception(f"Invalid args: {kwargs}!")
        

