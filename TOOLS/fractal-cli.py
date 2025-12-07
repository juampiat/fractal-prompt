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
import sys
import io
from pathlib import Path
from typing import Dict, List, Optional

# Force UTF-8 output for emojis on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class FractalCLI:
    """CLI tool for FRACTAL-PROMPT project management."""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.templates_path = self.base_path / "TEMPLATES"
        self.core_path = self.base_path / "CORE"
        self.technical_path = self.base_path / "TECHNICAL"

    def _get_files_to_copy(self, lang: str) -> List[Dict[str, Path]]:
        """Get list of files to copy based on language."""
        
        # Check if language directory exists for each section
        sections = {
            "CORE": self.core_path,
            "TECHNICAL": self.technical_path,
            "TEMPLATES": self.templates_path
        }
        
        files_to_copy = []
        
        for section_name, section_path in sections.items():
            lang_path = section_path / lang
            if not lang_path.exists():
                print(f"⚠️  Warning: No content found for language '{lang}' in {section_name}")
                continue
                
            # Iterate through files in the language directory
            for item in lang_path.iterdir():
                if item.is_file() and item.suffix == '.md':
                    # We will copy it to the project root or similar structure
                    # Strategy: Preserve original category? Or flat? 
                    # Original script copied distinct paths to distinct inputs.
                    # Let's keep the structure: Project/Category/File
                    files_to_copy.append({
                        "src": item,
                        "rel_path": f"{section_name}/{item.name}"
                    })
                    
        return files_to_copy

    def init_project(self, project_name: str, project_type: str = "general", lang: str = "es") -> None:
        """Initialize a new project with FRACTAL-PROMPT templates."""

        print(f"🚀 Initializing FRACTAL-PROMPT project: {project_name}")
        print(f"🌍 Language: {lang}")

        # Create project directory
        project_dir = Path(project_name)
        project_dir.mkdir(exist_ok=True)
        
        # Create subdirectories in project
        for subdir in ["CORE", "TECHNICAL", "TEMPLATES"]:
            (project_dir / subdir).mkdir(exist_ok=True)

        # Get files to copy
        files = self._get_files_to_copy(lang)
        
        if not files:
            print(f"❌ Error: No templates found for language '{lang}'")
            return

        copied_count = 0
        for file_info in files:
            src = file_info["src"]
            rel_path = file_info["rel_path"] # e.g. CORE/ESENCIA_COLABORATIVA.md
            dst = project_dir / rel_path
            
            shutil.copy2(src, dst)
            print(f"✅ Copied: {rel_path}")
            copied_count += 1

        # Create project configuration
        config = {
            "project_name": project_name,
            "created_date": str(datetime.datetime.now()),
            "fractal_version": "1.1",
            "project_type": project_type,
            "language": lang,
            "templates_count": copied_count
        }

        with open(project_dir / "fractal-config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ Created project configuration: fractal-config.json")
        print(f"\n🎯 Project '{project_name}' initialized successfully!")
        print(f"📁 Location: {project_dir.absolute()}")
        print("\n📋 Next steps:")
        
        if lang == "es":
            print("1. Edita TEMPLATES/PROJECT_INITIATION.md con los detalles de tu proyecto")
            print("2. Lee CORE/ESENCIA_COLABORATIVA.md para entender el espíritu colaborativo")
            print("3. Configura protocolos de backup usando TECHNICAL/BACKUP_PROTOCOLS.md")
        else:
            print("1. Edit TEMPLATES/PROJECT_INITIATION.md with your project details")
            print("2. Read CORE/COLLABORATIVE_ESSENCE.md to understand the collaborative spirit")
            print("3. Set up backup protocols using TECHNICAL/BACKUP_PROTOCOLS.md")

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
        
        # Determine available languages
        available_langs = []
        for lang_dir in self.core_path.iterdir():
            if lang_dir.is_dir():
                available_langs.append(lang_dir.name)

        print(f"\n🌍 Available Languages: {', '.join(available_langs)}")

        # Check templates for each language
        for lang in available_langs:
            print(f"\n📋 Templates ({lang}):")
            files = self._get_files_to_copy(lang)
            for f in files:
                print(f"  ✅ {f['rel_path']}")

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

        print(f"\n🏗️  FRACTAL-PROMPT v1.1 - Ready for collaboration! 🤝")

    def validate_collaboration(self, project_path: str) -> None:
        """Validate that a project follows FRACTAL-PROMPT protocols."""

        project_dir = Path(project_path)
        if not project_dir.exists():
            print(f"❌ Error: {project_path} does not exist")
            return

        print(f"🔍 Validating FRACTAL-PROMPT compliance for: {project_dir.name}")

        # Check required files
        required_files = [
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
                
        # Try to detect language from config
        lang = "es" # default
        config_path = project_dir / "fractal-config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    lang = config.get("language", "es")
            except:
                pass
        
        # Check core templates based on language (heuristic)
        # We check if at least ONE file from each category exists
        categories = ["CORE", "TECHNICAL"]
        
        print(f"\n📋 Content Structure ({lang}):")
        for cat in categories:
            cat_dir = project_dir / cat
            if cat_dir.exists() and any(cat_dir.iterdir()):
                print(f"  ✅ {cat}/ (contains files)")
            else:
                print(f"  ⚠️ {cat}/ (empty or missing)")
                # Not strictly failing if partial, but warning

        if all_present:
            print("\n🎉 Project is FRACTAL-PROMPT compliant!")
        else:
            print("\n⚠️  Project is missing required FRACTAL-PROMPT files")
            print("💡 Run 'fractal-cli init <project>' to set up properly")

    def tune_project(self, project_path: str, editor: str = "cursor") -> None:
        """
        Tune the project for AI editors by injecting FRACTAL-PROMPT essence.
        Currently supports: Cursor (.cursorrules), Github Copilot (copilot-instructions.md)
        """
        project_dir = Path(project_path)
        if not project_dir.exists():
            print(f"❌ Error: {project_path} does not exist")
            return

        print(f"🎵 Tuning project '{project_dir.name}' for {editor}...")

        # 1. Detect language from config or default to es
        lang = "es"
        config_path = project_dir / "fractal-config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    lang = config.get("language", "es")
            except:
                pass
        
        print(f"🌍 Detected language: {lang}")

        # 2. Locate Essence file
        # es: CORE/es/ESENCIA_COLABORATIVA.md
        # en: CORE/en/COLLABORATIVE_ESSENCE.md
        
        essence_file = None
        if lang == "es":
            essence_file = self.core_path / "es" / "ESENCIA_COLABORATIVA.md"
        else:
            essence_file = self.core_path / "en" / "COLLABORATIVE_ESSENCE.md"
            
        if not essence_file.exists():
             # Fallback logic if structure is different
            print(f"❌ Error: Could not find essence file at {essence_file}")
            return

        # 3. Read content
        try:
            with open(essence_file, 'r', encoding='utf-8') as f:
                essence_content = f.read()
        except Exception as e:
            print(f"❌ Error reading essence file: {e}")
            return

        # 4. Generate Target File
        target_file = None
        
        if editor.lower() == "cursor":
            target_file = project_dir / ".cursorrules"
            header = "# FRACTAL-PROMPT SYSTEM INSTRUCTIONS\n# This file allows Cursor to understand the project's collaborative philosophy.\n\n"
        
        elif editor.lower() == "copilot":
            github_dir = project_dir / ".github"
            github_dir.mkdir(exist_ok=True)
            target_file = github_dir / "copilot-instructions.md"
            header = "# FRACTAL-PROMPT INSTRUCTIONS for Github Copilot\n\n"
            
        else:
            print(f"❌ Error: Unsupported editor '{editor}'. Use 'cursor' or 'copilot'.")
            return

        # Write file
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(header + essence_content)
            print(f"✅ Created: {target_file.name}")
            print("✨ The AI editor is now tuned with FRACTAL-PROMPT essence! 🧠")
        except Exception as e:
            print(f"❌ Error writing target file: {e}")


def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description="FRACTAL-PROMPT CLI Tool for collaborative project management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fractal-cli init my-project --lang es          # Initialize Spanish project
  fractal-cli init my-project --lang en          # Initialize English project
  fractal-cli tune my-project --editor cursor    # Generate .cursorrules
  fractal-cli tune my-project --editor copilot   # Generate copilot instructions
  fractal-cli backup ./src/                      # Create backup
  fractal-cli status                             # Show system status
  fractal-cli validate ./my-project/             # Validate project compliance
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new FRACTAL-PROMPT project")
    init_parser.add_argument("project_name", help="Name of the project to create")
    init_parser.add_argument("--type", default="general",
                           choices=["general", "web", "mobile", "data", "ai"],
                           help="Type of project (default: general)")
    init_parser.add_argument("--lang", default="es",
                           choices=["es", "en"],
                           help="Language for templates (default: es)")

    # Tune command
    tune_parser = subparsers.add_parser("tune", help="Tune project for AI editors (Context Injection)")
    tune_parser.add_argument("project_path", help="Path to the project to tune")
    tune_parser.add_argument("--editor", default="cursor",
                           choices=["cursor", "copilot"],
                           help="Target AI editor (default: cursor)")

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
        cli.init_project(args.project_name, args.type, args.lang)
    elif args.command == "tune":
        cli.tune_project(args.project_path, args.editor)
    elif args.command == "backup":
        cli.create_backup(args.target, args.name)
    elif args.command == "status":
        cli.show_status()
    elif args.command == "validate":
        cli.validate_collaboration(args.project_path)


if __name__ == "__main__":
    main()