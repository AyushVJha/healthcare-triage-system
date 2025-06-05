import pandas as pd
import numpy as np
from typing import Dict, List
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LightweightSymptomAnalyzer:
    def __init__(self):
        # Lightweight rule-based approach instead of heavy BERT models
        self.severity_keywords = {
            'critical': {
                'keywords': ['chest pain', 'difficulty breathing', 'severe bleeding', 'unconscious', 'stroke', 'heart attack', 'severe allergic reaction'],
                'score': 10
            },
            'urgent': {
                'keywords': ['high fever', 'severe pain', 'vomiting blood', 'severe headache', 'difficulty swallowing', 'severe burns'],
                'score': 7
            },
            'moderate': {
                'keywords': ['fever', 'headache', 'nausea', 'dizziness', 'fatigue', 'cough', 'stomach pain'],
                'score': 4
            },
            'low': {
                'keywords': ['mild pain', 'runny nose', 'slight fever', 'minor cut', 'bruise', 'sore throat'],
                'score': 2
            }
        }
        
        self.specialty_mapping = {
            'Emergency': ['chest pain', 'difficulty breathing', 'severe bleeding', 'unconscious', 'stroke'],
            'Cardiology': ['chest pain', 'heart palpitations', 'shortness of breath', 'irregular heartbeat'],
            'Neurology': ['headache', 'dizziness', 'seizure', 'numbness', 'confusion', 'memory loss'],
            'Gastroenterology': ['stomach pain', 'nausea', 'vomiting', 'diarrhea', 'constipation', 'acid reflux'],
            'Dermatology': ['rash', 'skin irritation', 'itching', 'acne', 'mole changes', 'skin lesion'],
            'Orthopedics': ['joint pain', 'back pain', 'fracture', 'sprain', 'muscle pain', 'bone pain'],
            'General Practice': ['fever', 'fatigue', 'general discomfort', 'cold symptoms', 'flu symptoms']
        }
        
        # Initialize lightweight TF-IDF vectorizer for symptom matching
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self._initialize_symptom_database()
    
    def _initialize_symptom_database(self):
        """Initialize lightweight symptom database"""
        self.symptom_database = []
        for severity, data in self.severity_keywords.items():
            for keyword in data['keywords']:
                self.symptom_database.append({
                    'symptom': keyword,
                    'severity': severity,
                    'score': data['score']
                })
    
    def analyze_symptoms(self, symptom_text: str) -> Dict:
        """Analyze symptoms with minimal resource usage"""
        cleaned_text = self._clean_text(symptom_text)
        
        # Calculate severity using keyword matching
        severity_score = self._calculate_severity_lightweight(cleaned_text)
        
        # Determine specialty
        specialty = self._determine_specialty_lightweight(cleaned_text)
        
        # Calculate priority
        priority = self._calculate_priority(severity_score)
        
        # Extract key symptoms
        key_symptoms = self._extract_key_symptoms(cleaned_text)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(severity_score, specialty)
        
        return {
            'severity_score': round(severity_score, 2),
            'priority_level': priority,
            'recommended_specialty': specialty,
            'key_symptoms': key_symptoms,
            'recommendations': recommendations,
            'estimated_wait_time': self._estimate_wait_time(priority),
            'urgency_flag': severity_score > 7,
            'confidence_score': self._calculate_confidence(cleaned_text)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _calculate_severity_lightweight(self, text: str) -> float:
        """Calculate severity using lightweight keyword matching"""
        total_score = 0
        matches = 0
        
        for severity, data in self.severity_keywords.items():
            for keyword in data['keywords']:
                if keyword in text:
                    total_score += data['score']
                    matches += 1
        
        if matches == 0:
            return 3.0  # Default moderate score
        
        # Normalize score
        avg_score = total_score / matches
        return min(avg_score, 10.0)
    
    def _determine_specialty_lightweight(self, text: str) -> str:
        """Determine specialty using keyword matching"""
        specialty_scores = {}
        
        for specialty, keywords in self.specialty_mapping.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            specialty_scores[specialty] = score
        
        if not any(specialty_scores.values()):
            return 'General Practice'
        
        return max(specialty_scores, key=specialty_scores.get)
    
    def _calculate_priority(self, severity_score: float) -> str:
        """Calculate priority level"""
        if severity_score >= 8:
            return "CRITICAL"
        elif severity_score >= 6:
            return "URGENT"
        elif severity_score >= 4:
            return "MODERATE"
        else:
            return "LOW"
    
    def _extract_key_symptoms(self, text: str) -> List[str]:
        """Extract key symptoms from text"""
        found_symptoms = []
        for severity_data in self.severity_keywords.values():
            for keyword in severity_data['keywords']:
                if keyword in text:
                    found_symptoms.append(keyword)
        
        return list(set(found_symptoms))[:5]
    
    def _generate_recommendations(self, severity_score: float, specialty: str) -> List[str]:
        """Generate medical recommendations"""
        recommendations = []
        
        if severity_score >= 8:
            recommendations = [
                "🚨 Seek immediate emergency care",
                "📞 Call emergency services if symptoms worsen",
                "🚫 Do not drive yourself to hospital",
                "⏰ Time-sensitive condition - act now"
            ]
        elif severity_score >= 6:
            recommendations = [
                f"⚡ Schedule urgent appointment with {specialty}",
                "👀 Monitor symptoms closely",
                "🕐 Seek care within 24 hours",
                "📝 Document symptom progression"
            ]
        elif severity_score >= 4:
            recommendations = [
                f"📅 Schedule appointment with {specialty}",
                "📊 Monitor symptoms for changes",
                "💊 Consider appropriate over-the-counter remedies",
                "🏠 Rest and maintain hydration"
            ]
        else:
            recommendations = [
                f"📋 Routine consultation with {specialty} if symptoms persist",
                "🏠 Home care and monitoring",
                "💊 Over-the-counter remedies may help",
                "📞 Contact healthcare provider if symptoms worsen"
            ]
        
        return recommendations
    
    def _estimate_wait_time(self, priority: str) -> str:
        """Estimate wait time based on priority"""
        wait_times = {
            "CRITICAL": "Immediate (0-15 minutes)",
            "URGENT": "Priority (30-60 minutes)",
            "MODERATE": "Standard (1-3 hours)",
            "LOW": "Routine (2-4 hours)"
        }
        return wait_times.get(priority, "2-4 hours")
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score based on symptom specificity"""
        word_count = len(text.split())
        symptom_matches = sum(1 for severity_data in self.severity_keywords.values() 
                            for keyword in severity_data['keywords'] if keyword in text)
        
        if word_count == 0:
            return 0.0
        
        confidence = min((symptom_matches / word_count) * 100, 95.0)
        return round(confidence, 1)
