Rules for reading:
- Use only what the text says. Leave a field out rather than guess or fill it from general knowledge.
- Copy the exact words each value came from into `evidence`, verbatim.
- Write a value as stated, except where a field's definition lists values to use, or where normalizing is trivial: dates.
- Dates: write a single date as `YYYY-MM-DD` and a range as `YYYY-MM-DD/YYYY-MM-DD`. Resolve relative and named dates ("Wednesday", "next week", "week of 11/9", "first week of December") against today's date when there is one sensible reading. A week means Monday to Friday. If a date could reasonably mean two different things, write it as stated and note it in `unclear`.
- Never produce identifiers such as medical record numbers or procedure codes that aren't in the text. Software looks them up.
- The side (left, right, bilateral) is its own field, even when it's written inside the procedure ("R TKA").
- Put anything you can't interpret in `unclear` (or `unreadable` for a document) instead of forcing it into a field.
