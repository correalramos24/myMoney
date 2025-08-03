
from domain import Domain

from utils import utils_print as up
from utils import utils_py as upy

from dash import Dash, html, dcc, dash_table,callback, Output, Input

import plotly.express as px

from pathlib import Path

class frontendCLI():
    def __init__(self, root: Path):
        self.__print("INIT")
        self.domain = Domain(root)
        self.root = Dash()
        
    def loop(self):        
        print("CLI for myMoney!")
        print("* Inputs expect a coma-separated values string!")
        print("* Use format day-month-year-hour for the dates!")
        print("* now() will point to today!")
        print("* negative command will exit the CLI!")
        print("#"*80)
        
        cmd : int = 0
        while cmd >= 0:
            cmd = self.__next_op()
            if cmd < 0: break
            
            match cmd:
                case 1: self.__add_mvmnt()
                case 2: self.__del_mvmnt()
                case 3: self.__edt_mvmnt()
                case 4: self.__all_movs()
                case 5: self.__movs_per_month()
                case 6: self.__movs_per_tag()
                case 7: self.__add_budget()
                case _: print("Invalid cmd:", cmd)
            print("-"*80)
    
    @upy.check_excpetions
    def __add_budget(self):
        fields = self.domain.budget_fields
        usr = input(f"Enter budget. values ({upy.stringfy(fields)}):")\
            .split(",")
        self.domain.add_budget(**dict(zip(fields, usr))) 
    
    
    @upy.check_excpetions
    def __add_mvmnt(self):
        fields = self.domain.movement_fields
        usr = input(f"Enter mov. values ({upy.stringfy(fields)}):")\
            .split(",")
        self.domain.add_movement(**dict(zip(fields, usr))) 

    @upy.check_excpetions
    def __all_movs(self): print(self.domain.get_movs())
    
    @upy.check_excpetions
    def __del_mvmnt(self):
        self.__all_movs()
        usr = input("Enter id/ids to be removed (split by commas)")
        for mov_id in usr.split(","):
            self.domain.del_movement(mov_id)

    @upy.check_excpetions
    def __edt_mvmnt(self):
        pass
    
    @upy.check_excpetions
    def __movs_per_month(self):
        print(self.domain.list_avail_months())
        usr = input("Enter month/months(split by commas)")
        for month in usr.split(","):
            print(self.domain.get_movs(month))
    
    @upy.check_excpetions
    def __movs_per_tag(self):
        print(self.domain.list_avail_months())
        for month in self.domain.list_avail_months():
            print(self.domain.get_movs(month))

    @upy.safe_return(default=0)
    def __next_op(self):
        for i, cmd in enumerate(self.__list_cmd()):
            print('>',i+1, cmd)
        return int(input("ENTER COMMAND:"))
        
    def __list_cmd(self):
        return ["add movement", "del movement", "edit movement",
                "list all movements", "list movement per month", "list per tag"]
    
    def __print(self, *msg): up.info("PRSTN: ",*msg)

class frontendDash():
    
    def __init__(self, root: Path):
        self.__print("INIT")
        self.domain = Domain(root)
        self.root = Dash()
    
    def loop(self):
        self.root.layout = [
            html.H1(children='myMoney Dashboard', style={'textAlign':'center'}),
            html.H2(children='Status'),
            html.Hr(),
            html.H2(children="Month movements"),
            dcc.Dropdown(self.domain.list_avail_months(), id='month-dd'),
            dash_table.DataTable(data=self.domain.get_movs().to_dict('records'), id="table"),
            html.Button('Add movement', id='submit-val', n_clicks=0),
        ]
        
        
        @callback(
            Output('table','data'),
            Input('month-dd', 'value')
        )
        def update_table(value):
            self.__print('PRONTO?')
            return self.domain.get_movs(value).to_dict('records')
 
        self.root.run(debug=True)
        
    def __print(self, *msg): up.info("PRSTN: ",*msg)
        
    