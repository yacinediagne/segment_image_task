import os
import subprocess

print("------------Step 1 : Virtual Environment creation -----------.")


# Workdirectory path
working_dir = os.getcwd()

# Environment Name
venv_name = "venv"

# Create virtual environment
subprocess.run(["python", "-m", "venv", venv_name], check=True)

# Activate the environment
if os.name == "posix":  # Linux
    activate_path = os.path.join(working_dir, venv_name, "bin", "activate")
    subprocess.run(["source", activate_path], shell=True, check=True)
elif os.name == "nt":  # windowa
    activate_path = os.path.join(working_dir, venv_name, "Scripts", "activate")
    subprocess.run([activate_path], shell=True, check=True)

# Requirements i
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

print("Virtual environment created successfuly  ;).")

print("------------Step 2 : Testing -----------.")

#Executing the Test
subprocess.run(["pytest", "test_microservice.py"], check=True)