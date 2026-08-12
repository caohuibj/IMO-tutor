# Milestones

## v0.4 Retrieval + Redo

Scope is intentionally limited to three user actions:

1. exact problem-note lookup by ID;
2. structured fuzzy retrieval over Google Sheets with `search_text` only as fallback;
3. redo with history isolation before submission and Attempt-to-Attempt progress comparison after finalization.

Google Sheets remains the retrieval store. No vector database or additional persistence layer is introduced.
