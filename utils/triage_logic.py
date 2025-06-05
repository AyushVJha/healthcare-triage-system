from typing import Dict, List, Tuple
import numpy as np
from datetime import datetime, timedelta

class TriageLogic:
    def __init__(self):
        self.priority_weights = {
            'CRITICAL': 1.0,
            'URGENT': 0.8,
            'MODERATE': 0.5,
            'LOW': 0.2
        }
        
        self.wait_time_thresholds = {
            'CRITICAL': timedelta(minutes=15),
            'URGENT': timedelta(hours=1),
            'MODERATE': timedelta(hours=3),
            'LOW': timedelta(hours=4)
        }
    
    def calculate_queue_position(self, 
                               severity_score: float, 
                               arrival_time: datetime,
                               current_queue: List[Dict]) -> Tuple[int, str]:
        """Calculate patient's position in queue"""
        priority = self._get_priority_level(severity_score)
        weight = self.priority_weights[priority]
        
        # Calculate weighted position
        position = 1
        for patient in current_queue:
            if self.priority_weights[patient['priority']] > weight:
                position += 1
        
        return position, priority
    
    def estimate_wait_time(self, 
                          queue_position: int, 
                          priority: str,
                          avg_processing_time: timedelta = timedelta(minutes=15)) -> str:
        """Estimate wait time based on queue position and priority"""
        base_wait = queue_position * avg_processing_time
        priority_factor = self.priority_weights[priority]
        
        # Adjust wait time based on priority
        adjusted_wait = base_wait * (1 - priority_factor)
        
        # Ensure wait time doesn't exceed threshold
        max_wait = self.wait_time_thresholds[priority]
        final_wait = min(adjusted_wait, max_wait)
        
        return self._format_wait_time(final_wait)
    
    def _get_priority_level(self, severity_score: float) -> str:
        """Convert severity score to priority level"""
        if severity_score >= 8:
            return "CRITICAL"
        elif severity_score >= 6:
            return "URGENT"
        elif severity_score >= 4:
            return "MODERATE"
        else:
            return "LOW"
    
    def _format_wait_time(self, wait_time: timedelta) -> str:
        """Format wait time for display"""
        if wait_time < timedelta(minutes=1):
            return "Immediate"
        elif wait_time < timedelta(hours=1):
            minutes = int(wait_time.total_seconds() / 60)
            return f"{minutes} minutes"
        else:
            hours = int(wait_time.total_seconds() / 3600)
            minutes = int((wait_time.total_seconds() % 3600) / 60)
            if minutes == 0:
                return f"{hours} hours"
            return f"{hours} hours {minutes} minutes"
    
    def calculate_resource_allocation(self, 
                                    severity_score: float,
                                    specialty: str) -> Dict[str, str]:
        """Calculate resource allocation based on severity and specialty"""
        priority = self._get_priority_level(severity_score)
        
        resources = {
            'room_type': self._get_room_type(priority),
            'staff_level': self._get_staff_level(priority),
            'equipment': self._get_equipment(priority, specialty)
        }
        
        return resources
    
    def _get_room_type(self, priority: str) -> str:
        """Determine appropriate room type"""
        room_types = {
            'CRITICAL': 'Emergency Room',
            'URGENT': 'Urgent Care Room',
            'MODERATE': 'Examination Room',
            'LOW': 'Consultation Room'
        }
        return room_types[priority]
    
    def _get_staff_level(self, priority: str) -> str:
        """Determine required staff level"""
        staff_levels = {
            'CRITICAL': 'Emergency Team',
            'URGENT': 'Urgent Care Team',
            'MODERATE': 'Nurse + Doctor',
            'LOW': 'Nurse'
        }
        return staff_levels[priority]
    
    def _get_equipment(self, priority: str, specialty: str) -> List[str]:
        """Determine required equipment"""
        base_equipment = {
            'CRITICAL': ['Defibrillator', 'Ventilator', 'IV Supplies'],
            'URGENT': ['IV Supplies', 'Monitoring Equipment'],
            'MODERATE': ['Basic Medical Supplies'],
            'LOW': ['Basic Medical Supplies']
        }
        
        specialty_equipment = {
            'Cardiology': ['ECG Machine', 'Blood Pressure Monitor'],
            'Neurology': ['Neurological Assessment Kit'],
            'Dermatology': ['Dermatoscope', 'Skin Biopsy Kit'],
            'Orthopedics': ['X-ray Machine', 'Splinting Supplies']
        }
        
        equipment = base_equipment[priority].copy()
        if specialty in specialty_equipment:
            equipment.extend(specialty_equipment[specialty])
        
        return equipment 