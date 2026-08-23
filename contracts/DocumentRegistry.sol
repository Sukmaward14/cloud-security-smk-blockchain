// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentRegistry {

    struct Document {
        uint256 documentId;
        string documentHash;
        uint256 timestamp;
        address uploader;
    }

    mapping(uint256 => Document) public documents;

    event DocumentRegistered(
        uint256 documentId,
        string documentHash,
        uint256 timestamp,
        address uploader
    );

    function registerDocument(
        uint256 _documentId,
        string memory _documentHash
    ) public {

        documents[_documentId] = Document(
            _documentId,
            _documentHash,
            block.timestamp,
            msg.sender
        );

        emit DocumentRegistered(
            _documentId,
            _documentHash,
            block.timestamp,
            msg.sender
        );
    }

    function getDocument(
        uint256 _documentId
    )
        public
        view
        returns (
            uint256,
            string memory,
            uint256,
            address
        )
    {
        Document memory document = documents[_documentId];

        return (
            document.documentId,
            document.documentHash,
            document.timestamp,
            document.uploader
        );
    }
}