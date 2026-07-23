# 🦍 PrimeApes

**Manage and plan your workouts from a single dashboard.**

PrimeApes is a web application built with [Streamlit](https://streamlit.io/), designed for athletes and fitness enthusiasts who want to centralize the planning of their training cycles, track their sessions, and browse an exercise database — all from one simple, interactive interface.

![Python](https://img.shields.io/badge/python-100%25-blue)
![Streamlit](https://img.shields.io/badge/framework-Streamlit-FF4B4B)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

---

## Overview

PrimeApes organizes the training experience into four independent navigation sections, managed via Streamlit's `st.navigation`:

| Page | Icon | Purpose |
|---|---|---|
| **Main Page** | 🏠 | Main view / application home dashboard. |
| **Cycle Planner** | 📅 | Planning of training cycles and mesocycles. |
| **Workout Tracker** | ⏱️ | Logging and tracking of completed workout sessions. |
| **Exercise Database** | 🏋️ | Browsing a catalog of available exercises. |

## Features

- 📊 **Data visualization** of progress and performance through interactive charts (Plotly).
- 🗓️ **Training cycle planning** for medium/long-term programming.
- 📝 **Workout logging** to keep a history of sessions.
- 📚 **Exercise database** browsable directly from the app.
- ☁️ **Cloud data persistence** via [Supabase](https://supabase.com/).

> ℹ️ Some page-specific features may expand as the project evolves. This README describes the purpose of each module based on the current repository structure.

## Tech stack

| Category | Technology |
|---|---|
| Language | Python |
| Web framework / UI | [Streamlit](https://streamlit.io/) |
| Data visualization | [Plotly](https://plotly.com/python/) |
| Data handling | [Pandas](https://pandas.pydata.org/) |
| Backend / Database | [Supabase](https://supabase.com/) |

## Project structure

```
primeapes-app/
├── app.py                 # Application entry point (config and navigation)
├── requirements.txt       # Project dependencies
├── data/                  # Data used by the application (e.g. exercise catalog)
├── pages/                 # App pages (Streamlit multipage app)
│   ├── main_page.py
│   ├── cycle_planner.py
│   ├── workout_tracker.py
│   └── exercise_database.py
└── src/                   # Shared application logic and utilities
```

## Installation

### Prerequisites

- Python 3.9 or higher
- A [Supabase](https://supabase.com/) account and project (for the database connection)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/angelrbl/primeapes-app.git
   cd primeapes-app
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses Supabase as its data backend. You'll need to set your project credentials, via Streamlit's `secrets.toml` file:

```toml
# .streamlit/secrets.toml
SUPABASE_URL = "https://<your-project>.supabase.co"
SUPABASE_KEY = "<your-api-key>"
```

## Usage

Once the dependencies are installed and Supabase is configured, run the application with:

```bash
streamlit run app.py
```

The app will open automatically in your browser, showing the sidebar navigation with the four available sections.


## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Built by <a href="https://github.com/angelrbl">@angelrbl</a>
</div>
