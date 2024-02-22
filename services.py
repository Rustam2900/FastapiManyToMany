from models import Subject, Student, StudentSubject


def _subject_create(subject, db):
    subject = Subject(name=subject.name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def _student_create(student, db):
    student_dict = student.dict()
    subjects = student_dict.pop('subject')
    s = Student(**student_dict)
    db.add(s)
    db.commit()
    db.refresh(s)
    for id in subjects:
        sub = db.query(Subject).filter(Subject.id == id).first()
        ss = StudentSubject(student_id=s.id, subject_id=sub.id)
        db.add(ss)
        db.commit()
        db.refresh(ss)
    return student
