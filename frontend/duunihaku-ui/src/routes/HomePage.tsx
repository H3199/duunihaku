import { useQuery } from "@tanstack/react-query";
import { fetchJobs } from "../api/jobs";

export default function HomePage() {
  const { data, isLoading } = useQuery({
    queryKey: ["jobs"],
    queryFn: fetchJobs,
  });

  if (isLoading) return <p>Loading...</p>;
  if (!data) return <p>No data</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Job List</h1>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {data.map((job) => (
          <li
            key={job.id}
            style={{
              padding: "10px",
              marginBottom: "6px",
              border: "1px solid #ddd",
              borderRadius: "6px",
            }}
          >
            <strong>
              <a href={job.url} target="_blank" rel="noopener noreferrer">
                {job.title}
              </a>
            </strong>{" "}
            <span style={{ color: "#666" }}>({job.company})</span>
            <br />
            <small
              style={{ color: job.state === "applied" ? "green" : "#999" }}
            >
              Status: {job.state || "new"}
            </small>
            {job.notes && (
              <p
                style={{ marginTop: "4px", fontSize: "0.85rem", color: "#444" }}
              >
                📝 {job.notes}
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
