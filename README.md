# 🤖 AI Agent Project – Day 1: Ingest and Index GitHub Data

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Status](https://img.shields.io/badge/Status-Day%201%20Completed-success)

## 📌 Project Overview

This project is part of a **7-Day AI Agents Crash Course**, where the goal is to build intelligent AI systems capable of understanding and interacting with data.

On **Day 1**, the focus was on:

✅ Downloading data from a GitHub repository  
✅ Processing markdown documentation files  
✅ Extracting metadata using frontmatter  
✅ Preparing structured AI-ready data for future indexing and search

This project acts as the **first step in building an AI-powered documentation assistant** that can understand and answer questions from GitHub repositories.

---

# 🎯 Objective

The main objective of Day 1 was to build a **data ingestion pipeline** for GitHub repositories.

Instead of manually reading documentation, this pipeline:

📥 Downloads a repository as a ZIP file  
📂 Extracts markdown documentation files (`.md`, `.mdx`)  
🧠 Reads metadata using frontmatter  
📝 Extracts clean textual content  
⚙️ Converts repository documentation into structured data for AI systems

This structured data will later be used to build an AI Agent capable of answering repository-related questions.

---

# 🛠️ Technologies Used

The following tools and libraries were used:

| Technology | Purpose |
|------------|---------|
| Python 3.14 | Main programming language |
| Jupyter Notebook | Interactive development environment |
| requests | Download GitHub repositories |
| python-frontmatter | Parse markdown metadata |
| zipfile | Extract ZIP archives |
| io | Handle in-memory file operations |
| uv | Package and environment management |
| Git & GitHub | Version control and project hosting |

---

# 📂 Project Structure

```text
AI-Agent-/
│── day1.ipynb
│── README.md
│── pyproject.toml
│── uv.lock
