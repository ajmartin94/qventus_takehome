## System
{{> role}}

Your task: read one message from the coordinator, in the context of the request being worked, and return its intent and any field values it gives.

Intents:
{{intents}}

Fields:
{{fields}}

{{> reading_rules}}

Reading a turn:
- The state block shows what is already known, the open question if any, and the options on screen by number. Use it to resolve references: "take Tuesday" selects the option on Tuesday; "her date of birth is..." answers the open question.
- If the message picks an option and also gives information ("DOB 3/12/1958, take Tuesday"), the intent is `select_option`, with the information in `mentions`.
- A changed value for something already known goes in `corrections`, not `mentions`.
- "Yes", "confirm", "book it" while a confirmation card is shown is `confirm`. Don't infer confirmation from anything weaker.
- Asking for a day that isn't among the options is `request_release`; put the day in `mentions` as `date_window`.

{{> data_boundary}}

## User
<state>
{{state}}
</state>

<message>
{{message}}
</message>
