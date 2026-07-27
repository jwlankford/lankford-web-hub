export interface SignupInput {
  email: string;
  first_name?: string;
}

export interface ResearchTag {
  id?: number;
  name: string;
  slug: string;
}

export interface ResearchPaper {
  id?: number;
  title: string;
  authors: string;
  publication_year: number;
  journal_or_conf?: string;
  abstract?: string;
  key_findings?: string;
  methodology?: string;
  zotero_key?: string;
  url?: string;
  image_url?: string;
  created_at?: string;
  tenant?: string;
  tags?: ResearchTag[];
}

export interface NewResearchPaperInput {
  title: string;
  authors: string;
  publication_year: number;
  journal_or_conf?: string;
  abstract?: string;
  key_findings?: string;
  methodology?: string;
  zotero_key?: string;
  url?: string;
  image_url?: string;
  tags?: string[];
}

export interface Article {
  id?: number;
  title: string;
  summary: string;
  content?: string;
  linkedin_url?: string;
  image_url?: string;
  published_at?: string;
  is_published?: boolean;
  tenant?: string;
}

export interface NewArticleInput {
  title: string;
  summary: string;
  content?: string;
  linkedin_url?: string;
  image_url?: string;
  is_published?: boolean;
}

export interface GoogleNotebook {
  id?: number;
  title: string;
  description: string;
  notebook_url: string;
  audio_url?: string;
  sources_count?: number;
  is_public?: boolean;
  created_at?: string;
  tenant?: string;
}

export interface NewGoogleNotebookInput {
  title: string;
  description: string;
  notebook_url: string;
  audio_url?: string;
  sources_count?: number;
  is_public?: boolean;
}

export interface JupyterNotebook {
  id?: number;
  title: string;
  description: string;
  notebook_url: string;
  tags?: string;
  created_at?: string;
  tenant?: string;
}

export interface NewJupyterNotebookInput {
  title: string;
  description: string;
  notebook_url: string;
  tags?: string;
}


