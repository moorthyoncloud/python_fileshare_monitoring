# EFS Health Check Monitoring using Python

This Python script monitors the health of an Amazon Elastic File System (EFS) by verifying the accessibility of a specific health check file on the EFS mount. If the file becomes inaccessible or recovers, the script sends email alerts using a configured SMTP server.

## Features

- Monitor EFS Health: Periodically checks the presence and readability of a designated health check file on the EFS mount.
- State Change Alerts: Sends email alerts when the EFS health state changes (reachable to unreachable or vice versa).
- Logging: Stores the last known state (reachable or unreachable) in a local file for comparison in subsequent checks.
- Email Notification: Utilizes an SMTP server to notify administrators of EFS status changes.

## Prerequisites

- Python 3.6 or higher.
- Access to an SMTP server for sending emails.
- Permissions to read/write files in the /tmp directory and access the EFS mount.

## Usage

1. **Clone the repository** and navigate to the directory.

    ```bash
    git clone https://github.com/moorthyoncloud/python_fileshare_monitoring.git
    cd python_fileshare_monitoring
    ```

2. **Run the below command**

    ```bash
    python efs_health_check.py
    ```

## Configuration

- **SMTP_SERVER** = 'your SMTP Hostname'
- **SMTP_PORT** = 25  # Default port for non-authenticated SMTP
- **EMAIL_USER** = 'from_email_address'
- **EMAIL_TO** = 'to_email_address'


## EFS Health Check File (Assuming the EFS share is mounted under /efs)

- **efs_health_file** = "/efs/efshealth_DO_NOT_DELETE"

## Alert Messages (State Change Alerts)

**Failure Alert**:
- Subject: EFS Health Check Failed
- Body: EFS health file at <efs_health_file> is not reachable! on <hostname>

**Recovery Alert**:
- Subject: EFS Health Check Failed
- Body: EFS health file at <efs_health_file> is not reachable! on <hostname>

## Notes

- The script saves the last known state in a temporary file (/tmp/efs_last_state.txt) to track state changes. Ensure the script has write permissions for this location.
- You can uncomment the infinite loop (while True) and the time.sleep() line for continuous monitoring.

## License
This project is licensed under the MIT License.

## Author
- [Shenbagamoorthy](https://github.com/moorthyoncloud)
