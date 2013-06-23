NBHS Voting Site
================

Implements a web-based voting system for SRC/prefect/house captain
elections.

The system is basically finished, it lacks comprehensive testing,
however, and has only been used in production once.

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
- "num_votes" - the maximum number of people a person can vote for.
- "admin_hash" - the sha512 hash of the admin account (which is used
for monitoring vote counts).

Use in Practice
---------------

We've used the system once in practice, and we've noticed socket error
10053 "software caused connection to abort" come up occasionally, for
whatever reason. We think that using a stable version of bottle may
fix the problem.

Something to note is that the bottle server is single-threaded. If
someone has a bad connection, they may take ages to download nominee
photos, and in the meantime, everyone else will be held up. This has
happened in our experience. We may change this soon, but we will have
to swap bottle out for a different microframework, like cherry, which
is multi-threaded, but we will also have to switch to a different DBMS.

Site maintenance which requires the modification of code is currently
not advised during production, since cookies are not stored in the
database. We hope to change this at some point.

All in all, if you want to use it in situations where you have users
in more than one room, you should address these issues first (and
contribute upstream, please).

License
-------

Yet to be decided, will probably be Apache 2.0 or some variant of
GPL. If you want to use it, file an issue, or gain my attention in
whatever way is necessary, but file an issue first.
