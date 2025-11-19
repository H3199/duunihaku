import { KanbanBoard } from "../components/KanbanBoard";

export default function HomePage() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Job Kanban</h1>
      <KanbanBoard />
    </div>
  );
}
