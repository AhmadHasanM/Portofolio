# PPT Generator Backend

Backend service for generating PowerPoint presentations with AI-driven content, customizable templates, and export options.

---

## Overview

This project provides an API for dynamically creating presentations. It integrates external AI news sources, applies custom branding, and exports ready-to-use PPTX files.

### Key Features

- **Main API (`app/main`)**: Entry points and service orchestration.
- **Templating (`app/templating`)**: Manages slide templates and layout logic.
- **Branding (`app/branding`)**: Applies logos, colors, and fonts for customization.
- **Export (`app/export`)**: Generates and exports PPTX presentations.
- **Models (`app/models`)**: Defines data structures (e.g., users, presentations).

---

## Getting Started

### Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

### Setup

```bash
git clone https://github.com/Caprae-Capital-Partners/LeadGenAI.git
git checkout sandbox-database-ppt-gen
cd backend-database\backend\services\ppt-generator
python -m venv .env
.env\Scripts\activate  # On Mac: source .env/bin/activate
pip install -r requirements.txt
