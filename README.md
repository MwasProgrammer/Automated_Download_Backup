# Automated Download Backup (v1.0.0)

A robust, Python-based utility designed to automate the backup of files from your Downloads folder to external storage with integrity verification and disk space management.

## Key Features
* **Interactive Drive Discovery:** Uses Windows API calls to detect physical drives and allows for manual selection via a CLI menu.
* **Integrity Verification:** Uses SHA-256 hashing to ensure files are moved correctly without corruption.
* **Database Tracking:** SQLite-backed history prevents duplicate backups, saving time and storage.
* **Safety First:** Includes disk space pre-checks and "Verify-Before-Delete" logic to protect your data.

### Prerequisites
* **Python 3.10 or higher**
* **Windows OS** (Required for `ctypes` hardware discovery)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/MwasProgrammer/Automated_Download_Backup.git
    cd AutomatedDownloadBackup

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

 ## Configuration
3. **Copy the example configuration file:**
    ```bash
    cp config.json.example config.json

4. **Open config.json and adjust the settings:**
    volume_label: Set to "SELECT" for interactive mode, 
    "AUTO" for the first available drive, or 
    a specific label like "BACKUP_USB".

    BACKUP_BATCH: Number of files to process per run. (No. of files to be backed up)

## Usage
5. **Run the main script to start the backup process:**
    ```bash
    python main.py

## Licence
Automated Download Backup is an open-source project. Feel free to log issues or submit pull requests to improve the discovery logic or add support for additional OS platforms. See the licence details [here🔽](LICENCE).
