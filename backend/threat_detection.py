import os
from datetime import datetime


FAILED_ATTEMPTS = {}


def record_failed_login(username):

    if username not in FAILED_ATTEMPTS:

        FAILED_ATTEMPTS[username] = 0


    FAILED_ATTEMPTS[username] += 1


    log_security_event(
        username,
        "FAILED LOGIN ATTEMPT"
    )


    if FAILED_ATTEMPTS[username] >= 5:

        log_security_event(
            username,
            "BRUTE FORCE ATTACK DETECTED"
        )


        return True


    return False



def reset_attempts(username):

    if username in FAILED_ATTEMPTS:

        FAILED_ATTEMPTS[username] = 0



def log_security_event(username, event):

    os.makedirs(
        "security_logs",
        exist_ok=True
    )


    with open(
        "security_logs/threat.log",
        "a"
    ) as f:


        f.write(
            f"{datetime.utcnow()} | {username} | {event}\n"
        )
