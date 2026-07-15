
# ── Standard Library ──────────────────────────────────────────────────────────
import re
import string
import warnings

# ── Data Manipulation ─────────────────────────────────────────────────────────
import numpy as np
import pandas as pd

# ── Visualization ─────────────────────────────────────────────────────────────
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── NLP ───────────────────────────────────────────────────────────────────────
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ── Machine Learning ──────────────────────────────────────────────────────────
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

# ── Settings ──────────────────────────────────────────────────────────────────
warnings.filterwarnings('ignore')        # Suppress harmless warnings
np.random.seed(42)                       # Reproducibility

# Download required NLTK data (runs silently if already downloaded)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

print('✅ All libraries imported successfully!')


def create_sample_dataset():
    """
    Creates a balanced sample Amazon product review dataset.
    Returns a DataFrame with 'reviewText' and 'overall' columns.
    """
    # ── Positive Reviews (4–5 stars) ──────────────────────────────────────────
    positive_reviews = [
        "This product exceeded all my expectations. Absolutely love it!",
        "Amazing quality, fast shipping. Highly recommend to everyone!",
        "Best purchase I have made this year. Worth every penny.",
        "Fantastic product, works exactly as described. Very happy!",
        "Excellent build quality and great value for money.",
        "I am extremely satisfied with this product. It is perfect.",
        "Outstanding performance and beautiful design. Love it!",
        "Super happy with this purchase. Works perfectly right out of the box.",
        "Great product, great price. Arrived on time. Five stars!",
        "This is exactly what I was looking for. Excellent quality!",
        "Incredible product, surpassed all expectations. Would buy again!",
        "Very well made, durable and elegant. Perfect gift idea.",
        "Top notch quality, customer service was wonderful too. Highly recommend.",
        "This product is simply amazing. It changed my daily routine for the better.",
        "Easy to use, high quality materials, and looks great. No complaints!",
        "Phenomenal product at an affordable price. Very satisfied with my purchase.",
        "Arrived quickly and works beautifully. Would definitely purchase again.",
        "I have been using this for a month and it is holding up great!",
        "The quality is far better than I anticipated at this price point.",
        "Wonderful product! Easy to set up and works like a charm.",
        "This is a gem of a product. It does exactly what it promises.",
        "Super impressed with the build quality and attention to detail.",
        "Bought as a gift and the recipient absolutely loved it!",
        "Everything about this product is top tier. Packaging, quality, performance.",
        "Five stars without hesitation. I am completely blown away.",
        "Works flawlessly. So glad I chose this over the alternatives.",
        "Exceeded expectations in every possible way. True value for money.",
        "Hands down the best product in this category. A must buy!",
        "Gorgeous design, solid build. My whole family loves it!",
        "Delivery was fast and the product quality is beyond impressive.",
        "Absolutely perfect for my needs. Could not be happier with this purchase.",
        "I read hundreds of reviews before buying and they were all right. This is great!",
        "The product photos do not do it justice. It looks even better in person.",
        "Customer support was helpful and the product itself is amazing.",
        "This made my life so much easier. Totally worth the investment.",
        "Just as advertised! Great quality and very easy to use.",
        "I love this product so much I bought a second one as a gift.",
        "Well-packaged, arrived on time, and works better than expected.",
        "The performance of this product is remarkable for the price.",
        "I was skeptical at first but this has become one of my favorite purchases.",
        "No issues whatsoever. Everything works as it should. Very pleased.",
        "An absolute bargain for the quality you get. Strongly recommend!",
        "This product is genuinely impressive. I keep recommending it to friends.",
        "Sturdy, reliable, and user-friendly. Exactly what I needed.",
        "Clean, elegant, and functional. The perfect combination!",
        "Would rate it 6 stars if I could. An exceptional product!",
        "So easy to use even my grandparents figured it out immediately.",
        "Great packaging, arrived in perfect condition, fantastic quality.",
        "Product quality is exceptional and it works perfectly. Very happy!",
        "This is exactly what every customer review said. Just fantastic!",
        "I have tried many similar products and this is hands down the best.",
        "Setup was a breeze and the results are impressive. Totally satisfied!",
        "The product works as advertised. Solid build. Highly satisfied.",
        "Such a high quality product at a very reasonable price point.",
        "Very happy with my purchase. Will definitely buy from this brand again.",
        "Works better than the more expensive alternatives I have tried.",
        "Delivery on time, packaging excellent, and the product itself is superb!",
        "Clean design, great functionality. My whole team loves using it.",
        "Reliable and efficient. Has not let me down even once.",
        "One of the best investments I have made. Highly recommended!",
        "Stellar product in every dimension. I am completely satisfied!",
        "Wonderful! Works exactly as described and looks great too!",
        "Exceptional quality and rapid delivery. Exceeded my expectations entirely.",
        "I cannot say enough good things about this product. It is simply superb.",
        "Perfect size, perfect quality, and arrived perfectly packaged.",
        "This product really delivers on its promise. Truly impressed.",
        "Love everything about this product. Already recommended to 5 friends!",
        "Works great, looks great. Could not ask for more at this price.",
        "Very durable and well-crafted. Will last for years.",
        "Outstanding customer experience from order to delivery. Product is top notch.",
        "Simple to use and very effective. Saved me a lot of time.",
        "Beautifully designed and extremely functional. Rare combination!",
        "I was amazed at how well this product works. Top quality!",
        "Works exactly as described, maybe even better. Very impressed!",
        "Great for everyday use. Lightweight yet durable. Very happy!",
        "Could not be happier with this product. Everything about it is great!",
        "Very satisfied with the purchase. The quality is outstanding for the price.",
        "This product is everything I needed and more. Absolutely love it!",
        "Premium feel and performance. You get a lot of value for the price.",
        "Easy to set up, intuitive to use, and works perfectly. Great buy!",
        "The construction quality is superb. Feels like it will last forever.",
        "Unbelievably good quality for the price. I am very impressed.",
        "Does what it promises and does it well. No complaints at all!",
        "Brilliant product with no flaws. Highly recommend to anyone looking.",
        "This is a quality product through and through. Completely satisfied!",
        "Happy beyond words. This product has made such a difference in my life.",
        "Simply excellent. The product quality speaks for itself.",
        "Well worth the money. Performs above expectations on all counts.",
        "Incredible value. I would buy this again without hesitation.",
        "So glad I found this product. Exactly what I was looking for!",
        "My expectations were already high and this product still exceeded them.",
        "Works beautifully and looks great. The perfect purchase decision.",
        "Amazing product with zero flaws. Shipping was fast too. Five stars!",
        "Best quality I have seen at this price range. Highly impressed!",
        "I am thrilled with this product. It does everything it claims and more!",
        "Solid product, great customer service, and delivered ahead of schedule!",
        "This product makes my day easier every single day. So thankful I bought it.",
        "Top quality and very reliable. I am truly impressed by this purchase.",
        "Excellent craftsmanship and attention to detail. Very happy customer!",
        "Just what I was looking for! Excellent quality and super fast delivery.",
        "Absolutely brilliant! Does exactly what it says. Would buy again!",
        "Very happy with this product. It is exactly as described and works great.",
        "The quality and performance of this product surprised me in the best way.",
        "Product is exactly as shown and works better than expected. Five stars!",
        "Phenomenal quality at a fair price. Cannot ask for anything more.",
        "Runs flawlessly. I love it! Would recommend to family and friends.",
        "Great product backed by excellent customer service. Very happy overall.",
        "Impressively well-made and the performance matches the price perfectly.",
        "Such an amazing product. It does exactly what it says it will do.",
        "Well constructed, easy to use, and genuinely helpful. Love it!",
        "This product is a real winner. Excellent in every single way.",
        "Happy with every aspect of this purchase. Quality, delivery, and support.",
        "Smooth, efficient, and well-designed. I am beyond satisfied!",
        "Absolutely love this product. Works like a dream every single time.",
        "This was a perfect purchase decision. Would recommend it to everyone!",
        "High quality and very durable. Cannot ask for a better product.",
        "Exceeded all my expectations. I could not be happier with this product!",
        "Works exactly as advertised. The perfect addition to my collection!",
        "Very high quality product that performs exactly as described. Highly satisfied.",
        "I am completely blown away by the quality of this product. Five stars!",
        "Product quality is first class. Works perfectly and looks stunning.",
        "Simply the best product in its category. Highly recommend buying it!",
        "Very happy with this. Excellent quality and great performance overall.",
        "So pleased with this purchase. Exactly what I needed and then some!",
        "No complaints whatsoever. This product is truly excellent in every way.",
        "Works perfectly and arrived quickly. Excellent all around product!",
        "This product is a delight to use every day. Highly recommended!",
        "Premium quality and very effective. Well worth every penny I spent.",
        "Impressed by the quality and very satisfied with my purchase overall.",
        "This product lives up to the hype. Simply fantastic. Five stars!",
        "Perfect product for my needs. Great value and excellent quality.",
        "This is a top quality product and I am very pleased with my purchase.",
        "Received in perfect condition and works flawlessly. Very happy!",
        "I love how well this product works. It is absolutely fantastic!",
        "Quality is unmatched for the price. An excellent buy through and through.",
        "Works like a champ. Fast delivery and excellent packaging. Five stars!",
        "This product is superb. I am very impressed by its quality and performance.",
        "Loved it from the moment I opened the package. Simply the best!",
        "Perfect in every way. Would give it more than five stars if I could!",
        "An exceptional product that delivers on every single promise made.",
        "Extremely satisfied. This product is everything the description says it is.",
        "High quality, easy to use, and very effective. Five stars without doubt!",
        "I cannot recommend this product highly enough. Truly outstanding.",
        "Best product I have purchased in a long time. Absolutely love it!",
        "Works great and looks amazing. This is genuinely a perfect product.",
        "Stellar quality, fast delivery, and great value. Highly recommended!",
        "Very durable and effective. I am very happy I chose this product.",
        "Great experience from start to finish. Love this product so much!",
        "Totally impressed with the quality. A fantastic product overall!",
        "This product has made my life so much more convenient. Thank you!",
        "Quality and performance are excellent. I could not be more satisfied!",
        "Extremely pleased with this product. Worth every single penny I paid.",
        "This product is a winner! Excellent quality and superb performance.",
        "Brilliantly designed and a joy to use. I am thrilled with this purchase!",
        "Durable, stylish, and highly effective. An absolutely excellent buy."
    ]

    # ── Neutral Reviews (3 stars) ─────────────────────────────────────────────
    neutral_reviews = [
        "It is okay, not great, not terrible. Does the job.",
        "Average quality. Nothing special but works as expected.",
        "Decent product for the price. Nothing really stands out.",
        "It works fine, but I expected better based on the description.",
        "Middle of the road. Gets the job done but won't wow you.",
        "Acceptable quality, but I have seen better. Average experience.",
        "The product is fine. Not amazing, but not disappointing either.",
        "Somewhat useful. Not the best, but not the worst either.",
        "Average product with average performance. No strong feelings.",
        "Does what it should, nothing more. A mediocre experience overall.",
        "Moderate quality for the price point. Neither impressed nor upset.",
        "It is acceptable. Not exactly what I wanted but it works okay.",
        "I have mixed feelings about this product. Some good, some bad.",
        "Works as described but is not particularly impressive in any way.",
        "Reasonable quality but I expected a bit more for the money.",
        "Neither here nor there. A functional product with no wow factor.",
        "It gets three stars from me. Not bad but not great either.",
        "Just okay. I would neither strongly recommend nor discourage it.",
        "This product is average. Good enough to use but nothing special.",
        "Reasonable purchase, but there is room for improvement.",
        "Not bad. It does what it claims but it is not exciting.",
        "Mediocre product. Serviceable but unremarkable in every way.",
        "Works, but just barely meets my expectations. Average experience.",
        "Fair product at a fair price. You get exactly what you pay for.",
        "The product functions correctly but lacks the quality I hoped for.",
        "So-so. This product is definitely not the best but it is usable.",
        "Three stars feels right. Not disappointed but not thrilled either.",
        "Works adequately. There are better options but also worse ones.",
        "A typical product in this price range. Nothing to get excited about.",
        "Mixed bag. Has some nice features but let down in other areas.",
        "This is an average product. Has some good aspects and some bad.",
        "Not sure how I feel about this. Some days it seems great, others less so.",
        "Works as advertised. Nothing more, nothing less. Average all around.",
        "Satisfactory product. Does what it needs to do without standing out.",
        "It functions well enough but there is definitely room for improvement.",
        "A middle-of-the-pack product. It works but does not impress.",
        "Reasonable quality but I have had better experiences with similar products.",
        "Somewhat satisfied. The product works but does not exceed expectations.",
        "The quality is fair. You get what you pay for with this product.",
        "Average quality product that fulfills its basic purpose. That is all.",
        "Not impressed, but not disappointed either. Pretty much what I expected.",
        "This product is fine, I guess. It does the job but nothing noteworthy.",
        "Okay product. Not the worst I have seen but definitely not the best.",
        "Slightly above average. Some features are good, others are lacking.",
        "I feel indifferent about this product. It is neither great nor terrible.",
        "Expected better but it will do. An unremarkable, average product overall.",
        "It gets the job done but barely. Not sure if I would purchase again.",
        "It is usable but feels generic and lacks any standout qualities.",
        "Three out of five is fair. A middle-ground product without any real highlights.",
        "Works fine on most days. Has some limitations but nothing deal-breaking.",
        "The product is functional. Not great, just functional. Fair enough.",
        "Does not disappoint but does not impress either. A standard product.",
        "This product meets the bare minimum requirements. Just adequate.",
        "Not exactly what I was hoping for but it will serve its purpose.",
        "Perfectly average product. Nothing remarkable about it at all.",
        "Somewhat useful but the novelty wore off quickly. Average rating.",
        "It is okay. I would not buy again but I would not return it either.",
        "Performance is acceptable. Could be better but it is also not terrible.",
        "Good enough to get by with. But there are probably better options.",
        "A standard purchase with no real highs or lows. Average all round.",
        "Neither love it nor hate it. It works and that is enough I suppose.",
        "Works about 80% of the time. Not perfect but not a disaster.",
        "The packaging was nice but the product itself is pretty average.",
        "I have used better products before. This one is mediocre by comparison.",
        "Decent enough product. I am not unhappy but not particularly pleased.",
        "Mixed feelings here. The product has potential but does not deliver fully.",
        "An uninspiring product that gets the job done without any flair.",
        "The product is fine. Nothing wrong with it, but nothing special either.",
        "Three stars because it works but does not deliver on its promise.",
        "Not outstanding but not bad either. Right in the middle of the road.",
        "It serves its purpose. Would not rave about it but would not complain much.",
        "Average product at an average price. Nothing particularly noteworthy.",
        "This product is just okay. Works as expected but does not stand out.",
        "It could be better but at this price I suppose it is acceptable.",
        "Not bad but not good. Kind of in the middle. Unremarkable overall.",
        "I am on the fence about this product. Has pros and cons.",
        "Meets basic requirements. Does not impress but does not frustrate.",
        "Average performance and average build quality. Nothing to write home about.",
        "The product does its job but lacks the polish I expected.",
        "I do not love it and I do not hate it. A very average experience.",
        "Does what it claims but just barely. Three stars seems right.",
        "Not a bad product but not good enough to buy again. Very average.",
        "It works most of the time. Some minor issues but generally functional.",
        "Three stars for a product that is perfectly average in every way.",
        "I am kind of neutral on this. It works but it is not exciting.",
        "Solid product but nothing exciting. Does what it needs to do.",
        "Works as described. Not exceptional but not problematic either.",
        "Acceptable purchase for the price but lacks that wow factor.",
        "Okay product. Not the best option but is not the worst either.",
        "Pretty average in all aspects. Gets the job done at least.",
        "Not particularly impressed but also not bothered. Average product.",
        "I expected more but at least the product is functional. Just okay.",
        "The product delivers an average performance. Nothing really stands out.",
        "It does the job. I feel somewhat neutral about this overall purchase.",
        "Very average, very unremarkable. A three-star product through and through.",
        "Some features work well, some do not. Overall a mixed but average experience.",
        "Average in every way. Just an okay product that does its basic job.",
        "It is usable. I would call it just acceptable for the money spent.",
        "Works alright for the most part. Not something I would enthusiastically recommend.",
        "A fine product if you are not looking for anything special.",
        "This product does what it is supposed to. Nothing less, nothing more.",
        "Three stars. Not thrilled but not disappointed. Just neutral overall.",
        "The quality is about what you would expect at this price. Just average.",
        "Okay experience overall. Works adequately but has room to grow.",
        "An average product that performs averagely. Nothing to get excited about.",
        "The product is functional but not exceptional in any meaningful way.",
        "I am not unhappy, but not particularly satisfied either. Average rating.",
        "It performs adequately. Not groundbreaking but also not useless.",
        "Three stars seems fair. Some good points, some bad, averages out.",
        "I think it is an okay product. Does the job without any drama.",
        "This is a take-it-or-leave-it product. Works, but nothing special.",
        "Pretty standard product, nothing to get excited about. Average all around.",
        "Fair quality. You get a product that does its job without excelling.",
        "I see both positives and negatives in equal measure. Average overall.",
        "Works adequately for everyday use. Not remarkable but not a failure.",
        "This product is fine for what it is. Not great, not bad. Just okay.",
        "Average quality, average performance, average everything. Three stars.",
        "Does exactly what it says. I just expected a slightly higher quality.",
        "Neutral feelings about this product. It functions but lacks distinction.",
        "Satisfactory performance, nothing special. Exactly what average looks like.",
        "It works, so I cannot complain much. But it does not exceed expectations.",
        "The product is average. I give it three stars because it is not bad.",
        "Somewhat satisfied. The product works but there is definitely room for more.",
        "Nothing to rave about. A perfectly average product at an average price.",
        "The product is a bit underwhelming but functional enough for basic use.",
        "A mediocre product that meets my needs but does not stand out at all.",
        "Three stars. This product delivers acceptable performance nothing more.",
        "Very average. Works as expected but nothing exceptional about it.",
        "I find this product to be simply average. Not impressive, not terrible.",
        "Adequate product. Not the worst purchase but definitely not the best.",
        "It is fine. An ordinary product in an ordinary category. Average.",
        "Functional and basic. Meets minimum requirements without any surprise.",
        "This product earns a solid three stars. Not good, not bad, just average.",
        "A product that just barely meets expectations. Functional, but that is it.",
        "Works on most occasions. Has limitations but is overall acceptable.",
        "The performance is fair but not impressive. Average product overall.",
        "Three stars. I am not going to recommend it but also will not warn against it.",
        "A middle-ground product that does what it should, nothing more.",
        "I rate this an average three stars. Functional but ultimately forgettable.",
        "The quality is acceptable. Not mind-blowing but also not bad at all.",
        "Average experience. Neither a disappointment nor a happy surprise.",
        "It works fine. A standard product with standard results. Three stars.",
        "This is an ordinary product. It does its job but lacks any excitement.",
        "I feel neither strongly positive nor negative about this product.",
        "It is a decent product. I have no strong feelings one way or the other.",
        "The product gets the job done but without any outstanding qualities.",
        "It's an average product. Not the best and not the worst option available.",
        "This product is okay. I am not unhappy but also not particularly pleased."
    ]

    # ── Negative Reviews (1–2 stars) ──────────────────────────────────────────
    negative_reviews = [
        "Terrible product. Broke after two days. Complete waste of money!",
        "Absolute garbage. Do not waste your money on this junk product.",
        "Worst purchase I have ever made. Nothing works as advertised.",
        "Complete disappointment. The quality is shockingly poor.",
        "Do not buy this! It is a scam. Broke within a week of purchase.",
        "Horrible experience. The product is cheaply made and dysfunctional.",
        "Extremely disappointed. This product is nothing like the description.",
        "Returned immediately. The product was defective right out of the box.",
        "Save your money and avoid this at all costs. Absolutely terrible.",
        "Very poor quality. Fell apart in just days. Not worth a single penny.",
        "Waste of money. The product does not do what it claims to do at all.",
        "Would give zero stars if I could. Appalling quality and service.",
        "Cheaply made and breaks easily. Regret buying this completely.",
        "A disgrace of a product. Do not be fooled by the photos. Terrible.",
        "Does not work at all. Complete and utter waste of time and money.",
        "I am furious. This product broke on the very first day of use.",
        "Horrible quality. The product looks nothing like the listing photos.",
        "Utter disappointment from start to finish. I want my money back.",
        "The worst product I have ever bought. Completely useless garbage.",
        "Cheap materials, poor build quality, terrible performance. Avoid!",
        "This product is a fraud. The quality is atrocious and it broke quickly.",
        "Do not buy this product. It is shoddily made and does not work.",
        "I am absolutely disgusted. This product is dangerous and defective.",
        "The product is a joke. It literally fell apart as I was unboxing it.",
        "So disappointed. Spent good money on this and it is completely useless.",
        "Pathetic quality. Stopped working after just a few hours of use.",
        "Completely malfunctions every time. What a waste of my hard earned money.",
        "This is junk. Poor quality, poor design, poor performance. Avoid it!",
        "Huge disappointment. Does not even come close to what was promised.",
        "The worst purchase I have made online. This product is absolutely terrible.",
        "Shoddy craftsmanship and unreliable performance. I deeply regret this buy.",
        "Defective product. The seller sent me a broken item. Very unhappy!",
        "The quality is absolutely unacceptable. This is pure garbage.",
        "I cannot believe they are selling this. It is completely defective!",
        "Misleading description. The product is nothing like what was advertised.",
        "This product has caused me more problems than it solved. Very poor!",
        "Do yourself a favor and avoid this product entirely. Terrible quality!",
        "Absolute disaster. The product broke and customer service was useless.",
        "One star is too generous. This product is a complete and utter failure.",
        "The lowest quality product I have ever had the misfortune of purchasing.",
        "Do not be fooled by the reviews. This product is terrible and unreliable.",
        "Wasted my money on this junk. The product stopped working after one use.",
        "This is a defective and misleading product. I want a full refund.",
        "Dreadful quality. This product is flimsy, unreliable, and useless.",
        "Appalling product. The quality is nothing short of disgraceful.",
        "I was completely deceived by the product listing. It is awful.",
        "Do not buy. This product is cheap, poorly made, and just terrible.",
        "A complete rip-off. The product does not work and is very fragile.",
        "Awful in every possible way. I deeply regret purchasing this product.",
        "Extremely poor quality. Fell apart on first use. Deeply disappointed.",
        "This product is garbage. Breaks immediately and does not work at all.",
        "Avoid this product like the plague. It is simply terrible.",
        "Very angry with this purchase. The product is defective and useless.",
        "The product is completely nonfunctional. Save your money and look elsewhere.",
        "This product is a complete waste. It does not work and is poorly made.",
        "Terrible experience. The product broke immediately and was clearly defective.",
        "I have never been so disappointed with a purchase. This is truly awful.",
        "The quality is shockingly low for the price charged. Do not buy this!",
        "The product does not function at all. A total and complete waste of money.",
        "Garbage! It broke on the second day. Absolutely unacceptable quality.",
        "Worst product I have ever used. The quality is embarrassingly poor.",
        "I paid good money for this junk. It stopped working after three uses.",
        "Defective from the start. Returned it immediately. Terrible product.",
        "Extremely poor build quality. Would not even gift this to an enemy.",
        "This product has zero redeeming qualities. A total disappointment.",
        "Overpriced rubbish. Does not work as claimed. Absolutely terrible.",
        "Cheap, fragile, and completely useless. I want my money back!",
        "The product arrived broken and the return process was a nightmare.",
        "Very poor quality control. My product was defective right from day one.",
        "This is the worst thing I have ever bought online. Total garbage!",
        "Terrible product with terrible customer service. Avoid at all costs!",
        "This is junk. Breaks immediately and is completely useless.",
        "Absolute rubbish. Does not work as advertised. Total waste of money.",
        "I am so frustrated with this product. It has been a nightmare to use.",
        "Poor quality, does not work, and the seller ignored my complaint. Terrible!",
        "This product failed within hours of use. Absolutely worthless.",
        "I cannot express how disappointed I am. This product is dreadful.",
        "Horrific quality and performance. I would never recommend this to anyone.",
        "The product description is completely misleading. It is a terrible product.",
        "Fell apart within days of use. Zero quality control. Do not buy!"
    ]

    # Combine all reviews
    all_reviews = []
    for review in positive_reviews:
        all_reviews.append({
            "reviewText": review,
            "overall": np.random.choice([4, 5])
        })
    for review in neutral_reviews:
        all_reviews.append({
            "reviewText": review,
            "overall": 3
        })
    for review in negative_reviews:
        all_reviews.append({
            "reviewText": review,
            "overall": np.random.choice([1, 2])
        })
    
    # Create DataFrame and shuffle
    df = pd.DataFrame(all_reviews)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


