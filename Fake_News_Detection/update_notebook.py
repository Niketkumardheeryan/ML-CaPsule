import json

def update_notebook():
    with open('Fake_News_Detection.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            
            # 1. Update data loading
            if 'pd.read_csv("dataset.csv")' in source:
                new_source = [
                    "fake_data = pd.read_csv(\"data/Fake.csv\")\n",
                    "true_data = pd.read_csv(\"data/True.csv\")\n",
                    "\n",
                    "# Add labels: 0 for fake, 1 for true\n",
                    "fake_data[\"label\"] = 0\n",
                    "true_data[\"label\"] = 1\n",
                    "\n",
                    "# Combine datasets\n",
                    "data = pd.concat([fake_data, true_data], ignore_index=True)\n",
                    "\n",
                    "# Shuffle the dataset\n",
                    "data = data.sample(frac=1, random_state=42).reset_index(drop=True)\n",
                    "\n",
                    "data.head()"
                ]
                cell['source'] = new_source
                
            # 2. Update content merging
            elif 'data[\"author\"] + \' \' + data[\"title\"]' in source or 'data["author"] + \' \' + data["title"]' in source:
                new_source = [
                    "# Merging the news title and text to form the input\n",
                    "data['content'] = data[\"title\"] + ' ' + data[\"text\"]"
                ]
                cell['source'] = new_source

            # 3. Update dropping label error
            elif "data.drop(columns = 'label',axis = 1)" in source:
                new_source = [
                    "#To make predictions we will be using the content column as features and labels as targets\n",
                    "#Seperating the data and label\n",
                    "x = data.drop(columns=['label'])\n",
                    "y = data['label']"
                ]
                cell['source'] = new_source

    with open('Fake_News_Detection.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

if __name__ == "__main__":
    update_notebook()
    print("Notebook updated successfully.")
