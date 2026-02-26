#!/usr/bin/env python3
"""
Automated GitHub Upload Script with Git LFS Support
Handles large files (>100MB) by tracking them with Git LFS
Supports Personal Access Token (PAT) authentication
"""

import os
import subprocess
import sys
import getpass
from pathlib import Path

# Configuration
PROJECT_DIR = Path(__file__).parent.absolute()
GITHUB_REPO = "https://github.com/tarekmhmd/first_version.git"
GITHUB_USER = "tarekmhmd"
COMMIT_MESSAGE = "Initial commit for first_version project"
GIT_USER_NAME = "tarekmhmd"
GIT_USER_EMAIL = "tarekmhmd456@gmail.com"
LARGE_FILE_THRESHOLD_MB = 100


def run_command(cmd, check=True, capture_output=False, input_text=None):
    """Execute a shell command and return the result."""
    print(f"  > {cmd}")
    result = subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        shell=True,
        capture_output=capture_output,
        text=True,
        input=input_text
    )
    if check and result.returncode != 0:
        if capture_output and result.stderr:
            print(f"    Error: {result.stderr.strip()}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def check_git_installed():
    """Check if Git is installed."""
    print("[1/10] Checking Git installation...")
    result = run_command("git --version", check=False, capture_output=True)
    if result.returncode != 0:
        print("    ERROR: Git is not installed. Please install Git first.")
        sys.exit(1)
    print("    ✓ Git is installed")


def check_git_lfs_installed():
    """Check if Git LFS is installed."""
    print("[2/10] Checking Git LFS installation...")
    result = run_command("git lfs version", check=False, capture_output=True)
    if result.returncode != 0:
        print("    Git LFS not found. Attempting to install...")
        # Try winget
        install_result = run_command("winget install GitHub.GitLFS --accept-source-agreements --accept-package-agreements", check=False, capture_output=True)
        if install_result.returncode != 0:
            # Try chocolatey
            install_result = run_command("choco install git-lfs -y", check=False, capture_output=True)
        if install_result.returncode != 0:
            print("    WARNING: Could not auto-install Git LFS.")
            print("    Please install manually from: https://git-lfs.github.com/")
            print("    Continuing without LFS - large files may fail to upload...")
            return False
        # Initialize Git LFS
        run_command("git lfs install", check=False)
        print("    ✓ Git LFS installed and initialized")
        return True
    print("    ✓ Git LFS is installed")
    
    # Ensure LFS is initialized
    run_command("git lfs install", check=False)
    return True


def configure_git_identity():
    """Configure Git user identity with specified credentials."""
    print("[3/10] Configuring Git identity...")
    
    # Always set the specified credentials
    run_command(f'git config user.name "{GIT_USER_NAME}"')
    print(f"    ✓ Set user.name: {GIT_USER_NAME}")
    
    run_command(f'git config user.email "{GIT_USER_EMAIL}"')
    print(f"    ✓ Set user.email: {GIT_USER_EMAIL}")


def initialize_git_repo():
    """Initialize Git repository if not already initialized."""
    print("[4/10] Initializing Git repository...")
    git_dir = PROJECT_DIR / ".git"
    if git_dir.exists():
        print("    ✓ Git repository already initialized")
    else:
        run_command("git init")
        print("    ✓ Git repository initialized")


def find_large_files():
    """Find all files larger than the threshold."""
    print(f"[5/10] Scanning for large files (>{LARGE_FILE_THRESHOLD_MB}MB)...")
    large_files = []
    threshold_bytes = LARGE_FILE_THRESHOLD_MB * 1024 * 1024
    
    # Patterns to skip
    skip_dirs = {'.git', 'venv', 'node_modules', '__pycache__', 'uploads', '.idea', '.vscode'}
    
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip hidden and unwanted directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in skip_dirs]
        
        for file in files:
            file_path = Path(root) / file
            try:
                file_size = file_path.stat().st_size
                if file_size > threshold_bytes:
                    size_mb = file_size / (1024 * 1024)
                    relative_path = file_path.relative_to(PROJECT_DIR)
                    large_files.append((str(relative_path), size_mb))
                    print(f"    ! Large file: {relative_path} ({size_mb:.2f}MB)")
            except (OSError, PermissionError):
                continue
    
    if not large_files:
        print("    ✓ No large files found")
    else:
        print(f"    ! Found {len(large_files)} large file(s)")
    
    return large_files


def setup_git_lfs(large_files, lfs_available):
    """Configure Git LFS for large files."""
    print("[6/10] Setting up Git LFS tracking...")
    
    if not large_files:
        print("    ✓ No large files to track with LFS")
        return True
    
    if not lfs_available:
        print("    ! WARNING: Git LFS not available. Large files may fail to upload.")
        print("    ! Consider installing Git LFS and running this script again.")
        return False
    
    # Get unique file extensions from large files
    extensions = set()
    for file_path, _ in large_files:
        ext = Path(file_path).suffix.lower()
        if ext:
            extensions.add(ext)
        else:
            # For files without extension, track by name pattern
            extensions.add(Path(file_path).name)
    
    # Track each extension/pattern with Git LFS
    for pattern in extensions:
        if pattern.startswith('.'):
            run_command(f'git lfs track "*{pattern}"')
            print(f"    ✓ Tracking *{pattern} with Git LFS")
        else:
            run_command(f'git lfs track "{pattern}"')
            print(f"    ✓ Tracking {pattern} with Git LFS")
    
    print("    ✓ Git LFS tracking configured")
    return True


