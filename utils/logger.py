import logging
import os


def get_logger(name="booking_automation"):
    """
    Returns a named logger with two handlers:
    - File handler  → reports/test.log    (INFO and above)
    - Console handler → terminal output   (ERROR and above)

    Calling get_logger() multiple times with the same name
    is safe — handlers are only added once.
    """
    os.makedirs("reports", exist_ok=True)

    logger = logging.getLogger(name)

    # Guard: do not add duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── File handler: INFO+ ──────────────────────────────────────
    file_handler = logging.FileHandler("reports/test.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ── Console handler: ERROR+ ──────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger