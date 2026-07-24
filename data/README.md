# Data

Raw abstract text from Web of Science and Scopus is not redistributed here
due to publisher copyright restrictions.

- Search strings and PRISMA inclusion/exclusion criteria: see `/docs/prisma-protocol.md`
- Derived, non-copyrighted data (tokenized corpus, document-term matrix,
  topic-word distributions, co-occurrence edge list) will be added here as
  the pipeline is finalized.
  
- To reproduce the corpus: rerun the WoS/Scopus queries documented in
  `/docs/prisma-protocol.md` and apply the PRISMA screening criteria listed there.
  
  - A list of DOIs for the 968 included records that have a DOI available
  (968 of 1,027 total; 59 records in the final corpus lack a DOI in the
  original database export) is provided in `included-dois.csv`. Anyone with
  their own database access can use this list to re-fetch the abstracts
  directly, without redistributing this repository's original licensed
  Scopus/WoS export.