def add_files_to_staging():
    """Add all files to Git staging."""
    print("[7/10] Adding files to staging...")
    
    # First add .gitattributes if it exists (LFS config)
    gitattributes = PROJECT_DIR / ".gitattributes"
    if gitattributes.exists():
        run_command("git add .gitattributes")
        print("    ✓ Added .gitattributes")
    
    # Add all files
    run_command("git add .")
    print("    ✓ All files added to staging")


def create_commit():
    """Create the initial commit."""
    print("[8/10] Creating commit...")
    
    # Check if there are changes to commit
    result = run_command("git status --porcelain", check=False, capture_output=True)
    if not result.stdout.strip():
        print("    ! No changes to commit")
        return False
    
    run_command(f'git commit -m "{COMMIT_MESSAGE}"')
    print(f"    ✓ Commit created: {COMMIT_MESSAGE}")
    return True


def setup_main_branch():
    """Ensure we're on the main branch."""
    print("[9/10] Setting up main branch...")
    
    result = run_command("git branch --show-current", check=False, capture_output=True)
    current_branch = result.stdout.strip()
    
    if current_branch and current_branch != "main":
        run_command("git branch -M main")
        print("    ✓ Renamed branch to 'main'")
    elif not current_branch:
        run_command("git branch -M main")
        print("    ✓ Created 'main' branch")
    else:
        print("    ✓ Already on 'main' branch")


def prompt_for_pat():
    """Prompt user for Personal Access Token."""
    print("\n    " + "=" * 50)
    print("    GitHub Authentication Required")
    print("    " + "=" * 50)
    print("    The current credentials don't have permission to push.")
    print("    Please provide a Personal Access Token (PAT).")
    print()
    print("    To create a PAT:")
    print("    1. Go to: https://github.com/settings/tokens")
    print("    2. Click 'Generate new token (classic)'")
    print("    3. Select 'repo' scope")
    print("    4. Generate and copy the token")
    print("    " + "=" * 50)
    
    pat = getpass.getpass("    Enter your GitHub PAT (hidden): ").strip()
    return pat


def link_remote_and_push():
    """Link to remote repository and push with PAT support."""
    print("[10/10] Linking to remote and pushing...")
    
    # Check if remote exists
    result = run_command("git remote get-url origin", check=False, capture_output=True)
    
    if result.returncode == 0:
        print(f"    ✓ Remote already linked")
    else:
        run_command(f"git remote add origin {GITHUB_REPO}")
        print(f"    ✓ Remote added: {GITHUB_REPO}")
    
    # Try to push
    print("    Attempting to push to GitHub...")
    print("    (This may take a while for large repositories)")
    
    push_result = run_command("git push -u origin main", check=False, capture_output=True)
    
    if push_result.returncode == 0:
        print("    ✓ Successfully pushed to GitHub")
        return True
    
    # Check for permission error
    if "403" in push_result.stderr or "Permission denied" in push_result.stderr or "Authentication failed" in push_result.stderr:
        print(f"    ! Push failed: Permission denied")
        
        # Prompt for PAT
        pat = prompt_for_pat()
        
        if not pat:
            print("    ! No PAT provided. Cannot continue.")
            return False
        
        # Update remote URL with PAT
        pat_url = f"https://{GITHUB_USER}:{pat}@github.com/{GITHUB_USER}/first_version.git"
        run_command(f'git remote set-url origin "{pat_url}"')
        print("    ✓ Remote URL updated with PAT")
        
        # Try push again
        print("    Pushing with PAT authentication...")
        push_result = run_command("git push -u origin main", check=False, capture_output=True)
        
        if push_result.returncode == 0:
            print("    ✓ Successfully pushed to GitHub")
            return True
        else:
            print(f"    ! Push failed: {push_result.stderr.strip()}")
            return False
    
    else:
        print(f"    ! Push failed: {push_result.stderr.strip()}")
        print("    ! Possible solutions:")
        print("    ! 1. Check your internet connection")
        print("    ! 2. Verify the repository exists on GitHub")
        print("    ! 3. Ensure you have write access to the repository")
        return False


def main():
    """Main execution function."""
    print()
    print("=" * 60)
    print("   GitHub Upload Script with Git LFS Support")
    print("=" * 60)
    print(f"   Project Directory: {PROJECT_DIR}")
    print(f"   Target Repository: {GITHUB_REPO}")
    print(f"   Git User: {GIT_USER_NAME} <{GIT_USER_EMAIL}>")
    print("=" * 60)
    print()
    
    try:
        check_git_installed()
        lfs_available = check_git_lfs_installed()
        configure_git_identity()
        initialize_git_repo()
        large_files = find_large_files()
        setup_git_lfs(large_files, lfs_available)
        add_files_to_staging()
        
        if not create_commit():
            print("\n! No changes to commit. Exiting.")
            return
        
        setup_main_branch()
        success = link_remote_and_push()
        
        print()
        print("=" * 60)
        if success:
            print("   ✓ Project successfully uploaded to GitHub.")
            print(f"   Repository: https://github.com/{GITHUB_USER}/first_version")
        else:
            print("   ! Upload completed with issues. See messages above.")
        print("=" * 60)
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"\n! ERROR: Command failed with exit code {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n! Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n! ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()