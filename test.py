import os
import ast
import re

def extract_imports_from_content(content):
    submodules = set()
    tree = ast.parse(content)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in getattr(node, 'names', []):
                submodule = alias.name.split('.')[0]
                submodules.add(submodule)

    return submodules

def find_requirements_txt(folder):
    requirements_txt_path = os.path.join(folder, 'requirements.txt')
    return requirements_txt_path if os.path.exists(requirements_txt_path) else None

def find_python_files(folder):
    python_files = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_dependencies_from_requirements(requirements_txt_path):
    try:
        with open(requirements_txt_path, 'r', encoding='utf-8') as req_file:
            requirements = req_file.readlines()
    except UnicodeDecodeError:
        # Try using 'utf-8-sig' or 'latin-1' if 'utf-8' fails
        with open(requirements_txt_path, 'r', encoding='utf-8-sig') as req_file:
            requirements = req_file.readlines()

    dependencies_list = []
    for requirement in requirements:
        requirement = requirement.strip()

        # Ignore comments and blank lines
        if not requirement or requirement.startswith('#'):
            continue

        # Extract the package name, version, and platform
        parts = re.split(r'[=<>!]+', requirement, 1)
        name = parts[0].strip()
        version = parts[1].strip() if len(parts) > 1 else None

        # Assuming the platform is unknown for this example
        platform = 'PyPi'

        dependencies_list.append({'name': name, 'version': version, 'platform': platform})

    return dependencies_list

# Replace 'your_folder_path' with the path to the root folder containing .py files
folder_path = r'C:\Users\LENOVO\Desktop\magic-animate-main'
final_module = set()
final_dependencies = []
final_modules=[]

# Find the path to requirements.txt outside the loop
requirements_path = find_requirements_txt(folder_path)

# Now, iterate over Python files
python_files = find_python_files(folder_path)
for py_file in python_files:
    with open(py_file, 'r', encoding='utf-8') as file:
        script_content = file.read()

    script_modules = extract_imports_from_content(script_content)
    final_module.update(script_modules)

# Print the modules
print("\n") 
print("*******************************************************************")
print("MODULES:-")
print("*******************************************************************")
print("\n")
for module in final_module:
    print(f'Module: {module}')
# print(f'Modules:{final_modules}')
print("\n") 
print("*******************************************************************")
print("PACKAGES:-")
print("*******************************************************************")
print("\n")
# Print the requirements.txt file content
if requirements_path is not None:
    final_dependencies = extract_dependencies_from_requirements(requirements_path)

    if final_dependencies:
        for i in final_dependencies:
            print(f'package: {i}')