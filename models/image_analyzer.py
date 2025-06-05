import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Dict, List

class LightweightImageAnalyzer:
    def __init__(self):
        # Lightweight image analysis without heavy ML models
        self.skin_conditions_rules = {
            'redness_threshold': 150,
            'texture_variance_threshold': 1000,
            'color_uniformity_threshold': 50
        }
        
        self.analysis_categories = {
            'skin': ['rash', 'lesion', 'discoloration', 'texture_change'],
            'wound': ['cut', 'bruise', 'burn', 'swelling'],
            'general': ['inflammation', 'abnormal_growth', 'color_change']
        }
    
    def analyze_image(self, image_data, image_type: str = "skin") -> Dict:
        """Analyze medical image using lightweight computer vision"""
        try:
            # Convert image data
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Perform lightweight analysis
            analysis_results = self._analyze_image_features(cv_image, image_type)
            
            return {
                'image_type': image_type,
                'analysis_results': analysis_results,
                'recommendations': self._generate_image_recommendations(analysis_results),
                'confidence_score': analysis_results.get('confidence', 0.0),
                'requires_professional_review': analysis_results.get('severity_score', 0) > 6
            }
            
        except Exception as e:
            return {
                'error': f"Image analysis failed: {str(e)}",
                'recommendations': ["Please consult healthcare professional for proper evaluation"],
                'confidence_score': 0.0,
                'requires_professional_review': True
            }
    
    def _analyze_image_features(self, image: np.ndarray, image_type: str) -> Dict:
        """Analyze image features using basic computer vision"""
        # Resize image for consistent analysis
        height, width = image.shape[:2]
        if width > 512:
            scale = 512 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        # Basic color analysis
        color_analysis = self._analyze_colors(image)
        
        # Texture analysis
        texture_analysis = self._analyze_texture(image)
        
        # Shape analysis
        shape_analysis = self._analyze_shapes(image)
        
        # Calculate overall severity
        severity_score = self._calculate_image_severity(color_analysis, texture_analysis, shape_analysis)
        
        return {
            'color_analysis': color_analysis,
            'texture_analysis': texture_analysis,
            'shape_analysis': shape_analysis,
            'severity_score': severity_score,
            'confidence': min(85.0, max(40.0, severity_score * 10)),
            'findings': self._generate_findings(color_analysis, texture_analysis, shape_analysis)
        }
    
    def _analyze_colors(self, image: np.ndarray) -> Dict:
        """Analyze color distribution in image"""
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Calculate color statistics
        mean_hue = np.mean(hsv[:,:,0])
        mean_saturation = np.mean(hsv[:,:,1])
        mean_value = np.mean(hsv[:,:,2])
        
        # Detect redness (potential inflammation)
        red_mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red_percentage = (np.sum(red_mask > 0) / red_mask.size) * 100
        
        return {
            'mean_hue': float(mean_hue),
            'mean_saturation': float(mean_saturation),
            'mean_brightness': float(mean_value),
            'red_percentage': float(red_percentage),
            'color_uniformity': float(np.std(hsv[:,:,0]))
        }
    
    def _analyze_texture(self, image: np.ndarray) -> Dict:
        """Analyze texture patterns"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate texture variance
        texture_variance = float(np.var(gray))
        
        # Edge detection for texture analysis
        edges = cv2.Canny(gray, 50, 150)
        edge_density = (np.sum(edges > 0) / edges.size) * 100
        
        return {
            'texture_variance': texture_variance,
            'edge_density': float(edge_density),
            'smoothness': float(100 - edge_density)
        }
    
    def _analyze_shapes(self, image: np.ndarray) -> Dict:
        """Analyze shapes and contours"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Find contours
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze contour properties
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Calculate circularity
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
            else:
                circularity = 0
        else:
            area = 0
            perimeter = 0
            circularity = 0
        
        return {
            'contour_count': len(contours),
            'largest_area': float(area),
            'circularity': float(circularity),
            'irregularity_score': float(1 - circularity) if circularity > 0 else 1.0
        }
    
    def _calculate_image_severity(self, color_analysis: Dict, texture_analysis: Dict, shape_analysis: Dict) -> float:
        """Calculate severity score based on image analysis"""
        severity = 0
        
        # Color-based severity
        if color_analysis['red_percentage'] > 20:
            severity += 3
        if color_analysis['color_uniformity'] > 50:
            severity += 2
        
        # Texture-based severity
        if texture_analysis['texture_variance'] > 1000:
            severity += 2
        if texture_analysis['edge_density'] > 30:
            severity += 1
        
        # Shape-based severity
        if shape_analysis['irregularity_score'] > 0.7:
            severity += 2
        if shape_analysis['contour_count'] > 5:
            severity += 1
        
        return min(severity, 10)
    
    def _generate_findings(self, color_analysis: Dict, texture_analysis: Dict, shape_analysis: Dict) -> List[str]:
        """Generate findings based on analysis"""
        findings = []
        
        if color_analysis['red_percentage'] > 15:
            findings.append("Possible inflammation or irritation detected")
        
        if texture_analysis['texture_variance'] > 1500:
            findings.append("Irregular texture patterns observed")
        
        if shape_analysis['irregularity_score'] > 0.6:
            findings.append("Irregular shape characteristics noted")
        
        if color_analysis['color_uniformity'] > 60:
            findings.append("Non-uniform coloration detected")
        
        if not findings:
            findings.append("No significant abnormalities detected in basic analysis")
        
        return findings
    
    def _generate_image_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate recommendations based on image analysis"""
        severity = analysis_results.get('severity_score', 0)
        
        if severity >= 7:
            return [
                "🚨 Immediate medical attention recommended",
                "📸 Document changes with photos",
                "🏥 Visit emergency care or urgent care center",
                "📝 Note any associated symptoms"
            ]
        elif severity >= 4:
            return [
                "👨‍⚕️ Schedule appointment with healthcare provider",
                "📊 Monitor for changes",
                "📸 Take photos to track progression",
                "🩺 Consider dermatology consultation if skin-related"
            ]
        else:
            return [
                "👀 Continue monitoring",
                "🏠 Basic home care may be sufficient",
                "📞 Contact healthcare provider if symptoms worsen",
                "📝 Keep record of any changes"
            ]
