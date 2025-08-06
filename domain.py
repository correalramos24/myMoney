from domainBudgets import domainBudgets
from domainMovements import domainMovements

from utils.utils_controllers import metaAbstractClass

from pathlib import Path

class Domain(metaAbstractClass):
    
    def __init__(self, root: Path):
        self._info("INITIALIZING MyMoney DOMAIN!")
        self.budgets   = domainBudgets(Path(root, "budgets")) 
        self.movements = domainMovements(Path(root, "movs"))
        
    
   