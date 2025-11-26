from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password_hash: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    job_states: List["JobStateHistory"] = Relationship(back_populates="user")


class JobSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str]


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: Optional[str]
    title: str
    company: str
    url: str
    description: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    remote: Optional[bool] = False
    hybrid: Optional[bool] = False

    source_id: Optional[int] = Field(default=None, foreign_key="jobsource.id")
    source: Optional[JobSource] = Relationship()

    history: List["JobStateHistory"] = Relationship(back_populates="job")


class CVVersion(SQLModel, table=True):
    __tablename__ = "cvversion"

    id: Optional[int] = Field(default=None, primary_key=True)
    version_label: str
    file_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    history: List["JobStateHistory"] = Relationship(back_populates="cv_version")


class JobStateHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    job_id: int = Field(foreign_key="job.id")
    user_id: int = Field(foreign_key="user.id")
    cv_version_id: Optional[int] = Field(default=None, foreign_key="cvversion.id")

    state: str
    notes: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    job: Job = Relationship(back_populates="history")
    user: User = Relationship(back_populates="job_states")
    cv_version: Optional[CVVersion] = Relationship(back_populates="history")
