document.getElementById("submitPayment").addEventListener("click", async () => {
    const amount = document.getElementById("amount").value;
    const messageElement = document.getElementById("message");

    messageElement.textContent = ""; // Reset message

    const recipientAddress = "0xBD6963e713f4e67Cd1E39D12183767c6e25e8299"; // Địa chỉ nhận cố định

    if (typeof window.ethereum === "undefined") {
        messageElement.textContent = "MetaMask is not installed. Please install MetaMask!";
        messageElement.className = "message error";
        return;
    }

    try {
        const web3 = new Web3(window.ethereum);
        console.log("Web3 initialized successfully");

        // Kết nối với MetaMask và lấy địa chỉ ví người dùng
        const accounts = await ethereum.request({ method: "eth_requestAccounts" });
        const senderAddress = accounts[0];
        console.log("Accounts:", accounts);

        // Chuyển người dùng sang mạng Polygon (Chain ID 137)
        await ethereum.request({
            method: "wallet_switchEthereumChain",
            params: [{ chainId: "0x89" }],
        });
        console.log("Switched to Polygon network.");

        // Địa chỉ hợp đồng QHC
        const contractAddress = "0x280e43e7c28aDEe4fA7BD5d926E5d052693b40cC";
        const decimals = 3; // Số chữ số thập phân của QHC
        const amountInUnits = (amount * Math.pow(10, decimals)).toString();
        console.log("Amount in smallest unit:", amountInUnits);

        // ABI của hợp đồng token QHC
        const abi = [
            {
                constant: false,
                inputs: [
                    { name: "to", type: "address" },
                    { name: "tokens", type: "uint256" }
                ],
                name: "transfer",
                outputs: [{ name: "success", type: "bool" }],
                type: "function"
            }
        ];

        // Mã hóa dữ liệu giao dịch
        const encodedData = web3.eth.abi.encodeFunctionCall(abi[0], [
            recipientAddress,
            web3.utils.toHex(amountInUnits),
        ]);

        // Gửi giao dịch
        const txHash = await ethereum.request({
            method: "eth_sendTransaction",
            params: [
                {
                    from: senderAddress,
                    to: contractAddress,
                    data: encodedData,
                    value: "0x0",
                },
            ],
        });

        console.log("Transaction successful!");
        console.log("Tx Hash:", txHash);
        console.log("Sender Address:", senderAddress);
        console.log("Amount:", amount);

        // Hiển thị thông báo thành công
//        messageElement.textContent = `Transaction completed! Tx Hash: ${txHash}`;
//        messageElement.className = "message";

        // Gửi thông tin giao dịch về phía server (Flask server)
        const response = await fetch("http://127.0.0.1:5000/code/buyCode", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tx_hash: txHash, sender: senderAddress, amount: amount }),
        });

        const result = await response.json();

        // Kiểm tra trạng thái phản hồi từ server
        if (result.status) {
            messageElement.textContent = `Transaction completed! Code: ${result.code}`;
            messageElement.className = "message";
        } else {
            messageElement.textContent = `Transaction failed! Error: ${result.error}`;
            messageElement.className = "message error";
        }

    } catch (error) {
        console.error(error);
        messageElement.textContent = `Transaction failed: ${error.message}`;
        messageElement.className = "message error";
    }
});



