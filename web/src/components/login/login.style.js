import styled from "styled-components";

export const Overlay = styled.div`
  position: absolute;
  inset: 0;
  backdrop-filter: blur(0px);
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
`;

export const LogoWrapper = styled.div`
  position: absolute;
  top: 150px;
  display: flex;
  justify-content: center;
  width: 400px;
  pointer-events: none;

  @media (max-width: 768px) {
    top: 80px;
  }
`;

export const LogoImage = styled.img`
  width: 360px;
  opacity: 0.95;
  filter: drop-shadow(0 0 20px rgba(0, 255, 200, 0.3));

  @media (max-width: 768px) {
    width: 340px;
  }
`;


export const Card = styled.div`
  position: relative;
  top: 80px;
  width: 520px;
  max-width: 90%;
  background: rgba(20, 20, 20, 0.9);
  border: 1px solid rgba(0, 255, 200, 0.15);
  border-radius: 12px;
  padding: 28px;
  color: white;
  box-shadow: 0 0 40px rgba(0, 255, 200, 0.1);

  @media (max-width: 768px) {
    top: 40px;
    padding: 20px;
    width: 100%;
    border-radius: 12px;
  }
`;

export const Intro = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 18px;
  margin-bottom: 24px;
`;

export const Title = styled.h2`
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin: 0;

  span {
    background: linear-gradient(90deg, #00ffd0, #00aaff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  @media (max-width: 768px) {
    font-size: 18px;
  }
`;

export const Description = styled.p`
  font-size: 14px;
  line-height: 1.7;
  color: #ccc;
  max-width: 420px;
  margin: 0;

  @media (max-width: 768px) {
    font-size: 13px;
  }
`;


export const TabSwitch = styled.div`
  display: flex;
  border: 1px solid rgba(0, 255, 200, 0.2);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 24px;
`;

export const TabButton = styled.button`
  flex: 1;
  padding: 12px 0;
  background: ${({ active }) =>
    active ? "rgba(0, 180, 140, 0.8)" : "transparent"};
  color: ${({ active }) => (active ? "#00ffd0" : "#aaa")};
  border: none;
  cursor: pointer;
  transition: 0.2s ease;
  font-size: 14px;

  &:hover {
    background: rgba(0, 180, 140, 0.5);
  }
`;

export const Content = styled.div`
  ol {
    padding-left: 18px;
    margin-bottom: 20px;
  }

  li {
    margin-bottom: 10px;
    color: #ccc;
  }
`;

export const CodeBlock = styled.div`
  background: #111;
  border: 1px solid rgba(0, 255, 200, 0.15);
  padding: 14px;
  border-radius: 6px;
  font-family: monospace;
  color: #00ffd0;
  margin-bottom: 20px;
`;

export const ActionRow = styled.div`
  display: flex;
  gap: 12px;
`;

export const ActionButton = styled.button`
  flex: 1;
  padding: 10px;
  background: ${({ primary }) =>
    primary ? "rgba(0, 180, 140, 0.8)" : "transparent"};
  border: 1px solid rgba(0, 255, 200, 0.2);
  color: ${({ primary }) => (primary ? "#00ffd0" : "#ccc")};
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s ease;

  &:hover {
    background: rgba(0, 180, 140, 0.5);
  }
`;
