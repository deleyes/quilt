import os
import subprocess
import sys
import shutil

def create_quiltignore():
    """Create a .quiltignore file to exclude unwanted files and directories.
    See https://docs.quiltdata.com/quilt-python-sdk/advanced/.quiltignore
    """
    quiltignore_content = """
    venv/
    .DS_Store
    *.pyc
    __pycache__/
    """
    with open('.quiltignore', 'w') as f:
        f.write(quiltignore_content)
    print(".quiltignore file created")

def create_venv(venv_path):
    """Create a virtual environment."""
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print(f"Virtual environment created at {venv_path}")
    else:
        print(f"Virtual environment already exists at {venv_path}")

def activate_venv(venv_path):
    """Activate the virtual environment."""
    if os.name == 'nt':
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        subprocess.call(activate_script, shell=True)
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        subprocess.call(f'source {activate_script}', shell=True)

def install_packages(venv_path, packages):
    """Install packages in the virtual environment."""
    if os.name == 'nt':
        python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        python_executable = os.path.join(venv_path, 'bin', 'python')
    
    try:
        subprocess.check_call([python_executable, "-m", "pip", "install"] + packages)
    except Exception as e:
        print(f"Error installing packages: {e}")
        raise


import pandas as pd
import quilt3
import click

@click.command()
@click.option("--package-name", required=True, help="Name of the Quilt package (e.g., 'MGx/2025-02-07-MGx-test1').")
@click.option("--registry", required=True, help="Quilt registry (e.g., 's3://epa-dev-quilt-poc').")
def publish_to_quilt(package_name, registry):
    """
    Publish raw data from the current directory to a Quilt package using metadata from Excel file with name "quilt_metadata".
    Pre-requisites:
    Python needs to be installed on the system to run this script & AWS credentials need to be on the system as well.
    This script needs to be run in the same directory as the raw data files.
    Path to CA certificate needs to be set in the environment variable REQUESTS_CA_BUNDLE.
    """
    # # Create the virtual environment
    # env_name = "venv"
    # create_venv(env_name)
    # activate_venv(env_name)

    # # Install necessary packages in the virtual environment
    # install_packages(env_name, ["pandas", "quilt3", "click", "openpyxl"])
    
    # Automatically determine the data folder and find the metadata file
    data_folder = os.getcwd()
    metadata_file = None

    # Look for the first Excel file in the current directory
    for file in os.listdir(data_folder):
        if file.startswith("quilt_metadata") and (file.endswith('.xlsx') or file.endswith('.xls')):
            metadata_file = os.path.join(data_folder, file)
            break

    if not metadata_file:
        click.echo("No Excel metadata file found in the current directory.", err=True)
        return
    
    print(f"Data folder: {data_folder}")
    print(f"Metadata file: {metadata_file}")


    # Load metadata from the Excel file
    try:
        metadata_df = pd.read_excel(metadata_file)
        click.echo(f"Metadata loaded from {metadata_file}")
    except Exception as e:
        click.echo(f"Error loading metadata: {e}", err=True)
        return

    print(f"Metadata:\n{metadata_df}")

    # Convert the first row of metadata to a dictionary
    metadata_dict = metadata_df.iloc[0].to_dict()

    # Convert Timestamp to string to make it JSON serializable
    for key, value in metadata_dict.items():
        if isinstance(value, pd.Timestamp):
            metadata_dict[key] = value.isoformat()

    print(f"Metadata dictionary:\n{metadata_dict}")

    # Initialize a Quilt package
    pkg = quilt3.Package()

    # Add all files to the package
    
    pkg.set_dir(".", ".", meta=metadata_dict)
    create_quiltignore()
    pkg.set_dir(".", ".", meta=metadata_dict)
    click.echo("Added all files to package")

    # Set the custom CA bundle and push the package to Quilt
    os.environ['REQUESTS_CA_BUNDLE'] = "/Users/sdeleye/Library/CloudStorage/GoogleDrive-steven.deleye@lizard.bio/My Drive/Syngenta/cacert.pem"
    try:
        pkg.push(package_name, registry=registry, force=True)
        click.echo("Upload complete. Verifying integrity...")
        pkg.verify(".", extra_files_ok=True)
        click.echo("Integrity verified.")
    except Exception as e:
        click.echo(f"Error publishing package: {e}", err=True)


    """
    TODO 
    when large files taking long time run in background
    """
    

if __name__ == "__main__":
    publish_to_quilt()