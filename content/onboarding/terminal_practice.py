"""Small standard-library terminal exercise; writes only a learner-owned folder."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "work" / "onboarding"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "run", "check"])
    args = parser.parse_args()
    source = WORK / "request.json"
    result = WORK / "result.json"
    if args.command == "init":
        WORK.mkdir(parents=True, exist_ok=True)
        if source.exists():
            print("Kept existing input:", source)
        else:
            source.write_text(json.dumps({"trip": "Hill walk", "party_size": 0}, indent=2) + "\n")
            print("Created input:", source)
        return
    if not source.exists():
        parser.error("Run init first to create work/onboarding/request.json.")
    try:
        request = json.loads(source.read_text())
    except json.JSONDecodeError as error:
        parser.error("Input is not valid JSON: " + str(error))
    if not isinstance(request, dict):
        parser.error("Input must be a JSON object.")
    if args.command == "run":
        size = request.get("party_size")
        if type(size) is not int:
            parser.error("party_size must be an integer, not a quoted string or boolean.")
        output = {"trip": request.get("trip"), "party_size": size, "water_bottles": size * 2}
        result.write_text(json.dumps(output, indent=2) + "\n")
        print("Read input:", source)
        print("Wrote output:", result)
        return
    if not result.exists():
        parser.error("Run the run command to create result.json before checking.")
    output = json.loads(result.read_text())
    assert output.get("party_size") == request.get("party_size"), (
        "Output is stale: rerun run after editing request.json."
    )
    assert type(output.get("party_size")) is int and output["party_size"] >= 1, (
        "party_size must be an integer of at least 1; inspect request.json, then regenerate result.json."
    )
    assert output["water_bottles"] == output["party_size"] * 2, (
        "Each traveler needs two bottles in this invented exercise."
    )
    print("PASS: regenerated output satisfies the three preparation assertions.")
    print("Verified output:", result)


if __name__ == "__main__":
    main()
