import getpass
import time
import logging
import csv
import os
from telegram import Bot
from telegram.error import TelegramError

# ==========================================================
# 🛑 1. CRITICAL CONFIGURATION SECTION (Yahan values daalein)
# ==========================================================
# --- REQUIRED INPUTS ---
TELEGRAM_BOT_TOKEN = "8920338944:AAEYUIPF5VSnUeWL9IekRUhR_9bj4sIDUM4" # <-- APNA TELEGRAM TOKEN DAALEIN
TELEGRAM_CHAT_ID = "8076275820"            # <-- APNA CHANNEL/GROUP ID DAALEIN
MASTER_PASSWORD = "11115.8010164743"            # <-- BOMBER KA MAHA PASSWORD

# --- SYSTEM PARAMETERS ---
TARGET_FILE = "targets.csv" # Target list ka naam (File path)
RUN_DURATION_HOURS = 10      # System kitne ghante chalega
# ==========================================================

# --- LOGGING & SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- TELEGRAM INTEGRATION SETUP ---
telegram_bot = None
try:
    from telegram import Bot
    telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)
    print("\n✅ Telegram Bot Client Successfully Initialized.")
except ImportError:
    print("\n⚠️ WARNING: 'python-telegram-bot' not found. Running in local console mode only.")
except Exception as e:
    print(f"\n❌ ERROR during Telegram setup: {e}. Running in local console mode.")


def send_telegram_notification(message, severity="INFO"):
    """Telegram ko status, success, ya error bhejne ka function."""
    global telegram_bot
    if not telegram_bot:
        logger.info(f"[LOCAL LOG - {severity}]: {message}")
        return

    formatted_message = f"🤖 *[{severity}]*\n{message}"
    try:
        telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=formatted_message, parse_mode='Markdown')
        logger.info(f"➡️ Telegram notification sent successfully.")
    except TelegramError as e:
        logger.error(f"❌ Telegram Error (Check Token/Chat ID): {e}")
    except Exception as e:
        logger.error(f"❌ General Error while sending Telegram: {e}")


# --- CORE BOMBER MODULES (PLACEHOLDERS) ---
def run_sms_otp_bomber(targets):
    """SMS Aur OTP Bomber Logic."""
    logger.info(f"🚀 SMS/OTP Bomber Shuru Ho Raha Hai. Targets: {len(targets)}")
    # *** CORE LOGIC HERE ***
    success_count = len(targets) # Simulation
    send_telegram_notification(f"✅ SMS/OTP Bombing Poora Hua. Successfully Processed: {success_count}", "SUCCESS")

def run_call_bomber(targets):
    """Spam Call Bomber Logic."""
    logger.info(f"📞 Call Bomber Shuru Ho Raha Hai. Targets: {len(targets)}")
    # *** CORE LOGIC HERE ***
    call_count = len(targets) # Simulation
    send_telegram_notification(f"📞 Call Bomber: {call_count} targets ko call kiya gaya.", "INFO")

def run_whatsapp_bomber(targets):
    """WhatsApp Channel/SMS Bomber Logic."""
    logger.info(f"📱 WhatsApp Channel Bomber Shuru Ho Raha Hai. Targets: {len(targets)}")
    # *** CORE LOGIC HERE ***
    whatsapp_sent = len(targets) # Simulation
    send_telegram_notification(f"📱 WhatsApp Bombing Poora Hua. Total Messages Sent: {whatsapp_sent}", "SUCCESS")


# --- ORCHESTRATOR FUNCTIONS ---

def create_mock_csv(file_path):
    """If targets.csv doesn't exist, creates it with dummy data."""
    logger.warning(f"🚨 File '{file_path}' not found. Creating mock data for immediate testing.")

    mock_data = [
        {'number': '919876543210', 'type': 'SMS'}, 
        {'number': '1234567890', 'type': 'Call'},
        {'number': '07700900123', 'type': 'WhatsApp'},
        {'number': '12255554444', 'type': 'SMS'}
    ]

    fieldnames = ['number', 'type']
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mock_data)
        logger.info(f"✅ Mock file '{file_path}' successfully created with {len(mock_data)} dummy targets.")
        return mock_data
    except IOError as e:
        logger.error(f"❌ Fatal Error: Could not create Mock CSV file {file_path}: {e}")
        return None

