import subprocess
import sys

def compile_to_exe(python_file):
    # Install pyinstaller if not installed
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "pyinstaller"])
    # Compile the python script into a single .exe file
    subprocess.run(["pyinstaller", "--onefile", python_file])

if __name__ == "__main__":
    compile_to_exe("your_script.py")  # Replace 'your_script.py' with your actual Python filename
