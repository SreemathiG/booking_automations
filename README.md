🏨 Booking.com Test Automation Framework
A production-grade Selenium test automation framework for Booking.com that demonstrates Page Object Model, AI-powered dynamic test data generation, parallel execution, automatic screenshot capture on failure, and structured logging.

📋 Table of Contents

Prerequisites
Dependencies
Framework Structure
AI Architecture
Step-by-Step Execution
Test Scenarios
Reports and Logs
Run Commands Reference


✅ Prerequisites
Before running this framework, ensure you have the following installed:
PrerequisiteVersionDownloadPython3.10 or abovehttps://www.python.org/downloads/Google ChromeLatesthttps://www.google.com/chrome/GitLatesthttps://git-scm.com/downloads

Note: ChromeDriver is managed automatically by webdriver-manager — no manual installation needed.

You will also need:

A free Groq API key for AI test data generation → https://console.groq.com/keys
Internet connection (tests run against live Booking.com)


📦 Dependencies
All dependencies are listed in requirements.txt:
selenium          - Browser automation
pytest            - Test runner and assertions
webdriver-manager - Automatic ChromeDriver management
pyyaml            - YAML config file parsing
pytest-html       - HTML test report generation
pytest-xdist      - Parallel test execution
python-dotenv     - Environment variable management from .env file
Install all dependencies with:
powershellpip install -r requirements.txt

🏗️ Framework Structure
booking_automations/
│
├── ai_generator/                   ← AI-powered test data generation
│   ├── __init__.py
│   ├── generate_test_data.py       ← Calls AI API, saves JSON output
│   └── prompts.py                  ← AI prompt templates
│
├── test_data/
│   └── search_data.json            ← AI-generated test cases (consumed by tests)
│
├── locators/                       ← All element locators centralized here
│   ├── __init__.py
│   ├── home_locators.py            ← Locators for Booking.com homepage
│   ├── results_locators.py         ← Locators for search results page
│   └── hotel_locators.py           ← Locators for hotel detail page
│
├── pages/                          ← Page Object Model (POM) classes
│   ├── __init__.py
│   ├── base_page.py                ← Base class: explicit waits, JS click, scroll
│   ├── home_page.py                ← Homepage: popup handling, search
│   ├── results_page.py             ← Results: count cards, open first result
│   └── hotel_page.py               ← Hotel page: click Reserve button
│
├── tests/
│   ├── __init__.py
│   └── test_search.py              ← Parametrized end-to-end test cases
│
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py           ← Creates configured Chrome WebDriver
│   ├── logger.py                   ← Info + Error logging to file and console
│   └── screenshot.py               ← Auto screenshot on test failure
│
├── config/
│   └── config.yaml                 ← Non-sensitive config (default location etc.)
│
├── reports/                        ← Auto-generated test outputs
│   ├── report.html                 ← HTML test report
│   ├── test.log                    ← Full execution log
│   └── screenshots/                ← Failure screenshots (auto-saved)
│
├── .env                            ← Credentials and env variables (gitignored)
├── conftest.py                     ← Pytest fixtures + screenshot-on-failure hook
├── pytest.ini                      ← Pytest settings and default options
├── requirements.txt                ← Python package dependencies
├── .gitignore                      ← Git ignore rules
└── README.md                       ← This file
Key Design Decisions
DecisionReasonLocators in separate locators/ folderZero hardcoding in test files — single place to update if UI changes.env for credentialsKeeps sensitive data out of source codeExplicit Waits onlyNo time.sleep — tests wait exactly as long as neededAI data pre-generated to JSONTests run with zero API calls — fast, stable, deterministicFunction-scoped driver fixtureEach test gets its own browser — required for parallel safety

🤖 AI Architecture
This framework uses AI to dynamically generate test data once, which is then consumed by all tests.
┌─────────────────────────────────────────────────────────┐
│                   AI DATA PIPELINE                       │
│                                                          │
│  prompts.py  ──►  generate_test_data.py  ──►  Groq API  │
│                          │                               │
│                          ▼                               │
│               test_data/search_data.json                 │
│                          │                               │
│           ┌──────────────┼──────────────┐               │
│           ▼              ▼              ▼                │
│      test[Chennai]  test[Mumbai]  test[Delhi] ...        │
│                                                          │
│   Zero API calls during test execution — reads JSON only │
└─────────────────────────────────────────────────────────┘
Why this approach?

AI generates intelligent, varied, realistic test data
Tests are completely independent of AI availability
Regenerate test data anytime with a single command
Clean separation: AI for intelligence, Selenium for execution


🚀 Step-by-Step Execution
Step 1 — Clone the Repository
powershellgit clone https://github.com/YOUR_USERNAME/booking_automations.git
cd booking_automations
Step 2 — Create Virtual Environment
powershellpython -m venv venv
Step 3 — Activate Virtual Environment
powershellvenv\Scripts\activate
You should see (venv) at the start of your prompt.

