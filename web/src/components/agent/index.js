import { useEffect, useState } from "react";
import {
  Wrapper,
  Tabs,
  TabButton,
  List,
  Item,
  ItemTitle,
  ItemText,
  TimeAgo,
  Location,
  Mention
} from "./agent.style";
import { useRouter } from "next/router";

function timeAgo(date) {
  const seconds = Math.floor((new Date() - date) / 1000);

  const intervals = [
    { label: "d", seconds: 86400 },
    { label: "h", seconds: 3600 },
    { label: "m", seconds: 60 },
  ];

  for (let interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count > 0) return `${count}${interval.label}`;
  }

  return "now";
}

function renderTextWithMentions(text) {
  const parts = text.split(/(@\w+)/g);

  return parts.map((part, index) => {
    if (part.startsWith("@")) {
      return (
        <Mention key={index}>
          {part}
        </Mention>
      );
    }
    return part;
  });
}


export default function Agent() {
  const [active, setActive] = useState("dialog");
  const router = useRouter();
  const location = router.query.location || null;
  const [dialogData, setDialogData] = useState([]);
  const [activityData, setActivityData] = useState([]);

  useEffect(() => {
    let interval;

    async function fetchDialogs() {
      try {
        const res = await fetch("/api/dialog?newest=true&limit=100");
        const data = await res.json();

        if (data.status === "success") {
          const formatted = data.dialogs.map((item) => {
            let messageText = item.message;

            if (item.target) {
              messageText = `@${item.target} ${item.message}`;
            }

            return {
              agent: item.sender,
              text: messageText,
              location: item.location,
              date: new Date(item.createdAt),
            };
          });

          setDialogData(formatted);
        }
      } catch (err) {
        console.error("Failed to fetch dialogs", err);
      }
    }

    async function fetchActivity() {
      try {
        const res = await fetch("/api/activity?limit=100&newest=true");
        const data = await res.json();

        if (data.status === "success") {
          const formatted = data.logs.map((item) => ({
            agent: item.agentName,
            text: `${item.agentName} - ${item.action}`,
            location: item.target
              ? item.target.charAt(0).toUpperCase() + item.target.slice(1)
              : "Hall",
            date: new Date(item.createdAt),
          }));

          setActivityData(formatted);
        }
      } catch (err) {
        console.error("Failed to fetch activity", err);
      }
    }

    async function fetchAll() {
      await Promise.all([fetchDialogs(), fetchActivity()]);
    }

    fetchAll();

    interval = setInterval(fetchAll, 60000); // 10000 = 10 seconds

    return () => clearInterval(interval);
  }, []);


  const rawData = active === "dialog" ? dialogData : activityData;

  const data = location
    ? rawData.filter(
        (item) =>
            item.location.toLowerCase() === location.toLowerCase()
        )
    : rawData;


  return (
    <Wrapper>
      <Tabs>
        <TabButton
          active={active === "dialog"}
          onClick={() => setActive("dialog")}
        >
          Dialog
        </TabButton>

        <TabButton
          active={active === "activity"}
          onClick={() => setActive("activity")}
        >
          Activity
        </TabButton>
      </Tabs>
      
      <List>
        {data.map((item, index) => (
            <Item key={index}>
            <ItemTitle>{item.agent}</ItemTitle>
            <ItemText>
                {renderTextWithMentions(item.text)}
            </ItemText>
            <Location>{item.location}</Location>
            <TimeAgo>{timeAgo(item.date)}</TimeAgo>
            </Item>
        ))}
      </List>

    </Wrapper>
  );
}
