#!/usr/bin/env python3
"""
FRACTAL-PROMPT CLI Installation Script
Sets up the FRACTAL-PROMPT CLI tool for easy project management.

Author: FRACTAL-PROMPT Team
License: MIT
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(command, shell=True):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def make_executable(file_path):
    """Make a file executable on Unix-like systems."""
    if os.name != 'nt':  # Not Windows
        try:
            os.chmod(file_path, 0o755)
            return True
        except Exception:
            pass
    return False

def install_cli():
    """Install FRACTAL-PROMPT CLI tool."""

    print("🚀 FRACTAL-PROMPT CLI Installation")
    print("=" * 40)

    # Get current directory
    current_dir = Path(__file__).parent.absolute()
    cli_path = current_dir / "fractal-cli.py"

    if not cli_path.exists():
        print("❌ Error: fractal-cli.py not found!")
        return False

    # Create bin directory if it doesn't exist
    home_dir = Path.home()
    bin_dir = home_dir / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    # Copy CLI script
    dest_path = bin_dir / "fractal-cli"

    try:
        shutil.copy2(cli_path, dest_path)
        print(f"✅ Copied CLI to: {dest_path}")

        # Make executable
        if make_executable(dest_path):
            print("✅ Made CLI executable")

        # Check if bin directory is in PATH
        path_str = os.environ.get('PATH', '')
        if str(bin_dir) not in path_str:
            print("⚠️  Warning: ~/.local/bin is not in your PATH")
            print("💡 Add this line to your ~/.bashrc or ~/.profile:")
            print(f"   export PATH=\"$HOME/.local/bin:$PATH\"")
            print("   Then run: source ~/.bashrc")

        print("\n🎉 Installation completed successfully!")
        print("\n📋 Usage:")
        print("   fractal-cli init my-project          # Initialize new project")
        print("   fractal-cli backup ./src/            # Create backup")
        print("   fractal-cli status                   # Show system status")
        print("   fractal-cli validate ./my-project/   # Validate project")

        return True

    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False

def test_installation():
    """Test that the CLI was installed correctly."""

    print("\n🧪 Testing installation...")

    success, stdout, stderr = run_command("fractal-cli --help")

    if success:
        print("✅ CLI is working correctly!")
        print("📖 Help output:")
        print(stdout)
        return True
    else:
        print("❌ CLI test failed!")
        print(f"Error: {stderr}")
        return False

def main():
    """Main installation function."""

    print("Welcome to FRACTAL-PROMPT CLI Installation!")
    print("This will install the FRACTAL-PROMPT command-line tool.\n")

    # Check if CLI file exists
    cli_file = Path(__file__).parent / "fractal-cli.py"
    if not cli_file.exists():
        print("❌ Error: fractal-cli.py not found in the same directory as install.py")
        print("Make sure you're running this script from the TOOLS directory.")
        sys.exit(1)

    # Confirm installation
    print("This will install FRACTAL-PROMPT CLI to ~/.local/bin/")
    response = input("Continue? (y/N): ").lower().strip()

    if response not in ['y', 'yes']:
        print("Installation cancelled.")
        sys.exit(0)

    # Install CLI
    if install_cli():
        # Test installation
        test_installation()

        print("\n🎯 Next steps:")
        print("1. Make sure ~/.local/bin is in your PATH")
        print("2. Try: fractal-cli init test-project")
        print("3. Read the documentation in CORE/ and TECHNICAL/")

    else:
        print("\n❌ Installation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()