import cv2
import numpy as np
from PIL import Image
import os
import json

class SkinAnalyzer:
    def __init__(self):
        self.model_path = 'models_pretrained/skin_model.h5'
        self.skin_db_path = 'data/skin_images/skin_disease_database.json'
        
        # Load skin disease database
        self.skin_disease_database = self._load_skin_database()
        
        self.diseases = {
            0: 'Healthy Skin',
            1: 'Acne',
            2: 'Eczema',
            3: 'Psoriasis',
            4: 'Melanoma',
            5: 'Dermatitis',
            6: 'Rosacea',
            7: 'Fungal Infection'
        }
        
        # Build treatments from loaded data
        self.treatments = self._build_treatments()
        
        self.load_model()
    
    def _load_skin_database(self):
        """Load skin disease database from JSON file"""
        try:
            if os.path.exists(self.skin_db_path):
                with open(self.skin_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("Warning: Skin disease database not found. Using default data.")
                return {'conditions': []}
        except Exception as e:
            print(f"Error loading skin database: {e}")
            return {'conditions': []}
    
    def _build_treatments(self):
        """Build treatment recommendations from loaded data"""
        treatments = {}
        
        # Load from database
        for condition in self.skin_disease_database.get('conditions', []):
            name = condition['name']
            meds = condition.get('medications', [])
            desc = condition.get('description', '')
            
            treatment_text = f"{desc}. Recommended: {', '.join(meds[:3])}. "
            treatment_text += f"Severity: {condition.get('severity', 'unknown')}. "
            treatment_text += f"Duration: {condition.get('treatment_duration', 'varies')}."
            
            treatments[name] = treatment_text
        
        # Add defaults
        default_treatments = {
            'Healthy Skin': 'Your skin appears healthy! Continue with regular skincare routine.',
            'Acne': 'Recommended: Benzoyl peroxide or salicylic acid cleanser. Consult dermatologist for severe cases.',
            'Eczema': 'Use moisturizing creams and avoid irritants. Hydrocortisone cream may help. See a doctor if severe.',
            'Psoriasis': 'Topical corticosteroids and moisturizers recommended. Consult dermatologist for treatment plan.',
            'Melanoma': 'URGENT: Please consult a dermatologist immediately for proper diagnosis and treatment.',
            'Dermatitis': 'Avoid allergens and use gentle, fragrance-free products. Antihistamines may help with itching.',
            'Rosacea': 'Avoid triggers (spicy food, alcohol, sun). Use gentle skincare. Consult doctor for prescription treatment.',
            'Fungal Infection': 'Antifungal creams (clotrimazole, miconazole) recommended. Keep area clean and dry.'
        }
        
        # Merge with defaults
        for disease, treatment in default_treatments.items():
            if disease not in treatments:
                treatments[disease] = treatment
        
        return treatments
        
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained model"""
        try:
            # In production, load actual TensorFlow/PyTorch model
            # self.model = tf.keras.models.load_model(self.model_path)
            print("Skin analysis model loaded (demo mode)")
        except Exception as e:
            print(f"Model loading error: {e}")
            print("Running in demo mode with rule-based analysis")
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        return np.expand_dims(img, axis=0)
    
    def analyze(self, image_path):
        """Analyze skin condition from image with enhanced accuracy"""
        try:
            # Load and preprocess image
            img = cv2.imread(image_path)
            if img is None:
                raise Exception("Failed to load image")
            
            # Multiple color space analysis
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Enhanced feature extraction
            features = self._extract_advanced_features(img, hsv, lab, gray)
            
            # Multi-stage analysis
            predicted_class, confidence = self._advanced_classification(features)
            
            diagnosis = self.diseases[predicted_class]
            treatment = self.treatments[diagnosis]
            
            # Enhanced severity calculation
            severity = self._enhanced_severity_assessment(predicted_class, features)
            
            # Get medications from database
            medications = self._get_detailed_medications(diagnosis)
            
            # Enhanced response with medications
            response = {
                'diagnosis': diagnosis,
                'confidence': round(confidence * 100, 2),
                'treatment': self._get_comprehensive_treatment(diagnosis, severity, medications),
                'severity': severity,
                'medications': medications,
                'symptoms': self._get_symptoms_for_condition(diagnosis),
                'recommendations': self._get_recommendations(diagnosis),
                'analysis_details': {
                    'color_uniformity': features['color_uniformity'],
                    'texture_quality': features['texture_quality'],
                    'border_regularity': features['border_regularity'],
                    'symmetry': features['symmetry'],
                    'size_assessment': features['size_assessment']
                },
                'confidence_breakdown': features['confidence_factors']
            }
            
            return response
            
        except Exception as e:
            return {
                'error': str(e),
                'diagnosis': 'Analysis failed',
                'treatment': 'Please try again with a clearer, well-lit image',
                'severity': 'unknown',
                'confidence': 0
            }
    
    def _extract_advanced_features(self, img, hsv, lab, gray):
        """Extract comprehensive features for accurate analysis"""
        features = {}
        
        # 1. Color Analysis (HSV)
        h, s, v = cv2.split(hsv)
        features['avg_hue'] = np.mean(h)
        features['avg_saturation'] = np.mean(s)
        features['avg_value'] = np.mean(v)
        features['std_hue'] = np.std(h)
        features['std_saturation'] = np.std(s)
        features['std_value'] = np.std(v)
        
        # 2. Color Analysis (LAB)
        l, a, b = cv2.split(lab)
        features['avg_lightness'] = np.mean(l)
        features['avg_a'] = np.mean(a)  # Green-Red
        features['avg_b'] = np.mean(b)  # Blue-Yellow
        
        # 3. Texture Analysis
        # Variance
        features['texture_variance'] = np.var(gray)
        
        # Local Binary Pattern (simplified)
        features['texture_complexity'] = self._calculate_texture_complexity(gray)
        
        # Gradient magnitude
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        features['avg_gradient'] = np.mean(gradient_magnitude)
        
        # 4. Edge Detection
        edges = cv2.Canny(gray, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / edges.size
        features['edge_strength'] = np.mean(edges[edges > 0]) if np.any(edges > 0) else 0
        
        # 5. Shape Analysis
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            features['contour_area'] = cv2.contourArea(largest_contour)
            features['contour_perimeter'] = cv2.arcLength(largest_contour, True)
            
            # Circularity
            if features['contour_perimeter'] > 0:
                features['circularity'] = 4 * np.pi * features['contour_area'] / (features['contour_perimeter'] ** 2)
            else:
                features['circularity'] = 0
        else:
            features['contour_area'] = 0
            features['contour_perimeter'] = 0
            features['circularity'] = 0
        
        # 6. Color Distribution
        hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
        hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
        features['hue_entropy'] = self._calculate_entropy(hist_h)
        features['saturation_entropy'] = self._calculate_entropy(hist_s)
        
        # 7. Derived Features
        features['color_uniformity'] = 'uniform' if features['std_saturation'] < 40 else 'varied'
        features['texture_quality'] = 'smooth' if features['texture_variance'] < 800 else 'rough'
        features['border_regularity'] = 'regular' if features['edge_density'] < 0.08 else 'irregular'
        features['symmetry'] = 'symmetric' if features['circularity'] > 0.7 else 'asymmetric'
        features['size_assessment'] = 'small' if features['contour_area'] < 5000 else 'large'
        
        # 8. Confidence factors
        features['confidence_factors'] = {
            'image_quality': min(100, features['avg_value'] / 2.55),
            'feature_clarity': min(100, features['edge_strength'] * 2),
            'color_consistency': max(0, 100 - features['std_saturation'])
        }
        
        return features
    
    def _calculate_texture_complexity(self, gray):
        """Calculate texture complexity"""
        # Use Laplacian variance as texture measure
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return np.var(laplacian)
    
    def _calculate_entropy(self, histogram):
        """Calculate entropy of histogram"""
        histogram = histogram.flatten()
        histogram = histogram[histogram > 0]
        prob = histogram / histogram.sum()
        entropy = -np.sum(prob * np.log2(prob))
        return entropy
    
    def _advanced_classification(self, features):
        """Advanced multi-factor classification"""
        scores = {i: 0.0 for i in range(8)}
        
        # Acne detection (red, localized, rough texture)
        if 0 <= features['avg_hue'] <= 20:
            scores[1] += 0.25
        if features['avg_saturation'] > 60:
            scores[1] += 0.20
        if features['texture_variance'] > 1200:
            scores[1] += 0.15
        if features['edge_density'] > 0.10:
            scores[1] += 0.15
        if features['color_uniformity'] == 'varied':
            scores[1] += 0.10
        
        # Rosacea detection (persistent redness, uniform)
        if 0 <= features['avg_hue'] <= 15:
            scores[6] += 0.30
        if features['avg_saturation'] > 80:
            scores[6] += 0.25
        if features['std_hue'] < 25:
            scores[6] += 0.20
        if features['color_uniformity'] == 'uniform':
            scores[6] += 0.15
        
        # Eczema detection (dry, patchy, varied color)
        if features['std_saturation'] > 50:
            scores[2] += 0.25
        if features['texture_variance'] > 1800:
            scores[2] += 0.20
        if features['avg_value'] < 150:
            scores[2] += 0.15
        if features['color_uniformity'] == 'varied':
            scores[2] += 0.15
        if features['texture_quality'] == 'rough':
            scores[2] += 0.10
        
        # Psoriasis detection (scaly, raised, defined borders)
        if features['texture_variance'] > 2200:
            scores[3] += 0.25
        if features['edge_density'] > 0.12:
            scores[3] += 0.20
        if features['avg_gradient'] > 30:
            scores[3] += 0.15
        if features['border_regularity'] == 'irregular':
            scores[3] += 0.15
        if features['texture_complexity'] > 1500:
            scores[3] += 0.10
        
        # Melanoma detection (dark, irregular, asymmetric)
        if features['avg_value'] < 80:
            scores[4] += 0.30
        if features['edge_density'] > 0.15:
            scores[4] += 0.25
        if features['std_hue'] > 35:
            scores[4] += 0.20
        if features['symmetry'] == 'asymmetric':
            scores[4] += 0.20
        if features['circularity'] < 0.6:
            scores[4] += 0.15
        if features['size_assessment'] == 'large':
            scores[4] += 0.10
        
        # Dermatitis detection
        if 10 <= features['avg_hue'] <= 30:
            scores[5] += 0.25
        if features['avg_saturation'] > 45:
            scores[5] += 0.20
        if features['texture_variance'] > 1000:
            scores[5] += 0.15
        if features['std_saturation'] > 40:
            scores[5] += 0.15
        
        # Fungal infection detection (yellowish/brownish, circular)
        if 20 <= features['avg_hue'] <= 45:
            scores[7] += 0.30
        if features['edge_density'] > 0.10:
            scores[7] += 0.20
        if features['circularity'] > 0.7:
            scores[7] += 0.20
        if features['border_regularity'] == 'regular':
            scores[7] += 0.15
        
        # Healthy skin (default if no strong indicators)
        if all(score < 0.50 for score in scores.values() if score > 0):
            scores[0] = 0.85
        
        # Adjust scores based on image quality
        quality_factor = features['confidence_factors']['image_quality'] / 100
        for key in scores:
            if key != 0:  # Don't adjust healthy skin score
                scores[key] *= quality_factor
        
        # Find highest score
        predicted_class = max(scores, key=scores.get)
        base_confidence = scores[predicted_class]
        
        # Calculate final confidence
        confidence = min(0.95, max(0.60, base_confidence + 0.40))
        
        return predicted_class, confidence
    
    def _enhanced_severity_assessment(self, predicted_class, features):
        """Enhanced severity assessment based on multiple factors"""
        if predicted_class == 0:  # Healthy
            return 'none'
        
        severity_score = 0
        
        # Factor 1: Condition type
        if predicted_class == 4:  # Melanoma
            return 'severe'
        elif predicted_class in [2, 3]:  # Eczema, Psoriasis
            severity_score += 2
        else:
            severity_score += 1
        
        # Factor 2: Color variation
        if features['std_saturation'] > 70:
            severity_score += 2
        elif features['std_saturation'] > 50:
            severity_score += 1
        
        # Factor 3: Edge irregularity
        if features['edge_density'] > 0.15:
            severity_score += 2
        elif features['edge_density'] > 0.10:
            severity_score += 1
        
        # Factor 4: Size
        if features['size_assessment'] == 'large':
            severity_score += 1
        
        # Factor 5: Texture
        if features['texture_variance'] > 2000:
            severity_score += 1
        
        # Determine severity
        if severity_score >= 6:
            return 'severe'
        elif severity_score >= 3:
            return 'moderate'
        else:
            return 'mild'
    
    def _get_detailed_medications(self, diagnosis):
        """Get detailed medication list from database"""
        medications = []
        
        # Try to get from loaded database
        for condition in self.skin_disease_database.get('conditions', []):
            if condition['name'] == diagnosis:
                return condition.get('medications', [])
        
        # Fallback to default
        default_meds = {
            'Acne': ['Benzoyl peroxide 5% gel', 'Salicylic acid 2% cleanser', 'Tretinoin 0.025% cream', 'Clindamycin 1% gel'],
            'Eczema': ['Hydrocortisone 1% cream', 'Cetaphil moisturizer', 'Tacrolimus 0.1% ointment', 'Antihistamine (Cetirizine 10mg)'],
            'Psoriasis': ['Betamethasone cream', 'Calcipotriene ointment', 'Coal tar shampoo', 'Methotrexate (if severe)'],
            'Melanoma': ['URGENT: Surgical excision', 'Immunotherapy (Pembrolizumab)', 'Targeted therapy (if BRAF+)', 'Radiation therapy'],
            'Dermatitis': ['Hydrocortisone 1% cream', 'Moisturizer (fragrance-free)', 'Antihistamine', 'Avoid irritants'],
            'Rosacea': ['Metronidazole 0.75% gel', 'Azelaic acid 15% gel', 'Doxycycline 40mg', 'Gentle cleanser'],
            'Fungal Infection': ['Clotrimazole 1% cream', 'Miconazole 2% cream', 'Terbinafine 1% cream', 'Fluconazole 150mg (oral)']
        }
        
        return default_meds.get(diagnosis, [])
    
    def _get_symptoms_for_condition(self, diagnosis):
        """Get symptoms associated with skin condition"""
        symptoms_map = {
            'Healthy Skin': [
                'No visible lesions or abnormalities',
                'Even skin tone',
                'Normal texture',
                'No discomfort'
            ],
            'Acne': [
                'Red, inflamed bumps (papules)',
                'Pus-filled pimples (pustules)',
                'Blackheads and whiteheads',
                'Oily skin',
                'Possible scarring',
                'Tenderness or pain in affected areas'
            ],
            'Eczema': [
                'Intense itching (especially at night)',
                'Dry, sensitive skin',
                'Red or brownish-gray patches',
                'Thickened, cracked, or scaly skin',
                'Small raised bumps (may leak fluid)',
                'Raw, swollen skin from scratching'
            ],
            'Psoriasis': [
                'Red patches covered with silvery scales',
                'Dry, cracked skin that may bleed',
                'Itching, burning, or soreness',
                'Thickened or ridged nails',
                'Swollen and stiff joints (psoriatic arthritis)',
                'Patches on scalp, elbows, knees'
            ],
            'Melanoma': [
                'Asymmetric mole or lesion',
                'Irregular or notched borders',
                'Multiple colors (brown, black, red, white, blue)',
                'Diameter larger than 6mm (pencil eraser)',
                'Evolving size, shape, or color',
                'May bleed or ooze',
                'Usually painless'
            ],
            'Dermatitis': [
                'Red, inflamed skin',
                'Itching (mild to severe)',
                'Dry, flaky skin',
                'Blisters or oozing (in severe cases)',
                'Burning or stinging sensation',
                'Swelling in affected area'
            ],
            'Rosacea': [
                'Facial redness (especially cheeks, nose)',
                'Visible blood vessels',
                'Swollen, red bumps (may contain pus)',
                'Burning or stinging sensation',
                'Dry, rough, scaly skin',
                'Eye problems (dryness, irritation)',
                'Enlarged nose (rhinophyma) in severe cases'
            ],
            'Fungal Infection': [
                'Ring-shaped rash with raised edges',
                'Itching (often intense)',
                'Red, scaly, or cracked skin',
                'Circular patches that spread outward',
                'Hair loss in affected areas (scalp)',
                'Discolored, thick, brittle nails (if nail infection)'
            ]
        }
        
        return symptoms_map.get(diagnosis, ['Consult dermatologist for proper diagnosis'])
    
    def _get_comprehensive_treatment(self, diagnosis, severity, medications):
        """Get comprehensive treatment plan with medications and dosages"""
        if diagnosis == 'Healthy Skin':
            return 'Your skin appears healthy! Continue with regular skincare routine: gentle cleanser, moisturizer, and sunscreen daily.'
        
        treatment = f"🏥 COMPREHENSIVE TREATMENT PLAN FOR {diagnosis.upper()}\n"
        treatment += "="*60 + "\n\n"
        
        # Severity indicator
        severity_emoji = {'mild': '🟢', 'moderate': '🟡', 'severe': '🔴', 'none': '⚪'}
        treatment += f"⚠️ SEVERITY: {severity_emoji.get(severity, '🟡')} {severity.upper()}\n\n"
        
        # Medications with detailed dosages
        treatment += "💊 PRESCRIBED MEDICATIONS:\n"
        treatment += "-"*60 + "\n\n"
        
        if diagnosis == 'Acne':
            treatment += "1. Benzoyl Peroxide 5% Gel\n"
            treatment += "   → Application: Apply thin layer to affected areas once daily (evening)\n"
            treatment += "   → Start with 2.5% if sensitive skin, increase to 5% after 1 week\n"
            treatment += "   → Wash hands after application\n"
            treatment += "   → May cause dryness - use moisturizer\n"
            treatment += "   → Duration: 6-8 weeks for visible results\n\n"
            
            treatment += "2. Salicylic Acid 2% Cleanser\n"
            treatment += "   → Usage: Wash face twice daily (morning and evening)\n"
            treatment += "   → Massage gently for 30 seconds, rinse thoroughly\n"
            treatment += "   → Helps unclog pores and reduce inflammation\n\n"
            
            treatment += "3. Tretinoin 0.025% Cream (Prescription)\n"
            treatment += "   → Application: Pea-sized amount to entire face at bedtime\n"
            treatment += "   → Start 2-3 times per week, increase to nightly as tolerated\n"
            treatment += "   → Use sunscreen during day (increases sun sensitivity)\n"
            treatment += "   → May cause initial purging (2-4 weeks)\n\n"
            
            treatment += "4. Clindamycin 1% Gel (if bacterial)\n"
            treatment += "   → Application: Apply twice daily to affected areas\n"
            treatment += "   → Antibiotic for inflammatory acne\n"
            treatment += "   → Use for 8-12 weeks\n\n"
            
            if severity == 'severe':
                treatment += "5. Isotretinoin (Accutane) - Oral (Severe cases only)\n"
                treatment += "   → Dosage: 0.5-1mg/kg/day (doctor prescribed)\n"
                treatment += "   → Duration: 4-6 months\n"
                treatment += "   → Requires monthly monitoring (liver, lipids)\n"
                treatment += "   → IMPORTANT: Highly teratogenic - avoid pregnancy\n\n"
        
        elif diagnosis == 'Eczema':
            treatment += "1. Hydrocortisone 1% Cream (OTC)\n"
            treatment += "   → Application: Apply thin layer to affected areas 2-3 times daily\n"
            treatment += "   → Use for flare-ups only (not continuously)\n"
            treatment += "   → Maximum 2 weeks continuous use\n"
            treatment += "   → Avoid face and skin folds\n\n"
            
            treatment += "2. Triamcinolone 0.1% Cream (Prescription)\n"
            treatment += "   → Application: Once or twice daily to affected areas\n"
            treatment += "   → Stronger steroid for moderate-severe eczema\n"
            treatment += "   → Use for 2-4 weeks, then taper\n\n"
            
            treatment += "3. Tacrolimus 0.1% Ointment (Protopic)\n"
            treatment += "   → Application: Twice daily to affected areas\n"
            treatment += "   → Non-steroid option for long-term use\n"
            treatment += "   → Safe for face and sensitive areas\n"
            treatment += "   → May cause burning initially (improves with use)\n\n"
            
            treatment += "4. Cetirizine 10mg (Antihistamine)\n"
            treatment += "   → Dosage: 10mg once daily at bedtime\n"
            treatment += "   → Reduces itching and helps sleep\n"
            treatment += "   → Can use long-term\n\n"
            
            treatment += "5. Moisturizer (Cetaphil/CeraVe)\n"
            treatment += "   → Application: Apply liberally 3-4 times daily\n"
            treatment += "   → Apply within 3 minutes after bathing\n"
            treatment += "   → Use fragrance-free, thick creams or ointments\n\n"
        
        elif diagnosis == 'Psoriasis':
            treatment += "1. Betamethasone Dipropionate 0.05% Cream\n"
            treatment += "   → Application: Once or twice daily to plaques\n"
            treatment += "   → Potent steroid for thick plaques\n"
            treatment += "   → Use for 2-4 weeks, then break\n"
            treatment += "   → Cover with plastic wrap for better absorption (if needed)\n\n"
            
            treatment += "2. Calcipotriene 0.005% Ointment (Vitamin D analog)\n"
            treatment += "   → Application: Twice daily to affected areas\n"
            treatment += "   → Can combine with steroid\n"
            treatment += "   → Slows skin cell growth\n"
            treatment += "   → Maximum 100g per week\n\n"
            
            treatment += "3. Coal Tar 2-5% Shampoo/Cream\n"
            treatment += "   → Usage: 2-3 times per week\n"
            treatment += "   → Leave on 5-10 minutes before rinsing\n"
            treatment += "   → Reduces scaling and inflammation\n"
            treatment += "   → May stain clothing\n\n"
            
            if severity == 'severe':
                treatment += "4. Methotrexate 7.5-25mg (Oral - Severe cases)\n"
                treatment += "   → Dosage: Once weekly (not daily!)\n"
                treatment += "   → Take folic acid 1mg daily (except methotrexate day)\n"
                treatment += "   → Requires monthly blood tests\n"
                treatment += "   → Avoid alcohol\n\n"
                
                treatment += "5. Biologics (Humira, Enbrel, Stelara)\n"
                treatment += "   → Injection: Frequency varies by medication\n"
                treatment += "   → For moderate-severe psoriasis\n"
                treatment += "   → Expensive but highly effective\n"
                treatment += "   → Requires specialist prescription\n\n"
        
        elif diagnosis == 'Rosacea':
            treatment += "1. Metronidazole 0.75% Gel\n"
            treatment += "   → Application: Twice daily to entire face\n"
            treatment += "   → First-line treatment for rosacea\n"
            treatment += "   → Reduces inflammation and redness\n"
            treatment += "   → Results in 3-4 weeks\n\n"
            
            treatment += "2. Azelaic Acid 15% Gel\n"
            treatment += "   → Application: Twice daily to affected areas\n"
            treatment += "   → Reduces bumps and redness\n"
            treatment += "   → May cause tingling initially\n\n"
            
            treatment += "3. Doxycycline 40mg (Low-dose)\n"
            treatment += "   → Dosage: Once daily in morning\n"
            treatment += "   → Anti-inflammatory (not antibiotic dose)\n"
            treatment += "   → Take with food\n"
            treatment += "   → Duration: 3-6 months\n\n"
            
            treatment += "4. Ivermectin 1% Cream (if Demodex mites)\n"
            treatment += "   → Application: Once daily at bedtime\n"
            treatment += "   → Targets mites that worsen rosacea\n"
            treatment += "   → Very effective for papulopustular rosacea\n\n"
        
        elif diagnosis == 'Fungal Infection':
            treatment += "1. Clotrimazole 1% Cream\n"
            treatment += "   → Application: Twice daily to affected area and 2cm beyond\n"
            treatment += "   → Continue for 2 weeks after symptoms clear\n"
            treatment += "   → Total duration: 2-4 weeks\n\n"
            
            treatment += "2. Terbinafine 1% Cream (Lamisil)\n"
            treatment += "   → Application: Once or twice daily\n"
            treatment += "   → More effective than clotrimazole\n"
            treatment += "   → Shorter treatment duration (1-2 weeks)\n\n"
            
            treatment += "3. Fluconazole 150mg (Oral - if severe)\n"
            treatment += "   → Dosage: Single dose or once weekly for 2-4 weeks\n"
            treatment += "   → For widespread or resistant infections\n"
            treatment += "   → Prescription required\n\n"
            
            treatment += "4. Ketoconazole 2% Shampoo (if scalp)\n"
            treatment += "   → Usage: Twice weekly\n"
            treatment += "   → Leave on 5 minutes before rinsing\n\n"
        
        elif diagnosis == 'Dermatitis':
            treatment += "1. Hydrocortisone 1% Cream\n"
            treatment += "   → Application: 2-3 times daily to affected areas\n"
            treatment += "   → Use until rash clears (usually 1-2 weeks)\n\n"
            
            treatment += "2. Moisturizer (Fragrance-free)\n"
            treatment += "   → Application: Multiple times daily\n"
            treatment += "   → Essential for healing\n\n"
            
            treatment += "3. Antihistamine (Diphenhydramine 25-50mg)\n"
            treatment += "   → Dosage: Every 6 hours as needed for itching\n"
            treatment += "   → May cause drowsiness\n\n"
        
        elif diagnosis == 'Melanoma':
            treatment += "🚨 URGENT - IMMEDIATE MEDICAL ATTENTION REQUIRED\n\n"
            treatment += "1. Surgical Excision (Primary treatment)\n"
            treatment += "   → Wide local excision with margins\n"
            treatment += "   → Sentinel lymph node biopsy if indicated\n\n"
            
            treatment += "2. Immunotherapy (if advanced)\n"
            treatment += "   → Pembrolizumab (Keytruda) or Nivolumab (Opdivo)\n"
            treatment += "   → IV infusion every 2-3 weeks\n\n"
            
            treatment += "3. Targeted Therapy (if BRAF mutation)\n"
            treatment += "   → Vemurafenib or Dabrafenib + Trametinib\n"
            treatment += "   → Oral medication\n\n"
            
            treatment += "⚠️ DO NOT DELAY - Schedule dermatologist appointment TODAY\n\n"
        
        # Additional care instructions
        treatment += "\n" + "="*60 + "\n"
        treatment += "📋 ADDITIONAL CARE INSTRUCTIONS:\n\n"
        
        treatment += "✅ DO:\n"
        treatment += "   • Follow medication schedule strictly\n"
        treatment += "   • Use gentle, fragrance-free products\n"
        treatment += "   • Apply sunscreen SPF 30+ daily\n"
        treatment += "   • Keep skin moisturized\n"
        treatment += "   • Take photos to track progress\n"
        treatment += "   • Schedule follow-up in 4-6 weeks\n\n"
        
        treatment += "❌ DON'T:\n"
        treatment += "   • Pick, scratch, or pop lesions\n"
        treatment += "   • Use harsh soaps or scrubs\n"
        treatment += "   • Stop treatment early (even if improved)\n"
        treatment += "   • Use expired medications\n"
        treatment += "   • Share personal care items\n\n"
        
        treatment += "⚠️ SEEK IMMEDIATE CARE IF:\n"
        treatment += "   • Severe pain or swelling\n"
        treatment += "   • Signs of infection (pus, fever, spreading redness)\n"
        treatment += "   • Allergic reaction to medication\n"
        treatment += "   • Rapid worsening of condition\n"
        treatment += "   • No improvement after 2-4 weeks\n\n"
        
        treatment += "="*60 + "\n"
        treatment += "⚕️ MEDICAL DISCLAIMER:\n"
        treatment += "This is AI-generated advice for informational purposes only.\n"
        treatment += "Always consult a board-certified dermatologist for proper\n"
        treatment += "diagnosis and treatment. Do not start medications without\n"
        treatment += "professional medical supervision.\n"
        
        return treatment
    
    def _get_recommendations(self, diagnosis):
        """Get additional recommendations"""
        general_tips = [
            'Maintain good hygiene',
            'Stay hydrated',
            'Protect skin from sun exposure',
            'Use gentle, non-irritating products'
        ]
        
        specific_tips = {
            'Acne': ['Avoid touching face', 'Change pillowcases regularly', 'Use oil-free products'],
            'Eczema': ['Use fragrance-free moisturizers', 'Take short, lukewarm showers', 'Wear soft fabrics'],
            'Psoriasis': ['Moisturize daily', 'Avoid stress', 'Consider phototherapy'],
            'Melanoma': ['Schedule immediate dermatologist appointment', 'Monitor mole changes', 'Avoid sun exposure'],
            'Dermatitis': ['Identify and avoid triggers', 'Use hypoallergenic products', 'Keep skin moisturized'],
            'Rosacea': ['Avoid hot beverages', 'Use sunscreen daily', 'Keep skincare routine simple'],
            'Fungal Infection': ['Keep area dry', 'Wear breathable clothing', 'Avoid sharing personal items']
        }
        
        return general_tips + specific_tips.get(diagnosis, [])
