# Arcnetic Spider -- Web Crawling & Audit Platform

## 📌 Problem Statement

Manual website monitoring and data collection is time-consuming and
requires technical tools and expertise. Organizations and developers
often need automated solutions to fetch website content, verify page
status, and maintain visual records of webpages. This project provides a
web-based crawling platform that automates website fetching, screenshot
capture, and structured data storage using modern web technologies.

------------------------------------------------------------------------

## 💡 Project Overview

Arcnetic Spider is a full-stack web crawling and auditing system that
enables users to submit website URLs and automatically extract webpage
content using browser automation.

Users can: - Submit website URLs for scanning - Automatically load
webpages using headless browser automation - Capture screenshots of
webpages - Store webpage metadata and HTML content - View scan history
in real time - Delete stored crawl records

------------------------------------------------------------------------

## 🚀 Features

-   Automated website crawling using browser automation\
-   Screenshot capture for visual verification\
-   Asynchronous background crawling tasks\
-   REST API based communication\
-   Real-time frontend updates using polling\
-   Docker-based containerized deployment\
-   Scalable modular architecture

------------------------------------------------------------------------

## 🧠 Core Technologies Used

### Playwright (Browser Automation Engine)

Playwright is used to launch a headless Chromium browser to load modern
websites that use JavaScript and dynamic content. It enables real
browser rendering, full-page screenshot capture, HTML content
extraction, and reliable webpage loading.

### FastAPI (Backend Framework)

FastAPI is used to build REST APIs and manage background crawling tasks.
It provides high-performance asynchronous APIs, automatic API
documentation, background task execution, and database integration
support.

### PostgreSQL (Database)

PostgreSQL is used to store website URLs, page titles, screenshot data,
HTML content, and crawl timestamps.

------------------------------------------------------------------------

## 🛠 Tech Stack

### Frontend

-   Next.js\
-   React\
-   Tailwind CSS\
-   Axios

### Backend

-   FastAPI (Python)\
-   Playwright\
-   SQLAlchemy (Async ORM)\
-   PostgreSQL

### Deployment Tools

-   Docker\
-   Docker Compose

------------------------------------------------------------------------

## 🏗 System Architecture

User (Browser) \| Frontend (Next.js Dashboard) \| REST API Communication
\| Backend (FastAPI Server) \| Crawler Engine (Playwright) \| PostgreSQL
Database

------------------------------------------------------------------------

## 📁 Project Directory Structure

Demo-test/
│
├── frontend/
│   ├── app/
│   │   ├── favicon.ico
│   │   ├── globals.css
│   │   ├── layout.js
│   │   └── page.js
│   │
│   ├── utils/
│   │   └── api.js
│   │
│   ├── public/
│   │
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.mjs
│   ├── postcss.config.mjs
│   └── jsconfig.json
│
├── crawler_engine.py
├── database.py
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── .dockerignore

------------------------------------------------------------------------

## ⚙ Installation & Setup

### Step 1: Navigate to Project Directory

cd Demo-test

### Step 2: Configure Environment Variables

POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
POSTGRES_DB=spiderdb

DATABASE_URL=postgresql+asyncpg://postgres:postgres@spider_db:5432/spiderdb

### Step 3: Build Docker Images

docker compose build

### Step 4: Start Application

docker compose up -d

### Step 5: Verify Running Containers

docker ps

------------------------------------------------------------------------

## 🌐 Application Access

Frontend Interface: http://localhost:3000

Backend API Documentation: http://localhost:8000/docs

------------------------------------------------------------------------

## 🔄 How The System Works

1.  User enters website URL on frontend dashboard\
2.  Frontend sends POST request to backend API\
3.  Backend starts crawler as a background task\
4.  Playwright browser loads the webpage\
5.  Screenshot and HTML content are extracted\
6.  Data is stored in PostgreSQL database\
7.  Frontend polls backend for updated scan results\
8.  Results are displayed automatically

------------------------------------------------------------------------

## 🔧 Major Backend Functions Explained

### run_crawler_task()

-   Launches headless browser\
-   Opens website URL\
-   Extracts page title\
-   Captures screenshot\
-   Fetches HTML content\
-   Stores extracted data in database

### retry_goto()

-   Handles webpage loading retries\
-   Improves reliability during slow connections\
-   Prevents crawler failures

### init_db()

-   Initializes database connection\
-   Creates required tables\
-   Ensures database readiness during startup

------------------------------------------------------------------------

## 🎯 Use Cases

-   Website monitoring\
-   SEO auditing\
-   Compliance verification\
-   Screenshot archiving\
-   Automated web data collection\
-   Academic and research projects

------------------------------------------------------------------------

## 👨‍💻 Author

Binil K Joseph
Full Stack Developer Intern
Arcnetic Pvt.Ltd
