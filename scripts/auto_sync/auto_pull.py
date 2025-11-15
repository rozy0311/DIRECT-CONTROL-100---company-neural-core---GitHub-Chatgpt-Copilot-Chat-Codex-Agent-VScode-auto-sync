import subprocess


if __name__ == "__main__":
    subprocess.run("git pull --rebase", shell=True, check=False)
