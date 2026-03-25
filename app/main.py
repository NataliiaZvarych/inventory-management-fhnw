"""Main currently runs only database setup tasks.

At this stage, this file is used only to:
- create database tables
- insert seed data

It does not run the full application yet.

Run examples:
- python -m app.main --init-db
- python -m app.main --seed
- python -m app.main --init-db --seed
"""

import argparse

from app.db import create_db_and_tables
from app.seed import seed_database


def run(init_db: bool, seed: bool) -> None:
	"""Run actions selected by command-line flags."""

	# Step 1: If user did not select any action, show help message and stop.
	if not init_db and not seed:
		print("No action selected. Use --init-db and/or --seed.")
		return

	# Step 2: Create database tables when --init-db is provided.
	if init_db:
		print("[1/2] Creating database tables...")
		create_db_and_tables()
		print("Database tables created.")

	# Step 3: Insert demo/seed data when --seed is provided.
	if seed:
		print("[2/2] Inserting seed data...")
		seed_database()
		print("Seed process finished.")


def build_parser() -> argparse.ArgumentParser:
	"""Create parser for command-line options."""
	parser = argparse.ArgumentParser(description="Inventory backend setup")

	# --init-db means: create all tables from SQLModel classes.
	parser.add_argument(
		"--init-db",
		action="store_true",
		help="Create database tables",
	)

	# --seed means: insert initial records (categories, users, products, etc.).
	parser.add_argument(
		"--seed",
		action="store_true",
		help="Insert seed data (if not already present)",
	)
	return parser


if __name__ == "__main__":
	# This block runs only when you execute: python -m app.main
	# It will NOT run when this file is imported from another file.
	args = build_parser().parse_args()
	run(init_db=args.init_db, seed=args.seed)
