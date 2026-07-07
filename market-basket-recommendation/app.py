import pandas as pd
import streamlit as st
from apyori import apriori

df=pd.read_csv("data.csv")

transactions = []
for i in range(0, 7218):
  transactions.append([str(df.values[i,j]) for j in range(0, 20)])


rules = apriori(
    transactions=transactions,
    min_support=0.005,
    min_confidence=0.1,
    min_lift=3,
    min_length=2,
    max_length=2
)
res=list(rules)


# Define inspect function
def inspect(results):
    product1         = [tuple(result[2][0][0])[0] for result in results]
    product2         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(product1, product2, supports, confidences, lifts))
DataFrame_intelligence = pd.DataFrame(inspect(res), columns = ['product1', 'product2', 'Support', 'Confidence', 'Lift'])
  


# Define get_recommendations function
def get_recommendations(user_item, rules_df, confidence_threshold=0.2, lift_threshold=1.0):
    related_items = []
    for _, row in rules_df.iterrows():
        if user_item == row['product1'] and row['Confidence'] >= confidence_threshold and row['Lift'] >= lift_threshold:
            related_items.append((row['product2'], row['Confidence'], row['Lift']))
        elif user_item == row['product2'] and row['Confidence'] >= confidence_threshold and row['Lift'] >= lift_threshold:
            related_items.append((row['product1'], row['Confidence'], row['Lift']))
    
    if related_items:
        related_items.sort(key=lambda x: (x[1], x[2]), reverse=True)
        top_recommendations = related_items[:3]
        return top_recommendations
    else:
        return []

# Define display_recommendations function
def display_recommendations(user_item):
    recommendations = get_recommendations(user_item, DataFrame_intelligence)

    if recommendations:
        st.write("\nYou may also need:")
        for item, _, _ in recommendations:  # Ignoring confidence and lift values
            st.write(f"{item} - because customers who bought {user_item} also bought {item}.")
    else:
        st.write("No strong recommendations found for the item you entered.")

        new_items = st.text_input(f"What would you like to buy along with {user_item}? (Enter items separated by commas): ",key="new_items").strip().split(',')
        new_items = [item.strip() for item in new_items]
        add_new_association(user_item, new_items)
        # Display recommendations after adding new 
        display_recommendations(user_item)


# Define add_new_association function
def add_new_association(item1, item2):
    global DataFrame_intelligence
    new_row = pd.DataFrame({
        'product1': [item1],
        'product2': [item2],
        'Support': [0.001],  
        'Confidence': [0.5],  
        'Lift': [2.0]  
    })
    DataFrame_intelligence = pd.concat([DataFrame_intelligence, new_row], ignore_index=True)
    st.write(f"New association added: {item1} -> {item2}")

# Main function for Streamlit app
def main():
    st.title("Recommendation System")
    st.write("This is a recommendation system.")

    while True:
        user_item = st.text_input("Enter an item (or type 'exit' to quit): ", key=f"user_item_{st.session_state['iteration_count']}", value='', help='Enter item here')
        if user_item.lower() == 'exit' or not user_item:
            break
        display_recommendations(user_item)
        st.session_state['iteration_count'] += 1

    st.write("Thank you for using the recommendation system!")

if __name__ == "__main__":
    st.session_state['iteration_count'] = 0
    main()


