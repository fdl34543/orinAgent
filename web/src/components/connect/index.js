import { useEffect, useState } from "react";
import { useAccount, useConnect, useDisconnect } from "wagmi";
import styled from "styled-components";

const Button = styled.button`
  position: absolute;
  top: 30px;
  right: 30px;
  z-index: 20;
  padding: 10px 18px;
  background: rgba(0, 200, 150, 0.9);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
`;

export default function ConnectButton() {
  const [mounted, setMounted] = useState(false);

  const { address, isConnected } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  if (isConnected) {
    return (
      <Button onClick={() => disconnect()}>
        {address.slice(0, 6)}...{address.slice(-4)}
      </Button>
    );
  }

  return (
    <Button onClick={() => connect({ connector: connectors[0] })}>
      Connect Wallet
    </Button>
  );
}
