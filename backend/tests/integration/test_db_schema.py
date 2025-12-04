from datetime import datetime
from sqlmodel import Session
from uuid import uuid4
from sqlalchemy import inspect
from models.schema import (
    User,
    Job,
    JobSource,
    CVVersion,
    JobStateHistory,
    JobState,
    JobRegion,
)


def test_schema_tables_exist(test_engine):
    #Ensure all tables are created in the test DB.
    insp = inspect(test_engine)

    tables = set(insp.get_table_names())

    assert "user" in tables
    assert "job" in tables
    assert "jobstatehistory" in tables
    assert "cvversion" in tables
    assert "jobsource" in tables


def test_create_user_job_cv_history(test_engine):
    # Validate full object creation and relationships.
    with Session(test_engine) as session:

        # Create a user
        user = User(email="test@example.com")
        session.add(user)

        # Create a job source
        src = JobSource(name="TestSource", url="https://example.com")
        session.add(src)

        # Create a job
        job = Job(
            external_id="12345",
            title="DevOps Engineer",
            company="ExampleCorp",
            url="https://example.com/job",
            region=JobRegion.EMEA,
            source=src
        )
        session.add(job)

        # Create a CV version
        cv = CVVersion(
            version_label="v1",
            file_path="/tmp/cv.pdf"
        )
        session.add(cv)

        # Create job state history
        hist = JobStateHistory(
            job=job,
            user=user,
            cv_version=cv,
            state=JobState.APPLIED,
            notes="Initial application",
            timestamp=datetime.utcnow(),
        )
        session.add(hist)

        session.commit()

        # Refresh everything
        session.refresh(job)
        session.refresh(user)
        session.refresh(cv)

        assert job.id is not None
        assert user.id is not None
        assert cv.id is not None
        assert hist.id is not None

        # Relationship: Job → History
        assert len(job.history) == 1
        assert job.history[0].state == JobState.APPLIED

        # Relationship: User → History
        assert len(user.job_states) == 1
        assert user.job_states[0].notes == "Initial application"

        # Relationship: CVVersion → History
        assert len(cv.history) == 1
        assert cv.history[0].state == JobState.APPLIED

        # Backrefs check
        assert hist.job.id == job.id
        assert hist.user.id == user.id
        assert hist.cv_version.id == cv.id


def test_required_fields_enforced(test_engine):
    # Ensure missing required fields cause errors.
    with Session(test_engine) as session:

        bad_job = Job(
            title="Missing required fields",
            company=None,  # should fail at commit
            url=None,
        )
        session.add(bad_job)

        failed = False
        try:
            session.commit()
        except Exception:
            failed = True
            session.rollback()

        assert failed is True
