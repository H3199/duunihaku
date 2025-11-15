#!/usr/bin/env python3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json
import os
from job_state import JobState
from mytypes import JobRecord


def get_state_file() -> str:
    return os.getenv("STATE_FILE", "jaysons/job_state.json")


@dataclass
class Job:
    id: int
    job_title: str
    company: str
    url: str
    description: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    remote: Optional[bool] = False
    hybrid: Optional[bool] = False

    # local/persistence fields:
    state: JobState = JobState.NEW
    notes: str = ""
    updated_at: Optional[str] = None


    # Convert API dict (TypedDict) into Job class instance.
    @classmethod
    def from_raw(cls, data: JobRecord) -> "Job":
        return cls(
            id=data["id"],
            job_title=data.get("job_title", ""),
            company=data.get("company", ""),
            url=data.get("url", ""),
            description=data.get("description", ""),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            remote=data.get("remote"),
            hybrid=data.get("hybrid"),
        )


    def update_state(self, new_state: JobState, notes: Optional[str] = None):
        self.state = new_state
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.now().astimezone().isoformat(timespec="seconds")
        self.save()


    def save(self):
        state_file = get_state_file()

        if os.path.exists(state_file):
            with open(state_file) as f:
                state = json.load(f)
        else:
            state = {}

        state[str(self.id)] = {
            "state": self.state.value,
            "notes": self.notes,
            "updated_at": self.updated_at,
        }

        os.makedirs(os.path.dirname(state_file), exist_ok=True)
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)


    @classmethod
    def apply_saved_state(cls, jobs: list["Job"]) -> list["Job"]:
        state_file = get_state_file()

        if not os.path.exists(state_file):
            return jobs

        with open(state_file) as f:
            saved = json.load(f)

        for job in jobs:
            stored = saved.get(str(job.id))
            if stored:
                job.state = JobState(stored["state"])
                job.notes = stored.get("notes", "")
                job.updated_at = stored.get("updated_at")

        return jobs
