# Lab 5 – Reflection

**Q1. Which tool caught the most serious problem in election_system.py, and why was it hard to see by reading the code?**

Bandit (B613) and Pylint (E2502) both flagged line 22 for bidirectional control characters. In the editor, isOfficer looked like a normal check with a comment saying only election officers pass. The hidden characters were actually inside the string, so the role was compared with "voter" plus invisible text, the two never matched, and every role came back as an officer. Anyone reviewing the file would have approved it. Printing the line with repr() exposes the \u202e and \u2066 codes. I replaced it with a check against an allow-list, OFFICER_ROLES = {"officer"}.

**Q2. Which bugs did none of the tools detect, and how did you find them?**

The tools check how code is written, not what an election is supposed to do, so every rule-breaking result got past them. Running the original program showed six: Asha, aged 18, could not register because the check was age > 18; Ben voted twice and both votes counted; 'bob' and 'Bob' were tallied as different candidates; Dia's vote at 18:30 was accepted after the polls closed; turnout was 166.67% because it divided ballots by voters; and Alice was declared winner in a 2-2 tie with Bob. I found each one by comparing a printed line with the voting rules, then fixed them with a shared record_vote() function and corrected comparisons.

**Q3. Did any warning seem wrong, or rated at the wrong severity for this program?**

Some ratings did not match the real damage here. Bandit marked MD5 as High, but in this file the hash only labels a voter record and protects nothing. The hardcoded ADMIN_PASSWORD was only Low, although anyone who can open the repo gets the admin password. The try/except/pass was also Low, yet it was silently hiding failed postal ballot imports. On the Pylint side, missing docstrings and camelCase names pulled the score down the most but changed no behaviour. So I fixed issues in order of actual impact, not by the label each tool gave them.

**Q4. What would you do differently in your next project after this lab?**

I would run the tools from the first commit instead of at the end. Most of the 30 Flake8 warnings were blank lines, long lines and trailing spaces that an auto-formatter such as black fixes on save. A pre-commit hook that blocks Bandit Medium and High findings would have stopped MD5, unsafe XML and the hidden characters from ever being committed, and a GitHub Actions job could run all three tools on every push. Since the logic bugs passed every tool, I would also write small tests for rules like "one vote per voter" and "no votes after 18:00". A clean Pylint score does not prove the election result is correct.
