import subprocess
import sys
import re
from pathlib import Path

REQ_FILE = Path("requirements.txt")

def normalize_name(req_line: str) -> str:
    m = re.match(r"^\s*([A-Za-z0-9_.-]+)", req_line)
    return m.group(1).lower() if m else req_line.lower()

def has_version_specifier(s: str) -> bool:
    return any(op in s for op in ("==", ">=", "<=", "~=", ">", "<", "!="))

def parse_requirements(path: Path):
    if not path.exists():
        print(f"Error: {path} not found.", file=sys.stderr)
        sys.exit(2)

    lines = path.read_text(encoding="utf-8").splitlines()
    cleaned = []
    for ln in lines:
        ln2 = ln.split("#", 1)[0].strip() 
        if ln2:
            cleaned.append(ln2)

    chosen = {}
    for entry in cleaned:
        key = normalize_name(entry)
        prev = chosen.get(key)
        if prev is None:
            chosen[key] = entry
        else:
            if has_version_specifier(entry) and not has_version_specifier(prev):
                chosen[key] = entry

    ordered = []
    for entry in cleaned:
        key = normalize_name(entry)
        if key in chosen:
            ordered.append(chosen.pop(key))
    ordered.extend(chosen.values())
    return ordered

def install_package(pkg: str) -> int:
    cmd = [sys.executable, "-m", "pip", "install", pkg]
    print(f"\n>>> Installing: {pkg}")
    try:
        res = subprocess.run(cmd, check=False)
        return res.returncode
    except Exception as e:
        print(f"Error running pip for {pkg}: {e}", file=sys.stderr)
        return 1

def main():
    pkgs = parse_requirements(REQ_FILE)
    if not pkgs:
        print("No packages found in requirements.txt")
        return

    print("Packages to install (in order):")
    for p in pkgs:
        print("  -", p)

    failures = []
    for p in pkgs:
        rc = install_package(p)
        if rc != 0:
            failures.append((p, rc))

    if failures:
        print("\nSome installs failed:")
        for p, rc in failures:
            print(f"  {p} -> returncode {rc}")
        print("You can re-run the script or try installing the failed packages manually.")
        sys.exit(1)
    else:
        print("\nAll packages installed successfully.")

if __name__ == "__main__":
    main()
