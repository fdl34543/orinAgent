import { useState, useEffect, useRef } from "react";
import { useAccount } from "wagmi";
import {
  Wrapper,
  Header,
  Messages,
  Message,
  Username,
  MessageText,
  InputRow,
  Input,
  SendButton,
  WarningText,
} from "./chat.style";

export default function Chat() {
  const { address, isConnected } = useAccount();

  const [mounted, setMounted] = useState(false);
  const [input, setInput] = useState("");
  const [chatData, setChatData] = useState([]);

  const messagesEndRef = useRef(null);
  const messagesRef = useRef(null);


  useEffect(() => {
    setMounted(true);
  }, []);

  // Fetch chat
  useEffect(() => {
    async function fetchChats() {
      try {
        const res = await fetch("/api/chat?limit=50");
        const data = await res.json();

        if (data.status === "success") {
          const formatted = data.chats.map((item) => {
            const shortAddress =
              item.address.slice(0, 6) +
              "..." +
              item.address.slice(-4);

            return {
              username: shortAddress,
              text: item.chat,
              date: new Date(item.createdAt),
            };
          });

          // Oldest -> newest
          const sorted = formatted.sort(
            (a, b) => a.date - b.date
          );

          setChatData(sorted);
        }
      } catch (err) {
        console.error("Failed to fetch chats", err);
      }
    }

    fetchChats();
  }, []);

  // Auto scroll to bottom
  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop =
        messagesRef.current.scrollHeight;
    }
  }, [chatData]);

  function scrollToBottom() {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }

  if (!mounted) return null;

  async function handleSend() {
    if (!isConnected) return;
    if (!input.trim()) return;

    const shortAddress =
      address.slice(0, 6) + "..." + address.slice(-4);

    const messageToSend = input;

    // Optimistic update
    setChatData((prev) => [
      ...prev,
      { username: shortAddress, text: messageToSend, date: new Date() },
    ]);

    setInput("");

    try {
      const res = await fetch("/api/send-chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          address,
          chat: messageToSend,
        }),
      });

      const data = await res.json();

      if (data.status !== "success") {
        console.error("Send failed:", data);
      }
    } catch (err) {
      console.error("Failed to send chat", err);
    }
  }

  return (
    <Wrapper>
      <Header>Human Chat</Header>

      <Messages ref={messagesRef}>
        {chatData.map((msg, index) => (
          <Message key={index}>
            <Username>{msg.username}:</Username>
            <MessageText>{msg.text}</MessageText>
          </Message>
        ))}

      </Messages>

      {!isConnected && (
        <WarningText>
          Connect wallet to send message
        </WarningText>
      )}

      <InputRow>
        <Input
          placeholder={
            isConnected
              ? "Send a message..."
              : "Wallet not connected"
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={!isConnected}
        />
        <SendButton
          onClick={handleSend}
          disabled={!isConnected}
        >
          SEND
        </SendButton>
      </InputRow>
    </Wrapper>
  );
}
