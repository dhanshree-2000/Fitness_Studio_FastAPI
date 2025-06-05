from database import SessionLocal, FitnessClassDB
from datetime import datetime, timedelta

def seed():
    db = SessionLocal()
    db.query(FitnessClassDB).delete()
    now = datetime.now()
    classes = [
        FitnessClassDB(
            name="Yoga", datetime=now + timedelta(days=1), instructor="Alice", available_slots=10
        ),
        FitnessClassDB(
            name="Zumba", datetime=now + timedelta(days=2), instructor="Bob", available_slots=8
        ),
        FitnessClassDB(
            name="HIIT", datetime=now + timedelta(days=3), instructor="Carol", available_slots=12
        ),
    ]
    db.add_all(classes)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
