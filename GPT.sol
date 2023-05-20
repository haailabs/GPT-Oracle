// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract RequestContract is Ownable {
    struct Request {
        string prompt;
        string result;
        string openaiRequestId;
        address requester;
        bool fulfilled;
    }

    mapping (uint => Request) public requests;
    mapping (address => uint[]) public requesterToRequestIds;

    uint public requestCounter = 0;

    event RequestCreated(uint indexed requestId, string prompt, address requester);
    event RequestFulfilled(uint indexed requestId, string result, string openaiRequestId);

    function createRequest(string memory _prompt) public {
        requests[requestCounter] = Request(_prompt, "", "", msg.sender, false);
        requesterToRequestIds[msg.sender].push(requestCounter);

        emit RequestCreated(requestCounter, _prompt, msg.sender);
        requestCounter++;
    }

    function fulfillRequest(uint _requestId, string memory _result, string memory _openaiRequestId) public onlyOwner {
        Request storage req = requests[_requestId];
        require(req.fulfilled == false, "Request has been fulfilled already");
        req.result = _result;
        req.openaiRequestId = _openaiRequestId;
        req.fulfilled = true;

        emit RequestFulfilled(_requestId, _result, _openaiRequestId);
    }
}
