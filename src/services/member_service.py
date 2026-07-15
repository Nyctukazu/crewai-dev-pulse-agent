from datetime import datetime, timedelta
from src.models.project_model import MemberInfo, Status

def update_member_statuses(session):
    """
    Updates member status based on how they contributed each day
    """
    now = datetime.utcnow()
    three_days_ago = now - timedelta(hours=72)
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    members = session.query(MemberInfo).all()

    for member in members:
        if member.last_active_at < three_days_ago:
            member.status = Status.INACTIVE
        else:
            member.status = Status.ACTIVE

        if member.last_active_at >= start_of_today:
            member.has_contributed_today = True
        else:
            member.has_contributed_today = False
    
    session.commit()
    print("Database state programmatically synced and updated!")
