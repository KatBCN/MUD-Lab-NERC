# MUD-Lab-NERC
Mining Unstructured Data - Name Entity Recognition

The Baseline folder contains all of the code required to run the program as provided by the professors.

Each experiment folder contains an updated extract-features.py file that includes changes, and the results obtained.

- Exp 1: Added features for token two places before current token.
- Exp 2: Added features for token two places after current token.
- Exp 3: Removed feature from Exp2 that identifies token as second to last place in sentence.
- Exp 4: Added feature for prefix of length 3 to current token
- Exp 5: Added feature for suffix and prefix of length 4 to current token
- Exp 6: Added feature for suffix and prefix of length 5 to current token
- Exp 7: Removed all prefix lengths from current token (kept all suffixes)
- Exp 8: Added back prefix of length 3 to current token (kept all suffixes)
- Exp 9: Added feature if current token is uppercase
- Exp 10: Added feature if current token is titlecase, removed feature if token is uppercase
- Exp 11: Added feature if current token is lowercase, removed feature if token is titlecase
- Exp 12: Included all features related to uppercase, lowercase, titlecase for current token
- Exp 13: Added features related to uppercase and lowercase for two previous tokens
- Exp 14: Added features related to uppercase and lowercase for two next tokens
