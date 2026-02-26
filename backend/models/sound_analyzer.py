import librosa
import numpy as np
import soundfile as sf
import os
import json

class SoundAnalyzer:
    def __init__(self):
        self.model_path = 'models_pretrained/sound_model.h5'
        self.respiratory_db_path = 'data/respiratory_sounds/respiratory_database.json'
        
        # Load respiratory database
        self.respiratory_database = self._load_respiratory_database()
        
        self.conditions = {
            0: 'Healthy Breathing',
            1: 'Asthma',
            2: 'Bronchitis',
            3: 'Pneumonia',
            4: 'COPD',
            5: 'Whooping Cough'
        }
        
        # Build treatments from loaded data
        self.treatments = self._build_treatments()
        
        self.load_model()
    
    def _load_respiratory_database(self):
        """Load respiratory conditions database from JSON file"""
        try:
            if os.path.exists(self.respiratory_db_path):
                with open(self.respiratory_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("Warning: Respiratory database not found. Using default data.")
                return {'conditions': []}
        except Exception as e:
            print(f"Error loading respiratory database: {e}")
            return {'conditions': []}
    
    def _build_treatments(self):
        """Build treatment recommendations from loaded data"""
        treatments = {}
        
        # Load from database
        for condition in self.respiratory_database.get('conditions', []):
            name = condition['name']
            meds = condition.get('medications', [])
            desc = condition.get('description', '')
            
            treatment_text = f"{desc}. Recommended: {', '.join(meds[:3])}. "
            if 'emergency_signs' in condition:
                treatment_text += f"⚠️ Emergency signs: {', '.join(condition['emergency_signs'])}. "
            treatment_text += f"Severity: {condition.get('severity', 'unknown')}."
            
            treatments[name] = treatment_text
        
        # Add defaults
        default_treatments = {
            'Healthy Breathing': 'Your breathing sounds normal. Continue maintaining good respiratory health.',
            'Asthma': 'Use prescribed inhaler as directed. Avoid triggers. Keep rescue inhaler available. Consult pulmonologist.',
            'Bronchitis': 'Rest, stay hydrated, use humidifier. Avoid smoking. See doctor if symptoms persist over 3 weeks.',
            'Pneumonia': 'IMPORTANT: Consult doctor immediately. May require antibiotics. Rest and stay hydrated.',
            'COPD': 'Follow prescribed treatment plan. Quit smoking. Pulmonary rehabilitation recommended. Regular doctor visits.',
            'Whooping Cough': 'Seek medical attention. Antibiotics may be needed. Isolate to prevent spread. Stay hydrated.'
        }
        
        # Merge with defaults
        for condition, treatment in default_treatments.items():
            if condition not in treatments:
                treatments[condition] = treatment
        
        return treatments
        
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained sound analysis model"""
        try:
            # In production, load actual audio classification model
            print("Sound analysis model loaded (demo mode)")
        except Exception as e:
            print(f"Model loading error: {e}")
    
    def extract_features(self, audio_path):
        """Extract audio features for analysis"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Extract features
            features = {}
            
            # MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features['mfcc_mean'] = np.mean(mfccs, axis=1)
            features['mfcc_std'] = np.std(mfccs, axis=1)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            features['spectral_centroid_mean'] = np.mean(spectral_centroids)
            
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)
            features['zcr_mean'] = np.mean(zcr)
            
            # RMS Energy
            rms = librosa.feature.rms(y=y)
            features['rms_mean'] = np.mean(rms)
            
            return features
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return None
    
    def analyze(self, audio_path):
        """Analyze respiratory sound"""
        try:
            # Extract features
            features = self.extract_features(audio_path)
            
            if features is None:
                raise Exception("Failed to extract audio features")
            
            # In production, use actual model prediction
            # prediction = self.model.predict(features)
            # predicted_class = np.argmax(prediction)
            # confidence = float(prediction[predicted_class])
            
            # Demo mode: Rule-based analysis
            predicted_class, confidence = self._rule_based_analysis(features)
            
            diagnosis = self.conditions[predicted_class]
            treatment = self.treatments[diagnosis]
            
            # Determine severity
            if predicted_class == 0:
                severity = 'none'
            elif predicted_class in [1, 2, 5]:
                severity = 'moderate'
            else:
                severity = 'severe'
            
            return {
                'diagnosis': diagnosis,
                'confidence': round(confidence * 100, 2),
                'treatment': treatment,
                'severity': severity,
                'recommendations': self._get_recommendations(diagnosis),
                'audio_features': {
                    'spectral_centroid': float(features['spectral_centroid_mean']),
                    'rms_energy': float(features['rms_mean']),
                    'zero_crossing_rate': float(features['zcr_mean'])
                }
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'diagnosis': 'Analysis failed',
                'treatment': 'Please upload a clear audio recording of breathing or coughing',
                'severity': 'unknown',
                'confidence': 0
            }
    
    def _rule_based_analysis(self, features):
        """Simple rule-based analysis for demo"""
        # Analyze based on audio characteristics
        spectral_centroid = features['spectral_centroid_mean']
        rms = features['rms_mean']
        zcr = features['zcr_mean']
        
        # Simple heuristics
        if rms < 0.02:  # Very quiet
            return 0, 0.85  # Healthy
        elif zcr > 0.1 and spectral_centroid > 2000:  # High frequency, noisy
            return 1, 0.75  # Asthma
        elif rms > 0.05 and spectral_centroid < 1500:  # Loud, low frequency
            return 2, 0.70  # Bronchitis
        else:
            return 0, 0.80  # Default to healthy
    
    def _get_recommendations(self, diagnosis):
        """Get comprehensive health recommendations"""
        general_tips = [
            '🚭 Avoid smoking and secondhand smoke (most important!)',
            '💧 Stay well hydrated (8-10 glasses of water daily)',
            '🧘 Practice deep breathing exercises (diaphragmatic breathing)',
            '🏠 Maintain good air quality at home (use air purifiers)',
            '😷 Avoid air pollutants and irritants',
            '🌡️ Keep indoor humidity at 30-50%',
            '💪 Regular moderate exercise to strengthen lungs',
            '😴 Get adequate sleep (7-9 hours) for immune function'
        ]
        
        specific_tips = {
            'Asthma': [
                '📋 Keep a symptom diary to identify triggers',
                '💊 Always carry rescue inhaler (albuterol)',
                '🏃 Warm up before exercise, avoid cold air',
                '🧹 Reduce allergens: dust mites, pet dander, mold',
                '💉 Get flu vaccine annually',
                '📊 Monitor peak flow regularly',
                '🚨 Have an asthma action plan',
                '👨‍⚕️ Regular follow-ups with pulmonologist',
                '🌡️ Avoid temperature extremes',
                '😰 Manage stress (can trigger attacks)'
            ],
            'Bronchitis': [
                '🌫️ Use cool-mist humidifier',
                '❄️ Avoid cold air exposure',
                '😴 Get plenty of rest',
                '🚫 Avoid irritants: smoke, fumes, dust',
                '🍯 Honey and warm liquids for cough relief',
                '🧴 Use saline nasal spray',
                '💊 Take prescribed antibiotics if bacterial',
                '🤧 Cover mouth when coughing',
                '🧼 Wash hands frequently',
                '⏰ Seek care if symptoms worsen after 3 weeks'
            ],
            'Pneumonia': [
                '🚨 URGENT: Complete full antibiotic course',
                '😴 Rest adequately, avoid strenuous activity',
                '🌡️ Monitor temperature regularly',
                '💧 Drink plenty of fluids',
                '🫁 Deep breathing exercises to prevent complications',
                '💊 Take all prescribed medications',
                '📞 Seek immediate care if breathing worsens',
                '💉 Get pneumonia vaccine (if eligible)',
                '🏥 Follow-up chest X-ray after treatment',
                '⚠️ Watch for complications: chest pain, confusion'
            ],
            'COPD': [
                '🚭 QUIT SMOKING immediately (most critical!)',
                '💊 Use prescribed inhalers correctly',
                '🏋️ Follow pulmonary rehabilitation program',
                '💨 Use oxygen therapy as prescribed',
                '💉 Get flu and pneumonia vaccines',
                '⚖️ Maintain healthy weight',
                '🥗 Eat nutritious, high-protein diet',
                '😷 Avoid respiratory infections',
                '🏠 Keep home well-ventilated',
                '👨‍⚕️ Regular check-ups with pulmonologist',
                '📊 Monitor oxygen saturation',
                '🚨 Have emergency action plan'
            ],
            'Whooping Cough': [
                '🚨 URGENT: Isolate to prevent spread',
                '💊 Complete full antibiotic course (erythromycin)',
                '🤧 Cover mouth when coughing',
                '🧼 Disinfect surfaces regularly',
                '💧 Stay hydrated, small frequent sips',
                '🍽️ Eat small, frequent meals',
                '😴 Rest in upright position',
                '🌫️ Use cool-mist humidifier',
                '🚫 Avoid irritants and smoke',
                '👶 Keep away from infants (very dangerous for them)',
                '💉 Ensure family members are vaccinated',
                '📞 Seek immediate care if turning blue or severe coughing'
            ],
            'Healthy Breathing': [
                '✅ Continue healthy lifestyle',
                '🏃 Regular cardiovascular exercise',
                '🧘 Practice breathing exercises',
                '🥗 Eat antioxidant-rich foods',
                '💪 Maintain good posture',
                '🌳 Spend time in fresh air',
                '😌 Manage stress effectively',
                '💉 Stay up-to-date with vaccinations'
            ]
        }
        
        # Combine general and specific recommendations
        all_tips = general_tips + specific_tips.get(diagnosis, [])
        
        # Add emergency warning for severe conditions
        if diagnosis in ['Pneumonia', 'COPD', 'Whooping Cough']:
            all_tips.insert(0, '🚨 IMPORTANT: This is a serious condition. Follow medical advice strictly!')
        
        return all_tips
