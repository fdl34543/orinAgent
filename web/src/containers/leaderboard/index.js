import { Wrapper } from "./main.style";
import MapCanvas from "../../components/mapMain";
import Login from "../../components/leaderboard";

export default function MainContainer() {
  return (
    <Wrapper>
      <MapCanvas />
      <Login />
    </Wrapper>
  );
}
