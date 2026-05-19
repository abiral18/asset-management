# IT Asset Management System

A SQL-backed inventory tracker with a Python CLI for managing hardware and software assets across multiple lab environments.

## Features
- Track hardware assets (laptops, servers, monitors) across multiple labs
- Assign software and licenses to specific hardware
- Update asset status (active/inactive/maintenance/retired)
- Search assets by name or serial number
- Generate per-lab inventory reports
- Full CRUD operations backed by SQLite

## Tech Stack
- Python 3
- SQLite (via Python's built-in sqlite3 module)
- tabulate (for formatted CLI output)

## Setup
```bash
git clone https://github.com/abiral18/asset-management
cd asset-management
pip install tabulate
python app.py
```

## Menu Options
| Option | Description |
|--------|-------------|
| 1 | Add hardware asset to a lab |
| 2 | Assign software/license to hardware |
| 3 | View all assets across all labs |
| 4 | Search by name or serial number |
| 5 | Update asset status |
| 6 | Delete an asset |
| 7 | Generate lab summary report |

## Database Schema
- `labs` — lab environments with name and location
- `hardware` — devices assigned to labs with status tracking
- `software` — software licenses linked to specific hardware