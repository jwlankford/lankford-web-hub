import sqlite3
import os
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), "lankford_hub.db")

print(f"[SYSTEM] Connecting to database at {db_path}...")
if not os.path.exists(db_path):
    print("[SYSTEM] Database file does not exist yet. It will be initialized when the backend starts.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    notebooks = [
        (
            "Colab Notebook: Multi-Agent Evaluation & Verification",
            "Interactive Google Colab workspace demonstrating live feed integration, multi-agent evaluation workflows, and runtime verification constraints.",
            "https://colab.research.google.com/drive/1XEQT-oTF_KkmY5FHkMIcWEuAlJziBaoe?usp=sharing",
            "Colab,Agentic,Integrations",
            "academic"
        ),
        (
            "Colab Notebook: Multi-Agent Evaluation & Verification",
            "Interactive Google Colab workspace demonstrating live feed integration, multi-agent evaluation workflows, and runtime verification constraints.",
            "https://colab.research.google.com/drive/1XEQT-oTF_KkmY5FHkMIcWEuAlJziBaoe?usp=sharing",
            "Colab,Agentic,Integrations",
            "professional"
        )
    ]

    for title, desc, url, tags, tenant in notebooks:
        # Check if this notebook URL already exists for this tenant
        cursor.execute(
            "SELECT id FROM jupyter_notebooks WHERE notebook_url = ? AND tenant = ?", 
            (url, tenant)
        )
        row = cursor.fetchone()
        if row is None:
            print(f"[SYSTEM] Inserting notebook '{title}' for tenant '{tenant}'...")
            cursor.execute(
                """
                INSERT INTO jupyter_notebooks (title, description, notebook_url, tags, tenant, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, desc, url, tags, tenant, datetime.utcnow().isoformat())
            )
        else:
            print(f"[SYSTEM] Notebook '{title}' for tenant '{tenant}' already exists.")

    conn.commit()
    conn.close()
    print("[SYSTEM] Database migration completed successfully.")
