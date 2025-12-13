import os
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# -----------------------
# CONFIGURATION
# -----------------------
DATA_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images"
IMG_HEIGHT, IMG_WIDTH = 128, 128
BATCH_SIZE = 32
EPOCHS = 10
MODEL_SAVE_PATH = r"C:\Users\abanu\Documents\t_iq_hr\models\resume_cnn.h5"

# -----------------------
# LOAD DATA
# -----------------------
# Option 1: Use CSV
csv_path = os.path.join(DATA_DIR, "resume_images_labels.csv")
df = pd.read_csv(csv_path)

# Split train/test
train_df, val_df = train_test_split(
    df, test_size=0.2, stratify=df["label"], random_state=42
)

# -----------------------
# IMAGE GENERATORS
# -----------------------
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
)

val_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_gen = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col="image_path",
    y_col="label",
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode="rgb",
    class_mode="binary",
    batch_size=BATCH_SIZE,
    shuffle=True,
)

val_gen = val_datagen.flow_from_dataframe(
    dataframe=val_df,
    x_col="image_path",
    y_col="label",
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    color_mode="rgb",
    class_mode="binary",
    batch_size=BATCH_SIZE,
    shuffle=False,
)

# -----------------------
# BUILD CNN MODEL
# -----------------------
model = Sequential(
    [
        Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation="relu"),
        Dropout(0.5),
        Dense(1, activation="sigmoid"),  # binary classification
    ]
)

model.compile(
    optimizer=Adam(learning_rate=1e-4), loss="binary_crossentropy", metrics=["accuracy"]
)

model.summary()

# -----------------------
# TRAIN MODEL
# -----------------------
history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

# -----------------------
# SAVE MODEL
# -----------------------
model.save(MODEL_SAVE_PATH)
print(f"\nModel saved to: {MODEL_SAVE_PATH}")


import pandas as pd

csv_path = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images\resume_images_labels.csv"
df = pd.read_csv(csv_path)
print(df["label"].value_counts())

# -----------------------
# CLASS WEIGHTS (IMPORTANT)
# -----------------------
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.array([0, 1]),  # 0 = real, 1 = fake
    y=train_df["label"].map({"real": 0, "fake": 1}).values,
)

class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

print("Class weights:", class_weight_dict)
