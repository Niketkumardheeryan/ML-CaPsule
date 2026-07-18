import argparse
from model import train_classifier


def main():
    parser = argparse.ArgumentParser(description='Train QR risk classifier')
    parser.add_argument('--data_csv', required=True, help='Path to CSV file with url,label columns')
    parser.add_argument('--model_path', default='qr_risk_model.joblib', help='Output path for trained model')
    args = parser.parse_args()

    train_classifier(args.data_csv, args.model_path)


if __name__ == '__main__':
    main()
