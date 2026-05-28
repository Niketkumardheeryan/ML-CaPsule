import pandas as pd

# Load dataset
df = pd.read_csv("/content/Rick-n-Morty.csv")

# Keep needed columns
df = df[['speaker', 'dialouge']]

# Remove empty rows
df.dropna(inplace=True)
df = df.head(1000)

# Reset index
df.reset_index(drop=True, inplace=True)

# Store conversations
conversations = []

# Create conversation pairs
for i in range(len(df)-1):

    current_speaker = df.iloc[i]['speaker']
    current_dialouge = df.iloc[i]['dialouge']

    next_speaker = df.iloc[i+1]['speaker']
    next_dialouge = df.iloc[i+1]['dialouge']

    text = (
        f"{current_speaker}: {current_dialouge}\n"
        f"{next_speaker}: {next_dialouge}"
    )

    conversations.append(text)

# Save processed text
with open("/content/processed.txt", "w", encoding="utf-8") as f:
    for convo in conversations:
        f.write(convo + "\n\n")

print("Dataset preprocessing complete!")