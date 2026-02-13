import styled from "styled-components";

export const Wrapper = styled.div`
  height: 90%;
  display: flex;
  flex-direction: column;
  padding: 12px;
  color: #ccc;
`;

export const Tabs = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
`;

export const TabButton = styled.button`
  flex: 1;
  padding: 8px;
  background: ${({ active }) =>
    active ? "rgba(0, 200, 150, 0.2)" : "transparent"};
  border: 1px solid rgba(0, 255, 200, 0.15);
  color: ${({ active }) =>
    active ? "rgba(0, 200, 150, 0.9)" : "#888"};
  cursor: pointer;
  border-radius: 6px;
  font-size: 13px;
`;

export const List = styled.div`
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;

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

export const Item = styled.div`
  background: rgba(10, 20, 35, 0.9);
  padding: 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 255, 200, 0.08);
  position: relative;
`;

export const ItemTitle = styled.div`
  font-size: 12px;
  color: rgba(0, 200, 150, 0.9);
  font-weight: 600;
  margin-bottom: 4px;
`;

export const ItemText = styled.div`
  font-size: 13px;
  color: #aaa;
`;

export const TimeAgo = styled.div`
  position: absolute;
  top: 8px;
  right: 10px;
  font-size: 11px;
  color: #666;
`;

export const Location = styled.div`
  font-size: 11px;
  color: rgba(0, 200, 150, 0.6);
  margin-top: 4px;
`;

export const Mention = styled.span`
  color: rgba(0, 200, 150, 0.9);
  font-weight: 600;
  padding: 2px 4px;
  border-radius: 4px;
`;
