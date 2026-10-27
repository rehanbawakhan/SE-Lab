"""Voting and election management system.

Registers voters, checks election officers, casts votes before the polls
close, tallies ballots, picks a winner, reports percentages and turnout,
announces results, issues receipts and imports postal ballots from XML.
"""
import os
import secrets
import hashlib
from datetime import datetime
from defusedxml import pulldom, DefusedXmlException

ADMIN_PASSWORD = os.environ.get("ELECTION_ADMIN_PASSWORD", "")
POLLS_CLOSE_HOUR = 18
MIN_VOTING_AGE = 18
START_ELEMENT = "START_ELEMENT"  # same value as xml.dom.pulldom.START_ELEMENT
OFFICER_ROLES = {"officer"}
voters = {}
ballots = []
candidates = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id, name, age):
    """Register a voter if they are at least MIN_VOTING_AGE years old."""
    if age >= MIN_VOTING_AGE:
        voters[voter_id] = {
            "name": name,
            "hash": hashlib.sha256(voter_id.encode()).hexdigest(),
            "voted": False,
            "receipt": None,
        }
        return True
    return False


def is_officer(role):
    """Return True only for election-officer roles."""
    return role in OFFICER_ROLES


def normalise_candidate(candidate):
    """Map a candidate name to its official spelling, or None if unknown."""
    for official in candidates:
        if official.lower() == str(candidate).strip().lower():
            return official
    return None


def record_vote(voter_id, candidate):
    """Validate and store one ballot. Returns the receipt or None."""
    official = normalise_candidate(candidate)
    if voter_id not in voters or voters[voter_id]["voted"] or official is None:
        return None
    ballots.append(official)
    receipt = receipt_number()
    voters[voter_id]["voted"] = True
    voters[voter_id]["receipt"] = receipt
    return receipt


def cast_vote(voter_id, candidate, when):
    """Cast an in-person vote; polls close at POLLS_CLOSE_HOUR:00."""
    if when.hour >= POLLS_CLOSE_HOUR:
        return False
    return record_vote(voter_id, candidate) is not None


def tally():
    """Return a dict of candidate -> vote count (every candidate listed)."""
    counts = {name: 0 for name in candidates}
    for ballot in ballots:
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts


def winner():
    """Return the winning candidate, a tie message, or None if no votes."""
    counts = tally()
    if not ballots:
        return None
    top = max(counts.values())
    leaders = [name for name, votes in counts.items() if votes == top]
    if len(leaders) > 1:
        return "Tie: " + ", ".join(leaders)
    return leaders[0]


def vote_percent(name):
    """Return the candidate's share of ballots as a percentage."""
    if not ballots:
        return 0.0
    return round(count_for(name, ballots) * 100 / len(ballots), 2)


def turnout():
    """Return the percentage of registered voters who voted."""
    if not voters:
        return 0.0
    voted = sum(1 for voter in voters.values() if voter["voted"])
    return round(voted / len(voters) * 100, 2)


def count_for(candidate, ballot_list):
    """Count how many ballots in ballot_list are for candidate."""
    total = 0
    for ballot in ballot_list:
        if ballot == candidate:
            total += 1
    return total


def announce():
    """Return one result line per candidate."""
    counts = tally()
    return [name + ": " + str(counts[name]) for name in candidates]


def receipt_number():
    """Return an unpredictable receipt number."""
    return "RCPT-" + str(secrets.randbelow(900000) + 100000)


def import_postal_ballots(xml_text):
    """Import postal ballots from XML; each must name a registered voter."""
    imported = 0
    try:
        events = pulldom.parseString(xml_text)
        for event, node in events:
            if event == START_ELEMENT and node.tagName == "ballot":
                voter_id = node.getAttribute("voter")
                if record_vote(voter_id, node.getAttribute("candidate")):
                    imported += 1
    except DefusedXmlException as err:
        raise ValueError("Unsafe postal ballot XML: " + str(err)) from err
    return imported


def main():
    """Run a demo election."""
    print("Register Asha (age 18):", register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    day = datetime(2026, 11, 20)
    print("Ben votes Alice:",
          cast_vote("V2", "Alice", day.replace(hour=10)))
    print("Ben votes Alice again:",
          cast_vote("V2", "Alice", day.replace(hour=11)))
    print("Chen votes 'bob':",
          cast_vote("V3", "bob", day.replace(hour=12)))
    print("Dia votes Bob at 18:30:",
          cast_vote("V4", "Bob", day.replace(hour=18, minute=30)))
    postal_xml = "<postal><ballot voter='V1' candidate='Bob'/></postal>"
    print("Postal ballots imported:", import_postal_ballots(postal_xml))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
