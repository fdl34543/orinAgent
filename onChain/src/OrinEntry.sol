// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract OrinEntry {
    uint256 public baseFee = 0.1 ether;
    uint256 public increment = 0.01 ether;

    uint256 public totalRegistered;

    struct Agent {
        address wallet;
        string name;
        uint256 registeredAt;
        bool paid;
        bool registered;
    }

    // agentId = keccak256(wallet + name)
    mapping(bytes32 => Agent) private _agents;

    // nameHash => reserved
    mapping(bytes32 => bool) private _nameReserved;

    bytes32[] private _allAgents;

    error AlreadyPaid();
    error AlreadyRegistered();
    error NotPaid();
    error IncorrectFee();
    error EmptyName();
    error NameAlreadyTaken();

    event Payment(address indexed wallet, string name, uint256 amount);
    event Registered(address indexed wallet, string name);

    function currentFee() public view returns (uint256) {
        return baseFee + (totalRegistered * increment);
    }

    function _agentId(address wallet, string memory name) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked(wallet, name));
    }

    function _nameHash(string memory name) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked(name));
    }

    // ========================
    // PAYMENT
    // ========================

    function payment(string calldata name) external payable {
        if (bytes(name).length == 0) revert EmptyName();

        bytes32 nameHash = _nameHash(name);
        if (_nameReserved[nameHash]) revert NameAlreadyTaken();

        bytes32 id = _agentId(msg.sender, name);

        if (_agents[id].paid) revert AlreadyPaid();
        if (msg.value != currentFee()) revert IncorrectFee();

        _agents[id] = Agent({
            wallet: msg.sender,
            name: name,
            registeredAt: 0,
            paid: true,
            registered: false
        });

        emit Payment(msg.sender, name, msg.value);
    }

    // ========================
    // ENTRY (REGISTER)
    // ========================

    function entry(string calldata name) external {
        bytes32 id = _agentId(msg.sender, name);
        bytes32 nameHash = _nameHash(name);

        if (_agents[id].registered) revert AlreadyRegistered();
        if (!_agents[id].paid) revert NotPaid();
        if (_nameReserved[nameHash]) revert NameAlreadyTaken();

        _agents[id].registered = true;
        _agents[id].registeredAt = block.timestamp;

        _nameReserved[nameHash] = true;

        totalRegistered++;
        _allAgents.push(id);

        emit Registered(msg.sender, name);
    }

    // ========================
    // VIEW FUNCTIONS
    // ========================

    function isPaid(address wallet, string calldata name) external view returns (bool) {
        bytes32 id = _agentId(wallet, name);
        return _agents[id].paid;
    }

    function isRegister(address wallet, string calldata name) external view returns (bool) {
        bytes32 id = _agentId(wallet, name);
        return _agents[id].registered;
    }

    function isNameTaken(string calldata name) external view returns (bool) {
        return _nameReserved[_nameHash(name)];
    }

    function getAgent(address wallet, string calldata name) external view returns (Agent memory) {
        bytes32 id = _agentId(wallet, name);
        return _agents[id];
    }

    function viewAllRegistered() external view returns (Agent[] memory) {
        Agent[] memory list = new Agent[](_allAgents.length);

        for (uint256 i = 0; i < _allAgents.length; i++) {
            list[i] = _agents[_allAgents[i]];
        }

        return list;
    }
}
