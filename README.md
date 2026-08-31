\# PR Reviewer Bot



An automated code review tool that fetches a GitHub pull request's diff, runs static analysis with flake8, and generates an AI-powered code review using the Anthropic API — then posts it as a comment on the PR. 

*this repo includes a deliberately vulnerable test file used to demonstrate the review bot's detection*



\## How it works

1\. Fetches the diff for a given PR via the GitHub API (PyGithub)

2\. Runs flake8 against the changed file for static analysis

3\. Sends the diff + lint output to Claude with a system prompt specifying review priorities (security, performance, edge cases)

4\. Posts the generated review as a comment on the PR



\## Setup

```bash

pip install -r requirements.txt

```



Create a `.env` file in the project root:

GITHUB\_TOKEN=your\_github\_token

ANTHROPIC\_API\_KEY=your\_anthropic\_key



\## Usage

```bash

python fetch\_pr.py

```

Edit `repo\_name` and `pr\_number` in the `\_\_main\_\_` block to point at the PR you want reviewed.



\## Example output

The bot caught a SQL injection and a command injection vulnerability in a test PR, along with a missing import — see PR #1 in this repo for a live example.



\## Tech stack

Python, PyGithub, Anthropic API, flake8