df = create_sample_dataset()
print('✅ Dataset created successfully!')
print(df.head())


# Data Cleaning Functions
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenization
    tokens = text.split()
    
    # Stopword removal
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)


df['cleaned_text'] = df['reviewText'].apply(preprocess_text)
print('✅ Text preprocessing completed!')


# Sentiment Label Creation
def get_sentiment(rating):
    if rating <= 2:
        return 'Negative'
    elif rating == 3:
        return 'Neutral'
    else:
        return 'Positive'


df['sentiment'] = df['overall'].apply(get_sentiment)
print('✅ Sentiment labels created!')


# Exploratory Data Analysis & Plotting
plt.style.use('seaborn-v0_8')

# 1. Rating Distribution
fig, ax = plt.subplots(figsize=(10, 6))
rating_counts = df['overall'].value_counts().sort_index()
rating_counts.plot(kind='bar', ax=ax, color=['#FF6B6B', '#FFA07A', '#FFD700', '#90EE90', '#32CD32'])
ax.set_title('Distribution of Star Ratings', fontsize=16)
ax.set_xlabel('Star Rating', fontsize=12)
ax.set_ylabel('Number of Reviews', fontsize=12)
plt.tight_layout()
plt.savefig('Screenshots/rating_distribution.png', dpi=300)
print('✅ Saved rating_distribution.png')

