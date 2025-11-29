import { useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Text,
  Title,
  Button,
  ScrollArea,
  Loader,
  Group,
  Badge,
} from "@mantine/core";
import { updateJobState } from "../api/jobsApi";

const API_URL = import.meta.env.VITE_API_URL;

export default function JobPage() {
  const { id } = useParams();
  const queryClient = useQueryClient();

  // Fetch job details
  const { data, isLoading } = useQuery({
    queryKey: ["job", id],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/api/v1/jobs/${id}`);
      if (!res.ok) throw new Error("Failed to fetch job");
      return res.json();
    },
  });

  // Mutation: Update job state
  const stateMutation = useMutation({
    mutationFn: ({ state }: { state: string }) => updateJobState(id!, state),
    onSuccess: () => {
      // Refresh job detail + the main kanban list
      queryClient.invalidateQueries({ queryKey: ["job", id] });
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
    },
  });

  if (isLoading) return <Loader />;
  if (!data) return <>Job not found</>;

  return (
    <ScrollArea style={{ padding: "2rem" }}>
      <Title order={2}>{data.title}</Title>

      <Group mt="xs">
        <Text size="lg" weight={500}>
          {data.company}
        </Text>
        <Badge variant="filled" color="blue">
          {data.state?.toUpperCase() ?? "NEW"}
        </Badge>
      </Group>

      <Button
        component="a"
        href={data.url}
        target="_blank"
        mt="md"
        variant="light"
      >
        Open Job Posting
      </Button>

      {/* ---- ACTION BUTTONS ---- */}
      <Group mt="lg">
        <Button
          color="yellow"
          onClick={() => stateMutation.mutate({ state: "saved" })}
          disabled={stateMutation.isPending}
        >
          Save
        </Button>

        <Button
          color="green"
          onClick={() => stateMutation.mutate({ state: "applied" })}
          disabled={stateMutation.isPending}
        >
          Applied
        </Button>

        <Button
          color="red"
          variant="outline"
          onClick={() => stateMutation.mutate({ state: "trash" })}
          disabled={stateMutation.isPending}
        >
          Trash
        </Button>
      </Group>

      <Text mt="xl" size="sm" style={{ whiteSpace: "pre-line" }}>
        {data.description || "No description available."}
      </Text>
    </ScrollArea>
  );
}
