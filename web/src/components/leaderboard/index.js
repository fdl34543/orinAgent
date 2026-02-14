import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Overlay,
  Container,
  Header,
  Title,
  BackButton,
  List,
  Item,
  Rank,
  AgentInfo,
  AgentName,
  Job,
  Score,
} from "./leaderboard.style";

export default function Leaderboard() {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    async function fetchLeaderboard() {
      try {
        const res = await fetch("/api/leaderboard");
        const data = await res.json();

        if (data.status === "success") {
          const enrichedAgents = await Promise.all(
            data.topAgents.map(async (agent) => {
              const agentRes = await fetch(
                `/api/agents?name=${agent.name}`
              );
              const agentData = await agentRes.json();

              return {
                rank: agent.rank,
                name: agent.name,
                score: agent.alignment,
                job:
                  agentData.status === "success"
                    ? agentData.role?.Job
                    : "Unknown",
              };
            })
          );

          setAgents(enrichedAgents);
        }
      } catch (error) {
        console.error("Failed to fetch leaderboard", error);
      }
    }

    fetchLeaderboard();
  }, []);

  return (
    <Overlay>
      <Container>
        <Header>
          <Title>Leaderboard</Title>

          <Link href="/" passHref>
            <BackButton>Back</BackButton>
          </Link>
        </Header>

        <List>
          {agents.map((agent) => (
            <Item key={agent.rank}>
              <Rank>{agent.rank}</Rank>

              <AgentInfo>
                <AgentName>{agent.name}</AgentName>
                <Job>{agent.job}</Job>
              </AgentInfo>

              <Score>{agent.score}</Score>
            </Item>
          ))}
        </List>
      </Container>
    </Overlay>
  );
}
