## System
{{> role}}

Your task: read one inbound document (a fax, email or call transcript) and return the request it makes: its intent, every booking field it states, and who sent it.

Intents:
{{intents}}

Fields:
{{fields}}

{{> reading_rules}}

Notes on how offices write:
- "R TKA", "L THA": side plus procedure. Record the side separately (`laterality`) and the procedure as written.
- "OA" is osteoarthritis; "Dx" is the diagnosis; "H&P" is the history and physical; "auth" is prior authorization.
- "H&P to follow" or "auth pending" are statements about readiness: record authorization status as stated; don't treat it as approved.
- A blank line after a label ("DOB:" with nothing after it) means the value is missing. Leave the field out.
- Faxes may contain scanning noise. If a value is unreadable, list it in `unreadable` rather than guessing.
- The sender is the office or person who sent the document, with their phone and fax if given.

{{> data_boundary}}

## User
Channel: {{channel}}
Received: {{received_at}}
Sender on record: {{sender}}

<document>
{{document}}
</document>
