import subprocess
import sys

def install_packages():
    with open('requirements.txt', 'r') as file:
        packages = file.readlines()
    
    for package in packages:
        package = package.strip()
        if package:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

if __name__ == "__main__":
    install_packages()