# 2. Sentiment Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
sentiment_counts = df['sentiment'].value_counts()
colors = ['#32CD32', '#FFA07A', '#FF6B6B']
sentiment_counts.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('Sentiment Distribution (Bar Chart)', fontsize=14)
ax1.set_xlabel('Sentiment', fontsize=12)
ax1.set_ylabel('Number of Reviews', fontsize=12)

sentiment_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%', colors=colors, startangle=90)
ax2.set_title('Sentiment Distribution (Pie Chart)', fontsize=14)
ax2.set_ylabel('')
plt.tight_layout()
plt.savefig('Screenshots/sentiment_distribution.png', dpi=300)
print('✅ Saved sentiment_distribution.png')

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned_text'],
    df['sentiment'],
    test_size=0.2,
    random_state=42,
    stratify=df['sentiment']
)
print('✅ Train-test split completed!')

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)
print('✅ TF-IDF vectorization completed!')

# Model Training
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_tfidf, y_train)
print('✅ Model trained successfully!')

# Model Evaluation
y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"\n=== Model Evaluation ===")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# 3. Metrics Summary
fig, ax = plt.subplots(figsize=(10, 6))
metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
values = [accuracy, precision, recall, f1]
bars = ax.bar(metrics, values, color=['#4ECDC4', '#45B7D1', '#2E86AB', '#A23B72'])
ax.set_title('Model Evaluation Metrics', fontsize=16)
ax.set_ylim(0, 1)
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.01,
        f'{height:.4f}',
        ha='center',
        va='bottom',
        fontsize=12
    )