def load_targets(file_path):
    """Targets ko file se load karta hai (Creates mock file if not found)."""
    logger.info(f"⏳ Starting target loading from {file_path}...")

    if not os.path.exists(file_path):
        mock_data = create_mock_csv(file_path)
        if mock_data is None:
            return []
        return mock_data

    try:
        targets_list = []
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                targets_list.append(row)
        logger.info(f"✅ Successfully loaded {len(targets_list)} targets from {file_path}.")
        return targets_list
    except Exception as e:
        logger.error(f"❌ Critical Error reading targets file {file_path}: {e}")
        return []

def authenticate_user():
    """User se password maangta hai aur check karta hai. (SECURITY GATE)"""
    print("\n" + "="*60)
    print("🛡️ BOMBER SYSTEM ACCESS GATE: LOGIN REQUIRED 🛡️")
    print("="*60)

    # Added specific error handling for EOFError in case the environment closes the input stream
    try:
        password_input = getpass.getpass(f"🔑 System access: Enter Master Password: ")
    except EOFError:
        print("\n❌ Input Stream Closed (EOFError). Cannot authenticate. Aborting.")
        return False
    except Exception as e:
        print(f"\n❌ General Input Error: {e}. Cannot authenticate. Aborting.")
        return False

    if password_input == MASTER_PASSWORD:
        print("\n✅ Authentication SUCCESSFUL! System ready to deploy.")
        return True
    else:
        print("\n❌ Authentication FAILED. Incorrect Password provided. System halted.")
        return False

def main_bomber_system():
    """System ko start, run, aur stop karne ka mukhya control flow."""

    # 1. Load Targets
    all_targets = load_targets(TARGET_FILE)

    if not all_targets:
        logger.error("❌ System HALTED: No valid targets found. Cannot proceed with bombing.")
        send_telegram_notification("🔴 FATAL: Target list is empty or unreadable. System halted.", "CRITICAL")
        return

    # 2. Authentication Gate
    if not authenticate_user():
        return

    # 3. Main Execution Loop Setup
    print("\n" + "="*80)
    print(f"🚀 BOMBER SYSTEM LIVE MODE ACTIVATED! (Running for {RUN_DURATION_HOURS} hours) 🚀")
    print("================================================================================")

    start_time = time.time()
    run_duration_seconds = RUN_DURATION_HOURS * 3600 # 10 hours * 60 min * 60 sec

    try:
        while (time.time() - start_time) < run_duration_seconds:

            # --- A. Core Bombing Action ---
            logger.info("\n\n======== CYCLE START: Executing Bombing Modules ========")
            # Running sequentially. For high performance, implement ThreadPoolExecutor here.
            run_sms_otp_bomber(all_targets)
            run_call_bomber(all_targets)
            run_whatsapp_bomber(all_targets)

            # --- B. Monitoring and Pacing ---
            time_elapsed = int(time.time() - start_time)
            minutes_elapsed = time_elapsed // 60

            print("\n" + "="*50)
            print(f"📈 LIVE STATUS | Elapsed Time: {minutes_elapsed} mins | Remaining: {RUN_DURATION_HOURS - (minutes_elapsed/60):.1f} hrs")
            print("="*50)

            # Pacing: Wait 60 seconds before starting the next major cycle
            time.sleep(60) 

    except KeyboardInterrupt:
        print("\n\n🛑 [USER INTERRUPT] Ctrl+C pressed. Initiating graceful shutdown.")
    except Exception as e:
        error_msg = f"🚨 UNEXPECTED CRITICAL FAILURE: {type(e).__name__} - {str(e)}"
        print(f"\n--- CRITICAL ERROR --- {error_msg}")
        send_telegram_notification(error_msg, "CRITICAL")
    finally:
        # Final Shutdown Sequence
        print("\n" + "="*80)
        print("✅ BOMBER SYSTEM SHUTDOWN SEQUENCE INITIATED.")
        send_telegram_notification("🏁 BOMBER SYSTEM FINISHED ITS RUNTIME & SHUTDOWN SUCCESSFUL.", "FINISH")
        print("================================================================================")

if __name__ == "__main__":
    main_bomber_system()