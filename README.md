# Reddit Comment Extractor

Python application to extract comments from Reddit posts and export them to CSV.

## Requirements

- Python 3.11 or higher
- Reddit account
- Registered Reddit app

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/reddit-comment-extractor.git
cd reddit-comment-extractor
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure your credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Create a "script" type app
   - Copy `config.example.py` to `config.py`
   - Fill in your credentials in `config.py`

## Usage
```bash
python main.py
```

## Project Structure
```
reddit-comment-extractor/
│
├── venv/                  # Virtual environment (not uploaded to GitHub)
├── config.py              # Credentials (not uploaded to GitHub)
├── config.example.py      # Configuration example
├── main.py                # Main script
├── requirements.txt       # Dependencies
├── .gitignore            # Files ignored by Git
└── README.md             # This file
```

## License

MIT