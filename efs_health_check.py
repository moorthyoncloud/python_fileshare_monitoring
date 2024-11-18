import os
import socket
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# File to store the last known state (reachable/unreachable)
STATE_FILE = '/tmp/efs_last_state.txt'
SERVER_HOSTNAME = socket.gethostname()
# SMTP email settings (no authentication required)
SMTP_SERVER = 'your SMTP Hostname'
SMTP_PORT = 25
EMAIL_USER = 'from_email_address'
EMAIL_TO = 'to_email_address'

def check_efs_health_file(efs_health_file):
    """
    Check if the EFS health file is accessible.
    :param efs_health_file: Full path to the EFS health check file (e.g., "/efs/efshealth").
    :return: True if accessible, False otherwise.
    """
    try:
        if os.path.exists(efs_health_file):
            with open(efs_health_file, 'r') as f:
                f.read()  # Attempt to read the file
            return True
        else:
            return False
    except Exception:
        return False


def load_last_state():
    """
    Load the last known state from a file.
    :return: True if last known state was reachable, False otherwise.
    """
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            return file.read().strip() == 'reachable'
    return True  # Assume reachable by default if no state file exists


def save_current_state(is_reachable):
    """
    Save the current state to a file.
    :param is_reachable: Current state (True for reachable, False for unreachable).
    """
    state = 'reachable' if is_reachable else 'unreachable'
    with open(STATE_FILE, 'w') as file:
        file.write(state)


def send_email(subject, message):
    """
    Send an email alert using SMTP (without authentication).
    :param subject: The subject of the email.
    :param message: The message body of the email.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(message, 'plain'))

        # Establish an SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        # Send the email
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()
        print(f"Email sent to {EMAIL_TO} with subject '{subject}'.")

    except Exception as e:
        print(f"Failed to send email: {e}")


def send_alert(message, subject):
    """
    Trigger an email alert when the state changes.
    :param message: Message to be sent as an alert.
    :param subject: Subject of the alert email.
    """
    print(f"ALERT: {message}")
    send_email(subject, message)


if __name__ == "__main__":
    efs_health_file = "/efs/efshealth_DO_NOT_DELETE"  # Path to the EFS health check file
    check_interval = 60  # Check every 60 seconds

#    while True:
        # Load the last known state
    last_state_reachable = load_last_state()

        # Check the current EFS health by checking if the health file is accessible
    current_reachable = check_efs_health_file(efs_health_file)

        # If state has changed, trigger an alert
    if last_state_reachable and not current_reachable:
            send_alert(f"EFS health file at {efs_health_file} is not reachable! on {SERVER_HOSTNAME}",
                       subject="EFS Health Check Failed")
    elif not last_state_reachable and current_reachable:
            send_alert(f"EFS health file at {efs_health_file} is back online on {SERVER_HOSTNAME}",
                       subject="EFS Health Check Restored")

        # Save the current state for the next iteration
    save_current_state(current_reachable)

        # Wait before checking again
#        time.sleep(check_interval)

