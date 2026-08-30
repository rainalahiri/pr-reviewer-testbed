import os
from github import Github, Auth
import subprocess
import anthropic
from dotenv import load_dotenv

load_dotenv()


def get_pr_diff(repo_name: str, pr_number: int):
    token = os.environ["GITHUB_TOKEN"]
    g = Github(auth=Auth.Token(token))
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    print(f"PR #{pr_number}: {pr.title}")
    print(f"Files changed: {pr.changed_files}")
    print("-" * 40)

    files_data = []
    for f in pr.get_files():
        print(f"\nFile: {f.filename}")
        print(f"Status: {f.status}  (+{f.additions}/-{f.deletions})")
        print(f.patch)  # this is the actual diff text for the file
        files_data.append({"filename": f.filename, "patch": f.patch})

    return files_data

def run_linter(filepath: str) -> str:
    result = subprocess.run(
        ["python", "-m", "flake8", filepath],
        capture_output=True,
        text=True
    )
    return result.stdout or "No lint issues found."

def get_review(diff_text: str, lint_output: str) -> str:
    client = anthropic.Anthropic()

    system_prompt = """You are a senior software engineer reviewing a GitHub pull request.
Review the diff and static analysis output below. Flag:
- Security vulnerabilities
- Performance bottlenecks
- Missing edge case handling
- Code style issues (deprioritize these vs. the above)

Be concise and specific. Reference line numbers/file names where possible.
If the PR looks solid, say so briefly rather than inventing nitpicks."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"## Diff\n{diff_text}\n\n## Linter output\n{lint_output}"}
        ]
    )
    return message.content[0].text

def post_review_comment(repo_name: str, pr_number: int, review_text: str):
    token = os.environ["GITHUB_TOKEN"]
    g = Github(auth=Auth.Token(token))
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(f"## 🤖 AI Code Review\n\n{review_text}")

if __name__ == "__main__":
    repo_name = "rainalahiri/pr-reviewer-testbed"
    pr_number = 1

    files_data = get_pr_diff(repo_name, pr_number)
    lint_output = run_linter("app.py")
    print("\n--- Lint results ---")
    print(lint_output)

    diff_text = "\n".join(f["patch"] for f in files_data)
    print("\n--- AI Review ---")
    review = get_review(diff_text, lint_output)
    print(review)

    post_review_comment(repo_name, pr_number, review)
    print("\n✅ Review posted to PR!")