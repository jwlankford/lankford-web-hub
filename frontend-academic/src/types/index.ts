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
}
