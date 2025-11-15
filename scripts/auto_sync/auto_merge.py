import subprocess


if __name__ == "__main__":
    subprocess.run("git fetch origin", shell=True, check=False)
    subprocess.run("git merge origin/main --no-edit", shell=True, check=False)
