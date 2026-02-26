# AI Models Guide - Medical AI Assistant

## Overview

This document explains the AI models used in the Medical AI Assistant and how to train/replace them with your own models.

## Current Implementation

The application currently runs in **DEMO MODE** with rule-based analysis. To use actual AI models, follow the instructions below.

## Model Architecture

### 1. Skin Analysis Model

**Purpose**: Classify skin conditions from images

**Recommended Architecture**:
- Base: ResNet50 or DenseNet121 (pre-trained on ImageNet)
- Input: 224x224 RGB images
- Output: 8 classes (Healthy, Acne, Eczema, Psoriasis, Melanoma, Dermatitis, Rosacea, Fungal Infection)

**Training Data Sources**:
- HAM10000 Dataset
- ISIC Archive
- DermNet NZ

**Implementation Example**:
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.applications.ResNet50(
        include_top=False,
        weights='imagenet',
        input_shape=(224, 224, 3)
    ),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(8, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

### 2. Lab Results Analyzer

**Purpose**: Extract and interpret lab values from images

**Components**:
1. **OCR**: Tesseract for text extraction
2. **NER**: Named Entity Recognition for lab values
3. **Rule Engine**: Compare values with normal ranges

**Training Data**:
- Synthetic lab reports
- Public health datasets
- Anonymized real lab reports

**Implementation**:
- Uses Pytesseract for OCR
- Regex patterns for value extraction
- Dictionary-based normal range comparison

### 3. Medical Chatbot

**Purpose**: Provide medical advice based on symptoms

**Recommended Approach**:
- Fine-tuned BERT or GPT model
- Medical knowledge base
- Symptom-disease mapping

**Training Data**:
- Medical Q&A datasets
- Symptom databases
- Medical literature

**Current Implementation**:
- Rule-based keyword matching
- Symptom database lookup
- Template-based responses

**Upgrade Path**:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/BioGPT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

### 4. Sound Analysis Model

**Purpose**: Analyze respiratory sounds for health issues

**Architecture**:
- Input: Audio features (MFCCs, spectral features)
- Model: CNN or LSTM
- Output: 6 classes (Healthy, Asthma, Bronchitis, Pneumonia, COPD, Whooping Cough)

**Training Data**:
- ICBHI Respiratory Sound Database
- Coswara Dataset
- Custom recordings

**Feature Extraction**:
```python
import librosa

y, sr = librosa.load(audio_file)
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
```

## Replacing Demo Models with Real Models

### Step 1: Train Your Model

Train your model using TensorFlow or PyTorch:

```python
# Example: Training skin model
model.fit(
    train_dataset,
    epochs=50,
    validation_data=val_dataset,
    callbacks=[early_stopping, checkpoint]
)

# Save model
model.save('models_pretrained/skin_model.h5')
```

### Step 2: Update Model Loading

Edit the respective analyzer file (e.g., `backend/models/skin_analyzer.py`):

```python
def load_model(self):
    try:
        import tensorflow as tf
        self.model = tf.keras.models.load_model(self.model_path)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
```

### Step 3: Update Prediction Logic

```python
def analyze(self, image_path):
    img_array = self.preprocess_image(image_path)
    prediction = self.model.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    confidence = float(prediction[0][predicted_class])
    
    diagnosis = self.diseases[predicted_class]
    # ... rest of the logic
```

## Model Performance Metrics

### Skin Analysis
- Target Accuracy: >85%
- Precision: >80%
- Recall: >80%
- F1-Score: >80%

### Lab Analysis
- OCR Accuracy: >95%
- Value Extraction: >90%
- Classification Accuracy: >85%

### Chatbot
- Response Relevance: >90%
- Medical Accuracy: >85%
- User Satisfaction: >4/5

### Sound Analysis
- Accuracy: >80%
- Sensitivity: >85%
- Specificity: >80%

## Cloud Model Storage

### Using Google Drive

1. Upload model to Google Drive
2. Get shareable link
3. Extract file ID
4. Update `.env` file:

```
SKIN_MODEL_URL=https://drive.google.com/uc?id=YOUR_FILE_ID
```

5. Download in `setup_project.py`:

```python
import gdown

url = os.getenv('SKIN_MODEL_URL')
output = 'models_pretrained/skin_model.h5'
gdown.download(url, output, quiet=False)
```

### Using AWS S3

```python
import boto3

s3 = boto3.client('s3')
s3.download_file(
    'your-bucket',
    'models/skin_model.h5',
    'models_pretrained/skin_model.h5'
)
```

## Model Optimization

### Reduce Model Size

```python
# TensorFlow Lite conversion
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

### Quantization

```python
converter.optimizations = [tf.lite.Optimize.DEFAULT]
```

### Model Pruning

```python
import tensorflow_model_optimization as tfmot

pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
    initial_sparsity=0.0,
    final_sparsity=0.5,
    begin_step=0,
    end_step=1000
)

model = tfmot.sparsity.keras.prune_low_magnitude(
    model,
    pruning_schedule=pruning_schedule
)
```

## Ethical Considerations

1. **Data Privacy**: Never train on identifiable patient data
2. **Bias**: Ensure diverse training data
3. **Transparency**: Clearly communicate AI limitations
4. **Validation**: Clinical validation before deployment
5. **Monitoring**: Continuous performance monitoring

## Legal Compliance

- HIPAA compliance for US
- GDPR compliance for EU
- Medical device regulations
- Liability insurance
- Terms of service

## Future Improvements

1. **Multi-modal Analysis**: Combine multiple inputs
2. **Explainable AI**: Provide reasoning for diagnoses
3. **Continuous Learning**: Update models with new data
4. **Federated Learning**: Train without centralizing data
5. **Real-time Analysis**: Optimize for speed

## Resources

### Datasets
- Kaggle Medical Datasets
- NIH Clinical Center
- MIMIC-III Database
- PhysioNet

### Pre-trained Models
- TensorFlow Hub
- PyTorch Hub
- Hugging Face Model Hub

### Research Papers
- arXiv.org (Medical AI section)
- PubMed
- Google Scholar

## Support

For model-related questions:
- Email: ai-support@medicalai.com
- Documentation: docs.medicalai.com
- Community: forum.medicalai.com
