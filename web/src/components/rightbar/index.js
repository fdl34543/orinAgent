import { useState } from "react";
import { FaBars } from "react-icons/fa";
import {
  Container,
  CardTop,
  CardBottom,
  ToggleButton,
} from "./rightbar.style";
import Chat from "../chat";
import WalletButton from "../connect"
import Agent from "../agent";

export default function Rightbar() {
  const [open, setOpen] = useState(true);

  return (
    <>
      <Container open={open}>
        <WalletButton/>
        <CardTop>
          <Agent />
        </CardTop>
        <CardBottom>
          <Chat />
        </CardBottom>
      </Container>

      <ToggleButton onClick={() => setOpen(!open)}>
        <FaBars />
      </ToggleButton>
    </>
  );
}
