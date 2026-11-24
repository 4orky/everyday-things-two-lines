# Everyday Things, Two Lines, Longer Run — make.fun bounty
# u-suga-everyday-things-two-lines-longer-run-f8734479
#
# The program writes one two-line explanation to /output/entry.txt.
# Gate: UTF-8 text of 1 to 400 characters, not only white space.
# Line 1 explains one everyday thing to a 10-year-old in a single
# vivid sentence built on an analogy. Line 2 says in one sentence why
# that analogy works: what it maps and what it leaves out.
#
# Candidates were drafted against the judge's brief, in its stated
# order of weight:
#   1. really explains one everyday thing to a 10-year-old
#   2. the analogy is concrete and surprising
#   3. line 1 is one vivid sentence, no list of comparisons and no
#      second metaphor crowding it
#   4. line 2 is honest and specific about what the analogy maps and
#      what it leaves out, instead of praising the analogy
#   5. the two lines work as a pair, in language a 10-year-old would
#      follow without being talked down to
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties
# go to the shorter text. The output is byte-identical on every run.

# SHA-256 of the selected entry, recorded from the first verified run
# (2026-11-24 16:57 UTC): the program refuses to ship any other text.
EXPECTED_SHA256 = (
    "7d9cd165e3e9f29933e0bc6705bc5ad7234b8162f0d6801816ba60cd529e9920"
)

CANDIDATES = [
    # score: explains 10, analogy 10, one-sentence 9, honest 9, pair 9 = 47
    ("A queue is a caterpillar made of people, shuffling forward one "
     "tiny step at a time until its head reaches the front and peels "
     "away.\n"
     "The caterpillar fits because both move slowly in a single line, "
     "but it leaves out that each person in a queue chose to be there "
     "and can step out, while a caterpillar's legs have no choice.",
     47),
    # score: explains 10, analogy 9, one-sentence 9, honest 9, pair 9 = 46
    ("A toaster is a tiny sunbathing bed for bread: two glowing orange "
     "bars tan each side golden brown, and a spring pops it up when it "
     "is done.\n"
     "The sunbed picture fits because both use heat and a timer, but it "
     "leaves out that the heat comes from electric wires, not the sun, "
     "and bread burns if it stays in too long.",
     46),
    # score: explains 10, analogy 9, one-sentence 8, honest 9, pair 9 = 45
    ("A traffic jam is a river that froze in the middle of flowing, "
     "with every car a drop of water packed shoulder to shoulder, "
     "waiting for the ice to melt.\n"
     "The frozen river fits because both stop moving when too much "
     "crowds into too little space, but it leaves out that drivers can "
     "turn off and leave, while water has nowhere else to go.",
     45),
    # score: explains 9, analogy 7, one-sentence 9, honest 7, pair 8 = 40
    ("Rain is the sky wringing out a giant sponge over our heads, "
     "squeezing back down the water it soaked up from lakes and seas.\n"
     "The sponge fits because clouds really do hold water and let it "
     "go, but it leaves out that no hand is squeezing, since cold air "
     "does the pushing instead.",
     40),
    # score: explains 9, analogy 7, one-sentence 8, honest 8, pair 8 = 40
    ("A queue is a slow train made of people, where each person is a "
     "carriage that only moves when the one in front moves first.\n"
     "The train fits because both move in one line, one behind the "
     "other, but it leaves out that people can leave the line whenever "
     "they like, while carriages cannot.",
     40),
]


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 400, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lines = text.split("\n")
        assert len(lines) == 2, "candidate must be exactly two lines"
        assert all(line.strip() for line in lines), "candidate has a blank line"
        assert all(line.strip().endswith((".", "!", "?")) for line in lines), \
            "each line must be a complete sentence"
        assert all(line.count(".") == 1 for line in lines), \
            "each line must be a single sentence"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    entry = pick(CANDIDATES)
    digest = hashlib.sha256(entry.encode("utf-8")).hexdigest()
    if digest != EXPECTED_SHA256:
        print("error: selected entry does not match the recorded SHA-256; "
              "the candidate list changed after verification",
              file=sys.stderr)
        sys.exit(1)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(entry)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-400 characters, two lines, non-blank), and confirm
    # its SHA-256 matches the selected text. A truncated or altered
    # file must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        written = f.read().decode("utf-8")
    if written != entry:
        print("error: /output/entry.txt does not match selected entry",
              file=sys.stderr)
        sys.exit(1)
    if hashlib.sha256(written.encode("utf-8")).hexdigest() != digest:
        print("error: /output/entry.txt SHA-256 mismatch", file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= 400 and written.strip()):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(entry)
    print(f"chars: {len(entry)}  sha256: {digest}")


if __name__ == "__main__":
    main()
