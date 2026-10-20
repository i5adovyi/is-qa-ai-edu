# Terminal and Python catch-up worksheet

Use this alongside [entry check C](README.md#entry-check-c--use-the-terminal-and-inspect-a-failed-check). All commands below start at the repository root. On Windows use `py -3` instead of `python3` if that is your installed launcher. A path shown by the program is the actual location; do not copy a different learner's absolute path.

## 1 · Locate yourself

Run `python3 --version`. Then run `python3 -c "from pathlib import Path; print(Path.cwd())"`. In that folder you should find `README.md`, `content`, and `lab`. If not, open a terminal from the project folder or use `cd` with your actual folder path.

Write: “My working directory is ____. The command I ran was ____.” A command is the instruction you type; output is what the program prints. A nonzero exit status reports failure even if some reassuring text was printed first.

## 2 · Create and inspect

Run the `init` and `run` commands in entry check C. Open `work/onboarding/request.json` in a text editor. Open `work/onboarding/result.json` separately. Identify one field copied from the input and one field computed by the program.

JSON uses double quotes around keys and strings. A number such as `2` is different from `"2"`. Avoid trailing commas. If a parser reports a line and column, inspect that location before rerunning.

## 3 · Read the failure before changing anything

Run `check`. Find the final `AssertionError` line. Fill in:

```text
What the check required:
What the generated file actually contained:
Which input field might affect that result:
The smallest change I will try:
```

The checker describes the requirement; it does not mean the entire Python installation is broken. Keep the first failure in your log.

## 4 · Predict, edit, regenerate

Choose a valid input value yourself. Before running, predict the resulting `water_bottles` value. Edit your input, run `run`, and then run `check`. Compare your prediction with the output.

Now change the input again but run only `check`. Explain the new failure. Finally regenerate the result. This is a controlled lesson in stale artifacts, not a random troubleshooting exercise.

## 5 · Read the small program

Find `request.get("party_size")`, multiplication by two, and the three assertions in [terminal_practice.py](terminal_practice.py). Explain each in ordinary language. An assertion checks a condition; it does not repair the input.

If functions, dictionaries, or imports remain unfamiliar, read these selected sections of the [official Python tutorial](https://docs.python.org/3/tutorial/): “Using Python as a Calculator,” “Defining Functions,” “Dictionaries,” “Modules,” and “Reading and Writing Files.” Practice one example from each in a disposable folder. There is no requirement to read the whole tutorial before lesson 01.

**Stop condition:** you can reproduce the initial failure, make one valid input change, regenerate output, and explain why the check passes. Continue the concept route while building programming confidence; ask for a small hint rather than copying a finished program.
