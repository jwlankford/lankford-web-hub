import asyncio
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Add parent directory to path so database and models can be imported
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine
import models

def fetch_latest_arxiv_papers(query="all:\"Agentic Development Life Cycle\" OR all:\"ADLC\" OR all:\"Agentic Software Engineering\"", max_results=10):
    url = f"http://export.arxiv.org/api/query?search_query={query}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    print(f"[ARXIV] Querying ArXiv API: {url}")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"[ARXIV] Error: Received status code {response.status_code}")
            return []
            
        root = ET.fromstring(response.content)
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        entries = root.findall('atom:entry', ns)
        results = []
        for entry in entries:
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', ns).text
            paper_url = entry.find('atom:id', ns).text
            
            # Authors
            authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
            
            results.append({
                'title': title,
                'summary': summary,
                'published': published,
                'url': paper_url,
                'authors': authors
            })
        print(f"[ARXIV] Successfully fetched {len(results)} candidate papers.")
        return results
    except Exception as e:
        print(f"[ARXIV] Exception during fetch: {e}")
        return []

async def sync_one_paper():
    # 1. Fetch papers from ArXiv
    papers = fetch_latest_arxiv_papers()
    if not papers:
        print("[SYNC] No papers retrieved from ArXiv. Exiting.")
        return
    
    # 2. Connect to the Neon DB
    print("[SYNC] Connecting to Neon database...")
    async with AsyncSession(engine) as session:
        # Check papers one by one, starting from the newest
        for paper in papers:
            title = paper['title']
            url = paper['url']
            
            # Normalize title for duplicate checking
            stmt = select(models.ResearchPaper).where(
                (models.ResearchPaper.title == title) | (models.ResearchPaper.url == url)
            )
            result = await session.execute(stmt)
            existing = result.scalars().first()
            
            if existing:
                print(f"[SYNC] Paper already exists: '{title[:50]}...'. Skipping.")
                continue
            
            # Found a new paper! Insert it
            authors_str = "; ".join(paper['authors'])
            pub_year = int(paper['published'][:4])
            
            new_paper = models.ResearchPaper(
                title=title,
                authors=authors_str,
                publication_year=pub_year,
                abstract=paper['summary'],
                url=url,
                tenant="academic", # Always academic context for research papers
                journal_or_conf="arXiv Preprint"
            )
            
            session.add(new_paper)
            await session.commit()
            await session.refresh(new_paper)
            
            print(f"[SYNC] SUCCESS: Loaded new paper into Neon database!")
            print(f"       Title: {new_paper.title}")
            print(f"       Authors: {new_paper.authors}")
            print(f"       Year: {new_paper.publication_year}")
            print(f"       URL: {new_paper.url}")
            return # Stop after loading exactly one article
            
        print("[SYNC] All fetched papers already exist in the database. No new articles to load today.")

if __name__ == "__main__":
    # Ensure environment variables are loaded
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    asyncio.run(sync_one_paper())
