# Lankford Dual-Domain Web Hub

The Lankford Web Hub is a multi-tenant, dual-domain centralized platform designed to serve the professional and academic web presence for Jeremy Lankford.

The system unifies two distinct portfolios under a single monolithic repository:
1. **Professional Domain (`jeremylankford.com`)** - Showcases professional web development, system architecture, "Today's Software Developer" book, Udemy courses, and professional articles. 
2. **Academic Domain (`jwlankford.com`)** - Focuses on academic publications, research papers, educational resources, and interactive data science notebooks (Jupyter & Google Colab).

## Project Structure

This monorepo is divided into the following core directories:

### 1. Backend (`/backend`)
The backend is a high-performance **FastAPI** application serving as the Dual-Domain Core API. 
* **Database & ORM:** Uses `SQLModel` and `asyncio` to manage highly structured data like Research Papers, Articles, Jupyter Notebooks, and Book Mailing Lists. 
* **Multi-Tenancy:** Employs strict row-level isolation by inheriting from a `TenantBase` model. A custom FastAPI middleware inspects the `Host` or `X-Tenant` headers to automatically partition database access for `professional.localhost` vs `academic.localhost`.
* **Containerization:** Configured with `Dockerfile` and `docker-compose.yml` for isolated dev and prod deployments.

### 2. Professional Frontend (`/frontend-professional`)
The Professional Frontend is a **Vue 3 + TypeScript + Vite** Single Page Application (SPA).
* **UI Components:** Custom components to display Udemy Courses (`UdemyCourses.vue`), Book Outlines (`BookOutline.vue`), computational notebooks (`GoogleNotebookCard.vue`, `JupyterNotebookCard.vue`), and articles.
* **Admin Interface:** Contains authenticated modals (`AdminLoginModal.vue`, `AddArticleModal.vue`, `AddPaperModal.vue`) to allow dynamic CMS-like updates to the portfolio.

### 3. Client Professional (`/client-professional`)
*Reserved for future frontend / client-side components.*

## Setup & Local Development

### Backend
1. Navigate to the `backend/` directory.
2. Install dependencies: `pip install -r requirements.txt`.
3. Ensure the database is running (or will be initialized on startup).
4. Run the development server with Hot Reloading.

### Frontend
1. Navigate to `frontend-professional/`.
2. Install dependencies using `npm install` (or `yarn`).
3. Run the development server: `npm run dev`.
4. The frontend will communicate with the backend at its designated local port (usually mapped via vite / CORS configuration).

## Tech Stack
* **Backend:** Python 3, FastAPI, SQLModel, PostgreSQL / SQLite (managed via update scripts)
* **Frontend:** Vue 3 (Composition API), Vite, TypeScript, CSS 
* **Infrastructure:** Docker, Docker Compose

## Recent Updates (July 2026)
* **Collapsible Taxonomy Filters:** Modified the Research Index view to make the extensive list of topic filters collapsible by default under a new "Filter by Topic" toggle. Active filter states are clearly badge-counted and automatically expand when selecting tags elsewhere in the UI.
* **Secured Author Authentication UI:** Removed references to default credentials (`lankford2026`) from the `AdminLoginModal.vue` helper label and text placeholder.
* **GitHub Pages Custom Domain Persistence:** Added a `CNAME` file to `frontend-professional/public` mapping to `jeremylankford.com` to prevent the deploy action from stripping the custom domain configuration and breaking SSL provisioning on pushes.

