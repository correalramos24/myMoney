
from domain import Domain
from utils import utils_py as upy
from utils.utils_controllers import AbstractCLI

import pandas as pd
from pathlib import Path

class frontendCLI(AbstractCLI):
    def __init__(self, root: Path):
        self._info("INIT")
        self.domain = Domain(root)
        self.budg = self.domain.budgets
        self.movs = self.domain.movements
    
    def _pre_loop_txt(self):
        print("CLI for myMoney!")
        print("* Inputs expect a coma-separated values string!")
        print("* Use format day-month-year-hour for the dates!")
        print("* now() will point to today!")
        print("* start(*) will point to all instances")
        print("* negative command will exit the CLI!")
        print("#"*80)

    def get_callbacks(self):
        d = {
        "Add movement" : lambda : self.add_instance(self.movs.fields, self.movs.add_mov),
        "Add budget"   : lambda : self.add_instance(self.budg.fields, self.budg.add_budget),
        "Del movement" : self.__del_mvmnt,
        "Edt movement" : self.__edt_mvmnt,
        "All movs"     : lambda : self.data_from_callback(self.movs.get_movs),
        "All budgets"  : lambda : self.data_from_callback(self.budg.get_budgets),
        "Movs. x month": lambda : self.__movs_per_month(),
        "Movs. x tag"  : self.__movs_per_tag,
        "Budget x month": self.__budg_per_month,
        }
        return d
    
    @upy.check_excpetions
    def add_instance(self, req_fields, callback: callable):
        usr = input(f"Enter ({upy.stringfy(req_fields)}):").split(",")
        callback(**dict(zip(req_fields, usr)))

    @upy.check_excpetions
    def data_from_callback(self, data_callback: callable):
        data : pd.DataFrame = data_callback()
        if "date" in data.columns:
            data['date'] = pd.to_datetime(data['date'], errors='coerce')
            self._info("Sorting values by", "date")
            data.sort_values(by="date", inplace=True)
        print(data)
    
    @upy.check_excpetions
    def __del_mvmnt(self):
        usr = input("Enter id/ids to be removed (split by commas)")
        for mov_id in usr.split(","):
            pass
            #self.domain.del_movement(mov_id)

    @upy.check_excpetions
    def __edt_mvmnt(self):
        pass
    
    @upy.check_excpetions
    def __movs_per_month(self):
        selection = self.__get_month_from_usr(self.movs.get_avail_instances)
        for month in selection:
            print(self.movs.get_movs(month))
    
    @upy.check_excpetions
    def __budg_per_month(self):
        selection = self.__get_month_from_usr(self.budg.get_avail_instances)
        for month in selection:
            info = self.domain.get_budgets(month)
            print(info)
            print("NET:", info["amount"].sum())
    
    @upy.check_excpetions
    def __movs_per_tag(self):
        selection = self.__get_month_from_usr("movs")
        print(self.domain.monthly_per_tag(selection))


    def __get_month_from_usr(self, data_callback: callable):
        avail_months = data_callback()
        print(avail_months)
        
        usr = input("Enter month/months(split by commas): ")
        selection = avail_months if usr.strip() == "*" else usr.split(",")
        print("Selected", selection)
        return selection