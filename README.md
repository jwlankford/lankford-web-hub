# Lankford Dual-Domain Web Hub

The Lankford Web Hub is a multi-tenant, dual-domain centralized platform designed to serve the professional and academic web presence for Jeremy Lankford.

The system unifies two distinct portfolios under a single monolithic repository:
1. **Professional Domain (`jeremylankford.com`)** - Showcases professional web development, system architecture, "Today's Software Developer" book, Udemy courses, and professional articles.
2. **Academic Domain (`jwlankford.com`)** - Focuses on academic publications, research papers, educational resources, and interactive data science notebooks (Jupyter & Google Colab).

---

## Directory & File Structure

### 1. Backend (`/backend`)
A high-performance **FastAPI** application serving as the Dual-Domain Core API. It uses `SQLModel` and `asyncio` to manage highly structured data with row-level multi-tenancy isolation.

*   [main.py](file:///d:/lankford-web-hub/backend/main.py): Entry point of the FastAPI application. Sets up CORS, parses incoming headers via middleware to isolate tenant database requests, and defines routing for papers, notebooks, mailing list signups, contact messages, and articles.
*   [models.py](file:///d:/lankford-web-hub/backend/models.py): SQLModel schemas defining database structures for research papers, notebook references, mailing list entries, contact messages, and articles.
*   [database.py](file:///d:/lankford-web-hub/backend/database.py): Handles SQLite and PostgreSQL engines, async sessions, schema creation, and database initialization/seeding.
*   [config.py](file:///d:/lankford-web-hub/backend/config.py): System configurations utilizing `pydantic-settings` to manage environments, credentials, and API endpoints.
*   [sync_adlc_papers.py](file:///d:/lankford-web-hub/backend/sync_adlc_papers.py): Background script running queries against the ArXiv API to fetch and automatically insert the latest papers matching the "Agentic Development Life Cycle (ADLC)" search constraints.
*   [update_db.py](file:///d:/lankford-web-hub/backend/update_db.py): Database maintenance utility script to force database synchronization.
*   [Dockerfile](file:///d:/lankford-web-hub/backend/Dockerfile) & [docker-compose.yml](file:///d:/lankford-web-hub/backend/docker-compose.yml): Set up containerization settings for isolated dev/prod execution environments.
*   [Test.py](file:///d:/lankford-web-hub/backend/Test.py) & [scratch_test.py](file:///d:/lankford-web-hub/backend/scratch_test.py): Local sandbox testing scripts.

### 2. Professional Frontend (`/frontend-professional`)
A **Vue 3 + TypeScript + Vite** Single Page Application (SPA) designed to build dynamically and load content from the API server.

*   `src/components/`:
    *   [AdminLoginModal.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/AdminLoginModal.vue): Security interface allowing administrative mode selection (session storage) without displaying default plain-text credentials in the DOM/UI.
    *   [AddPaperModal.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/AddPaperModal.vue): Panel used by authenticated users to index new research papers.
    *   [AddArticleModal.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/AddArticleModal.vue): Interface used to draft and publish new articles.
    *   [AddNotebookModal.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/AddNotebookModal.vue): Form allowing administrative addition of Jupyter and Google Colab notebooks.
    *   [ResearchPaperCard.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/ResearchPaperCard.vue): Renders paper abstracts, publication dates, external link references, and tags.
    *   [PaperDetailModal.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/PaperDetailModal.vue): Renders expanded academic metadata views.
    *   [ArticleCard.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/ArticleCard.vue) & [ArticleDetailModal.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/ArticleDetailModal.vue): Card previews and full readers for published write-ups.
    *   [GoogleNotebookCard.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/GoogleNotebookCard.vue) & [JupyterNotebookCard.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/JupyterNotebookCard.vue): Render references and live browser integrations/iframes for computational notebooks.
    *   [BookOutline.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/BookOutline.vue): Interactive chapter-by-chapter table of contents view.
    *   [UdemyCourses.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/UdemyCourses.vue): Showcases training curriculum, ratings, lectures, and courses.
    *   [TaxonomyView.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/TaxonomyView.vue): Structured index view of taxonomy tags.
    *   [HeroSection.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/HeroSection.vue) & [AuthorSection.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/AuthorSection.vue): Dynamic landing text, bio, links, and avatar components.
    *   [ContactForm.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/ContactForm.vue) & [MailingListForm.vue](file:///d:/lankford-web-hub/frontend-professional/src/components/MailingListForm.vue): Submits inquiries and newsletter signups to the professional database.
*   `src/services/`:
    *   [api.ts](file:///d:/lankford-web-hub/frontend-professional/src/services/api.ts): Central HTTP client defining endpoints and requests matching FastAPI structures.
*   `src/composables/`:
    *   [useTheme.ts](file:///d:/lankford-web-hub/frontend-professional/src/composables/useTheme.ts): Handles dark mode preferences and state syncing.
*   `src/types/`:
    *   [index.ts](file:///d:/lankford-web-hub/frontend-professional/src/types/index.ts): Frontend model types matching database representations.
*   [App.vue](file:///d:/lankford-web-hub/frontend-professional/src/App.vue): Orchestrator layout organizing navigation tabs, global status messages, and responsive viewport routing.
*   [public/CNAME](file:///d:/lankford-web-hub/frontend-professional/public/CNAME): Force preserves the custom domain setting on GitHub Pages deployments.

### 3. Client Professional (`/client-professional`)
*Reserved for future frontend / client-side components.*

---

## Setup & Local Development

### Backend
1.  Navigate to the `backend/` directory.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Ensure the database is running (or will be initialized on startup).
4.  Run the development server: `uvicorn main:app --reload`.

### Frontend
1.  Navigate to `frontend-professional/`.
2.  Install dependencies using `npm install`.
3.  Run the development server: `npm run dev`.
4.  Build the production bundle: `npm run build`.

---

## Tech Stack & Infrastructure
*   **Backend Hosting:** Render.com (FastAPI application server)
*   **Frontend Hosting:** GitHub Pages (Static hosting for Vue SPA)
*   **Database:** Neon (Serverless PostgreSQL in production) / SQLite (for local development fallback)
*   **Core Languages & Frameworks:** Python 3, FastAPI, SQLModel, Vue 3, Vite, TypeScript
*   **Tooling & Containers:** Docker, Docker Compose, GitHub Actions (CI/CD build-and-deploy workflow)

---

## Recent Updates (July 2026)
*   **Collapsible Taxonomy Filters:** Modified the Research Index view to make the extensive list of topic filters collapsible by default under a new "Filter by Topic" toggle. Active filter states are clearly badge-counted and automatically expand when selecting tags elsewhere in the UI.
*   **Secured Author Authentication UI:** Removed references to default credentials (`lankford2026`) from the `AdminLoginModal.vue` helper label and text placeholder.
*   **GitHub Pages Custom Domain Persistence:** Added a `CNAME` file to `frontend-professional/public` mapping to `jeremylankford.com` to prevent the deploy action from stripping the custom domain configuration and breaking SSL provisioning on pushes.
*   **Persistent Contact Form Database Integration:** Created `ContactMessage` model in backend, added a POST endpoint `/api/v1/contact` to write submissions to the Neon database (or local SQLite), and updated `ContactForm.vue` to dynamically dispatch submissions to the backend API instead of using mock simulations.

