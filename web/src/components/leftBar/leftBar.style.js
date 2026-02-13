import styled from "styled-components";

export const Container = styled.div`
  position: absolute;
  left: 0;
  top: 0;
  width: 18vw;
  height: 85vh;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  z-index: 15;
  transition: 0.3s ease;

  transform: ${({ open }) =>
    open ? "translateX(0)" : "translateX(-100%)"};

  @media (max-width: 768px) {
    width: 90vw;
  }
`;

export const Logo = styled.img`
  width: 150px;
  margin-bottom: 10px;
`;

export const Card = styled.div`
  background: rgba(20, 20, 40, 0.9);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 200, 0.15);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 18px;
`;

export const Stats = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

export const Label = styled.div`
  font-size: 12px;
  color: #888;
`;

export const Value = styled.div`
  font-size: 16px;
  color: rgba(0, 200, 150, 0.9);
  font-weight: 600;
`;

export const ToggleButton = styled.button`
  position: absolute;
  bottom: 30px;
  left: 30px;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 200, 150, 0.9);
  color: white;
  font-size: 18px;
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
