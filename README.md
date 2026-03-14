# Lead Automation Project

Automated lead generation system that finds businesses with websites using Geoapify API and stores them in Google Sheets.

## Features

- 🔍 **Smart Business Search**: Uses Geoapify Places API to find businesses across multiple Indian cities
- 🌐 **Website Detection**: Automatically finds and validates business websites
- 📊 **Google Sheets Integration**: Stores leads directly in Google Sheets
- 🚫 **Duplicate Prevention**: Prevents duplicate entries
- 🏢 **Multi-Category Support**: Searches for restaurants, cafes, clinics, salons, stores, etc.
- 🌍 **Multi-Location**: Covers cities across Karnataka, Telangana, Andhra Pradesh, and Kerala
- ⚡ **24/7 Automation**: Runs automatically every 2 hours using GitHub Actions

## How It Works

1. **Location Rotation**: Cycles through different cities in India
2. **Category Selection**: Selects business categories based on schedule
3. **API Search**: Uses Geoapify API to find businesses in the selected location
4. **Website Discovery**: Attempts to find working websites for businesses
5. **Quality Filter**: Only adds businesses that have valid websites
6. **Google Sheets**: Stores the leads with business details and working website links

## Setup for GitHub Actions

### Required Secrets

Add these secrets in your GitHub repository settings:

1. **GEOAPIFY_API_KEY**: Your Geoapify API key
2. **SERVICE_ACCOUNT_JSON**: Google Service Account JSON (entire file content)

### Automation Schedule

The system runs automatically every 2 hours using GitHub Actions cron schedule:
```yaml
schedule:
  - cron: "0 */2 * * *"  # Every 2 hours
```

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up configuration files in `config/` directory
4. Run: `python main.py`

## Project Structure

```
automation-project/
├── .github/workflows/automation.yml  # GitHub Actions workflow
├── config/                          # Configuration files
├── data/                           # Data and logs
├── scraper/                        # Web scraping modules
├── utils/                          # Utility functions
├── main.py                         # Main automation script
└── requirements.txt                # Python dependencies
```

## Recent Results

The system successfully finds businesses with working websites:
- Nucleus Mall: https://www.nucleusmall.in
- LULU MALL: https://www.lulumall.in
- Hilite Mall: https://www.hilitemall.com
- Focus Mall: https://www.focusmall.in
- And many more...

## GitHub Actions Logs

Check the Actions tab in your repository to see:
- Script execution logs
- Number of leads found
- Any errors or issues
- Execution time and status