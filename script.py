import os
import subprocess

print("===============================Step 1 : Virtual Environment creation =================================")

# Workdirectory path
working_dir = os.getcwd()

# Environment Name
venv_name = "venv"

# Path to the virtual environment
venv_path = os.path.join(working_dir, venv_name)

# Check if the virtual environment exists
if not os.path.exists(venv_path):
    # Create virtual environment
    subprocess.run(["python", "-m", "venv", venv_name], check=True)
    
    # Activate the environment
    if os.name == "posix":  # Linux
        activate_path = os.path.join(venv_path, "bin", "activate")
        subprocess.run(["source", activate_path], shell=True, check=True)
    elif os.name == "nt":  # Windows
        activate_path = os.path.join(venv_path, "Scripts", "activate")
        subprocess.run([activate_path], shell=True, check=True)

    # Install requirements
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

print("=====================================Virtual environment created or exists already ;) ====================")

print("===================================== Step 2 : Testing ==============================================")

# Run tests with pytest
subprocess.run(["pytest", "test_microservice.py"], check=True)
