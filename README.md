NBHS Voting Site
================

Implements a web-based voting system for SRC/prefect/house captain
elections.

Half-finished currently. The nominations part of the system is basically
perfect and the voting part of the system is completely non-functional,
but work is certainly underway.

Configuration
-------------

- "name" - the name of the election you are holding.
- "prenominate" - whether or not you have an independent system for
nominations (as opposed to letting the system do them for you). This
means that only people marked as nominees can submit statements during
nomination mode.
- "status" - Allows you to change the status of voting ("nominations",
"voting", "closed")
- "nominee_fields" - a list of fields for nomination. (this contains
objects with the properties ("name" (short name of field), "question"
(question asked on nomination form), "text_area" (text appearing in
the text area on the nomination form) and "character_limit" (the
point at which the form will be truncated).
