import os
import sys
from dotenv import load_dotenv

# Load environment variables before importing database engine
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

import socket
socket.setdefaulttimeout(10)

import asyncio
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import google.generativeai as genai

# Add parent directory to path so database and models can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, init_db
import models

# Try to import scholarly for Google Scholar search
try:
    from scholarly import scholarly
    HAS_SCHOLARLY = True
except ImportError:
    HAS_SCHOLARLY = False


def generate_zotero_key(authors_list, year, title):
    """
    Generates Zotero Reference Key: AUTHOR LAST NAME, YEAR OF ARTICLE, first two words of title.
    Example: GUO_2026_WHY_GIT
    """
    if isinstance(authors_list, str):
        authors = [a.strip() for a in authors_list.split(';') if a.strip()]
    else:
        authors = authors_list
        
    last_name = "Unknown"
    if authors and len(authors) > 0:
        first_author = authors[0].strip()
        # Handle cases like "Lankford, J. W." (comma separation) vs "Frank Guo" (space separation)
        if ',' in first_author:
            last_name = first_author.split(',')[0].strip()
        else:
            last_name = first_author.split(' ')[-1].strip()
            
    # Clean last name to contain only alphanumeric characters
    last_name = "".join(c for c in last_name if c.isalnum())
    
    # Clean title to keep letters, numbers, and spaces
    clean_title = "".join(c if (c.isalnum() or c.isspace()) else "" for c in title)
    words = [w.strip() for w in clean_title.split() if w.strip()]
    first_two_words = words[:2]
    first_two_words_str = "_".join(first_two_words)
    
    # Assemble key: LASTNAME_YEAR_FIRST_SECOND
    key = f"{last_name.upper()}_{year}_{first_two_words_str.upper()}"
    return key


def generate_metadata_via_gemini(title, abstract, api_key):
    """
    Calls Gemini API to analyze paper abstract and extract taxonomy tags, key findings, and methodology.
    """
    if not api_key:
        return None
        
    print("[AI] Enriching paper metadata via Gemini...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
You are an expert academic research assistant specializing in Computer Science, Software Engineering, and AI Agents.
Analyze the following research paper title and abstract. Extract:
1. A list of 3 to 5 highly relevant taxonomy tags/keywords. Keep them concise (1-3 words each).
2. The key findings of the paper (1-2 sentences).
3. The methodology used in the paper (1-2 sentences).

Title: {title}
Abstract: {abstract}

Provide the output strictly in the following JSON format:
{{
  "tags": ["tag1", "tag2", "tag3"],
  "key_findings": "description of key findings",
  "methodology": "description of methodology"
}}
Do not include any other markdown formatting, wrap code blocks, or write conversational text besides the JSON object.
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean JSON block response if wrapped in markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"[AI] Error generating metadata with Gemini: {e}")
        return None


def fetch_google_scholar_papers(query, max_results=5):
    """
    Fetches publications from Google Scholar using the scholarly library.
    """
    if not HAS_SCHOLARLY:
        print("[SCHOLAR] scholarly library not installed. Skipping Google Scholar.")
        return []
        
    print(f"[SCHOLAR] Querying Google Scholar for: '{query}'")
    try:
        search_query = scholarly.search_pubs(query)
        results = []
        for i in range(max_results):
            try:
                pub = next(search_query)
                bib = pub.get('bib', {})
                title = bib.get('title', 'Unknown Title')
                
                # Fetch abstract/snippet from various potential scholarly locations
                abstract = bib.get('abstract') or pub.get('pub_info', {}).get('summary') or bib.get('pub_descr') or 'No abstract available.'
                pub_year = int(bib.get('pub_year')) if bib.get('pub_year') else datetime.now().year
                url = pub.get('pub_url') or pub.get('eprint_url') or ''
                
                # Authors can be a list or a comma-separated string
                authors_data = bib.get('author', [])
                if isinstance(authors_data, str):
                    authors = [a.strip() for a in authors_data.split(' and ') if a.strip()]
                else:
                    authors = [str(a).strip() for a in authors_data]
                
                results.append({
                    'title': title,
                    'summary': abstract,
                    'published': f"{pub_year}-01-01",
                    'url': url,
                    'authors': authors,
                    'journal_or_conf': bib.get('venue') or 'Google Scholar Index'
                })
            except StopIteration:
                break
            except Exception as e:
                print(f"[SCHOLAR] Error parsing result {i}: {e}")
                continue
        print(f"[SCHOLAR] Successfully retrieved {len(results)} candidate papers.")
        return results
    except Exception as e:
        print(f"[SCHOLAR] Exception querying Google Scholar (IP may be temporarily blocked): {e}")
        return []


def fetch_semantic_scholar_papers(query, max_results=10):
    """
    Fallback method: Query Semantic Scholar API (reliable, free, doesn't block GitHub runners).
    """
    print(f"[SEMANTIC_SCHOLAR] Querying Semantic Scholar for: '{query}'")
    try:
        clean_query = query.replace('"', '').replace(' OR ', ' ').replace(' AND ', ' ')
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={clean_query.replace(' ', '+')}&limit={max_results}&fields=title,authors,year,abstract,url,venue"
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"[SEMANTIC_SCHOLAR] Error: Status {response.status_code}")
            return []
            
        data = response.json()
        papers = data.get('data', [])
        results = []
        for paper in papers:
            title = paper.get('title')
            abstract = paper.get('abstract') or 'No abstract available.'
            pub_year = paper.get('year') or datetime.now().year
            paper_url = paper.get('url') or ''
            
            authors_data = paper.get('authors', [])
            authors = [a.get('name') for a in authors_data if a.get('name')]
            
            results.append({
                'title': title,
                'summary': abstract,
                'published': f"{pub_year}-01-01",
                'url': paper_url,
                'authors': authors,
                'journal_or_conf': paper.get('venue') or 'Semantic Scholar Index'
            })
        print(f"[SEMANTIC_SCHOLAR] Successfully fetched {len(results)} candidate papers.")
        return results
    except Exception as e:
        print(f"[SEMANTIC_SCHOLAR] Exception during query: {e}")
        return []


