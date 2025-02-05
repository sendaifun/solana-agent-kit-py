# Solana Agent Kit

<div align="center">

![Solana Agent Kit Cover 1 (3)](https://github.com/user-attachments/assets/cfa380f6-79d9-474d-9852-3e1976c6de70)

![GitHub forks](https://img.shields.io/github/forks/sendaifun/solana-agent-kit-py?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/sendaifun/solana-agent-kit-py?style=for-the-badge)

</div>

An open-source toolkit for connecting AI agents to Solana protocols. Now, any agent, using any model can autonomously perform 60+ Solana actions:

- Trade tokens
- Launch new tokens
- Lend assets
- Send compressed airdrops
- Execute blinks
- Launch tokens on AMMs
- And more...

Anyone - whether an SF-based AI researcher or a crypto-native builder - can bring their AI agents trained with any model and seamlessly integrate with Solana.

## 🔧 Core Blockchain Features

- **Token Operations**
  - Deploy SPL tokens by Metaplex
  - Transfer assets
  - Balance checks
  - Stake SOL
  - Zk compressed Airdrop by Light Protocol and Helius
- **NFTs on 3.Land**
  - Create your own collection
  - NFT creation and automatic listing on 3.land
  - List your NFT for sale in any SPL token
- **NFT Management via Metaplex**
  - Collection deployment
  - NFT minting
  - Metadata management
  - Royalty configuration

- **DeFi Integration**
  - Jupiter Exchange swaps
  - Launch on Pump via PumpPortal
  - Raydium pool creation (CPMM, CLMM, AMMv4)
  - Orca Whirlpool integration
  - Manifest market creation, and limit orders
  - Meteora Dynamic AMM, DLMM Pool, and Alpha Vault
  - Openbook market creation
  - Register and Resolve SNS
  - Jito Bundles
  - Pyth Price feeds for fetching Asset Prices
  - Register/resolve Alldomains
  - Perpetuals Trading with Adrena Protocol
  - Drift Vaults, Perps, Lending and Borrowing

- **Solana Blinks**
   - Lending by Lulo (Best APR for USDC)
   - Send Arcade Games
   - JupSOL staking
   - Solayer SOL (sSOL)staking

## 🤖 AI Integration Features

- **LangChain Integration**
  - Ready-to-use LangChain tools for blockchain operations
  - Autonomous agent support
  - Memory management for persistent interactions
  - Streaming responses for real-time feedback

- **Autonomous Modes**
  - Interactive chat mode for guided operations
  - Autonomous mode for independent agent actions
  - Configurable action intervals
  - Built-in error handling and recovery

## 📃 Documentation
You can view the full documentation of the kit at [docs.solanaagentkit.xyz](https://docs.solanaagentkit.xyz)

## 📦 Installation

```bash
pip install solana-agent-kit-py
```

## Quick Start

```python
from solana_agent_kit import SolanaAgentKit, create_solana_tools

# Initialize with private key and optional RPC URL
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

# Create LangChain tools
tools = create_solana_tools(agent)
```

## Usage Examples

### Deploy a New Token

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )
    
    result = await agent.deploy_token(
        "my ai token",  # name
        "uri",         # uri
        "token",       # symbol
        9,            # decimals
        1000000       # initial supply
    )
    print("Token Mint Address:", result.mint)

import asyncio
asyncio.run(main())
```

### Create NFT Collection

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )
    
    collection = await agent.deploy_collection({
        "name": "My NFT Collection",
        "uri": "https://arweave.net/metadata.json",
        "royalty_basis_points": 500,  # 5%
        "creators": [
            {
                "address": "creator-wallet-address",
                "percentage": 100
            }
        ]
    })

import asyncio
asyncio.run(main())
```

### Swap Tokens

```python
from solana_agent_kit import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )
    
    signature = await agent.trade(
        output_mint=Pubkey.from_string("target-token-mint"),
        input_amount=100,  # amount
        input_mint=Pubkey.from_string("source-token-mint"),
        slippage_bps=300  # 3% slippage
    )

import asyncio
asyncio.run(main())
```

### Lend Tokens

```python
from solana_agent_kit import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)
signature = await agent.lend_assets(
    amount=100  # amount
)

import asyncio
asyncio.run(main())
```

### Stake SOL

```python
from solana_agent_kit import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

signature = await agent.stake(
    amount=1  # amount in SOL
)

import asyncio
asyncio.run(main())
```

### Request Faucet Funds

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    response = await agent.request_faucet_funds()
    print(response)

import asyncio
asyncio.run(main())
```

### Fetch Current TPS

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    tps = await agent.get_tps()
    print(f"Current TPS: {tps}")

import asyncio
asyncio.run(main())
```

### Get Token Data by Ticker

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    token_data = await agent.get_token_data_by_ticker("SOL")
    print(token_data)

import asyncio
asyncio.run(main())
```

### Get Token Data by Address

```python
from solana_agent_kit import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    token_data = await agent.get_token_data_by_address("your-token-mint-address")
    print(token_data)

import asyncio
asyncio.run(main())
```

### Launch Pump Fun Token

```python
from solana_agent_kit import SolanaAgentKit
from solana_agent_kit.types import PumpfunTokenOptions

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    options = PumpfunTokenOptions(
        # Add your options here
    )

    response = await agent.launch_pump_fun_token(
        token_name="MyToken",
        token_ticker="MTK",
        description="This is a fun token",
        image_url="https://example.com/image.png",
        options=options
    )
    print(response)
```

### Create Meteora DLMM Pool

```python
from solana_agent_kit import SolanaAgentKit
from solders.pubkey import Pubkey
from solana_agent_kit.utils.meteora_dlmm.types import ActivationType

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    response = await agent.create_meteora_dlmm_pool(
        bin_step=1,
        token_a_mint=Pubkey.from_string("token-a-mint"),
        token_b_mint=Pubkey.from_string("token-b-mint"),
        initial_price=1.0,
        price_rounding_up=True,
        fee_bps=30,
        activation_type=ActivationType.Timestamp,
        has_alpha_vault=True,
        activation_point=None
    )
    print(response)

import asyncio
asyncio.run(main())
```

### Buy Tokens with Raydium

```python
from solana_agent_kit import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    confirmed = await agent.buy_with_raydium(
        pair_address=Pubkey.from_string("target-pair-address"),  # The pair you want to buy from
        sol_in=1,  # Amount of SOL or input token to spend
        slippage=300  # Maximum slippage in basis points (3% here)
    )
    print(f"Transaction confirmed: {confirmed}")

import asyncio
asyncio.run(main())
```

### Sell Tokens with Raydium

```python
from solana_agent_kit import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    confirmed = await agent.sell_with_raydium(
        input_mint=Pubkey.from_string("source-token-mint"),  # The token you want to sell
        percentage=100,
        slippage_bps=250  # Maximum slippage in basis points (2.5% here)
    )
    print(f"Transaction confirmed: {confirmed}")

import asyncio
asyncio.run(main())
```

### Burn and Close Token Account

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    response = await agent.burn_and_close_accounts("token-account-address")
    print("Account burned and closed:", response)

import asyncio
asyncio.run(main())
```

### Batch burn and Close Token Account

```python
from solana_agent_kit import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    token_accounts = ["token-account-address-1", "token-account-address-2"]
    responses = await agent.multiple_burn_and_close_accounts(token_accounts)
    print("Accounts burned and closed:", responses)

import asyncio
asyncio.run(main())
```

## Dependencies

The toolkit relies on several key Solana and Metaplex libraries:

- solana-py
- spl-token-py
- metaplex-python-sdk

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

## License

Apache-2 License

## Funding

If you wanna give back any tokens or donations to the OSS community -- The Public Solana Agent Kit Treasury Address:

Solana Network : EKHTbXpsm6YDgJzMkFxNU1LNXeWcUW7Ezf8mjUNQQ4Pa

## Security

This toolkit handles private keys and transactions. Always ensure you're using it in a secure environment and never share your private keys.
