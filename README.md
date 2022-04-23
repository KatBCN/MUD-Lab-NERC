# MUD-Lab-NERC
Mining Unstructured Data - Name Entity Recognition

The Baseline folder contains all of the code required to run the program as provided by the professors.

Each experiment folder contains an updated extract-features.py file that includes changes, and the results obtained.

- Exp 1: Added features for token two places before current token.
- Exp 2: Added features for token two places after current token.
- Exp 3: No change to previous experiment after correcting coding errors in Experiments 1 & 2
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
- Exp 15: Added feature to indicate if not all the characters in the current token are letters, removed features related to case for next tokens
- Exp 16: Added features to indicate if not all the characters in the previous two and next two tokens are letters.
- Exp 17: Added drug bank dictionary to main program and feature to indicate token's value in drug bank
- Exp 18: Modified drug bank dictionary to be in lowercase
- Exp 19: Added list of words provided in HSDB.txt and feature to indicate token's presence in the list
- Exp 20: Modified the HSDB list to be a set of tokenized words from the HSDB.txt
- Exp 21: Added feature to indicate previous token's drug bank dictionary value
- Exp 22: Reset experiment to baseline and added feature to indicate current token's value in drug bank in order to compare results
- Exp 23: Reset experiment to baseline and added feature to indicate current token's length in order to compare results
- Exp 24: Added feature for current token's length to Exp21 - this experiment has the most features: CRF M.avg=74.4
- Exp 25: Removed features related to the token two places after the current token: CRF M.avg=75.1
- Exp 26: Removed features related to uppercase, lowercase, and letters of token two places before current token: CRF M.avg=75
- Exp 27: Removed all features related to token two places before current token: CRF M.avg=74.8
- Exp 28: Removed all features related to case and dictionary of previous token, removed feature related to letters of next token, M.avg=75