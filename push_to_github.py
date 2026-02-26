#!/usr/bin/env python3
"""
Quick GitHub Push Script
Pushes the repository to GitHub using a Personal Access Token
"""

import subprocess
import sys
import getpass

def run_cmd(cmd):
    """Run a command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    print("=" * 50)
    print("   GitHub Push Script")
    print("=" * 50)
    
    # Check if we need to push
    code, out, err = run_cmd("git status --porcelain")
    if out.strip():
        print("There are uncommitted changes. Committing first...")
        run_cmd('git add .')
        run_cmd('git commit -m "Update project files"')
    
    # Try push first
    print("\nTrying to push...")
    code, out, err = run_cmd("git push -u origin main")
    
    if code == 0:
        print("\n" + "=" * 50)
        print("   Project successfully uploaded to GitHub.")
        print("   https://github.com/tarekmhmd/first_version")
        print("=" * 50)
        return
    
    # If failed, ask for PAT
    if "403" in err or "Permission" in err or "Authentication" in err:
        print("\nPermission denied. Need Personal Access Token.")
        print("\nTo create a PAT:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select 'repo' scope and generate")
        
        pat = getpass.getpass("\nEnter your GitHub PAT: ").strip()
        
        if pat:
            # Set remote with PAT
            url = f"https://tarekmhmd:{pat}@github.com/tarekmhmd/first_version.git"
            run_cmd(f'git remote set-url origin "{url}"')
            
            print("\nPushing...")
            code, out, err = run_cmd("git push -u origin main")
            
            if code == 0:
                print("\n" + "=" * 50)
                print("   Project successfully uploaded to GitHub.")
                print("   https://github.com/tarekmhmd/first_version")
                print("=" * 50)
            else:
                print(f"\nPush failed: {err}")
        else:
            print("No PAT provided.")
    else:
        print(f"Push failed: {err}")

if __name__ == "__main__":
    main()