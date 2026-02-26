import re
import random
import os
import json

class MedicalChatbot:
    def __init__(self):
        self.model_path = 'models_pretrained/chatbot_model.h5'
        self.disease_db_path = 'data/diseases/disease_database.json'
        
        # Load disease database
        self.disease_database = self._load_disease_database()
        
        # Enhanced Medical knowledge base from loaded data
        self.symptoms_database = self._build_symptoms_database()
        
        self.greetings = ['hello', 'hi', 'hey', 'greetings']
        self.farewells = ['bye', 'goodbye', 'see you', 'thanks']
        
        self.load_model()
    
    def _load_disease_database(self):
        """Load disease database from JSON file"""
        try:
            import json
            if os.path.exists(self.disease_db_path):
                with open(self.disease_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("Warning: Disease database not found. Using default data.")
                return {'diseases': []}
        except Exception as e:
            print(f"Error loading disease database: {e}")
            return {'diseases': []}
    
    def _build_symptoms_database(self):
        """Build symptoms database from disease data"""
        symptoms_db = {}
        
        # Build from loaded disease database
        for disease in self.disease_database.get('diseases', []):
            for symptom in disease.get('symptoms', []):
                symptom_key = symptom.lower().replace(' ', '_')
                
                if symptom_key not in symptoms_db:
                    symptoms_db[symptom_key] = {
                        'conditions': [],
                        'advice': '',
                        'severity': disease.get('severity', 'mild'),
                        'medications': disease.get('medications', [])
                    }
                
                symptoms_db[symptom_key]['conditions'].append(disease['name'])
                
                # Build advice
                meds = ', '.join(disease.get('medications', [])[:3])
                symptoms_db[symptom_key]['advice'] = f"Possible {disease['name']}. Recommended: {meds}. Duration: {disease.get('duration', 'varies')}."
        
        # Add comprehensive symptom database (fallback + enhancement)
        default_symptoms = {
            'fever': {
                'conditions': ['Common Cold', 'Flu', 'Viral Infection', 'Bacterial Infection'],
                'advice': 'Rest, stay hydrated, take fever reducers. Monitor temperature. See a doctor if fever persists over 3 days or exceeds 103°F.',
                'severity': 'mild',
                'medications': ['Acetaminophen 500mg', 'Ibuprofen 400mg', 'Plenty of fluids']
            },
            'fever': {
                'conditions': ['Common Cold', 'Flu', 'Viral Infection', 'Bacterial Infection'],
                'advice': 'Rest, stay hydrated, take fever reducers. Monitor temperature. See a doctor if fever persists over 3 days or exceeds 103°F.',
                'severity': 'mild',
                'medications': ['Acetaminophen 500mg', 'Ibuprofen 400mg', 'Plenty of fluids']
            },
            'headache': {
                'conditions': ['Tension Headache', 'Migraine', 'Dehydration', 'Sinusitis'],
                'advice': 'Rest in quiet, dark room. Stay hydrated. Apply cold/warm compress. Avoid triggers.',
                'severity': 'mild',
                'medications': ['Acetaminophen', 'Ibuprofen', 'Aspirin (if no contraindications)']
            },
            'cough': {
                'conditions': ['Common Cold', 'Bronchitis', 'Allergies', 'Asthma'],
                'advice': 'Stay hydrated, use honey, avoid irritants. Use humidifier. See doctor if persistent or bloody.',
                'severity': 'mild',
                'medications': ['Dextromethorphan', 'Guaifenesin', 'Honey with warm water']
            },
            'sore throat': {
                'conditions': ['Pharyngitis', 'Tonsillitis', 'Viral Infection', 'Strep Throat'],
                'advice': 'Gargle with salt water, stay hydrated, rest voice. Avoid irritants.',
                'severity': 'mild',
                'medications': ['Throat lozenges', 'Warm salt water gargle', 'Acetaminophen for pain']
            },
            'chest pain': {
                'conditions': ['Heart Attack', 'Angina', 'Anxiety', 'Costochondritis'],
                'advice': 'URGENT: Seek immediate medical attention. Call 911 if severe, radiating pain, or with other symptoms.',
                'severity': 'severe',
                'medications': ['DO NOT SELF-MEDICATE - SEEK EMERGENCY CARE']
            },
            'shortness of breath': {
                'conditions': ['Asthma', 'Pneumonia', 'Heart Problems', 'Anxiety'],
                'advice': 'Seek medical attention immediately. Use prescribed inhaler if available. Call 911 if severe.',
                'severity': 'severe',
                'medications': ['Use prescribed inhaler', 'SEEK EMERGENCY CARE']
            },
            'stomach pain': {
                'conditions': ['Indigestion', 'Gastritis', 'Appendicitis', 'Ulcer'],
                'advice': 'Avoid spicy/fatty foods, eat bland diet. If severe, persistent, or in lower right abdomen, seek immediate care.',
                'severity': 'moderate',
                'medications': ['Antacids', 'Avoid NSAIDs', 'Bland diet (BRAT)']
            },
            'abdominal pain': {
                'conditions': ['Gastroenteritis', 'IBS', 'Appendicitis', 'Constipation'],
                'advice': 'Monitor location and severity. Avoid solid foods if severe. Seek care if persistent or worsening.',
                'severity': 'moderate',
                'medications': ['Antacids', 'Anti-gas medication', 'Stay hydrated']
            },
            'nausea': {
                'conditions': ['Food Poisoning', 'Gastroenteritis', 'Pregnancy', 'Migraine'],
                'advice': 'Stay hydrated with small sips. Eat bland foods (crackers, toast). Rest. Avoid strong smells.',
                'severity': 'mild',
                'medications': ['Ginger tea', 'Small sips of water', 'Ondansetron if prescribed']
            },
            'vomiting': {
                'conditions': ['Gastroenteritis', 'Food Poisoning', 'Migraine', 'Pregnancy'],
                'advice': 'Stay hydrated. Avoid solid foods initially. Seek care if persistent, bloody, or with severe pain.',
                'severity': 'moderate',
                'medications': ['Oral rehydration solution', 'Clear liquids', 'Anti-emetics if prescribed']
            },
            'diarrhea': {
                'conditions': ['Gastroenteritis', 'Food Poisoning', 'IBS', 'Infection'],
                'advice': 'Stay hydrated with electrolyte solutions. Eat bland foods. Avoid dairy. See doctor if bloody or persistent.',
                'severity': 'moderate',
                'medications': ['Oral rehydration solution', 'Loperamide (if no fever)', 'Probiotics']
            },
            'dizziness': {
                'conditions': ['Low Blood Pressure', 'Dehydration', 'Inner Ear Problem', 'Anemia'],
                'advice': 'Sit or lie down immediately. Stay hydrated. Avoid sudden movements. See doctor if frequent.',
                'severity': 'moderate',
                'medications': ['Increase fluid intake', 'Avoid sudden position changes']
            },
            'fatigue': {
                'conditions': ['Anemia', 'Sleep Deprivation', 'Thyroid Issues', 'Depression'],
                'advice': 'Ensure 7-8 hours sleep, balanced diet, regular exercise. See doctor if persistent.',
                'severity': 'mild',
                'medications': ['Multivitamin', 'Iron supplement (if anemic)', 'Improve sleep hygiene']
            },
            'weakness': {
                'conditions': ['Anemia', 'Dehydration', 'Electrolyte Imbalance', 'Chronic Illness'],
                'advice': 'Rest, stay hydrated, eat nutritious meals. See doctor if sudden or severe.',
                'severity': 'moderate',
                'medications': ['Electrolyte drinks', 'Nutritious diet', 'Rest']
            },
            'rash': {
                'conditions': ['Allergic Reaction', 'Eczema', 'Contact Dermatitis', 'Viral Infection'],
                'advice': 'Avoid irritants, use gentle moisturizers. Antihistamines may help. See doctor if spreading.',
                'severity': 'mild',
                'medications': ['Hydrocortisone cream 1%', 'Antihistamine (Benadryl)', 'Calamine lotion']
            },
            'itching': {
                'conditions': ['Allergic Reaction', 'Dry Skin', 'Eczema', 'Insect Bite'],
                'advice': 'Avoid scratching, use moisturizers, take cool baths. Antihistamines may help.',
                'severity': 'mild',
                'medications': ['Antihistamine', 'Moisturizing cream', 'Hydrocortisone cream']
            },
            'back pain': {
                'conditions': ['Muscle Strain', 'Poor Posture', 'Herniated Disc', 'Kidney Issues'],
                'advice': 'Rest, apply heat/ice, gentle stretching. Maintain good posture. See doctor if severe or persistent.',
                'severity': 'moderate',
                'medications': ['Ibuprofen', 'Acetaminophen', 'Muscle relaxants (if prescribed)']
            },
            'joint pain': {
                'conditions': ['Arthritis', 'Injury', 'Gout', 'Infection'],
                'advice': 'Rest affected joint, apply ice, elevate. Gentle movement. See doctor if swollen or persistent.',
                'severity': 'moderate',
                'medications': ['Ibuprofen', 'Acetaminophen', 'Ice packs']
            },
            'muscle pain': {
                'conditions': ['Overexertion', 'Strain', 'Flu', 'Fibromyalgia'],
                'advice': 'Rest, apply heat, gentle stretching. Stay hydrated. Massage may help.',
                'severity': 'mild',
                'medications': ['Ibuprofen', 'Acetaminophen', 'Warm compress']
            },
            'runny nose': {
                'conditions': ['Common Cold', 'Allergies', 'Sinusitis', 'Flu'],
                'advice': 'Stay hydrated, use saline spray, rest. Avoid irritants. See doctor if persistent.',
                'severity': 'mild',
                'medications': ['Decongestant', 'Antihistamine', 'Saline nasal spray']
            },
            'congestion': {
                'conditions': ['Common Cold', 'Sinusitis', 'Allergies', 'Flu'],
                'advice': 'Use humidifier, stay hydrated, steam inhalation. Elevate head while sleeping.',
                'severity': 'mild',
                'medications': ['Decongestant', 'Saline spray', 'Steam inhalation']
            },
            'sneezing': {
                'conditions': ['Allergies', 'Common Cold', 'Irritants', 'Flu'],
                'advice': 'Avoid allergens, stay hydrated, rest. Use tissues and wash hands frequently.',
                'severity': 'mild',
                'medications': ['Antihistamine', 'Decongestant', 'Avoid triggers']
            }
        }
        
        # Merge loaded data with default symptoms
        for symptom, data in default_symptoms.items():
            if symptom not in symptoms_db:
                symptoms_db[symptom] = data
            else:
                # Merge medications
                existing_meds = set(symptoms_db[symptom].get('medications', []))
                new_meds = set(data.get('medications', []))
                symptoms_db[symptom]['medications'] = list(existing_meds | new_meds)
        
        return symptoms_db
        
        self.greetings = ['hello', 'hi', 'hey', 'greetings']
        self.farewells = ['bye', 'goodbye', 'see you', 'thanks']
        
        self.load_model()
    
    def load_model(self):
        """Load the chatbot model"""
        try:
            # In production, load actual NLP model (BERT, GPT, etc.)
            print("Chatbot model loaded (demo mode)")
        except Exception as e:
            print(f"Model loading error: {e}")
    
    def get_response(self, message):
        """Generate response to user message"""
        message_lower = message.lower().strip()
        
        # Handle greetings
        if any(greeting in message_lower for greeting in self.greetings):
            return "Hello! I'm your medical AI assistant. Please describe your symptoms, and I'll provide medical advice. Remember, I'm not a replacement for professional medical care."
        
        # Handle farewells
        if any(farewell in message_lower for farewell in self.farewells):
            return "Take care! Remember to consult with a healthcare professional for serious concerns. Stay healthy!"
        
        # Handle emergency keywords
        if any(word in message_lower for word in ['emergency', 'urgent', 'severe pain', 'can\'t breathe', 'heart attack']):
            return "⚠️ EMERGENCY: Please call emergency services (911) immediately or go to the nearest emergency room. This is a medical emergency that requires immediate professional attention."
        
        # Analyze symptoms
        detected_symptoms = self._detect_symptoms(message_lower)
        
        if detected_symptoms:
            return self._generate_medical_advice(detected_symptoms)
        else:
            return self._general_response(message_lower)
    
    def _detect_symptoms(self, message):
        """Detect symptoms mentioned in message"""
        detected = []
        
        for symptom in self.symptoms_database.keys():
            if symptom in message:
                detected.append(symptom)
        
        return detected
    
    def _generate_medical_advice(self, symptoms):
        """Generate comprehensive medical advice based on symptoms"""
        if not symptoms:
            return "I couldn't identify specific symptoms. Could you please describe what you're experiencing?"
        
        response = "🏥 MEDICAL ANALYSIS REPORT\n"
        response += "="*50 + "\n\n"
        
        # Collect all data
        all_conditions = {}  # condition: count
        all_medications = {}  # medication: [symptoms]
        all_advice = []
        max_severity = 'mild'
        severity_scores = {'mild': 1, 'moderate': 2, 'severe': 3}
        
        # Analyze each symptom
        for symptom in symptoms:
            symptom_data = self.symptoms_database.get(symptom, {})
            
            # Count conditions
            for condition in symptom_data.get('conditions', []):
                all_conditions[condition] = all_conditions.get(condition, 0) + 1
            
            # Collect medications
            for med in symptom_data.get('medications', []):
                if med not in all_medications:
                    all_medications[med] = []
                all_medications[med].append(symptom)
            
            all_advice.append(symptom_data.get('advice', ''))
            
            # Update severity
            symptom_severity = symptom_data.get('severity', 'mild')
            if severity_scores.get(symptom_severity, 0) > severity_scores.get(max_severity, 0):
                max_severity = symptom_severity
        
        # Sort conditions by frequency
        sorted_conditions = sorted(all_conditions.items(), key=lambda x: x[1], reverse=True)
        
        # Build response
        response += f"🔍 SYMPTOMS DETECTED: {', '.join(symptoms).upper()}\n\n"
        
        # Most likely conditions
        response += "📋 MOST LIKELY CONDITIONS:\n"
        for i, (condition, count) in enumerate(sorted_conditions[:3], 1):
            confidence = min(95, 60 + (count * 15))
            response += f"   {i}. {condition} (Confidence: {confidence}%)\n"
        response += "\n"
        
        # Severity assessment
        severity_emoji = {'mild': '🟢', 'moderate': '🟡', 'severe': '🔴'}
        response += f"⚠️ SEVERITY LEVEL: {severity_emoji.get(max_severity, '🟢')} {max_severity.upper()}\n\n"
        
        # Recommended medications with detailed info
        response += "💊 RECOMMENDED MEDICATIONS:\n"
        response += "-" * 50 + "\n"
        
        sorted_meds = sorted(all_medications.items(), key=lambda x: len(x[1]), reverse=True)
        for i, (med, related_symptoms) in enumerate(sorted_meds[:8], 1):
            response += f"\n{i}. {med}\n"
            response += f"   → For: {', '.join(related_symptoms)}\n"
            
            # Add dosage and timing info
            dosage_info = self._get_dosage_info(med)
            if dosage_info:
                response += f"   → Dosage: {dosage_info['dose']}\n"
                response += f"   → Timing: {dosage_info['timing']}\n"
                response += f"   → Duration: {dosage_info['duration']}\n"
        
        response += "\n" + "-" * 50 + "\n\n"
        
        # Detailed medical advice
        response += "📝 DETAILED MEDICAL ADVICE:\n"
        for i, advice in enumerate(all_advice[:5], 1):
            if advice:
                response += f"{i}. {advice}\n"
        response += "\n"
        
        # Additional recommendations
        response += "✅ ADDITIONAL RECOMMENDATIONS:\n"
        recommendations = self._get_symptom_specific_recommendations(symptoms, max_severity)
        for i, rec in enumerate(recommendations, 1):
            response += f"   • {rec}\n"
        response += "\n"
        
        # When to seek immediate care
        if max_severity == 'severe':
            response += "🚨 URGENT - SEEK IMMEDIATE MEDICAL ATTENTION:\n"
            response += "   • Your symptoms may indicate a serious condition\n"
            response += "   • Go to emergency room or call 911\n"
            response += "   • Do not delay medical care\n\n"
        elif max_severity == 'moderate':
            response += "⚠️ IMPORTANT:\n"
            response += "   • Consult a healthcare provider within 24-48 hours\n"
            response += "   • Monitor symptoms closely\n"
            response += "   • Seek immediate care if symptoms worsen\n\n"
        else:
            response += "✅ FOLLOW-UP:\n"
            response += "   • Symptoms typically mild\n"
            response += "   • Self-care measures should help\n"
            response += "   • Consult doctor if symptoms persist > 7 days\n\n"
        
        # Expected timeline
        response += "⏱️ EXPECTED TIMELINE:\n"
        timeline = self._get_treatment_timeline(sorted_conditions)
        response += f"   • Improvement expected: {timeline['improvement']}\n"
        response += f"   • Full recovery: {timeline['recovery']}\n\n"
        
        response += "="*50 + "\n"
        response += "⚕️ MEDICAL DISCLAIMER:\n"
        response += "This is AI-generated advice for informational purposes only.\n"
        response += "Always consult qualified healthcare professionals for diagnosis and treatment.\n"
        
        return response
    
    def _get_dosage_info(self, medication):
        """Get detailed dosage information for medication"""
        dosage_database = {
            'Acetaminophen 500mg': {
                'dose': '500mg per dose',
                'timing': 'Every 4-6 hours as needed',
                'duration': 'Maximum 3000mg per day, up to 7 days'
            },
            'Ibuprofen 400mg': {
                'dose': '400mg per dose',
                'timing': 'Every 6-8 hours with food',
                'duration': 'Maximum 1200mg per day, up to 10 days'
            },
            'Acetaminophen': {
                'dose': '500-1000mg per dose',
                'timing': 'Every 4-6 hours',
                'duration': 'Do not exceed 3000mg daily'
            },
            'Ibuprofen': {
                'dose': '200-400mg per dose',
                'timing': 'Every 6-8 hours with food',
                'duration': 'Short-term use only'
            },
            'Decongestant': {
                'dose': 'As directed on package',
                'timing': 'Usually every 12 hours',
                'duration': 'Maximum 3-5 days'
            },
            'Antihistamine': {
                'dose': 'As directed (e.g., 25-50mg)',
                'timing': 'Once daily or as needed',
                'duration': 'Continue as long as symptoms persist'
            },
            'Albuterol inhaler': {
                'dose': '2 puffs',
                'timing': 'Every 4-6 hours as needed',
                'duration': 'Use as prescribed by doctor'
            },
            'Hydrocortisone cream 1%': {
                'dose': 'Thin layer',
                'timing': 'Apply 2-3 times daily',
                'duration': 'Up to 7 days'
            }
        }
        
        # Try exact match first
        if medication in dosage_database:
            return dosage_database[medication]
        
        # Try partial match
        for key in dosage_database:
            if key.lower() in medication.lower() or medication.lower() in key.lower():
                return dosage_database[key]
        
        return None
    
    def _get_symptom_specific_recommendations(self, symptoms, severity):
        """Get specific recommendations based on symptoms"""
        recommendations = []
        
        # General recommendations
        recommendations.extend([
            'Stay well hydrated (8-10 glasses of water daily)',
            'Get adequate rest (7-9 hours of sleep)',
            'Maintain good hygiene (wash hands frequently)'
        ])
        
        # Symptom-specific
        if any(s in symptoms for s in ['fever', 'high_fever']):
            recommendations.extend([
                'Monitor temperature every 4 hours',
                'Use cool compresses if fever is high',
                'Avoid bundling up excessively'
            ])
        
        if any(s in symptoms for s in ['cough', 'persistent_cough']):
            recommendations.extend([
                'Use humidifier or steam inhalation',
                'Avoid irritants (smoke, strong odors)',
                'Try honey for throat soothing (if over 1 year old)'
            ])
        
        if any(s in symptoms for s in ['nausea', 'vomiting', 'stomach_pain']):
            recommendations.extend([
                'Eat bland foods (BRAT diet: Bananas, Rice, Applesauce, Toast)',
                'Avoid spicy, fatty, or acidic foods',
                'Small frequent meals instead of large meals'
            ])
        
        if any(s in symptoms for s in ['headache', 'severe_headache']):
            recommendations.extend([
                'Rest in quiet, dark room',
                'Apply cold or warm compress to head',
                'Avoid screens and bright lights'
            ])
        
        if severity == 'severe':
            recommendations.insert(0, '🚨 PRIORITY: Seek immediate medical attention')
        
        return recommendations[:8]  # Return top 8
    
    def _get_treatment_timeline(self, conditions):
        """Get expected treatment timeline"""
        if not conditions:
            return {'improvement': '3-5 days', 'recovery': '1-2 weeks'}
        
        # Get most likely condition
        top_condition = conditions[0][0] if conditions else 'Unknown'
        
        timelines = {
            'Common Cold': {'improvement': '3-5 days', 'recovery': '7-10 days'},
            'Flu': {'improvement': '3-7 days', 'recovery': '1-2 weeks'},
            'Pneumonia': {'improvement': '1-2 weeks', 'recovery': '3-4 weeks'},
            'Asthma': {'improvement': 'Hours with medication', 'recovery': 'Chronic management'},
            'Bronchitis': {'improvement': '1 week', 'recovery': '2-3 weeks'},
            'Gastroenteritis': {'improvement': '1-3 days', 'recovery': '3-7 days'},
            'Migraine': {'improvement': '4-72 hours', 'recovery': 'Varies'},
            'Hypertension': {'improvement': 'Weeks', 'recovery': 'Chronic management'},
            'Type 2 Diabetes': {'improvement': 'Weeks to months', 'recovery': 'Chronic management'},
            'Urinary Tract Infection': {'improvement': '2-3 days', 'recovery': '5-7 days'}
        }
        
        return timelines.get(top_condition, {'improvement': '3-7 days', 'recovery': '1-2 weeks'})
    
    def _get_medications(self, symptoms):
        """Get medication recommendations based on symptoms"""
        medications = []
        
        medication_map = {
            'fever': ['Acetaminophen (Tylenol) 500mg every 6 hours', 'Ibuprofen (Advil) 400mg every 6-8 hours'],
            'headache': ['Acetaminophen 500mg', 'Ibuprofen 400mg', 'Rest in dark room'],
            'cough': ['Dextromethorphan (cough suppressant)', 'Honey and warm water', 'Guaifenesin (expectorant)'],
            'chest pain': ['SEEK EMERGENCY CARE - Do not self-medicate', 'Call 911 immediately'],
            'shortness of breath': ['SEEK EMERGENCY CARE', 'Use prescribed inhaler if available'],
            'stomach pain': ['Antacids (Tums, Rolaids)', 'Avoid spicy foods', 'Drink plenty of water'],
            'nausea': ['Ondansetron (Zofran) if prescribed', 'Ginger tea', 'Small sips of water'],
            'dizziness': ['Sit or lie down', 'Drink water', 'Avoid sudden movements'],
            'fatigue': ['Multivitamin supplement', 'Iron supplement if anemic', 'Ensure 7-8 hours sleep'],
            'rash': ['Hydrocortisone cream 1%', 'Antihistamine (Benadryl)', 'Calamine lotion']
        }
        
        for symptom in symptoms:
            if symptom in medication_map:
                medications.extend(medication_map[symptom])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_meds = []
        for med in medications:
            if med not in seen:
                seen.add(med)
                unique_meds.append(med)
        
        return unique_meds if unique_meds else ['Consult a healthcare provider for appropriate medication']
    
    def _general_response(self, message):
        """Generate general response for non-symptom queries"""
        if 'how' in message and 'work' in message:
            return "I'm an AI medical assistant that analyzes symptoms and provides health advice. I can help with:\n• Skin condition analysis\n• Lab report interpretation\n• Symptom assessment\n• Sound/cough analysis\n\nHow can I help you today?"
        
        if 'what' in message and ('do' in message or 'should' in message):
            return "Please describe your symptoms in detail, and I'll provide appropriate medical advice. For example, tell me if you're experiencing pain, fever, cough, or any other symptoms."
        
        if 'help' in message:
            return "I'm here to help! You can:\n• Describe your symptoms for medical advice\n• Upload skin images for analysis\n• Upload lab reports for interpretation\n• Record cough sounds for respiratory analysis\n\nWhat would you like to do?"
        
        # Default response
        responses = [
            "I'm not sure I understand. Could you describe your symptoms or health concerns?",
            "Please provide more details about what you're experiencing.",
            "I'm here to help with medical questions. What symptoms are you experiencing?",
            "Could you elaborate on your health concern? I'm here to assist."
        ]
        
        return random.choice(responses)
