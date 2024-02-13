from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from nltk import word_tokenize
from nltk.corpus import stopwords,words
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


def filter_text(row):
    
    tokens = word_tokenize(row)

    filtered_words = []
    negate = False

    for word in tokens:
        if word.lower() == "not" or word.endswith("n't"):
            negate = not negate
        elif word.isalpha() or word in words.words() or (negate and word.lower() in words.words()):
            filtered_words.append(word)

    filtered_text = ' '.join(filtered_words)

    return filtered_text

def anxiety_calc(user_input):

    anxiety_data=pd.read_csv("C:/ML Project/Flask Repo/anxiety_data_clean.csv")
    
    anxiety_data['Sentence'] = anxiety_data['Sentence'].fillna('')

    # Assuming anxiety_data is your DataFrame
    X = anxiety_data.drop(['Anxiety Level'], axis=1)
    y = anxiety_data['Anxiety Level']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Assuming 'Sentence' is the text column
    text_transformer = Pipeline(steps=[
        ('tfidf', TfidfVectorizer()),  # You can customize TfidfVectorizer parameters
    ])

    # Assuming 'Tonality' and 'Mood' are categorical columns
    categorical_features = ['Tonality', 'Mood']
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('text', text_transformer, 'Sentence'),
            ('cat', categorical_transformer, categorical_features),
        ])

    # Ensemble Model
    rf_model = RandomForestClassifier(random_state=42)
    gb_model = GradientBoostingClassifier(random_state=42)
    svm_model = SVC(probability=True, random_state=42)

    ensemble_model = VotingClassifier(estimators=[('rf', rf_model), ('gb', gb_model), ('svm', svm_model)], voting='soft')

    # Use the preprocessor in the pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', ensemble_model),
    ])
    
    # Fit the model
    pipeline.fit(X_train, y_train)

    # Predictions
    y_pred = pipeline.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')

    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")


    # Create a DataFrame with the same structure as your training data
    columns = ['Filtered_Sentence', 'Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5', 'Feature6', 'Feature7', 'Feature8', 'Tonality', 'Mood']
    X_val_df = pd.DataFrame(user_input, columns=columns)

    X_val_df['Sentence'] = X_val_df['Filtered_Sentence'].apply(filter_text)

    # Drop the original 'Sentence' column if needed
    X_val_df = X_val_df.drop(['Filtered_Sentence'], axis=1)

    # Use the pipeline to make predictions
    y_val = pipeline.predict(X_val_df)

    print(y_val)
    return y_val

