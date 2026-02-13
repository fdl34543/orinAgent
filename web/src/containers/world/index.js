import { Wrapper } from "./main.style";
import MapCanvas from "../../components/mapMain";
import Rightbar from "../../components/rightbar";
import LeftBar from "../../components/leftBar";

export default function MainContainer() {
  return (
    <Wrapper>
      <MapCanvas />
      <Rightbar />
      <LeftBar />
    </Wrapper>
  );
}
