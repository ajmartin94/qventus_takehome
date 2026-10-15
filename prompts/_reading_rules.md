Rules for reading:
- Use only what the text says. Leave a field out rather than guess or fill it from general knowledge.
- Copy the exact words each value came from into `evidence`, verbatim.
- Write a value as stated. Normalize only when it is trivial and unambiguous: a date to ISO `YYYY-MM-DD`, a date range or "week of" to `YYYY-MM-DD/YYYY-MM-DD` (Monday to Friday for a week).
- Never produce identifiers such as medical record numbers or procedure codes that aren't in the text. Software looks them up.
- The side (left, right, bilateral) is its own field, even when it's written inside the procedure ("R TKA").
- Put anything you can't interpret in `unclear` (or `unreadable` for a document) instead of forcing it into a field.
