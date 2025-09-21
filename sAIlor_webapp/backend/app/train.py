from pathlib import Path
import joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from features import CAT_FEATURES, NUM_FEATURES, ALL_FEATURES

ROOT = Path(__file__).resolve().parents[1].parents[0]
DATA_DIR = ROOT / "data"
CACHE_DIR = Path(__file__).resolve().parents[1] / "cache"
TRAIN_CSV = DATA_DIR / "training.csv"
MODEL_PATH = CACHE_DIR / "model.joblib"

def main():
    if not TRAIN_CSV.exists():
        # build from raster + points.csv or generated grid
        from build_dataset import build as build_ds
        build_ds()

    df = pd.read_csv(TRAIN_CSV)
    X = df[ALL_FEATURES].copy()
    y = df["label"].astype(int)

    # Check if we have both classes
    unique_classes = y.unique()
    print(f"[train] Found {len(unique_classes)} classes: {unique_classes}")
    
    if len(unique_classes) < 2:
        print(f"[train] ERROR: Only {len(unique_classes)} class(es) found. Need at least 2 classes for training.")
        print(f"[train] Class distribution: {y.value_counts().to_dict()}")
        print("[train] This usually happens when the weak label generation creates unbalanced data.")
        print("[train] Try running build_dataset.py again or check the scoring logic.")
        return False

    # Check class balance
    class_counts = y.value_counts()
    print(f"[train] Class distribution: {class_counts.to_dict()}")
    
    # Warn if severely unbalanced
    min_class_count = class_counts.min()
    max_class_count = class_counts.max()
    if min_class_count < 5:
        print(f"[train] WARNING: Very few samples in minority class ({min_class_count}). Model may not perform well.")
    
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES),
        ("num", "passthrough", NUM_FEATURES),
    ])
    
    # Use class_weight='balanced' to handle imbalanced data
    clf = Pipeline([
        ("pre", pre), 
        ("lr", LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42))
    ])
    
    try:
        clf.fit(X, y)
        print("[train] Model training completed successfully")
    except Exception as e:
        print(f"[train] ERROR: Model training failed: {e}")
        return False

    yhat = clf.predict(X)
    print("\n[train] Classification Report:")
    print(classification_report(y, yhat, digits=3))

    CACHE_DIR.mkdir(exist_ok=True, parents=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"[train] Saved model → {MODEL_PATH}")
    return True

if __name__ == "__main__":
    main()
