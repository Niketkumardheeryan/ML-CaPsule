import sys
import os
import numpy as np
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
    'issue_title': [],
    'issue_body': []
}

for issue in all_issues:
    # Skip Pull Requests
    if issue.pull_request is not None:
        continue

    # Skip the target issue itself so it doesn't match 100% with itself
    if issue.number == issue_no:
        print(f"Skipping target issue #{issue_no}")
        continue

    # Append the CURRENT issue's number, not the target issue_no
    data['ids'].append(issue.number)
    data['issue_title'].append(issue.title)
    data['issue_body'].append("" if issue.body is None else issue.body)

# Handle case where there are no other issues to compare against
if not data['ids']:
    print("No other issues found to compare. Exiting.")
    sys.exit(0)

df = pd.DataFrame.from_dict(data=data)

print("Developed dataset")
print("Calculating embeddings for titles and descriptions")

target_issue = repo.get_issue(issue_no)
target_issue_body = "" if not target_issue.body else target_issue.body

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

# Create lists of embeddings (better compatibility with pandas)
df['embed_title'] = list(model.encode(df['issue_title'].tolist()))
df['embed_body'] = list(model.encode(df['issue_body'].tolist()))

print("Done!")

# Generate embeddings for the target issue
target_embeddings = model.encode([target_issue.title, target_issue_body])

print("Calculating cosine similarities")

# Sklearn cosine_similarity expects 2D arrays. We reshape the 1D arrays to (1, -1)
df['sim_title'] = df['embed_title'].apply(
    lambda x: cosine_similarity(target_embeddings[0].reshape(1, -1), x.reshape(1, -1))[0][0]
)
df['sim_body'] = df['embed_body'].apply(
    lambda x: cosine_similarity(target_embeddings[1].reshape(1, -1), x.reshape(1, -1))[0][0]
)

print("Done!")
print("Checking for similar issues")

# Calculate the combined average similarity score
df['avg_sim'] = (0.35*df['sim_title'] + 0.65*df['sim_body'])

# Find the row with the maximum similarity
max_sim_idx = df['avg_sim'].idxmax()
max_sim_score = df['avg_sim'].max()
sim_issue_id = df.loc[max_sim_idx, 'ids']

if max_sim_score > 0.85:
    print(f"Duplicate found! Issue #{sim_issue_id} with score {max_sim_score:.2f}")
    target_issue.create_comment(
        f"Found a similar issue #{sim_issue_id} with a similarity score of {max_sim_score:.2f}. Please explain the differences to respective maintainer or collaborator eith write access if you feel the bot made a false positive. The issue will be reopened if found genuine"
    )
    target_issue.add_to_labels("duplicate")
    target_issue.add_to_labels("needs-issue-review")
    print(f"Closing {issue_no}")
    target_issue.edit(state="closed")
else:
    print("No duplicates found.")
    sys.exit(0)
