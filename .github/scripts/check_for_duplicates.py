import sys
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from github import Github, Auth
from sklearn.metrics.pairwise import cosine_similarity

print("Creating the dataset")

# 1. Fetch Environment Variables & Handle Types
auth = Auth.Token(os.getenv("Token"))
g = Github(auth=auth)

# Convert to integer for proper comparisons
issue_no = int(os.getenv("Issue"))
repo_name = os.getenv("Repo")

repo = g.get_repo(repo_name)
all_issues = repo.get_issues(state="all")

data = {
    'ids': [],
    'issue_text': []
}

for issue in all_issues:
    # Skip Pull Requests
    if issue.pull_request is not None:
        continue

    # Skip the target issue itself so it doesn't match 100% with itself
    if issue.number == issue_no:
        print(f"Skipping target issue #{issue_no}")
        continue

    issue_body = "" if issue.body is None else issue.body
    issue_text = "\n\n".join(part for part in [issue.title, issue_body] if part).strip()

    if not issue_text:
        continue

    data['ids'].append(issue.number)
    data['issue_text'].append(issue_text)

# Handle case where there are no other issues to compare against
if not data['ids']:
    print("No other issues found to compare. Exiting.")
    sys.exit(0)

df = pd.DataFrame.from_dict(data=data)

print("Developed dataset")
print("Calculating embeddings for issue text")

target_issue = repo.get_issue(issue_no)
target_issue_body = "" if not target_issue.body else target_issue.body
target_issue_text = "\n\n".join(part for part in [target_issue.title, target_issue_body] if part).strip()

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

issue_embeddings = model.encode(df['issue_text'].tolist())

print("Done!")

target_embedding = model.encode([target_issue_text])[0]

print("Calculating cosine similarities")

scores = cosine_similarity(target_embedding.reshape(1, -1), issue_embeddings)[0]
df['similarity_score'] = scores
# Use the calculated similarity score directly
df['avg_sim'] = df['similarity_score']

print("Done!")
print("Checking for similar issues")

# Find the row with the maximum similarity
max_sim_idx = df['avg_sim'].idxmax()
max_sim_score = df['avg_sim'].max()
sim_issue_id = df.loc[max_sim_idx, 'ids']

if max_sim_score > 0.85:
    print(f"Duplicate found! Issue #{sim_issue_id} with score {max_sim_score:.2f}")
    target_issue.create_comment(
        f"Found a similar issue #{sim_issue_id} with a similarity score of {max_sim_score:.2f}. Please explain the differences to respective maintainer or collaborator with write access if you feel the bot made a false positive. The issue will be reopened if found genuine"
    )
    target_issue.add_to_labels("duplicate")
    target_issue.add_to_labels("needs-issue-review")
    print(f"Closing {issue_no}")
    target_issue.edit(state="closed")
else:
    print("No duplicates found.")
    sys.exit(0)
