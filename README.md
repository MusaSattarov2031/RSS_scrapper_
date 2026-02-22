# RSS News ETL Pipeline

A robust Data Engineering project that automates the Extraction, Transformation, and Loading (ETL) of news data from various RSS feeds into a centralized PostgreSQL database.
## 🚀 Project Overview

This pipeline is designed to handle the "messy" reality of web data. It pulls live feeds from sources like Google News and NASA, cleanses nested HTML artifacts, standardizes data formats using Pandas, and ensures data integrity before loading into a relational database.
Core Features:

Extraction: Multi-source RSS ingestion with custom Header Spoofing to bypass bot-detection.

Transformation: * Regex-based HTML stripping and entity decoding.

   Pandas-driven deduplication based on unique article URLs.

   Standardization of heterogeneous pubDate strings into ISO-8601 datetimes.

Loading: Automated schema management and data insertion via SQLAlchemy.

Quality Assurance: 100% test coverage for the parsing and cleansing logic using pytest.

## 🛠️ Installation & Setup
1. Clone the Repository
```bash
git clone https://github.com/yourusername/RSS_scrapper.git
cd RSS_scrapper
```

2. Initialize Virtual Environment

To keep the project dependencies isolated from your system, create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies

Instead of installing packages individually, use the existing requirements.txt file to set up the environment exactly as intended:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

🧪 Running Tests

The test suite is designed to run against local data samples to ensure the pipeline remains functional even without an internet connection.
```bash
# Run all tests
pytest tests/

# Run tests with verbose output
pytest -v
```
Author: Computer Engineering Student at Ankara University. Focus on Data Engineering and Backend Systems.
