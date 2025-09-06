import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    """Configuration settings for the AI Task Adventure app."""
    
    # App metadata
    APP_NAME = "AI Task Adventure"
    VERSION = "1.0.0"
    DESCRIPTION = "A gamified task management application"
    
    # Streamlit configuration
    PAGE_TITLE = "AI Task Adventure"
    PAGE_ICON = "🎯"
    LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # Points system
    POINTS_HIGH_PRIORITY = 15
    POINTS_MEDIUM_PRIORITY = 10
    POINTS_LOW_PRIORITY = 5
    
    # Achievement thresholds
    FIRST_TASK_THRESHOLD = 1
    GETTING_STARTED_THRESHOLD = 5
    TASK_MASTER_THRESHOLD = 20
    STREAK_STARTER_THRESHOLD = 3
    WEEK_WARRIOR_THRESHOLD = 7
    
    # Color scheme
    COLORS = {
        "primary_blue": "#2563eb",
        "secondary_teal": "#0d9488", 
        "success_green": "#059669",
        "warning_amber": "#d97706",
        "error_red": "#dc2626"
    }
    
    # Environment settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8501))
