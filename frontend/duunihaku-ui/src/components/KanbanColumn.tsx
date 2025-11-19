import { Paper, Title, Stack, Select, Text, Box, Badge } from "@mantine/core";
import type { Job } from "../api/jobs";

type Props = {
  title: string;
  jobs: Job[];
  onMove: (job: Job, newState: string) => void;
  allowedStates: string[];
};

export default function KanbanColumn({
  title,
  jobs,
  onMove,
  allowedStates,
}: Props) {
  return (
    <Box
      p="md"
      sx={{
        width: 300,
        background: "#f8f9fa",
        borderRadius: 8,
        border: "1px solid #ddd",
        height: "100%",
      }}
    >
      <Title order={4} mb="md">
        {title} <Badge size="sm">{jobs.length}</Badge>
      </Title>

      <Stack spacing="md">
        {jobs.map((job) => (
          <Paper
            key={job.id}
            withBorder
            p="sm"
            radius="md"
            shadow="xs"
            sx={{ background: "white" }}
          >
            <Text fw={600} size="sm">
              {job.title}
            </Text>
            <Text size="xs" c="dimmed">
              {job.company}
            </Text>

            {job.notes && (
              <Text size="xs" mt={4} c="gray">
                📝 {job.notes}
              </Text>
            )}

            <Select
              mt="sm"
              size="xs"
              value={job.state || "new"}
              data={allowedStates.map((s) => ({ value: s, label: s }))}
              onChange={(value) => value && onMove(job, value)}
            />
          </Paper>
        ))}
      </Stack>
    </Box>
  );
}
