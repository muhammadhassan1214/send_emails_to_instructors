# AHA Instructor Email Automation

An automated Python application that retrieves class and student enrollment data from the American Heart Association (AHA) Atlas portal and sends notification emails to instructors about new student enrollments.

## 🎯 Overview

This tool automates the process of:
1. Logging into the AHA Atlas portal
2. Fetching classes with enrolled students via API
3. Retrieving detailed class and student information
4. Generating personalized HTML emails for instructors
5. Sending emails via the Brevo (formerly Sendinblue) API
6. Running on a scheduled basis (9 AM & 9 PM Eastern Time)

## ✨ Features

- **Automated Login**: Selenium-based authentication to AHA Atlas portal
- **JWT Token Capture**: Extracts authentication tokens for API calls
- **API Integration**: Fetches class listings, class details, and student information
- **HTML Email Generation**: Creates professional, formatted notification emails
- **Email Delivery**: Sends emails via Brevo transactional email API
- **Scheduling**: Runs automatically twice daily (9 AM & 9 PM ET)
- **Duplicate Prevention**: Tracks processed classes to avoid sending duplicate emails
- **Session Persistence**: Maintains Chrome session data for reliable logins

## 📋 Requirements

- Python 3.10+
- Google Chrome browser
- Brevo API account (for email sending)
- AHA Atlas portal credentials

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd send_mails_to_instructors
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:** `venv\Scripts\activate`
   - **Linux/Mac:** `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# AHA Atlas Portal Credentials
AHA_USERNAME=your_aha_email@example.com
AHA_PASSWORD=your_aha_password

# Brevo Email API
BREVO_API_KEY=your_brevo_api_key
SENDER_EMAIL=sender@yourdomain.com

# Notification Copy Recipient
NATHAN_EMAIL=admin@example.com
```

## 🚀 Usage

Run the main script:

```bash
python script/main.py
```

The script will:
1. Schedule the next run at either 9 AM or 9 PM (Eastern Time)
2. Log into the AHA Atlas portal
3. Navigate to class listings for "Shell CPR, LLC."
4. Fetch all classes with enrolled students
5. For each class, retrieve student contact information
6. Generate and send notification emails to instructors
7. Track completed classes to prevent duplicate notifications

## 📁 Project Structure

```
send_mails_to_instructors/
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
└── script/
    ├── main.py                      # Main entry point
    └── utils/
        ├── __init__.py
        ├── automation.py            # Selenium automation (login, navigation)
        ├── scheduler.py             # Task scheduling (9 AM & 9 PM ET)
        ├── static.py                # Constants, locators, API endpoints
        ├── util.py                  # Selenium utilities (click, input, driver setup)
        ├── apis/
        │   ├── __init__.py
        │   ├── get_classes.py       # Fetch class listings API
        │   ├── get_class_info.py    # Fetch class details API
        │   └── get_student_info.py  # Fetch enrolled students API
        ├── data/
        │   ├── done_classes.txt     # Processed class IDs tracker
        │   └── instructorList.csv   # Instructor email lookup data
        ├── mail_sender/
        │   ├── __init__.py
        │   ├── email_generator.py   # HTML email template generator
        │   └── email_sender.py      # Brevo API email delivery
        └── chrome-dir/              # Chrome session data (auto-generated)
```

## 📊 Data Files

| File | Description |
|------|-------------|
| `data/done_classes.txt` | List of processed class IDs to prevent duplicate emails |
| `data/instructorList.csv` | CSV file containing instructor IDs and email addresses |

## 🔧 Key Components

### Automation (`automation.py`)
- `login()` - Authenticates to AHA Atlas portal
- `capture_jwt_token()` - Extracts JWT from browser localStorage
- `navigate_to_class_listings()` - Navigates to the class management section
- `get_email_by_id()` - Looks up instructor email from CSV by ID

### APIs (`apis/`)
- `get_classes()` - Fetches paginated list of classes with enrolled students
- `get_class_details()` - Retrieves class date, time, and location
- `get_students_in_class()` - Gets enrolled student contact information

### Email System (`mail_sender/`)
- `generate_email()` - Creates HTML email with student enrollment details
- `send_email()` - Sends email via Brevo transactional email API

### Scheduler (`scheduler.py`)
- `schedule_morning_and_night()` - Schedules task execution at 9 AM & 9 PM Eastern Time

## 📧 Email Content

The generated emails include:
- Instructor greeting
- Class date and location
- Student contact table (Name, Email, Phone)
- Training Center Coordinator signature
- Contact information and website links

## ⏰ Schedule

The script runs automatically at:
- **Morning:** 9:00 AM Eastern Time
- **Evening:** 9:00 PM Eastern Time

## 🔒 Security Notes

- Store sensitive credentials in `.env` file (never commit to version control)
- Chrome session data persists in `chrome-dir/` for authentication continuity
- JWT tokens are captured dynamically and not stored permanently

## 📝 Dependencies

| Package | Purpose |
|---------|---------|
| `selenium` | Browser automation |
| `webdriver-manager` | Chrome driver management |
| `requests` | HTTP API calls |
| `pandas` | Data manipulation |
| `python-dotenv` | Environment variable management |

## 🐛 Troubleshooting

1. **Login fails**: Ensure AHA credentials are correct in `.env`
2. **Email not sending**: Verify Brevo API key and sender email configuration
3. **Chrome issues**: Delete `chrome-dir/` folder and restart
4. **Missing instructor emails**: Update `instructorList.csv` with current data

## 📄 License

This project is proprietary software for Code Blue CPR Services.

## 👤 Author

Developed for **Shell CPR, LLC** / **Code Blue CPR Services**

---

*For support or questions, contact the development team.*
