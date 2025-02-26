
from datetime import datetime, timezone
from app import db
from app.models import AuditLog

# Singleton class for logging user actions
# 
# 
# Usage:
# AuditLogger.log(current_user.id, 'new_project', f'Created project id: {project.id}')

class AuditLogger:
    _instance = None

    # Types of logs to track
    active_log_types = {
        'login': True,
        'new_project': True,
        'edit_project': True,
        'remove_project': True,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditLogger, cls).__new__(cls)
        return cls._instance

    @classmethod
    def log(cls, user_id, action, message):
        # Only log if action is enabled
        if cls.active_log_types.get(action, False): 
            log_entry = AuditLog(user_id=user_id, action=action, message=message, timestamp=datetime.now(timezone.utc))
            db.session.add(log_entry)
            db.session.commit()

    # Toggle active log types
    @classmethod
    def toggle_log_type(cls, action, enable=True):
        if action in cls.active_log_types:
            cls.active_log_types[action] = enable
        else:
            raise ValueError(f"Action '{action}' not recognised.")