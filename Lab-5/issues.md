# Lab 5 – Issue Documentation Table

**File:** `election_system.py` · **SRN:** PES2UG25CS820 · **Repo:** L5_62_voting-election-system

Line numbers refer to the **original** file (commit `c6f385e`). Ordered by severity (High → Low).

| # | Issue | Type / Tool | Line(s) | Description | Fix Approach |
|---|-------|-------------|---------|-------------|--------------|
| 1 | Trojan-source bidirectional characters | Security – Bandit B613 (High), Pylint E2502 | 22 | Hidden `U+202E`/`U+2066` bidi characters made `isOfficer` look like it checked for officers, but `role != "voter<hidden>"` returned **True for every role**, so a plain voter was treated as an election officer. | Removed all bidi characters; rewrote as `return role in OFFICER_ROLES` (allow-list `{"officer"}`). |
| 2 | Weak MD5 hash | Security – Bandit B324 (High) | 17 | `hashlib.md5` is cryptographically broken and collision-prone. | Replaced with `hashlib.sha256`. |
| 3 | Unsafe XML parsing (XXE / billion-laughs) | Security – Bandit B319 (Medium), B409 (Low) | 7, 75 | `xml.dom.pulldom.parseString` on untrusted postal-ballot XML is vulnerable to entity-expansion attacks. | Switched to `defusedxml.pulldom`; malicious XML raises `DefusedXmlException`, re-raised as `ValueError`. |
| 4 | Hard-coded admin password | Security – Bandit B105 (Low) | 9 | `ADMIN_PASSWORD = "Election@2026"` leaks a secret in source control. | Read from environment: `os.environ.get("ELECTION_ADMIN_PASSWORD", "")`. |
| 5 | Insecure random for receipts | Security – Bandit B311 (Low) | 72 | `random.randint` is predictable, so receipt numbers can be guessed/forged. | Used `secrets.randbelow(900000) + 100000`. |
| 6 | Bare `except: pass` | Bug – Bandit B110, Pylint W0702, Flake8 E722 | 82–83 | Silently swallows every error (even `KeyboardInterrupt`), hiding real failures. | Removed; catch only `DefusedXmlException` and raise a clear `ValueError` with `from err`. |
| 7 | Late-binding lambda in loop | Bug – Pylint W0640 | 68 | Every lambda captured the same `name`, so `announce()` printed **NOTA** for all three lines. | Replaced with a list comprehension that evaluates each name immediately. |
| 8 | Postal ballots skip validation | Logic bug (manual) | 80 | Postal ballots were appended without checking the voter is registered/hasn't voted or that the candidate is valid. | Added shared `record_vote()` used by both in-person and postal voting. |
| 9 | Double voting & invalid candidates | Logic bug (manual) | 26–34 | `castVote` never checked `voted`, so Ben could vote twice; `"bob"` was stored as a separate candidate. | `record_vote()` rejects voters with `voted=True`; `normalise_candidate()` maps names case-insensitively to the official list. |
| 10 | Off-by-one age and poll-closing checks | Logic bug (manual) | 16, 29 | `age > 18` rejected 18-year-olds; `when.hour > 18` accepted votes at 18:30. | Changed to `age >= MIN_VOTING_AGE` and `when.hour >= POLLS_CLOSE_HOUR`. |
| 11 | Division by zero / wrong turnout & percent | Logic bug (manual) | 52, 56 | `votePercent` and `turnout` crash with no ballots/voters; turnout used ballot count (including invalid ballots) and `//` truncated percentages. | Guarded empty cases, turnout counts voters with `voted=True`, true division rounded to 2 dp. |
| 12 | Unused imports & variables | Quality – Pylint W0611/W0612, Flake8 F401/F841 | 1–4, 32, 45, 55 | `sys`, `json`, `random`, and variables `receipt`, `total`, `now` were unused. | Removed unused imports/variables; `receipt` is now stored on the voter record. |
| 13 | Naming & docstrings | Style – Pylint C0103, C0114, C0116 | 15–86 | camelCase function names and no module/function docstrings. | Renamed to snake_case (`register_voter`, `cast_vote`, …) and added docstrings. |
| 14 | Shadowed global | Quality – Pylint W0621 | 58 | Parameter `ballots` in `countFor` shadowed the global list. | Renamed parameter to `ballot_list`. |
| 15 | PEP 8 formatting | Style – Flake8 E302, E305, E501, W291; Pylint C0301, C0303 | throughout | Missing 2 blank lines between functions, lines > 79 chars, trailing whitespace. | Added blank lines, wrapped long lines, stripped trailing whitespace. |
| 16 | Module-level `main()` call | Style – Flake8 E305 | 104 | Program ran on import. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.33/10 | **10.00/10** |
| Bandit | 7 issues (2 High, 1 Medium, 4 Low) | **0 issues** |
| Flake8 | 30 violations | **0 violations** |

## Commits

1. `13dfc47` – Fix Bandit security issues
2. `0261ffa` – Fix Pylint issues and logic bugs (5.33 -> 10.00/10)
3. `94fe10d` – Fix Flake8 style issues (30 -> 0 violations)
