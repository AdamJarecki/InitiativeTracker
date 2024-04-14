from src.team2_read_data import read_csv_with_tab_separator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier


def process_data(data_path):
    df = read_csv_with_tab_separator(data_path)
    X = df[['Keywords', 'Description']]
    y = df['Class']
    vectorizer = TfidfVectorizer(stop_words='english')
    X['combined_data'] = X['Keywords'] + ' ' + X['Description']
    X = vectorizer.fit_transform(X['combined_data'])
    return X, y


def split_data(X, y): 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    #model = MultinomialNB()
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    #print(f"{X_test}=")
    print(f"{y_test}=")
    print(f"{y_pred}=")
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report


def run(data_path):
    X, y = process_data(data_path)
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_model(X_train, y_train)
    accuracy, report = evaluate_model(model, X_test, y_test)
    return accuracy, report


if __name__ == '__main__':
    data_path = 'data\\characters.csv'
    accuracy, report = run(data_path)
    print(f'Accuracy: {accuracy}')
    print(f'Report: {report}')