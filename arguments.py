from utils.utils_bash import execute_command_get_ouput
from utils.utils_print import enable_info

import argparse
from pathlib import Path

VERSION="ALFA"

def parse_user_args():
    
    # Declare the flags:
    parser = argparse.ArgumentParser(description="myMoney - Money manager",
                                    usage="myMoney.py", 
                                    epilog=f"VERSION: {VERSION}")
    
    parser.add_argument("--root", help="Set root to store data",
                        default=None, type=Path)
    
    parser.add_argument("--mode", help="Set mode to run the app", 
                        choices=['dash', 'cli', 'telegramServer'],
                        default='cli')
    
    parser.add_argument('--info', help="Add info messages", 
                        action='store_true')
    
    parser.add_argument('--verbose', help="Set verbose level", 
                        type=int, default=0)    
        
    parser.add_argument('--version', help="Print YAW version", 
                        action='store_true')
    parser.add_argument('--dev-version', help="Print YAW version, detailed", 
                        action='store_true')

    # Parse the arguments:
    if parser.parse_args().dev_version:
        home = Path(__file__).parent
        print("Yaw installed at", home)
        br = execute_command_get_ouput("git rev-parse --abbrev-ref HEAD", home)
        cm = execute_command_get_ouput("git rev-parse --short HEAD", home)
        tg = execute_command_get_ouput("git describe --tags --abbrev=0", home)
        print(f"VERSION: {VERSION} ({tg}) => BRANCH: {br} @ COMMIT: {cm}")
        exit(0)
    if parser.parse_args().version:
        print(f"VERSION: {VERSION}")
        exit(0)
    
    enable_info(parser.parse_args().info)
    
    return parser.parse_args()
    