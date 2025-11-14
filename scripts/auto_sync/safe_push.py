import subprocess, pathlib, time, datetime, os, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SAFE_DIRS = {"ai", "business", "config", "workflows", "scripts"}
MAX_FILE_SIZE_MB = 10
BRANCH = os.environ.get("AUTO_SYNC_BRANCH", "").strip()  # optional

def sh(cmd):
    return subprocess.run(cmd, cwd=ROOT, shell=True, capture_output=True, text=True)

def changed_files():
    r = sh("git status --porcelain")
    files = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        p = pathlib.Path(path)
        parts = p.parts
        if not parts:
            continue
        # only safe roots
        if parts[0] not in SAFE_DIRS:
            continue
        # skip big files
        fp = ROOT / p
        if fp.exists() and fp.is_file():
            try:
                if fp.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                    continue
            except Exception:
                pass
        files.append(p)
    return files

def ensure_branch():
    if not BRANCH:
        return True
    # create or switch to branch if needed
    sh(f"git fetch --all --quiet")
    sh(f"git checkout -B {BRANCH} || true")
    return True

def main():
    print(f"[auto-sync] root={ROOT}")
    ensure_branch()
    while True:
        files = changed_files()
        if files:
            print(f"[auto-sync] {len(files)} safe file(s) changed → commit & push")
            sh("git add -A")
            msg = f'auto-sync: {datetime.datetime.now().isoformat()}'
            # prevent failing when nothing to commit
            sh(f"git commit -m '{msg}' || true")
            # rebase to avoid diverging history
            sh("git pull --rebase --autostash --quiet || true")
            res = sh("git push --quiet || true")
            if res.returncode == 0:
                print("[auto-sync] pushed.")
            else:
                sys.stderr.write(res.stderr or "[auto-sync] push failed
")
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("
[auto-sync] stopped")
