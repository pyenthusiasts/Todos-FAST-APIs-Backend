#!/usr/bin/env python3
"""Database backup utility script."""
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings


def backup_database():
    """Create a backup of the database."""
    # Create backups directory if it doesn't exist
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Extract database file path from DATABASE_URL
    if settings.DATABASE_URL.startswith("sqlite"):
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        if db_path.startswith("./"):
            db_path = db_path[2:]

        db_file = Path(db_path)

        if not db_file.exists():
            print(f"Error: Database file {db_file} not found")
            sys.exit(1)

        backup_file = backup_dir / f"todos_backup_{timestamp}.db"

        # Copy database file
        shutil.copy2(db_file, backup_file)

        print(f"Database backed up successfully to: {backup_file}")
        print(f"Backup size: {backup_file.stat().st_size / 1024:.2f} KB")

        # Keep only last 10 backups
        cleanup_old_backups(backup_dir, keep=10)

    else:
        print("Error: Only SQLite databases are supported for this backup script")
        print("For PostgreSQL, use pg_dump or similar tools")
        sys.exit(1)


def cleanup_old_backups(backup_dir: Path, keep: int = 10):
    """
    Clean up old backup files, keeping only the most recent ones.

    Args:
        backup_dir: Directory containing backups
        keep: Number of backups to keep
    """
    backups = sorted(
        backup_dir.glob("todos_backup_*.db"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if len(backups) > keep:
        for old_backup in backups[keep:]:
            old_backup.unlink()
            print(f"Removed old backup: {old_backup.name}")


def restore_database(backup_file: str):
    """
    Restore database from a backup file.

    Args:
        backup_file: Path to the backup file
    """
    backup_path = Path(backup_file)

    if not backup_path.exists():
        print(f"Error: Backup file {backup_file} not found")
        sys.exit(1)

    # Extract database file path
    if settings.DATABASE_URL.startswith("sqlite"):
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        if db_path.startswith("./"):
            db_path = db_path[2:]

        db_file = Path(db_path)

        # Create backup of current database before restoring
        if db_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_backup = Path(f"{db_file}.before_restore_{timestamp}")
            shutil.copy2(db_file, current_backup)
            print(f"Current database backed up to: {current_backup}")

        # Restore from backup
        shutil.copy2(backup_path, db_file)

        print(f"Database restored successfully from: {backup_file}")

    else:
        print("Error: Only SQLite databases are supported for this restore script")
        sys.exit(1)


def list_backups():
    """List all available database backups."""
    backup_dir = Path("backups")

    if not backup_dir.exists():
        print("No backups directory found")
        return

    backups = sorted(
        backup_dir.glob("todos_backup_*.db"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not backups:
        print("No backups found")
        return

    print(f"\nAvailable backups ({len(backups)} total):\n")
    print(f"{'Filename':<40} {'Size (KB)':<12} {'Date'}")
    print("-" * 70)

    for backup in backups:
        size_kb = backup.stat().st_size / 1024
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{backup.name:<40} {size_kb:<12.2f} {date_str}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database backup utility")
    parser.add_argument(
        "action",
        choices=["backup", "restore", "list"],
        help="Action to perform"
    )
    parser.add_argument(
        "--file",
        help="Backup file path (for restore action)"
    )

    args = parser.parse_args()

    if args.action == "backup":
        backup_database()
    elif args.action == "restore":
        if not args.file:
            print("Error: --file argument required for restore action")
            sys.exit(1)
        restore_database(args.file)
    elif args.action == "list":
        list_backups()
