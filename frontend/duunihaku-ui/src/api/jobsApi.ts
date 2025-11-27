import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // later env var
});

export const getJobs = () => api.get("/api/v1/jobs").then((res) => res.data);

export const updateJobState = (id: number, state: string) =>
  api.post(`/api/v1/jobs/${id}`, { state });

export const updateNotes = (id: number, notes: string) =>
  api.patch(`/api/v1/jobs/${id}/notes`, { notes });
