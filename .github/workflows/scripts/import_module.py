import os
import shutil
import subprocess
import tempfile
import requests
import sys
from pathlib import Path

# Only these files will be copied from the official module
ESSENTIAL_FILES = {"main.tf", "variables.tf", "outputs.tf", "versions.tf"}

# All modules will be organized under this directory
MODULES_BASE_DIR = Path("terraform")

def normalize_module_name(module_slug: str) -> str:
    """
    Converts a full Terraform Registry slug like 'terraform-aws-modules/ec2-instance/aws'
    into a simplified folder name like 'ec2-instance'
    """
    return module_slug.split("/")[1] if "/" in module_slug else module_slug

def get_latest_release(module_slug: str) -> str:
    """
    Fetches the latest version of a module from the Terraform Registry
    """
    url = f"https://registry.terraform.io/v1/modules/{module_slug}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["version"]

def clone_module(module_slug: str, version: str, temp_dir: str) -> Path:
    """
    Clones the specified version of the module from GitHub to a temporary directory
    """
    repo_url = f"https://github.com/{module_slug}.git"
    clone_path = Path(temp_dir) / normalize_module_name(module_slug)
    subprocess.run(["git", "clone", "--depth", "1", "--branch", version, repo_url, str(clone_path)], check=True)
    return clone_path

def copy_essential_files(source_dir: Path, target_dir: Path):
    """
    Copies only the essential Terraform files to the internal module directory
    """
    os.makedirs(target_dir, exist_ok=True)
    for file in ESSENTIAL_FILES:
        src = source_dir / file
        if src.exists():
            shutil.copy(src, target_dir / file)

def update_readme(module_dir: Path, version: str):
    """
    Appends version entry to README.md in the module directory
    """
    readme = module_dir / "README.md"
    line = f"- Version {version} imported automatically.\n"

    if not readme.exists():
        readme.write_text("# Version History\n" + line)
    else:
        content = readme.read_text()
        if line not in content:
            with readme.open("a") as f:
                f.write(line)

def update_changelog(module_dir: Path, version: str):
    """
    Adds a changelog entry for the imported version
    """
    changelog = module_dir / "CHANGELOG.md"
    entry = f"## [{version}]\n- Automated update to version {version}\n"

    if not changelog.exists():
        changelog.write_text(entry)
    else:
        content = changelog.read_text()
        if f"[{version}]" not in content:
            changelog.write_text(entry + "\n" + content)

def version_exists(module_name: str, version: str) -> bool:
    """
    Checks whether the module version is already imported locally
    """
    module_dir = MODULES_BASE_DIR / module_name
    changelog = module_dir / "CHANGELOG.md"
    if not changelog.exists():
        return False
    content = changelog.read_text()
    return f"[{version}]" in content

def main():
    if len(sys.argv) < 2:
        print("Usage: python import_module.py 'terraform-aws-modules/ec2-instance/aws,...'")
        sys.exit(1)

    modules = sys.argv[1].split(",")

    for module_slug in modules:
        module_slug = module_slug.strip()
        module_name = normalize_module_name(module_slug)

        print(f"\n🔍 Checking module: {module_slug}")
        version = get_latest_release(module_slug)
        print(f"📦 Latest version available: {version}")

        if version_exists(module_name, version):
            print(f"✅ Module {module_name} is already at version {version}. Skipping.")
            continue

        with tempfile.TemporaryDirectory() as tmp:
            print(f"📥 Cloning module {module_slug} at version {version}")
            repo_path = clone_module(module_slug, version, tmp)

            dest_path = MODULES_BASE_DIR / module_name
            print(f"📂 Copying essential files to {dest_path}")
            copy_essential_files(repo_path, dest_path)

            print(f"📝 Updating changelog and README")
            update_changelog(dest_path, version)
            update_readme(dest_path, version)

    print("\n✅ All modules processed. Ready for commit and PR!")

if __name__ == "__main__":
    main()