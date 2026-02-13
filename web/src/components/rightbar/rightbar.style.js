import styled from "styled-components";

export const Container = styled.div`
  position: absolute;
  right: 0;
  top: 0;
  width: 18vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  z-index: 15;

  pointer-events: ${({ open }) => (open ? "auto" : "none")};
  opacity: ${({ open }) => (open ? 1 : 0)};
  transform: ${({ open }) =>
    open ? "translateX(0)" : "translateX(100%)"};
  transition: 0.3s ease;

  @media (max-width: 768px) {
    width: 98vw;
    right: 50%;
    height: 85vh;
    transform: ${({ open }) =>
      open ? "translate(50%, 0)" : "translate(150%, 0)"};
  }
`;

export const CardTop = styled.div`
  height: 55vh;
  position: relative;
  top: 60px;
  background: rgba(20, 20, 40, 0.9);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 200, 0.15);

  @media (max-width: 768px) {
    height: 55%;
  }
`;

export const CardBottom = styled.div`
  position: relative;
  top: 60px;
  height: 25vh;
  background: rgba(20, 20, 40, 0.95);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 200, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;

  @media (max-width: 768px) {
    height: 25%;
  }
`;

export const ToggleButton = styled.button`
  position: absolute;
  bottom: 30px;
  right: 30px;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 200, 150, 0.9);
  color: white;
  font-size: 20px;
  cursor: pointer;
  z-index: 20;
  box-shadow: 0 0 20px rgba(0, 255, 200, 0.4);
  transition: 0.2s ease;

  &:hover {
    transform: scale(1.1);
  }

  @media (max-width: 768px) {
    bottom: 100px;
  }
`;
