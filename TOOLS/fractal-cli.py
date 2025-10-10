#!/usr/bin/env python3
"""
FRACTAL-PROMPT CLI Tool
Automates project initialization and template management for FRACTAL-PROMPT methodology.

Author: FRACTAL-PROMPT Team
License: MIT
"""

import argparse
import os
import shutil
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

class FractalCLI:
    """CLI tool for FRACTAL-PROMPT project management."""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.templates_path = self.base_path / "TEMPLATES"
        self.core_path = self.base_path / "CORE"
        self.technical_path = self.base_path / "TECHNICAL"

    def init_project(self, project_name: str, project_type: str = "general") -> None:
        """Initialize a new project with FRACTAL-PROMPT templates."""

        print(f"🚀 Initializing FRACTAL-PROMPT project: {project_name}")

        # Create project directory
        project_dir = Path(project_name)
        project_dir.mkdir(exist_ok=True)

        # Copy core templates
        templates_to_copy = [
            "TEMPLATES/PROJECT_INITIATION.md",
            "TEMPLATES/COLLABORATION_CHECKPOINT.md",
            "TEMPLATES/ERROR_RECOVERY.md",
            "CORE/ESENCIA_COLABORATIVA.md",
            "TECHNICAL/IMPLEMENTATION_GUIDELINES.md"
        ]

        for template in templates_to_copy:
            src = self.base_path / template
            if src.exists():
                dst = project_dir / src.name
                shutil.copy2(src, dst)
                print(f"✅ Copied: {src.name}")

        # Create project configuration
        config = {
            "project_name": project_name,
            "created_date": str(datetime.datetime.now()),
            "fractal_version": "1.0",
            "project_type": project_type,
            "templates_used": [t.split('/')[-1] for t in templates_to_copy]
        }

        with open(project_dir / "fractal-config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ Created project configuration: fractal-config.json")
        print(f"\n🎯 Project '{project_name}' initialized successfully!")
        print(f"📁 Location: {project_dir.absolute()}")
        print("\n📋 Next steps:")
        print("1. Edit PROJECT_INITIATION.md with your project details")
        print("2. Read ESENCIA_COLABORATIVA.md to understand the collaborative spirit")
        print("3. Set up backup protocols using IMPLEMENTATION_GUIDELINES.md")

    def create_backup(self, target_path: str, backup_name: Optional[str] = None) -> None:
        """Create a backup following FRACTAL-PROMPT protocols."""

        target = Path(target_path)
        if not target.exists():
            print(f"❌ Error: {target_path} does not exist")
            return

        # Generate backup name with timestamp
        if backup_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{target.name}_backup_{timestamp}"

        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)

        backup_path = backup_dir / backup_name

        if target.is_file():
            shutil.copy2(target, backup_path)
        else:
            shutil.copytree(target, backup_path)

        print(f"✅ Backup created: {backup_path}")

        # Log backup
        log_entry = {
            "timestamp": str(datetime.datetime.now()),
            "original_path": str(target),
            "backup_path": str(backup_path),
            "backup_type": "file" if target.is_file() else "directory"
        }

        log_file = backup_dir / "backup_log.json"
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

        print(f"📝 Backup logged in: {log_file}")

    def show_status(self) -> None:
        """Show FRACTAL-PROMPT system status."""

        print("🌟 FRACTAL-PROMPT System Status")
        print("=" * 40)

        # Check core files
        core_files = [
            "README.md",
            "CORE/ESENCIA_COLABORATIVA.md",
            "TECHNICAL/IMPLEMENTATION_GUIDELINES.md"
        ]

        print("\n📋 Core Files:")
        for file in core_files:
            path = self.base_path / file
            status = "✅" if path.exists() else "❌"
            print(f"  {status} {file}")

        # Check templates
        print("\n📋 Templates:")
        if self.templates_path.exists():
            for template in self.templates_path.iterdir():
                if template.is_file() and template.suffix == ".md":
                    print(f"  ✅ {template.name}")

        # Show recent backups
        backup_dir = Path("backups")
        if backup_dir.exists():
            print("\n📋 Recent Backups:")
            try:
                with open(backup_dir / "backup_log.json", 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    recent_backups = logs[-5:] if len(logs) > 5 else logs
                    for log in reversed(recent_backups):
                        print(f"  📅 {log['timestamp']}: {Path(log['original_path']).name}")
            except (FileNotFoundError, json.JSONDecodeError):
                print("  No backup logs found")

        print(f"\n🏗️  FRACTAL-PROMPT v1.0 - Ready for collaboration! 🤝")

    def validate_collaboration(self, project_path: str) -> None:
        """Validate that a project follows FRACTAL-PROMPT protocols."""

        project_dir = Path(project_path)
        if not project_dir.exists():
            print(f"❌ Error: {project_path} does not exist")
            return

        print(f"🔍 Validating FRACTAL-PROMPT compliance for: {project_name}")

        # Check required files
        required_files = [
            "PROJECT_INITIATION.md",
            "fractal-config.json"
        ]

        print("\n📋 Required Files:")
        all_present = True
        for file in required_files:
            path = project_dir / file
            status = "✅" if path.exists() else "❌"
            print(f"  {status} {file}")
            if not path.exists():
                all_present = False

        # Check core templates
        core_templates = [
            "ESENCIA_COLABORATIVA.md",
            "IMPLEMENTATION_GUIDELINES.md"
        ]

        print("\n📋 Core Templates:")
        for template in core_templates:
            path = project_dir / template
            status = "✅" if path.exists() else "⚠️ "
            print(f"  {status} {template}")

        if all_present:
            print("\n🎉 Project is FRACTAL-PROMPT compliant!")
        else:
            print("\n⚠️  Project is missing required FRACTAL-PROMPT files")
            print("💡 Run 'fractal-cli init <project>' to set up properly")

def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description="FRACTAL-PROMPT CLI Tool for collaborative project management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fractal-cli init my-project                    # Initialize new project
  fractal-cli init my-project --type web        # Initialize web project
  fractal-cli backup ./src/                     # Create backup
  fractal-cli status                            # Show system status
  fractal-cli validate ./my-project/            # Validate project compliance
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new FRACTAL-PROMPT project")
    init_parser.add_argument("project_name", help="Name of the project to create")
    init_parser.add_argument("--type", default="general",
                           choices=["general", "web", "mobile", "data", "ai"],
                           help="Type of project (default: general)")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create backup following FRACTAL-PROMPT protocols")
    backup_parser.add_argument("target", help="File or directory to backup")
    backup_parser.add_argument("--name", help="Custom name for backup")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show FRACTAL-PROMPT system status")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate FRACTAL-PROMPT compliance")
    validate_parser.add_argument("project_path", help="Path to project to validate")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = FractalCLI()

    if args.command == "init":
        cli.init_project(args.project_name, args.type)
    elif args.command == "backup":
        cli.create_backup(args.target, args.name)
    elif args.command == "status":
        cli.show_status()
    elif args.command == "validate":
        cli.validate_collaboration(args.project_path)


if __name__ == "__main__":
    main()