⚠️ Important: Run this activation command every time you open a new terminal.

Step 4 — Install Dependencies
powershellpip install -r requirements.txt
Step 5 — Configure Environment Variables
Create a .env file in the project root:
powershellnotepad .env
Add the following content:
BASE_URL=https://www.booking.com/
BROWSER=chrome
TIMEOUT=15
GROQ_API_KEY=gsk_your-api-key-here
Get your free Groq API key at: 👉 https://console.groq.com/keys
Step 6 — Generate AI Test Data
This step calls the AI API once and saves test cases to test_data/search_data.json.
powershellpython -m ai_generator.generate_test_data
Expected output:
Calling Groq API (LLaMA3)...

✅ Generated 5 test cases → test_data/search_data.json

   1. [Chennai]   Search for hotels in Chennai and validate results
   2. [Mumbai]    Search for hotels in Mumbai and validate results
   3. [Delhi]     Search for hotels in Delhi and validate results
   4. [Bangalore] Search for hotels in Bangalore and validate results
   5. [Hyderabad] Search for hotels in Hyderabad and validate results

ℹ️ You only need to run this once. Re-run it anytime you want fresh AI-generated test data.

Step 7 — Run Tests Sequentially
powershellpytest -v
Expected output:
collected 5 items

tests/test_search.py::test_booking_flow[Chennai]   PASSED
tests/test_search.py::test_booking_flow[Mumbai]    PASSED
tests/test_search.py::test_booking_flow[Delhi]     PASSED
tests/test_search.py::test_booking_flow[Bangalore] PASSED
tests/test_search.py::test_booking_flow[Hyderabad] PASSED

5 passed in 177.87s
Step 8 — Run Tests in Parallel
powershellpytest -v -n 2
Expected output:
2 workers [5 items]

[gw0] PASSED tests/test_search.py::test_booking_flow[Chennai]
[gw1] PASSED tests/test_search.py::test_booking_flow[Delhi]
[gw1] PASSED tests/test_search.py::test_booking_flow[Bangalore]
[gw0] PASSED tests/test_search.py::test_booking_flow[Mumbai]
[gw0] PASSED tests/test_search.py::test_booking_flow[Hyderabad]

5 passed in 267.67s
Step 9 — View HTML Report
powershellstart reports\report.html

🧪 Test Scenarios
Each test case follows this complete end-to-end flow:
StepActionValidation1. SearchEnter city name in search box, handle autocomplete dropdown, submit searchSearch form submitted successfully2. Validate ResultsWait for property cards to loadAssert that results count > 03. Open HotelClick first property card, switch to new tabHotel detail page opens4. ReserveClick the Reserve / Book Now buttonButton clicked successfully
What Makes This Real-World Ready

Popup handling — automatically dismisses sign-in banners and cookie notices
Autocomplete handling — selects first dropdown suggestion via JavaScript click
Overlay handling — uses JS click to bypass intercepting elements
Tab switching — handles Booking.com opening hotels in new tabs
Renderer timeout recovery — robust wait strategy handles slow page loads


📊 Reports and Logs
HTML Report
Generated automatically after every test run at reports/report.html.
Contains:

Pass/fail status per test
Test duration
Environment metadata
Full captured logs per test
Error messages and stack traces for failures

Execution Log
Every test run appends to reports/test.log.
Format:
2026-03-22 16:45:01 [INFO    ] test_search - TEST START: Search for hotels in Chennai
2026-03-22 16:45:12 [INFO    ] ResultsPage - Property cards found: 25
2026-03-22 16:45:15 [INFO    ] test_search - PASS: 25 results found for 'Chennai'
2026-03-22 16:45:30 [INFO    ] test_search - TEST PASSED
Failure Screenshots
When any test fails, a screenshot is automatically saved to:
reports/screenshots/test_booking_flow_Chennai__20260322_164501.png

🔧 Run Commands Reference
powershell# Activate virtual environment (run every session)
venv\Scripts\activate

# Generate AI test data (run once or to refresh)
python -m ai_generator.generate_test_data

# Run all tests sequentially
pytest -v

# Run all tests in parallel (2 workers)
pytest -v -n 2

# Run a specific city only
pytest -v -k "Chennai"

# Run with explicit HTML report path
pytest -v --html=reports\report.html --self-contained-html

# View HTML report in browser
start reports\report.html

# View logs
type reports\test.log

🔒 Environment Variables Reference
VariableDescriptionExampleBASE_URLBooking.com URLhttps://www.booking.com/BROWSERBrowser to usechromeTIMEOUTDefault wait timeout (seconds)15GROQ_API_KEYGroq API key for AI data gengsk_xxx...

⚠️ Never commit .env to version control. It is listed in .gitignore.

Author:
Sreemathi G
Selenium Automation Framework — Booking.com
Python | Selenium | Pytest | AI Test Data Generation
