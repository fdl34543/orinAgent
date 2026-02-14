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

export const Container = styled.div`
  position: relative;
  top: 0px;
  width: 40vw;
  max-width: 95%;
  height: 70vh;
  background: rgba(15, 15, 25, 0.95);
  border: 1px solid rgba(0, 200, 150, 0.2);
  border-radius: 12px;
  padding: 24px;
  overflow-y: auto;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 200, 150, 0.9);
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 200, 150, 1);
  }
`;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

export const BackButton = styled.a`
  padding: 6px 14px;
  border-radius: 6px;
  background: rgba(0, 200, 150, 0.15);
  border: 1px solid rgba(0, 200, 150, 0.3);
  color: rgba(0, 200, 150, 0.9);
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(0, 200, 150, 0.3);
  }
`;


export const Title = styled.h2`
  color: rgba(0, 200, 150, 0.9);
  margin-bottom: 20px;
`;

export const List = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

export const Item = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(20, 20, 30, 0.9);
  border: 1px solid rgba(0, 200, 150, 0.1);
  padding: 14px 18px;
  border-radius: 8px;
`;

export const Rank = styled.div`
  font-weight: bold;
  color: rgba(255, 200, 0, 0.9);
  width: 50px;
`;

export const AgentInfo = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

export const AgentName = styled.div`
  font-size: 16px;
  font-weight: 600;
  color: white;
`;

export const Job = styled.div`
  font-size: 13px;
  color: rgba(0, 200, 150, 0.7);
`;

export const Score = styled.div`
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 200, 150, 0.9);
`;
