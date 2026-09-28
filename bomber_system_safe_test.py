"""
Safe test-mode campaign simulator.

This version is designed for deployment/testing:
- No password prompt or interactive input.
- No real SMS, calls, WhatsApp messages, or OTP requests.
- No Twilio API calls.
- Uses an in-memory test target list.
- Telegram reporting is disabled by default.
"""

import logging
import random
import threading
import time
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------
TELEGRAM_BOT_TOKEN = "8920338944:AAEYUIPF5VSnUeWL9IekRUhR_9bj4sIDUM4"
TELEGRAM_CHAT_ID = "8076275820"

# Test-only identifiers. Do not replace these with real people's numbers.
TARGET_LIST = [f"TEST-{i:03d}" for i in range(1, 11)]

TARGET_COUNT = len(TARGET_LIST)
CAMPAIGN_DURATION_MINUTES = 2
MAX_CONCURRENT_WORKERS = 5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

campaign_results = {
    "CALL_SIMULATION": {"success": 0, "failed": 0, "attempted": 0},
    "SMS_SIMULATION": {"success": 0, "failed": 0, "attempted": 0},
    "WHATSAPP_SIMULATION": {"success": 0, "failed": 0, "attempted": 0},
}

result_lock = threading.Lock()
semaphore = threading.Semaphore(MAX_CONCURRENT_WORKERS)


def send_telegram_notification(message, severity="INFO"):
    """Local-only reporting; no network request is made."""
    logger.info("[REPORT %s] %s", severity, message)


def simulate_service(service_name, target):
    """Simulate work without contacting any external service."""
    time.sleep(random.uniform(0.1, 0.4))
    success = random.choice([True, True, False])

    with result_lock:
        campaign_results[service_name]["attempted"] += 1
        if success:
            campaign_results[service_name]["success"] += 1
        else:
            campaign_results[service_name]["failed"] += 1

    logger.info(
        "[%s] %s -> %s",
        service_name,
        target,
        "SIMULATED SUCCESS" if success else "SIMULATED FAILURE",
    )


def worker(service_name, target):
    with semaphore:
        simulate_service(service_name, target)


def orchestrate_campaigns():
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=CAMPAIGN_DURATION_MINUTES)

    logger.info(
        "SAFE TEST MODE started: %d test targets, %d minute(s), max workers=%d",
        TARGET_COUNT,
        CAMPAIGN_DURATION_MINUTES,
        MAX_CONCURRENT_WORKERS,
    )

    threads = []

    for target in TARGET_LIST:
        for service in campaign_results:
            t = threading.Thread(
                target=worker,
                args=(service, target),
                daemon=False,
            )
            threads.append(t)
            t.start()

    while datetime.now() < end_time and any(t.is_alive() for t in threads):
        time.sleep(1)

    for t in threads:
        t.join()

    runtime = (datetime.now() - start_time).total_seconds()

    logger.info("=" * 60)
    logger.info("SAFE TEST REPORT")
    logger.info("=" * 60)

    for name, data in campaign_results.items():
        attempted = data["attempted"]
        success = data["success"]
        failed = data["failed"]
        rate = (success / attempted * 100) if attempted else 0.0
        logger.info(
            "%s: attempts=%d, success=%d, failed=%d, success_rate=%.1f%%",
            name,
            attempted,
            success,
            failed,
            rate,
        )

    logger.info("System complete. Runtime: %.2f seconds", runtime)


if __name__ == "__main__":
    orchestrate_campaigns()