plt.tight_layout()
plt.savefig('Screenshots/metrics_summary.png', dpi=300)
print('✅ Saved metrics_summary.png')

# 4. Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=['Positive', 'Neutral', 'Negative'])
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
ax.figure.colorbar(im, ax=ax)
ax.set(xticks=np.arange(cm.shape[1]),
       yticks=np.arange(cm.shape[0]),
       xticklabels=['Positive', 'Neutral', 'Negative'],
       yticklabels=['Positive', 'Neutral', 'Negative'],
       title='Confusion Matrix',
       ylabel='True Label',
       xlabel='Predicted Label')

# Rotate the tick labels and set their alignment
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations
fmt = 'd'
thresh = cm.max() / 2
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm[i, j], fmt),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black")
fig.tight_layout()
plt.savefig('Screenshots/confusion_matrix.png', dpi=300)
print('✅ Saved confusion_matrix.png')


# Interactive Prediction Function
def predict_sentiment(review):
    cleaned = preprocess_text(review)
    tfidf_text = tfidf.transform([cleaned])
    prediction = model.predict(tfidf_text)[0]
    return prediction


# Example Predictions
print("\n=== Example Predictions ===")
example_reviews = [
    "This product is absolutely amazing! Works perfectly.",
    "It's okay, nothing special. Average quality.",
    "Terrible quality. Broke after two days. Complete waste of money.",
    "Great value for money, would highly recommend to everyone!",
    "Not what I expected. The description was misleading."
]

for review in example_reviews:
    sentiment = predict_sentiment(review)
    print(f"\nReview: {review}")
    print(f"Predicted Sentiment: {sentiment}")


print("\n✅ All screenshots generated successfully!")
