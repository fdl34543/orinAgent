import { useState, useEffect } from "react";
import { FaInfo } from "react-icons/fa";
import {
  Container,
  Logo,
  Card,
  Stats,
  Label,
  Value,
  ToggleButton,
} from "./leftBar.style";

export default function LeftBar() {
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  const [utcTime, setUtcTime] = useState("");
  const [utcDate, setUtcDate] = useState("");

  const activeAgents = 27;

  useEffect(() => {
    setMounted(true);

    if (window.innerWidth > 768) {
      setOpen(true); // desktop default open
    } else {
      setOpen(false); // mobile default closed
    }
  }, []);

  useEffect(() => {
    function updateTime() {
      const now = new Date();
      const date = now.toUTCString().split(" ");
      setUtcDate(`${date[1]} ${date[2]} ${date[3]}`);
      setUtcTime(now.toUTCString().split(" ")[4]);
    }

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Container open={open}>
        <Logo src="/img/logo.png" alt="Orin Logo" />

        <Card>
          <Stats>
            <Label>Active Agents</Label>
            <Value>{activeAgents}</Value>
          </Stats>

          <Stats>
            <Label>Date/Time</Label>
            <Value>{utcDate} {utcTime}</Value>
          </Stats>

        </Card>
      </Container>

      <ToggleButton onClick={() => setOpen(!open)}>
        <FaInfo />
      </ToggleButton>
    </>
  );
}
