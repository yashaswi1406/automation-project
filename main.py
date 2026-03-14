import json
import os
from datetime import datetime

from scraper.search_engine import get_daily_businesses

from utils.sheet_handler import get_all_emails, append_rows, clear_sheet_formatting
from utils.duplicate_checker import is_duplicate
from utils.scheduler_state import get_today_category
from utils.logger import log_event
from utils.website_validator import is_valid_business_website


SPREADSHEET_ID = "1m5Fehqq_cVAb7jitVw1IMo1l_R8XGG0XiQK-gFpKX8I"


def load_email_config():
    try:
        with open("config/email_config.json", "r") as f:
            return json.load(f)
    except:
        return {}


def ensure_directories():
    """Ensure all necessary directories exist"""
    os.makedirs("config", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Create default config files if they don't exist
    if not os.path.exists("config/categories.json"):
        with open("config/categories.json", "w") as f:
            json.dump({}, f)
    
    if not os.path.exists("config/location_state.json"):
        with open("config/location_state.json", "w") as f:
            json.dump({"index": 0}, f)
    
    if not os.path.exists("data/scheduler_state.json"):
        with open("data/scheduler_state.json", "w") as f:
            json.dump({}, f)
    
    if not os.path.exists("data/logs.txt"):
        with open("data/logs.txt", "w") as f:
            f.write("")


def main():
    ensure_directories()
    
    log_event("===== Lead Automation Started =====")
    log_event(f"Running in environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")

    # Clear any existing formatting in the sheet
    try:
        clear_sheet_formatting()
    except Exception as e:
        log_event(f"Could not clear formatting: {e}")

    business_category = get_today_category()
    log_event(f"Selected category: {business_category}")

    leads = get_daily_businesses(business_category, limit=6)
    log_event(f"Leads fetched: {len(leads)}")

    if not leads:
        log_event("No leads found. Exiting.")
        return

    existing_identifiers = get_all_emails()
    log_event(f"Existing websites loaded: {len(existing_identifiers)}")

    new_rows = []

    # Only process leads that have websites
    leads_with_websites = [lead for lead in leads if lead.get("website", "").strip()]
    leads_without_websites = [lead for lead in leads if not lead.get("website", "").strip()]
    
    log_event(f"Leads with websites: {len(leads_with_websites)}, without websites: {len(leads_without_websites)} (ignored)")

    # Process only leads with websites
    for lead in leads_with_websites:
        website = lead.get("website", "").strip()
        name = lead.get("name", "")
        address = lead.get("address", "")

        # Skip if no name, address, or website
        if not name or not address or not website:
            continue

        # 🚫 Block invalid websites
        if not is_valid_business_website(website):
            continue

        # Use website as identifier
        identifier = website.lower().strip()

        # 🚫 Block duplicates forever
        if is_duplicate(identifier, existing_identifiers):
            continue

        row = [
            business_category,
            name,
            address,
            lead.get("phone", ""),
            website,
            "",
            lead.get("city", ""),
            datetime.today().strftime("%Y-%m-%d"),
            "NO",
            "",
            "",
            ""
        ]

        new_rows.append(row)
        existing_identifiers.add(identifier)

    if new_rows:
        append_rows(new_rows)
        log_event(f"Rows added: {len(new_rows)}")
        
        # Print results for GitHub Actions logs
        print(f"✅ Successfully added {len(new_rows)} new businesses with websites:")
        for row in new_rows:
            print(f"  - {row[1]} | {row[4]} | {row[6]}")
    else:
        log_event("No new unique leads found")
        print("ℹ️ No new unique leads found")

    log_event("===== Automation Completed =====")


if __name__ == "__main__":
    main()
