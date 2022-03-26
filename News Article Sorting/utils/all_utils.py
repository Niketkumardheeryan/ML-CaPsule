from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk,argparse,yaml
import pymongo,logging,os


def read_config():
    args=argparse.ArgumentParser()
    args.add_argument("--config","-c",default="config.yaml")
    parsed_args = args.parse_args()
    config_path = parsed_args.config

    with open(config_path) as config_file:
        content = yaml.safe_load(config_file)

    return content

def preprocess_text(Text):
    Text = nltk.word_tokenize(Text)
    logging.info("Tokenized Text: " + str(Text))
    stemmer = PorterStemmer()
    stem = [stemmer.stem(word) for word in Text]
    words = [word for word in stem if word not in stopwords.words('english')]
    Text = " ".join(words)
    logging.info("Preprocessed Text: " + Text)
    return Text


def Database_Connection(News):
    config = read_config()
    database = config["mongodb"]["database"]
    collection = config["mongodb"]["collection"]
    mongo_url = config["mongodb"]["mongo_url"]
    client = pymongo.MongoClient(mongo_url)
    dataBase = client[database]
    collection = dataBase[collection]

    record = {"News" : News}
    collection.insert_one(record)

def Writing_log():
    config = read_config()

    logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
    log_dir=config["logs"]["logs_dir"]
    general_logs = config["logs"]["general_log"]
    general_log_path_dir=os.path.join(log_dir,general_logs)

    os.makedirs(general_log_path_dir, exist_ok=True)
    general_logs_name = config["logs"]["general_log_file"]
    general_log_path = os.path.join(general_log_path_dir,general_logs_name)
    print(general_log_path)
    logging.basicConfig(filename = general_log_path, level=logging.INFO, format=logging_str)
    
    