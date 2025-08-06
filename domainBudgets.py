from persistance import KeyValuePersistance
from utils.utils_controllers import AbstractDomain

from utils import utils_py as upy

import pandas as pd
from datetime import datetime

class domainBudgets(AbstractDomain):

    fields  = ["concept", "tag", "amount", "date"]
    budget_types   = ["str", "str", "float64", "datetime"]
    
    def init_database(self, db_root): return KeyValuePersistance(db_root)
    def _create_new_instance(self): return dict()
            
    def add_budget(self, **kwargs):
        pass
    
    def del_budget(self, mov_id, unique_id):
        pass
    
    def edit_budget(self, mov_id, unique_id, **kwargs):
        pass
    
    def get_budgets(self, dom_id: str | list[str] | None = None) -> pd.DataFrame:
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
    
            
    @staticmethod
    def __get_month(dt: datetime):
        "Return a string with format month-year"
        return dt.strftime("%m_%y")
    

    @staticmethod 
    def __check_params_correct(kwargs: dict[str, any]):
        #TODO: Increase error management (throw which params are missing)
        if not (list(kwargs.keys()) == domainBudgets.fields):
            raise Exception(f"Invalid args: {kwargs}!")
        
