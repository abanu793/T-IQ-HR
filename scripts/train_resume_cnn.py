import os
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# -----------------------
# CONFIG
# -----------------------
CSV_PATH = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images\resume_images_labels.csv"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
MODEL_OUT = r"C:\Users\abanu\Documents\resume_cnn_v2.keras"


os.makedirs(MODEL_OUT, exist_ok=True)

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(CSV_PATH)

df["label"] = df["label"].map({"real": 0, "fake": 1})

train_df, val_df = train_test_split(
    df, test_size=0.2, stratify=df["label"], random_state=42
)


# -----------------------
# IMAGE LOADER
# -----------------------
def load_image(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_png(img, channels=3)
    img = tf.image.resize(img, IMG_SIZE)
    img = img / 255.0
    return img, label


def make_dataset(dataframe, shuffle=True):
    ds = tf.data.Dataset.from_tensor_slices(
        (dataframe["image_path"].values, dataframe["label"].values)
    )
    ds = ds.map(load_image, num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle:
        ds = ds.shuffle(1000)
    return ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)


train_ds = make_dataset(train_df)
val_ds = make_dataset(val_df, shuffle=False)

# -----------------------
# CLASS WEIGHTS
# -----------------------
weights = compute_class_weight(
    class_weight="balanced", classes=np.array([0, 1]), y=train_df["label"].values
)
class_weights = {0: weights[0], 1: weights[1]}

print("Class weights:", class_weights)

# -----------------------
# MODEL
# -----------------------
base = tf.keras.applications.EfficientNetB0(
    include_top=False, weights="imagenet", input_shape=(*IMG_SIZE, 3)
)

base.trainable = False

model = tf.keras.Sequential(
    [
        base,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ]
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
)

model.summary()

# -----------------------
# TRAIN
# -----------------------
history = model.fit(
    train_ds, validation_data=val_ds, epochs=EPOCHS, class_weight=class_weights
)

# -----------------------
# SAVE
# -----------------------
model.save(MODEL_OUT, overwrite=True)
print(f"\n✅ MODEL SAVED AT: {MODEL_OUT}")