def fetch_arxiv_papers(query, max_results=10):
    """
    Fallback method: Query ArXiv API.
    """
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
            authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
            
            results.append({
                'title': title,
                'summary': summary,
                'published': published,
                'url': paper_url,
                'authors': authors,
                'journal_or_conf': 'arXiv Preprint'
            })
        print(f"[ARXIV] Successfully fetched {len(results)} candidate papers.")
        return results
    except Exception as e:
        print(f"[ARXIV] Exception during fetch: {e}")
        return []


async def sync_one_paper():
    # Run database initialization & sequence resets first
    await init_db()
    query = "all:\"Agentic Development Life Cycle\" OR all:\"ADLC\" OR all:\"Agentic Software Engineering\""
    
    # 1. Fetch papers from Google Scholar
    papers = fetch_google_scholar_papers("\"Agentic Development Life Cycle\" OR \"ADLC\" OR \"Agentic Software Engineering\"", max_results=5)
    
    # If Google Scholar is blocked/fails, fall back to Semantic Scholar
    if not papers:
        print("[SYNC] Falling back to Semantic Scholar...")
        papers = fetch_semantic_scholar_papers("Agentic Software Engineering", max_results=10)
        
    # If Semantic Scholar also fails/returns nothing, fall back to ArXiv
    if not papers:
        print("[SYNC] Falling back to ArXiv...")
        papers = fetch_arxiv_papers(query, max_results=10)
        
    if not papers:
        print("[SYNC] No papers could be retrieved from any source. Exiting.")
        return
        
    # 2. Connect to the Neon DB
    print("[SYNC] Connecting to Neon database...")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    async with AsyncSession(engine) as session:
        for paper in papers:
            title = paper['title']
            url = paper['url']
            
            # Normalize title and check for duplicates in DB
            stmt = select(models.ResearchPaper).where(
                (models.ResearchPaper.title == title) | (models.ResearchPaper.url == url)
            )
            result = await session.execute(stmt)
            existing = result.scalars().first()
            
            if existing:
                print(f"[SYNC] Paper already exists: '{title[:50]}...'. Skipping.")
                continue
                
            # Found a new paper! Process it
            pub_year = int(paper['published'][:4])
            authors_str = "; ".join(paper['authors'])
            
            # Generate Zotero key: LASTNAME_YEAR_FIRST_SECOND
            zotero_key = generate_zotero_key(paper['authors'], pub_year, title)
            
            # Use Gemini to generate tags, findings, and methodology
            ai_tags = []
            findings_text = "Optimizing software development and runtime performance using advanced automation techniques."
            methodology_text = "Empirical research and framework analysis."
            
            if gemini_key:
                ai_data = generate_metadata_via_gemini(title, paper['summary'], gemini_key)
                if ai_data:
                    ai_tags = ai_data.get("tags", [])
                    findings_text = ai_data.get("key_findings", findings_text)
                    methodology_text = ai_data.get("methodology", methodology_text)
            else:
                print("[AI] GEMINI_API_KEY is not set. Using fallback metadata generation.")
                # Basic heuristic fallback tags based on keywords
                lower_title = title.lower()
                if "agent" in lower_title:
                    ai_tags.append("Agentic AI")
                if "software" in lower_title or "code" in lower_title:
                    ai_tags.append("Software Engineering")
                if "lifecycle" in lower_title or "sdlc" in lower_title:
                    ai_tags.append("ADLC")
                if not ai_tags:
                    ai_tags = ["Academic Research", "Systems Engineering"]
            
            new_paper = models.ResearchPaper(
                title=title,
                authors=authors_str,
                publication_year=pub_year,
                abstract=paper['summary'],
                url=url,
                tenant="professional", # Unified portal context
                journal_or_conf=paper['journal_or_conf'],
                zotero_key=zotero_key,
                key_findings=findings_text,
                methodology=methodology_text
            )
            
            session.add(new_paper)
            await session.flush()
            
            # Link tags
            for t_name in ai_tags:
                t_slug = t_name.lower().strip().replace(' ', '-')
                t_slug = "".join(c for c in t_slug if (c.isalnum() or c == '-'))
                
                # Check if tag already exists in database
                tag_stmt = select(models.ResearchTag).where(models.ResearchTag.name == t_name)
                tag_res = await session.execute(tag_stmt)
                db_tag = tag_res.scalars().first()
                
                if not db_tag:
                    db_tag = models.ResearchTag(
                        name=t_name,
                        slug=t_slug,
                        tenant="professional"
                    )
                    session.add(db_tag)
                    await session.flush()
                
                link = models.ResearchPaperTagLink(paper_id=new_paper.id, tag_id=db_tag.id)
                session.add(link)
                
            await session.commit()
            await session.refresh(new_paper)
            
            print(f"[SYNC] SUCCESS: Loaded new paper into Neon database!")
            print(f"       Title: {new_paper.title}")
            print(f"       Authors: {new_paper.authors}")
            print(f"       Year: {new_paper.publication_year}")
            print(f"       Zotero Key: {new_paper.zotero_key}")
            print(f"       Key Findings: {new_paper.key_findings}")
            print(f"       Methodology: {new_paper.methodology}")
            print(f"       Tags: {', '.join(ai_tags)}")
            return # Stop after loading exactly one article
            
        print("[SYNC] All fetched papers already exist in the database. No new articles to load today.")


if __name__ == "__main__":
    asyncio.run(sync_one_paper())
