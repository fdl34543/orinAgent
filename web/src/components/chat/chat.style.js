import styled from "styled-components";

export const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  color: #ccc;
`;

export const Header = styled.div`
  padding: 12px 16px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
`;

export const Messages = styled.div`
  flex: 1;
  padding: 12px 16px;
  overflow-y: auto;
  font-size: 13px;

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

export const InputRow = styled.div`
  display: flex;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
`;

export const Input = styled.input`
  flex: 1;
  padding: 10px;
  background: #111;
  border: none;
  color: white;
  outline: none;
`;

export const SendButton = styled.button`
  padding: 10px 16px;
  background: rgba(0, 200, 150, 0.9);
  border: none;
  color: white;
  cursor: pointer;

  &:disabled {
    background: #333;
    cursor: not-allowed;
  }
`;


export const Message = styled.div`
  margin-bottom: 10px;
  display: flex;
  gap: 6px;
  align-items: flex-start;
`;

export const Username = styled.span`
  color: rgba(0, 200, 150, 0.9);
  font-weight: 600;
  white-space: nowrap;
`;

export const MessageText = styled.span`
  color: #ccc;
  word-break: break-word;
`;

export const WarningText = styled.div`
  padding: 8px 16px;
  font-size: 12px;
  color: #ff6b6b;
`;
