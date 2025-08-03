from arguments import *
from frontend import frontendDash, frontendCLI
from utils.utils_print import enable_info
from utils.utils_controllers import AbstractFrontend
from pathlib import Path


def main():
    # 0. PARSE APP ARGUMENTS:
    app_args = parse_user_args()
    root : Path = app_args.root
    mode : str  = app_args.mode
    
    frontend : AbstractFrontend
    
    # 1. LAUNCH PRESENTATION:
    root = Path(Path(__file__).parent, "myMoney") if not root else root
    if mode == "cli":
        frontend = frontendCLI(root)
    elif mode == "dash":
        frontend = frontendDash(root)
    
        # 2. LOOP
    frontend.loop()


if __name__ == "__main__":
    main()