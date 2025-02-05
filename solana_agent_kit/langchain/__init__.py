import json

from langchain.tools import BaseTool
from solders.pubkey import Pubkey  # type: ignore

from solana_agent_kit.agent import SolanaAgentKit
from solana_agent_kit.tools import create_image
from solana_agent_kit.utils import toJSON
from solana_agent_kit.utils.meteora_dlmm.types import ActivationType


class SolanaBalanceTool(BaseTool):
    name:str = "solana_balance"
    description:str = """
    Get the balance of a Solana wallet or token account.

    If you want to get the balance of your wallet, you don't need to provide the tokenAddress.
    If no tokenAddress is provided, the balance will be in SOL.
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            token_address = Pubkey.from_string(input) if input else None
            balance = await self.solana_kit.get_balance(token_address)
            return {
                "status": "success",
                "balance": balance,
                "token": input or "SOL",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTransferTool(BaseTool):
    name:str = "solana_transfer"
    description:str = """
    Transfer tokens or SOL to another address.

    Input (JSON string):
    {
        "to": "wallet_address",
        "amount": 1,
        "mint": "mint_address" (optional)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            recipient = Pubkey.from_string(data["to"])
            mint_address = Pubkey.from_string(data["mint"]) if "mint" in data else None

            transaction = await self.solana_kit.transfer(recipient, data["amount"], mint_address)

            return {
                "status": "success",
                "message": "Transfer completed successfully",
                "amount": data["amount"],
                "recipient": data["to"],
                "token": data.get("mint", "SOL"),
                "transaction": transaction,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaDeployTokenTool(BaseTool):
    name:str = "solana_deploy_token"
    description:str = """
    Deploy a new SPL token. Input should be JSON string with:
    {
        "decimals": 9,
        "initialSupply": 1000
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            decimals = data.get("decimals", 9)

            if decimals < 0 or decimals > 9:
                raise ValueError("Decimals must be between 0 and 9")

            token_details = await self.solana_kit.deploy_token(decimals)
            return {
                "status": "success",
                "message": "Token deployed successfully",
                "mintAddress": token_details["mint"],
                "decimals": decimals,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaTradeTool(BaseTool):
    name:str = "solana_trade"
    description:str = """
    Execute a trade on Solana.

    Input (JSON string):
    {
        "output_mint": "output_mint_address",
        "input_amount": 100,
        "input_mint": "input_mint_address" (optional),
        "slippage_bps": 100 (optional)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            output_mint = Pubkey.from_string(data["output_mint"])
            input_mint = Pubkey.from_string(data["input_mint"]) if "input_mint" in data else None
            slippage_bps = data.get("slippage_bps", 100)

            transaction = await self.solana_kit.trade(
                output_mint, data["input_amount"], input_mint, slippage_bps
            )

            return {
                "status": "success",
                "message": "Trade executed successfully",
                "transaction": transaction,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaFaucetTool(BaseTool):
    name:str = "solana_request_funds"
    description:str = "Request test funds from a Solana faucet."
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            result = await self.solana_kit.request_faucet_funds()
            return {
                "status": "success",
                "message": "Faucet funds requested successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaStakeTool(BaseTool):
    name:str = "solana_stake"
    description:str = "Stake assets on Solana. Input is the amount to stake."
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            amount = int(input)
            result = await self.solana_kit.stake(amount)
            return {
                "status": "success",
                "message": "Assets staked successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetWalletAddressTool(BaseTool):
    name:str = "solana_get_wallet_address"
    description:str = "Get the wallet address of the agent"
    solana_kit: SolanaAgentKit
    
    async def _arun(self):
        try:
            result = await self.solana_kit.wallet_address
            return {
                "status": "success",
                "message": "Wallet address fetched successfully",
                "result": str(result),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaCreateImageTool(BaseTool):
    name: str = "solana_create_image"
    description: str = """
    Create an image using OpenAI's DALL-E.

    Input (JSON string):
    {
        "prompt": "description of the image",
        "size": "image_size" (optional, default: "1024x1024"),
        "n": "number_of_images" (optional, default: 1)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            prompt = data["prompt"]
            size = data.get("size", "1024x1024")
            n = data.get("n", 1)

            if not prompt.strip():
                raise ValueError("Prompt must be a non-empty string.")

            result = await create_image(self.solana_kit, prompt, size, n)

            return {
                "status": "success",
                "message": "Image created successfully",
                "images": result["images"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR")
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTPSCalculatorTool(BaseTool):
    name: str = "solana_get_tps"
    description: str = "Get the current TPS of the Solana network."
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            tps = await self.solana_kit.get_tps()

            return {
                "status": "success",
                "message": f"Solana (mainnet-beta) current transactions per second: {tps}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error fetching TPS: {str(e)}",
                "code": getattr(e, "code", "UNKNOWN_ERROR")
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaPumpFunTokenTool(BaseTool):
    name:str = "solana_launch_pump_fun_token"
    description:str = """
    Launch a Pump Fun token on Solana.

    Input (JSON string):
    {
        "token_name": "MyToken",
        "token_ticker": "MTK",
        "description": "A test token",
        "image_url": "http://example.com/image.png"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            result = await self.solana_kit.launch_pump_fun_token(
                data["token_name"],
                data["token_ticker"],
                data["description"],
                data["image_url"],
                options=data.get("options")
            )
            return {
                "status": "success",
                "message": "Pump Fun token launched successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaFetchPriceTool(BaseTool):
    """
    Tool to fetch the price of a token in USDC.
    """
    name:str = "solana_fetch_price"
    description:str = """Fetch the price of a given token in USDC.

    Inputs:
    - tokenId: string, the mint address of the token, e.g., "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    """
    solana_kit: SolanaAgentKit

    async def call(self, input: str) -> str:
        try:
            token_id = input.strip()
            price = await self.solana_kit.fetch_price(token_id)
            return json.dumps({
                "status": "success",
                "tokenId": token_id,
                "priceInUSDC": price,
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "UNKNOWN_ERROR"),
            })
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTokenDataTool(BaseTool):
    """
    Tool to fetch token data for a given token mint address.
    """
    name:str = "solana_token_data"
    description:str = """Get the token data for a given token mint address.

    Inputs:
    - mintAddress: string, e.g., "So11111111111111111111111111111111111111112" (required)
    """
    solana_kit: SolanaAgentKit

    async def call(self, input: str) -> str:
        try:
            mint_address = input.strip()
            token_data = await self.solana_kit.get_token_data_by_address(mint_address)
            return json.dumps({
                "status": "success",
                "tokenData": token_data,
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "UNKNOWN_ERROR"),
            })
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTokenDataByTickerTool(BaseTool):
    """
    Tool to fetch token data for a given token ticker.
    """
    name:str = "solana_token_data_by_ticker"
    description:str = """Get the token data for a given token ticker.

    Inputs:
    - ticker: string, e.g., "USDC" (required)
    """
    solana_kit: SolanaAgentKit

    async def call(self, input: str) -> str:
        try:
            ticker = input.strip()
            token_data = await self.solana_kit.get_token_data_by_ticker(ticker)
            return json.dumps({
                "status": "success",
                "tokenData": token_data,
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "UNKNOWN_ERROR"),
            })
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaMeteoraDLMMTool(BaseTool):
    """
    Tool to create dlmm pool on meteora.
    """
    name: str = "solana_create_meteora_dlmm_pool"
    description: str = """
    Create a Meteora DLMM Pool on Solana.

    Input (JSON string):
    {
        "bin_step": 5,
        "token_a_mint": "7S3d7xxFPgFhVde8XwDoQG9N7kF8Vo48ghAhoNxd34Zp",
        "token_b_mint": "A1b1xxFPgFhVde8XwDoQG9N7kF8Vo48ghAhoNxd34Zp",
        "initial_price": 1.23,
        "price_rounding_up": true,
        "fee_bps": 300,
        "activation_type": "Instant",  // Options: "Instant", "Delayed", "Manual"
        "has_alpha_vault": false,
        "activation_point": null      // Optional, only for Delayed type
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str) -> dict:
        try:
            # Parse input
            data = toJSON(input)

            # Ensure required keys exist
            required_keys = [
                "bin_step",
                "token_a_mint",
                "token_b_mint",
                "initial_price",
                "price_rounding_up",
                "fee_bps",
                "activation_type",
                "has_alpha_vault"
            ]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key: {key}")

            activation_type_mapping = {
                "Slot": ActivationType.Slot,
                "Timestamp": ActivationType.Timestamp,
            }
            activation_type = activation_type_mapping.get(data["activation_type"])
            if activation_type is None:
                raise ValueError("Invalid activation_type. Valid options are: Slot, Timestamp.")

            activation_point = data.get("activation_point", None)

            result = await self.solana_kit.create_meteora_dlmm_pool(
                bin_step=data["bin_step"],
                token_a_mint=data["token_a_mint"],
                token_b_mint=data["token_b_mint"],
                initial_price=data["initial_price"],
                price_rounding_up=data["price_rounding_up"],
                fee_bps=data["fee_bps"],
                activation_type=activation_type,
                has_alpha_vault=data["has_alpha_vault"],
                activation_point=activation_point
            )

            return {
                "status": "success",
                "message": "Meteora DLMM pool created successfully",
                "result": result,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to process input: {input}. Error: {str(e)}",
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaRaydiumBuyTool(BaseTool):
    name: str = "raydium_buy"
    description: str = """
    Buy tokens using Raydium's swap functionality.

    Input (JSON string):
    {
        "pair_address": "address_of_the_trading_pair",
        "sol_in": 0.01,  # Amount of SOL to spend (optional, defaults to 0.01)
        "slippage": 5  # Slippage tolerance in percentage (optional, defaults to 5)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            pair_address = data["pair_address"]
            sol_in = data.get("sol_in", 0.01)  # Default to 0.01 SOL if not provided
            slippage = data.get("slippage", 5)  # Default to 5% slippage if not provided

            result = await self.solana_kit.buy_with_raydium(pair_address, sol_in, slippage)

            return {
                "status": "success",
                "message": "Buy transaction completed successfully",
                "pair_address": pair_address,
                "sol_in": sol_in,
                "slippage": slippage,
                "transaction": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaRaydiumSellTool(BaseTool):
    name: str = "raydium_sell"
    description: str = """
    Sell tokens using Raydium's swap functionality.

    Input (JSON string):
    {
        "pair_address": "address_of_the_trading_pair",
        "percentage": 100,  # Percentage of tokens to sell (optional, defaults to 100)
        "slippage": 5  # Slippage tolerance in percentage (optional, defaults to 5)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            pair_address = data["pair_address"]
            percentage = data.get("percentage", 100)  # Default to 100% if not provided
            slippage = data.get("slippage", 5)  # Default to 5% slippage if not provided

            result = await self.solana_kit.sell_with_raydium(pair_address, percentage, slippage)

            return {
                "status": "success",
                "message": "Sell transaction completed successfully",
                "pair_address": pair_address,
                "percentage": percentage,
                "slippage": slippage,
                "transaction": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaBurnAndCloseTool(BaseTool):
    name: str = "solana_burn_and_close_account"
    description: str = """
    Burn and close a single Solana token account.

    Input: A JSON string with:
    {
        "token_account": "public_key_of_the_token_account"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            token_account = data["token_account"]

            if not token_account:
                raise ValueError("Token account is required.")

            result = await self.solana_kit.burn_and_close_accounts(token_account)

            return {
                "status": "success",
                "message": "Token account burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaBurnAndCloseMultipleTool(BaseTool):
    name: str = "solana_burn_and_close_multiple_accounts"
    description: str = """
    Burn and close multiple Solana token accounts.

    Input: A JSON string with:
    {
        "token_accounts": ["public_key_1", "public_key_2", ...]
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            token_accounts = data.get("token_accounts", [])

            if not isinstance(token_accounts, list) or not token_accounts:
                raise ValueError("A list of token accounts is required.")

            result = await self.solana_kit.multiple_burn_and_close_accounts(token_accounts)

            return {
                "status": "success",
                "message": "Token accounts burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaCreateGibworkTaskTool(BaseTool):
    name: str = "solana_create_gibwork_task"
    description: str = """
    Create an new task on Gibwork

    Input: A JSON string with:
    {
        "title": "title of the task",
        "content: "description of the task",
        "requirements": "requirements to complete the task",
        "tags": ["tag1", "tag2", ...] # list of tags associated with the task,
        "token_mint_address": "token mint address for payment",
        "token_amount": 1000 # amount of token to pay for the task
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            title = data["title"]
            content = data["content"]
            requirements = data["requirements"]
            tags = data.get("tags", [])
            token_mint_address = Pubkey.from_string(data["token_mint_address"])
            token_amount = data["token_amount"]
            
            result = await self.solana_kit.create_gibwork_task(title, content, requirements, tags, token_mint_address, token_amount)

            return {
                "status": "success",
                "message": "Token accounts burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }


    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaCreateGibworkTaskTool(BaseTool):
    name: str = "solana_create_gibwork_task"
    description: str = """
    Create an new task on Gibwork

    Input: A JSON string with:
    {
        "title": "title of the task",
        "content: "description of the task",
        "requirements": "requirements to complete the task",
        "tags": ["tag1", "tag2", ...] # list of tags associated with the task,
        "token_mint_address": "token mint address for payment",
        "token_amount": 1000 # amount of token to pay for the task
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            title = data["title"]
            content = data["content"]
            requirements = data["requirements"]
            tags = data.get("tags", [])
            token_mint_address = Pubkey.from_string(data["token_mint_address"])
            token_amount = data["token_amount"]
            
            result = await self.solana_kit.create_gibwork_task(title, content, requirements, tags, token_mint_address, token_amount)

            return {
                "status": "success",
                "message": "Token accounts burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaBuyUsingMoonshotTool(BaseTool):
    name: str = "solana_buy_using_moonshot"
    description:str = """
    Buy a token using Moonshot.

    Input: A JSON string with:
    {
        "mint_str": "string, the mint address of the token to buy",
        "collateral_amount": 0.01, # optional, collateral amount in SOL to use for the purchase (default: 0.01)
        "slippage_bps": 500 # optional, slippage in basis points (default: 500)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            mint_str = data["mint_str"]
            collateral_amount = data.get("collateral_amount", 0.01)
            slippage_bps = data.get("slippage_bps", 500)
            
            result = await self.solana_kit.buy_using_moonshot(mint_str, collateral_amount, slippage_bps)

            return {
                "status": "success",
                "message": "Token purchased successfully using Moonshot.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaSellUsingMoonshotTool(BaseTool):
    name: str = "solana_sell_using_moonshot"
    description:str = """
    Sell a token using Moonshot.

    Input: A JSON string with:
    {
        "mint_str": "string, the mint address of the token to sell",
        "token_balance": 0.01, # optional, token balance to sell (default: 0.01)
        "slippage_bps": 500 # optional, slippage in basis points (default: 500)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            mint_str = data["mint_str"]
            token_balance = data.get("token_balance", 0.01)
            slippage_bps = data.get("slippage_bps", 500)
            
            result = await self.solana_kit.sell_using_moonshot(mint_str, token_balance, slippage_bps)

            return {
                "status": "success",
                "message": "Token sold successfully using Moonshot.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
            
class SolanaPythGetPriceTool(BaseTool):
    name: str = "solana_pyth_get_price"
    description: str = """
    Fetch the price of a token using the Pyth Oracle.

    Input: A JSON string with:
    {
        "mint_address": "string, the mint address of the token"
    }

    Output:
    {
        "price": float, # the token price (if trading),
        "confidence_interval": float, # the confidence interval (if trading),
        "status": "UNKNOWN", "TRADING", "HALTED", "AUCTION", "IGNORED",
        "message": "string, if not trading"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            mint_address = data["mint_address"]

            result = await self.solana_kit.pythFetchPrice(mint_address)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusGetBalancesTool(BaseTool):
    name: str = "solana_helius_get_balances"
    description: str = """
    Fetch the balances for a given Solana address.

    Input: A JSON string with:
    {
        "address": "string, the Solana address"
    }

    Output: {
        "balances": List[dict], # the list of token balances for the address
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            address = data["address"]

            result = await self.solana_kit.get_balances(address)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class SolanaHeliusGetAddressNameTool(BaseTool):
    name: str = "solana_helius_get_address_name"
    description: str = """
    Fetch the name of a given Solana address.

    Input: A JSON string with:
    {
        "address": "string, the Solana address"
    }

    Output: {
        "name": "string, the name of the address",
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            address = data["address"]

            result = await self.solana_kit.get_address_name(address)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class SolanaHeliusGetNftEventsTool(BaseTool):
    name: str = "solana_helius_get_nft_events"
    description: str = """
    Fetch NFT events based on the given parameters.

    Input: A JSON string with:
    {
        "accounts": "List of addresses to fetch NFT events for",
        "types": "Optional list of event types",
        "sources": "Optional list of sources",
        "start_slot": "Optional start slot",
        "end_slot": "Optional end slot",
        "start_time": "Optional start time",
        "end_time": "Optional end time",
        "first_verified_creator": "Optional list of verified creators",
        "verified_collection_address": "Optional list of verified collection addresses",
        "limit": "Optional limit for results",
        "sort_order": "Optional sort order",
        "pagination_token": "Optional pagination token"
    }

    Output: {
        "events": List[dict], # list of NFT events matching the criteria
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            accounts = data["accounts"]
            types = data.get("types")
            sources = data.get("sources")
            start_slot = data.get("start_slot")
            end_slot = data.get("end_slot")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            first_verified_creator = data.get("first_verified_creator")
            verified_collection_address = data.get("verified_collection_address")
            limit = data.get("limit")
            sort_order = data.get("sort_order")
            pagination_token = data.get("pagination_token")

            result = await self.solana_kit.get_nft_events(
                accounts, types, sources, start_slot, end_slot, start_time, end_time, first_verified_creator, verified_collection_address, limit, sort_order, pagination_token
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class SolanaHeliusGetMintlistsTool(BaseTool):
    name: str = "solana_helius_get_mintlists"
    description: str = """
    Fetch mintlists for a given list of verified creators.

    Input: A JSON string with:
    {
        "first_verified_creators": "List of first verified creator addresses",
        "verified_collection_addresses": "Optional list of verified collection addresses",
        "limit": "Optional limit for results",
        "pagination_token": "Optional pagination token"
    }

    Output: {
        "mintlists": List[dict], # list of mintlists matching the criteria
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            first_verified_creators = data["first_verified_creators"]
            verified_collection_addresses = data.get("verified_collection_addresses")
            limit = data.get("limit")
            pagination_token = data.get("pagination_token")

            result = await self.solana_kit.get_mintlists(first_verified_creators, verified_collection_addresses, limit, pagination_token)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class SolanaHeliusGetNFTFingerprintTool(BaseTool):
    name: str = "solana_helius_get_nft_fingerprint"
    description: str = """
    Fetch NFT fingerprint for a list of mint addresses.

    Input: A JSON string with:
    {
        "mints": ["string, the mint addresses of the NFTs"]
    }

    Output:
    {
        "fingerprint": "list of NFT fingerprint data"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            mints = data["mints"]

            result = await self.solana_kit.get_nft_fingerprint(mints)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaHeliusGetActiveListingsTool(BaseTool):
    name: str = "solana_helius_get_active_listings"
    description: str = """
    Fetch active NFT listings from various marketplaces.

    Input: A JSON string with:
    {
        "first_verified_creators": ["string, the addresses of verified creators"],
        "verified_collection_addresses": ["optional list of verified collection addresses"],
        "marketplaces": ["optional list of marketplaces"],
        "limit": "optional limit to the number of listings",
        "pagination_token": "optional token for pagination"
    }

    Output:
    {
        "active_listings": "list of active NFT listings"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            first_verified_creators = data["first_verified_creators"]
            verified_collection_addresses = data.get("verified_collection_addresses", [])
            marketplaces = data.get("marketplaces", [])
            limit = data.get("limit", None)
            pagination_token = data.get("pagination_token", None)

            result = await self.solana_kit.get_active_listings(
                first_verified_creators, verified_collection_addresses, marketplaces, limit, pagination_token
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaHeliusGetNFTMetadataTool(BaseTool):
    name: str = "solana_helius_get_nft_metadata"
    description: str = """
    Fetch metadata for NFTs based on their mint accounts.

    Input: A JSON string with:
    {
        "mint_accounts": ["string, the mint addresses of the NFTs"]
    }

    Output:
    {
        "metadata": "list of NFT metadata"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            mint_accounts = data["mint_accounts"]

            result = await self.solana_kit.get_nft_metadata(mint_accounts)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaHeliusGetRawTransactionsTool(BaseTool):
    name: str = "solana_helius_get_raw_transactions"
    description: str = """
    Fetch raw transactions for a list of accounts.

    Input: A JSON string with:
    {
        "accounts": ["string, the account addresses"],
        "start_slot": "optional start slot",
        "end_slot": "optional end slot",
        "start_time": "optional start time",
        "end_time": "optional end time",
        "limit": "optional limit",
        "sort_order": "optional sort order",
        "pagination_token": "optional pagination token"
    }

    Output:
    {
        "transactions": "list of raw transactions"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            accounts = data["accounts"]
            start_slot = data.get("start_slot", None)
            end_slot = data.get("end_slot", None)
            start_time = data.get("start_time", None)
            end_time = data.get("end_time", None)
            limit = data.get("limit", None)
            sort_order = data.get("sort_order", None)
            pagination_token = data.get("pagination_token", None)

            result = await self.solana_kit.get_raw_transactions(
                accounts, start_slot, end_slot, start_time, end_time, limit, sort_order, pagination_token
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaHeliusGetParsedTransactionsTool(BaseTool):
    name: str = "solana_helius_get_parsed_transactions"
    description: str = """
    Fetch parsed transactions for a list of transaction IDs.

    Input: A JSON string with:
    {
        "transactions": ["string, the transaction IDs"],
        "commitment": "optional commitment level"
    }

    Output:
    {
        "parsed_transactions": "list of parsed transactions"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transactions = data["transactions"]
            commitment = data.get("commitment", None)

            result = await self.solana_kit.get_parsed_transactions(transactions, commitment)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaHeliusGetParsedTransactionHistoryTool(BaseTool):
    name: str = "solana_helius_get_parsed_transaction_history"
    description: str = """
    Fetch parsed transaction history for a given address.

    Input: A JSON string with:
    {
        "address": "string, the account address",
        "before": "optional before transaction timestamp",
        "until": "optional until transaction timestamp",
        "commitment": "optional commitment level",
        "source": "optional source of transaction",
        "type": "optional type of transaction"
    }

    Output:
    {
        "transaction_history": "list of parsed transaction history"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            address = data["address"]
            before = data.get("before", "")
            until = data.get("until", "")
            commitment = data.get("commitment", "")
            source = data.get("source", "")
            type = data.get("type", "")

            result = await self.solana_kit.get_parsed_transaction_history(
                address, before, until, commitment, source, type
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusCreateWebhookTool(BaseTool):
    name: str = "solana_helius_create_webhook"
    description: str = """
    Create a webhook for transaction events.

    Input: A JSON string with:
    {
        "webhook_url": "URL to send the webhook data",
        "transaction_types": "List of transaction types to listen for",
        "account_addresses": "List of account addresses to monitor",
        "webhook_type": "Type of webhook",
        "txn_status": "optional, transaction status to filter by",
        "auth_header": "optional, authentication header for the webhook"
    }

    Output:
    {
        "status": "success",
        "data": "Webhook creation response"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            webhook_url = data["webhook_url"]
            transaction_types = data["transaction_types"]
            account_addresses = data["account_addresses"]
            webhook_type = data["webhook_type"]
            txn_status = data.get("txn_status", "all")
            auth_header = data.get("auth_header", None)

            result = await self.solana_kit.create_webhook(
                webhook_url, transaction_types, account_addresses, webhook_type, txn_status, auth_header
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusGetAllWebhooksTool(BaseTool):
    name: str = "solana_helius_get_all_webhooks"
    description: str = """
    Fetch all webhooks created in the system.

    Input: None (No parameters required)

    Output:
    {
        "status": "success",
        "data": "List of all webhooks"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            result = await self.solana_kit.get_all_webhooks()
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusGetWebhookTool(BaseTool):
    name: str = "solana_helius_get_webhook"
    description: str = """
    Retrieve a specific webhook by ID.

    Input: A JSON string with:
    {
        "webhook_id": "ID of the webhook to retrieve"
    }

    Output:
    {
        "status": "success",
        "data": "Webhook details"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            webhook_id = data["webhook_id"]

            result = await self.solana_kit.get_webhook(webhook_id)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
class SolanaHeliusEditWebhookTool(BaseTool):
    name: str = "solana_helius_edit_webhook"
    description: str = """
    Edit an existing webhook by its ID.

    Input: A JSON string with:
    {
        "webhook_id": "ID of the webhook to edit",
        "webhook_url": "Updated URL for the webhook",
        "transaction_types": "Updated list of transaction types",
        "account_addresses": "Updated list of account addresses",
        "webhook_type": "Updated webhook type",
        "txn_status": "optional, updated transaction status filter",
        "auth_header": "optional, updated authentication header"
    }

    Output:
    {
        "status": "success",
        "data": "Updated webhook details"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            webhook_id = data["webhook_id"]
            webhook_url = data["webhook_url"]
            transaction_types = data["transaction_types"]
            account_addresses = data["account_addresses"]
            webhook_type = data["webhook_type"]
            txn_status = data.get("txn_status", "all")
            auth_header = data.get("auth_header", None)

            result = await self.solana_kit.edit_webhook(
                webhook_id, webhook_url, transaction_types, account_addresses, webhook_type, txn_status, auth_header
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusDeleteWebhookTool(BaseTool):
    name: str = "solana_helius_delete_webhook"
    description: str = """
    Delete a webhook by its ID.

    Input: A JSON string with:
    {
        "webhook_id": "ID of the webhook to delete"
    }

    Output:
    {
        "status": "success",
        "data": "Webhook deletion confirmation"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            webhook_id = data["webhook_id"]

            result = await self.solana_kit.delete_webhook(webhook_id)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaFetchTokenReportSummaryTool(BaseTool):
    name: str = "solana_fetch_token_report_summary"
    description: str = """
    Fetch a summary report for a specific token.

    Input: A JSON string with:
    {
        "mint": "Mint address of the token"
    }

    Output:
    {
        "status": "success",
        "data": <TokenCheck object as a dictionary>
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        """
        Asynchronous implementation of the tool.
        """
        try:
            data = json.loads(input)
            mint = data.get("mint")
            if not mint:
                raise ValueError("Missing 'mint' in input.")
            
            result = self.solana_kit.fetch_token_report_summary(mint)
            return {
                "status": "success",
                "data": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """
        Synchronous version of the tool, not implemented for async-only tools.
        """
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaFetchTokenDetailedReportTool(BaseTool):
    name: str = "solana_fetch_token_detailed_report"
    description: str = """
    Fetch a detailed report for a specific token.

    Input: A JSON string with:
    {
        "mint": "Mint address of the token"
    }

    Output:
    {
        "status": "success",
        "data": <TokenCheck object as a dictionary>
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        """
        Asynchronous implementation of the tool.
        """
        try:
            data = json.loads(input)
            mint = data.get("mint")
            if not mint:
                raise ValueError("Missing 'mint' in input.")
            
            result = self.solana_kit.fetch_token_detailed_report(mint)
            return {
                "status": "success",
                "data": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """
        Synchronous version of the tool, not implemented for async-only tools.
        """
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetPumpCurveStateTool(BaseTool):
    name: str = "solana_get_pump_curve_state"
    description: str = """
    Get the pump curve state for a specific bonding curve.

    Input: A JSON string with:
    {
        "conn": "AsyncClient instance or connection object",
        "curve_address": "The public key of the bonding curve as a string"
    }

    Output:
    {
        "status": "success",
        "data": <PumpCurveState object as a dictionary>
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            conn = data.get("conn")
            curve_address = data.get("curve_address")
            if not conn or not curve_address:
                raise ValueError("Missing 'conn' or 'curve_address' in input.")

            curve_address_key = Pubkey(curve_address)
            result = await self.solana_kit.get_pump_curve_state(conn, curve_address_key)
            return {
                "status": "success",
                "data": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution.")

class SolanaCalculatePumpCurvePriceTool(BaseTool):
    name: str = "solana_calculate_pump_curve_price"
    description: str = """
    Calculate the price for a bonding curve based on its state.

    Input: A JSON string with:
    {
        "curve_state": "BondingCurveState object as a dictionary"
    }

    Output:
    {
        "status": "success",
        "price": "The calculated price"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            curve_state = data.get("curve_state")
            if not curve_state:
                raise ValueError("Missing 'curve_state' in input.")

            result = await self.solana_kit.calculate_pump_curve_price(curve_state)
            return {
                "status": "success",
                "price": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution.")

class SolanaBuyTokenTool(BaseTool):
    name: str = "solana_buy_token"
    description: str = """
    Buy a specific amount of tokens using the bonding curve.

    Input: A JSON string with:
    {
        "mint": "The mint address of the token as a string",
        "bonding_curve": "The bonding curve public key as a string",
        "associated_bonding_curve": "The associated bonding curve public key as a string",
        "amount": "The amount of tokens to buy",
        "slippage": "The allowed slippage percentage",
        "max_retries": "Maximum retries for the transaction"
    }

    Output:
    {
        "status": "success",
        "transaction": "Details of the successful transaction"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            required_keys = ["mint", "bonding_curve", "associated_bonding_curve", "amount", "slippage", "max_retries"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing '{key}' in input.")

            mint = Pubkey(data["mint"])
            bonding_curve = Pubkey(data["bonding_curve"])
            associated_bonding_curve = Pubkey(data["associated_bonding_curve"])
            amount = data["amount"]
            slippage = data["slippage"]
            max_retries = data["max_retries"]

            result = await self.solana_kit.buy_token(
                mint, bonding_curve, associated_bonding_curve, amount, slippage, max_retries
            )
            return {
                "status": "success",
                "transaction": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution.")

class SolanaSellTokenTool(BaseTool):
    name: str = "solana_sell_token"
    description: str = """
    Sell a specific amount of tokens using the bonding curve.

    Input: A JSON string with:
    {
        "mint": "The mint address of the token as a string",
        "bonding_curve": "The bonding curve public key as a string",
        "associated_bonding_curve": "The associated bonding curve public key as a string",
        "amount": "The amount of tokens to sell",
        "slippage": "The allowed slippage percentage",
        "max_retries": "Maximum retries for the transaction"
    }

    Output:
    {
        "status": "success",
        "transaction": "Details of the successful transaction"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            required_keys = ["mint", "bonding_curve", "associated_bonding_curve", "amount", "slippage", "max_retries"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing '{key}' in input.")

            mint = Pubkey(data["mint"])
            bonding_curve = Pubkey(data["bonding_curve"])
            associated_bonding_curve = Pubkey(data["associated_bonding_curve"])
            amount = data["amount"]
            slippage = data["slippage"]
            max_retries = data["max_retries"]

            result = await self.solana_kit.sell_token(
                mint, bonding_curve, associated_bonding_curve, amount, slippage, max_retries
            )
            return {
                "status": "success",
                "transaction": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution.")

class SolanaSNSResolveTool(BaseTool):
    name: str = "solana_sns_resolve"
    description: str = """
    Resolves a Solana Name Service (SNS) domain to its corresponding address.

    Input: A JSON string with:
    {
        "domain": "string, the SNS domain (e.g., example.sol)"
    }

    Output:
    {
        "address": "string, the resolved Solana address",
        "message": "string, if resolution fails"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            domain = data["domain"]
            if not domain:
                raise ValueError("Domain is required.")

            address = await self.solana_kit.resolve_name_to_address(domain)
            return {
                "address": address or "Not Found",
                "message": "Success" if address else "Domain not found."
            }
        except Exception as e:
            return {
                "address": None,
                "message": f"Error resolving domain: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaSNSRegisterDomainTool(BaseTool):
    name: str = "solana_sns_register_domain"
    description: str = """
    Prepares a transaction to register a new SNS domain.

    Input: A JSON string with:
    {
        "domain": "string, the domain to register",
        "buyer": "string, base58 public key of the buyer's wallet",
        "buyer_token_account": "string, base58 public key of the buyer's token account",
        "space": "integer, bytes to allocate for the domain",
        "mint": "string, optional, the token mint public key (default: USDC)",
        "referrer_key": "string, optional, base58 public key of the referrer"
    }

    Output:
    {
        "transaction": "string, base64-encoded transaction object",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            domain = data["domain"]
            buyer = data["buyer"]
            buyer_token_account = data["buyer_token_account"]
            space = data["space"]
            mint = data.get("mint")
            referrer_key = data.get("referrer_key")

            if not all([domain, buyer, buyer_token_account, space]):
                raise ValueError("Domain, buyer, buyer_token_account, and space are required.")

            transaction = await self.solana_kit.get_registration_transaction(
                domain, buyer, buyer_token_account, space, mint, referrer_key
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error preparing registration transaction: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaSNSGetFavouriteDomainTool(BaseTool):
    name: str = "solana_sns_get_favourite_domain"
    description: str = """
    Fetches the favorite domain of a given owner using Solana Name Service.

    Input: A JSON string with:
    {
        "owner": "string, the base58-encoded public key of the domain owner"
    }

    Output:
    {
        "domain": "string, the favorite domain of the owner",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            owner = data["owner"]
            if not owner:
                raise ValueError("Owner address is required.")

            domain = await self.solana_kit.get_favourite_domain(owner)
            return {
                "domain": domain or "Not Found",
                "message": "Success" if domain else "No favorite domain found for this owner."
            }
        except Exception as e:
            return {
                "domain": None,
                "message": f"Error fetching favorite domain: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaSNSGetAllDomainsTool(BaseTool):
    name: str = "solana_sns_get_all_domains"
    description: str = """
    Fetches all domains associated with a given owner using Solana Name Service.

    Input: A JSON string with:
    {
        "owner": "string, the base58-encoded public key of the domain owner"
    }

    Output:
    {
        "domains": ["string", "string", ...], # List of domains owned by the owner
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            owner = data["owner"]
            if not owner:
                raise ValueError("Owner address is required.")

            domains = await self.solana_kit.get_all_domains_for_owner(owner)
            return {
                "domains": domains or [],
                "message": "Success" if domains else "No domains found for this owner."
            }
        except Exception as e:
            return {
                "domains": [],
                "message": f"Error fetching domains: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaDeployCollectionTool(BaseTool):
    name: str = "solana_deploy_collection"
    description: str = """
    Deploys an NFT collection using the Metaplex program.

    Input: A JSON string with:
    {
        "name": "string, the name of the NFT collection",
        "uri": "string, the metadata URI",
        "royalty_basis_points": "int, royalty percentage in basis points (e.g., 500 for 5%)",
        "creator_address": "string, the creator's public key"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "string, the transaction signature if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            name = data["name"]
            uri = data["uri"]
            royalty_basis_points = data["royalty_basis_points"]
            creator_address = data["creator_address"]

            if not all([name, uri, royalty_basis_points, creator_address]):
                raise ValueError("All input fields are required.")

            result = await self.solana_kit.deploy_collection(
                name=name,
                uri=uri,
                royalty_basis_points=royalty_basis_points,
                creator_address=creator_address,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error deploying collection: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class SolanaGetMetaplexAssetTool(BaseTool):
    name: str = "solana_get_metaplex_asset"
    description: str = """
    Fetches detailed information about a specific Metaplex asset.

    Input: A JSON string with:
    {
        "asset_id": "string, the unique identifier of the asset"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "object, detailed asset information if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            asset_id = data["asset_id"]

            if not asset_id:
                raise ValueError("Asset ID is required.")

            result = await self.solana_kit.get_metaplex_asset(asset_id)
            return result
        except Exception as e:
            return {"success": False, "message": f"Error fetching Metaplex asset: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
    
class SolanaGetMetaplexAssetsByCreatorTool(BaseTool):
    name: str = "solana_get_metaplex_assets_by_creator"
    description: str = """
    Fetches assets created by a specific creator.

    Input: A JSON string with:
    {
        "creator": "string, the creator's public key",
        "only_verified": "bool, fetch only verified assets (default: False)",
        "sort_by": "string, field to sort by (e.g., 'date')",
        "sort_direction": "string, 'asc' or 'desc'",
        "limit": "int, maximum number of assets",
        "page": "int, page number for paginated results"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "list, the list of assets if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            creator = data["creator"]
            only_verified = data.get("only_verified", False)
            sort_by = data.get("sort_by")
            sort_direction = data.get("sort_direction")
            limit = data.get("limit")
            page = data.get("page")

            if not creator:
                raise ValueError("Creator address is required.")

            result = await self.solana_kit.get_metaplex_assets_by_creator(
                creator=creator,
                onlyVerified=only_verified,
                sortBy=sort_by,
                sortDirection=sort_direction,
                limit=limit,
                page=page,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error fetching assets by creator: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class SolanaGetMetaplexAssetsByAuthorityTool(BaseTool):
    name: str = "solana_get_metaplex_assets_by_authority"
    description: str = """
    Fetches assets created by a specific authority.

    Input: A JSON string with:
    {
        "authority": "string, the authority's public key",
        "sort_by": "string, field to sort by (e.g., 'date')",
        "sort_direction": "string, 'asc' or 'desc'",
        "limit": "int, maximum number of assets",
        "page": "int, page number for paginated results"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "list, the list of assets if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            authority = data["authority"]
            sort_by = data.get("sort_by")
            sort_direction = data.get("sort_direction")
            limit = data.get("limit")
            page = data.get("page")

            if not authority:
                raise ValueError("Creator address is required.")

            result = await self.solana_kit.get_metaplex_assets_by_authority(
                authority=authority,
                sortBy=sort_by,
                sortDirection=sort_direction,
                limit=limit,
                page=page,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error fetching assets by authority: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class SolanaMintMetaplexCoreNFTTool(BaseTool):
    name: str = "solana_mint_metaplex_core_nft"
    description: str = """
    Mints an NFT using the Metaplex Core program.

    Input: A JSON string with:
    {
        "collection_mint": "string, the collection mint's public key",
        "name": "string, the name of the NFT",
        "uri": "string, the metadata URI",
        "seller_fee_basis_points": "int, royalty in basis points",
        "address": "string, the creator's public key",
        "share": "string, share percentage for the creator",
        "recipient": "string, recipient's public key"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "transaction": "string, the transaction signature if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            collection_mint = data["collection_mint"]
            name = data["name"]
            uri = data["uri"]
            seller_fee_basis_points = data.get("seller_fee_basis_points")
            address = data.get("address")
            share = data.get("share")
            recipient = data.get("recipient")

            if not all([collection_mint, name, uri]):
                raise ValueError("Collection mint, name, and URI are required.")

            result = await self.solana_kit.mint_metaplex_core_nft(
                collectionMint=collection_mint,
                name=name,
                uri=uri,
                sellerFeeBasisPoints=seller_fee_basis_points,
                address=address,
                share=share,
                recipient=recipient,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error minting NFT: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class SolanaDeBridgeCreateTransactionTool(BaseTool):
    name: str = "debridge_create_transaction"
    description: str = """
    Creates a transaction for bridging assets across chains using DeBridge.

    Input: A JSON string with:
    {
        "src_chain_id": "string, the source chain ID",
        "src_chain_token_in": "string, the token address on the source chain",
        "src_chain_token_in_amount": "string, the token amount to send on the source chain",
        "dst_chain_id": "string, the destination chain ID",
        "dst_chain_token_out": "string, the token address on the destination chain",
        "dst_chain_token_out_recipient": "string, the recipient address on the destination chain",
        "src_chain_order_authority_address": "string, source chain order authority address",
        "dst_chain_order_authority_address": "string, destination chain order authority address",
        "affiliate_fee_percent": "string, optional, affiliate fee percent (default: '0')",
        "affiliate_fee_recipient": "string, optional, affiliate fee recipient address",
        "prepend_operating_expenses": "bool, optional, whether to prepend operating expenses (default: True)",
        "dst_chain_token_out_amount": "string, optional, amount of destination chain tokens out (default: 'auto')"
    }

    Output:
    {
        "transaction_data": "dict, the transaction data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_data = await self.solana_kit.create_debridge_transaction(
                src_chain_id=data["src_chain_id"],
                src_chain_token_in=data["src_chain_token_in"],
                src_chain_token_in_amount=data["src_chain_token_in_amount"],
                dst_chain_id=data["dst_chain_id"],
                dst_chain_token_out=data["dst_chain_token_out"],
                dst_chain_token_out_recipient=data["dst_chain_token_out_recipient"],
                src_chain_order_authority_address=data["src_chain_order_authority_address"],
                dst_chain_order_authority_address=data["dst_chain_order_authority_address"],
                affiliate_fee_percent=data.get("affiliate_fee_percent", "0"),
                affiliate_fee_recipient=data.get("affiliate_fee_recipient", ""),
                prepend_operating_expenses=data.get("prepend_operating_expenses", True),
                dst_chain_token_out_amount=data.get("dst_chain_token_out_amount", "auto")
            )
            return {
                "transaction_data": transaction_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_data": None,
                "message": f"Error creating DeBridge transaction: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaDeBridgeExecuteTransactionTool(BaseTool):
    name: str = "debridge_execute_transaction"
    description: str = """
    Executes a prepared DeBridge transaction.

    Input: A JSON string with:
    {
        "transaction_data": "dict, the prepared transaction data"
    }

    Output:
    {
        "result": "dict, the result of transaction execution",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_data = data["transaction_data"]
            if not transaction_data:
                raise ValueError("Transaction data is required.")

            result = await self.solana_kit.execute_debridge_transaction(transaction_data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing DeBridge transaction: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaDeBridgeCheckTransactionStatusTool(BaseTool):
    name: str = "debridge_check_transaction_status"
    description: str = """
    Checks the status of a DeBridge transaction.

    Input: A JSON string with:
    {
        "tx_hash": "string, the transaction hash"
    }

    Output:
    {
        "status": "string, the transaction status",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            tx_hash = data["tx_hash"]
            if not tx_hash:
                raise ValueError("Transaction hash is required.")

            status = await self.solana_kit.check_transaction_status(tx_hash)
            return {
                "status": status,
                "message": "Success"
            }
        except Exception as e:
            return {
                "status": None,
                "message": f"Error checking transaction status: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaCybersCreateCoinTool(BaseTool):
    name: str = "cybers_create_coin"
    description: str = """
    Creates a new coin using the CybersManager.

    Input: A JSON string with:
    {
        "name": "string, the name of the coin",
        "symbol": "string, the symbol of the coin",
        "image_path": "string, the file path to the coin's image",
        "tweet_author_id": "string, the Twitter ID of the coin's author",
        "tweet_author_username": "string, the Twitter username of the coin's author"
    }

    Output:
    {
        "coin_id": "string, the unique ID of the created coin",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            name = data["name"]
            symbol = data["symbol"]
            image_path = data["image_path"]
            tweet_author_id = data["tweet_author_id"]
            tweet_author_username = data["tweet_author_username"]

            if not all([name, symbol, image_path, tweet_author_id, tweet_author_username]):
                raise ValueError("All fields (name, symbol, image_path, tweet_author_id, tweet_author_username) are required.")

            coin_id = await self.solana_kit.cybers_create_coin(
                name=name,
                symbol=symbol,
                image_path=image_path,
                tweet_author_id=tweet_author_id,
                tweet_author_username=tweet_author_username
            )
            return {
                "coin_id": coin_id,
                "message": "Success"
            }
        except Exception as e:
            return {
                "coin_id": None,
                "message": f"Error creating coin: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetTipAccounts(BaseTool):
    name: str = "get_tip_accounts"
    description: str = """
    Get all available Jito tip accounts.

    Output:
    {
        "accounts": "List of Jito tip accounts"
    }
    """
    solana_kit: SolanaAgentKit
    
    async def _arun(self, input: str):
        try:
            result = await self.solana_kit.get_tip_accounts()
            return {
                "accounts": result
            }
        except Exception as e:
            return {
                "accounts": None
            }
    
    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
        
class SolanaGetRandomTipAccount(BaseTool):
    name: str = "get_random_tip_account"
    description: str = """
    Get a randomly selected Jito tip account from the existing list.

    Output:
    {
        "account": "Randomly selected Jito tip account"
    }
    """
    solana_kit: SolanaAgentKit
    
    async def _arun(self, input: str):
        try:
            result = await self.solana_kit.get_random_tip_account()
            return {
                "account": result
            }
        except Exception as e:
            return {
                "account": None
            }
    
    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
        
class SolanaGetBundleStatuses(BaseTool):
    name: str = "get_bundle_statuses"
    description: str = """
    Get the current statuses of specified Jito bundles.

    Output:
    {
        "statuses": "List of corresponding bundle statuses"
    }
    """
    solana_kit: SolanaAgentKit
    
    async def _arun(self, input: str):
        try:
            bundle_uuids = input["bundle_uuids"]
            result = await self.solana_kit.get_bundle_statuses(bundle_uuids)
            return {
                "statuses": result
            }
        except Exception as e:
            return {
                "statuses": None
            }
    
    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
        
class SolanaSendBundle(BaseTool):
    name: str = "send_bundle"
    description: str = """
    Send a bundle of transactions to the Jito network for processing.

    Output:
    {
        "bundle_ids": "List of unique identifiers for the submitted bundles"
    }
    """
    solana_kit: SolanaAgentKit
    
    async def _arun(self, input: str):
        try:
            params = input["txn_signatures"]
            result = await self.solana_kit.send_bundle(params)
            return {
                "bundle_ids": result
            }
        except Exception as e:
            return {
                "bundle_ids": None
            }
    
    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
        
class SolanaGetInflightBundleStatuses(BaseTool):
    name: str = "get_inflight_bundle_statuses"
    description: str = """
    Get the statuses of bundles that are currently in flight.

    Output:
    {
        "statuses": "List of statuses corresponding to currently inflight bundles"
    }
    """
    solana_kit: SolanaAgentKit
    
    async def _arun(self, input: str):
        try:
            bundle_uuids = input["bundle_uuids"]
            result = await self.solana_kit.get_inflight_bundle_statuses(bundle_uuids)
            return {
                "statuses": result
            }
        except Exception as e:
            return {
                "statuses": None
            }
    
    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
        
class SolanaSendTxn(BaseTool):
    name: str = "send_txn"
    description: str = """
    Send an individual transaction to the Jito network for processing.

    Output:
    {
        "status": "Unique identifier of the processed transaction bundle"
    }
    """
    solana_kit: SolanaAgentKit
    
    async def _arun(self, input: str):
        try:
            params = [input["txn_signature"]]
            bundleOnly = input["bundleOnly"]
            result = await self.solana_kit.send_txn(params, bundleOnly)
            return {
                "status": result
            }
        except Exception as e:
            return {
                "status": None
            }
    
    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
class BackpackGetAccountBalancesTool(BaseTool):
    name: str = "backpack_get_account_balances"
    description: str = """
    Fetches account balances using the BackpackManager.

    Input: None
    Output:
    {
        "balances": "dict, the account balances",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            balances = await self.solana_kit.get_account_balances()
            return {
                "balances": balances,
                "message": "Success"
            }
        except Exception as e:
            return {
                "balances": None,
                "message": f"Error fetching account balances: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackRequestWithdrawalTool(BaseTool):
    name: str = "backpack_request_withdrawal"
    description: str = """
    Requests a withdrawal using the BackpackManager.

    Input: A JSON string with:
    {
        "address": "string, the destination address",
        "blockchain": "string, the blockchain name",
        "quantity": "string, the quantity to withdraw",
        "symbol": "string, the token symbol",
        "additional_params": "optional additional parameters as JSON object"
    }
    Output:
    {
        "result": "dict, the withdrawal request result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.request_withdrawal(
                address=data["address"],
                blockchain=data["blockchain"],
                quantity=data["quantity"],
                symbol=data["symbol"],
                **data.get("additional_params", {})
            )
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error requesting withdrawal: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetAccountSettingsTool(BaseTool):
    name: str = "backpack_get_account_settings"
    description: str = """
    Fetches account settings using the BackpackManager.

    Input: None
    Output:
    {
        "settings": "dict, the account settings",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            settings = await self.solana_kit.get_account_settings()
            return {
                "settings": settings,
                "message": "Success"
            }
        except Exception as e:
            return {
                "settings": None,
                "message": f"Error fetching account settings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackUpdateAccountSettingsTool(BaseTool):
    name: str = "backpack_update_account_settings"
    description: str = """
    Updates account settings using the BackpackManager.

    Input: A JSON string with additional parameters for the account settings.
    Output:
    {
        "result": "dict, the result of the update",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.update_account_settings(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error updating account settings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowLendPositionsTool(BaseTool):
    name: str = "backpack_get_borrow_lend_positions"
    description: str = """
    Fetches borrow/lend positions using the BackpackManager.

    Input: None
    Output:
    {
        "positions": "list, the borrow/lend positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            positions = await self.solana_kit.get_borrow_lend_positions()
            return {
                "positions": positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "positions": None,
                "message": f"Error fetching borrow/lend positions: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackExecuteBorrowLendTool(BaseTool):
    name: str = "backpack_execute_borrow_lend"
    description: str = """
    Executes a borrow/lend operation using the BackpackManager.

    Input: A JSON string with:
    {
        "quantity": "string, the amount to borrow or lend",
        "side": "string, either 'borrow' or 'lend'",
        "symbol": "string, the token symbol"
    }
    Output:
    {
        "result": "dict, the result of the operation",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.execute_borrow_lend(
                quantity=data["quantity"],
                side=data["side"],
                symbol=data["symbol"]
            )
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing borrow/lend operation: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFillHistoryTool(BaseTool):
    name: str = "backpack_get_fill_history"
    description: str = """
    Fetches the fill history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the fill history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_fill_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching fill history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowPositionHistoryTool(BaseTool):
    name: str = "backpack_get_borrow_position_history"
    description: str = """
    Fetches the borrow position history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the borrow position history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_borrow_position_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching borrow position history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFundingPaymentsTool(BaseTool):
    name: str = "backpack_get_funding_payments"
    description: str = """
    Fetches funding payments using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "payments": "list, the funding payments records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            payments = await self.solana_kit.get_funding_payments(**data)
            return {
                "payments": payments,
                "message": "Success"
            }
        except Exception as e:
            return {
                "payments": None,
                "message": f"Error fetching funding payments: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOrderHistoryTool(BaseTool):
    name: str = "backpack_get_order_history"
    description: str = """
    Fetches order history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the order history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_order_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching order history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetPnlHistoryTool(BaseTool):
    name: str = "backpack_get_pnl_history"
    description: str = """
    Fetches PNL history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the PNL history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_pnl_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching PNL history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSettlementHistoryTool(BaseTool):
    name: str = "backpack_get_settlement_history"
    description: str = """
    Fetches settlement history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the settlement history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_settlement_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching settlement history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetUsersOpenOrdersTool(BaseTool):
    name: str = "backpack_get_users_open_orders"
    description: str = """
    Fetches user's open orders using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "open_orders": "list, the user's open orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            open_orders = await self.solana_kit.get_users_open_orders(**data)
            return {
                "open_orders": open_orders,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_orders": None,
                "message": f"Error fetching user's open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackExecuteOrderTool(BaseTool):
    name: str = "backpack_execute_order"
    description: str = """
    Executes an order using the BackpackManager.

    Input: A JSON string with order parameters.
    Output:
    {
        "result": "dict, the execution result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.execute_order(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackCancelOpenOrderTool(BaseTool):
    name: str = "backpack_cancel_open_order"
    description: str = """
    Cancels an open order using the BackpackManager.

    Input: A JSON string with order details.
    Output:
    {
        "result": "dict, the cancellation result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.cancel_open_order(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error canceling open order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOpenOrdersTool(BaseTool):
    name: str = "backpack_get_open_orders"
    description: str = """
    Fetches open orders using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "open_orders": "list, the open orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            open_orders = await self.solana_kit.get_open_orders(**data)
            return {
                "open_orders": open_orders,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_orders": None,
                "message": f"Error fetching open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackCancelOpenOrdersTool(BaseTool):
    name: str = "backpack_cancel_open_orders"
    description: str = """
    Cancels multiple open orders using the BackpackManager.

    Input: A JSON string with order details.
    Output:
    {
        "result": "dict, the cancellation result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.cancel_open_orders(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error canceling open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSupportedAssetsTool(BaseTool):
    name: str = "backpack_get_supported_assets"
    description: str = """
    Fetches supported assets using the BackpackManager.

    Input: None
    Output:
    {
        "assets": "list, the supported assets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            assets = await self.solana_kit.get_supported_assets()
            return {
                "assets": assets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "assets": None,
                "message": f"Error fetching supported assets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetTickerInformationTool(BaseTool):
    name: str = "backpack_get_ticker_information"
    description: str = """
    Fetches ticker information using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "ticker_information": "dict, the ticker information",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            ticker_info = await self.solana_kit.get_ticker_information(**data)
            return {
                "ticker_information": ticker_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "ticker_information": None,
                "message": f"Error fetching ticker information: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetMarketsTool(BaseTool):
    name: str = "backpack_get_markets"
    description: str = """
    Fetches all markets using the BackpackManager.

    Input: None
    Output:
    {
        "markets": "list, the available markets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            markets = await self.solana_kit.get_markets()
            return {
                "markets": markets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "markets": None,
                "message": f"Error fetching markets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetMarketTool(BaseTool):
    name: str = "backpack_get_market"
    description: str = """
    Fetches a specific market using the BackpackManager.

    Input: A JSON string with market query parameters.
    Output:
    {
        "market": "dict, the market data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            market = await self.solana_kit.get_market(**data)
            return {
                "market": market,
                "message": "Success"
            }
        except Exception as e:
            return {
                "market": None,
                "message": f"Error fetching market: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetTickersTool(BaseTool):
    name: str = "backpack_get_tickers"
    description: str = """
    Fetches tickers for all markets using the BackpackManager.

    Input: None
    Output:
    {
        "tickers": "list, the market tickers",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            tickers = await self.solana_kit.get_tickers()
            return {
                "tickers": tickers,
                "message": "Success"
            }
        except Exception as e:
            return {
                "tickers": None,
                "message": f"Error fetching tickers: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetDepthTool(BaseTool):
    name: str = "backpack_get_depth"
    description: str = """
    Fetches the order book depth for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol"
    }
    Output:
    {
        "depth": "dict, the order book depth",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            symbol = data["symbol"]
            depth = await self.solana_kit.get_depth(symbol)
            return {
                "depth": depth,
                "message": "Success"
            }
        except Exception as e:
            return {
                "depth": None,
                "message": f"Error fetching depth: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetKlinesTool(BaseTool):
    name: str = "backpack_get_klines"
    description: str = """
    Fetches K-Lines data for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "interval": "string, the interval for K-Lines",
        "start_time": "int, the start time for data",
        "end_time": "int, optional, the end time for data"
    }
    Output:
    {
        "klines": "dict, the K-Lines data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            klines = await self.solana_kit.get_klines(
                symbol=data["symbol"],
                interval=data["interval"],
                start_time=data["start_time"],
                end_time=data.get("end_time")
            )
            return {
                "klines": klines,
                "message": "Success"
            }
        except Exception as e:
            return {
                "klines": None,
                "message": f"Error fetching K-Lines: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetMarkPriceTool(BaseTool):
    name: str = "backpack_get_mark_price"
    description: str = """
    Fetches mark price, index price, and funding rate for a given market symbol.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol"
    }
    Output:
    {
        "mark_price_data": "dict, the mark price data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            symbol = data["symbol"]
            mark_price_data = await self.solana_kit.get_mark_price(symbol)
            return {
                "mark_price_data": mark_price_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "mark_price_data": None,
                "message": f"Error fetching mark price: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOpenInterestTool(BaseTool):
    name: str = "backpack_get_open_interest"
    description: str = """
    Fetches the open interest for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol"
    }
    Output:
    {
        "open_interest": "dict, the open interest data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            symbol = data["symbol"]
            open_interest = await self.solana_kit.get_open_interest(symbol)
            return {
                "open_interest": open_interest,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_interest": None,
                "message": f"Error fetching open interest: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFundingIntervalRatesTool(BaseTool):
    name: str = "backpack_get_funding_interval_rates"
    description: str = """
    Fetches funding interval rate history for futures using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "limit": "int, optional, maximum results to return (default: 100)",
        "offset": "int, optional, records to skip (default: 0)"
    }
    Output:
    {
        "funding_rates": "dict, the funding interval rate data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            funding_rates = await self.solana_kit.get_funding_interval_rates(
                symbol=data["symbol"],
                limit=data.get("limit", 100),
                offset=data.get("offset", 0)
            )
            return {
                "funding_rates": funding_rates,
                "message": "Success"
            }
        except Exception as e:
            return {
                "funding_rates": None,
                "message": f"Error fetching funding interval rates: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetStatusTool(BaseTool):
    name: str = "backpack_get_status"
    description: str = """
    Fetches the system status and any status messages using the BackpackManager.

    Input: None
    Output:
    {
        "status": "dict, the system status",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            status = await self.solana_kit.get_status()
            return {
                "status": status,
                "message": "Success"
            }
        except Exception as e:
            return {
                "status": None,
                "message": f"Error fetching system status: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackSendPingTool(BaseTool):
    name: str = "backpack_send_ping"
    description: str = """
    Sends a ping and expects a "pong" response using the BackpackManager.

    Input: None
    Output:
    {
        "response": "string, the response ('pong')",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            response = await self.solana_kit.send_ping()
            return {
                "response": response,
                "message": "Success"
            }
        except Exception as e:
            return {
                "response": None,
                "message": f"Error sending ping: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSystemTimeTool(BaseTool):
    name: str = "backpack_get_system_time"
    description: str = """
    Fetches the current system time using the BackpackManager.

    Input: None
    Output:
    {
        "system_time": "string, the current system time",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            system_time = await self.solana_kit.get_system_time()
            return {
                "system_time": system_time,
                "message": "Success"
            }
        except Exception as e:
            return {
                "system_time": None,
                "message": f"Error fetching system time: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetRecentTradesTool(BaseTool):
    name: str = "backpack_get_recent_trades"
    description: str = """
    Fetches the most recent trades for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "limit": "int, optional, maximum results to return (default: 100)"
    }
    Output:
    {
        "recent_trades": "dict, the recent trade data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            recent_trades = await self.solana_kit.get_recent_trades(
                symbol=data["symbol"],
                limit=data.get("limit", 100)
            )
            return {
                "recent_trades": recent_trades,
                "message": "Success"
            }
        except Exception as e:
            return {
                "recent_trades": None,
                "message": f"Error fetching recent trades: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetHistoricalTradesTool(BaseTool):
    name: str = "backpack_get_historical_trades"
    description: str = """
    Fetches historical trades for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "limit": "int, optional, maximum results to return (default: 100)",
        "offset": "int, optional, records to skip (default: 0)"
    }
    Output:
    {
        "historical_trades": "dict, the historical trade data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            historical_trades = await self.solana_kit.get_historical_trades(
                symbol=data["symbol"],
                limit=data.get("limit", 100),
                offset=data.get("offset", 0)
            )
            return {
                "historical_trades": historical_trades,
                "message": "Success"
            }
        except Exception as e:
            return {
                "historical_trades": None,
                "message": f"Error fetching historical trades: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetCollateralInfoTool(BaseTool):
    name: str = "backpack_get_collateral_info"
    description: str = """
    Fetches collateral information using the BackpackManager.

    Input: A JSON string with:
    {
        "sub_account_id": "int, optional, the sub-account ID for collateral information"
    }
    Output:
    {
        "collateral_info": "dict, the collateral information",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            collateral_info = await self.solana_kit.get_collateral_info(
                sub_account_id=data.get("sub_account_id")
            )
            return {
                "collateral_info": collateral_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "collateral_info": None,
                "message": f"Error fetching collateral information: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetAccountDepositsTool(BaseTool):
    name: str = "backpack_get_account_deposits"
    description: str = """
    Fetches account deposits using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "deposits": "dict, the account deposit data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            deposits = await self.solana_kit.get_account_deposits(**data)
            return {
                "deposits": deposits,
                "message": "Success"
            }
        except Exception as e:
            return {
                "deposits": None,
                "message": f"Error fetching account deposits: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOpenPositionsTool(BaseTool):
    name: str = "backpack_get_open_positions"
    description: str = """
    Fetches open positions using the BackpackManager.

    Input: None
    Output:
    {
        "open_positions": "list, the open positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            open_positions = await self.solana_kit.get_open_positions()
            return {
                "open_positions": open_positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_positions": None,
                "message": f"Error fetching open positions: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowHistoryTool(BaseTool):
    name: str = "backpack_get_borrow_history"
    description: str = """
    Fetches borrow history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "borrow_history": "list, the borrow history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            borrow_history = await self.solana_kit.get_borrow_history(**data)
            return {
                "borrow_history": borrow_history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "borrow_history": None,
                "message": f"Error fetching borrow history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetInterestHistoryTool(BaseTool):
    name: str = "backpack_get_interest_history"
    description: str = """
    Fetches interest history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "interest_history": "list, the interest history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            interest_history = await self.solana_kit.get_interest_history(**data)
            return {
                "interest_history": interest_history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "interest_history": None,
                "message": f"Error fetching interest history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class ClosePerpTradeShortTool(BaseTool):
    name: str = "close_perp_trade_short"
    description: str = """
    Closes a perpetual short trade.

    Input: A JSON string with:
    {
        "price": "float, execution price for closing the trade",
        "trade_mint": "string, token mint address for the trade"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.close_perp_trade_short(
                price=data["price"],
                trade_mint=data["trade_mint"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error closing perp short trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class ClosePerpTradeLongTool(BaseTool):
    name: str = "close_perp_trade_long"
    description: str = """
    Closes a perpetual long trade.

    Input: A JSON string with:
    {
        "price": "float, execution price for closing the trade",
        "trade_mint": "string, token mint address for the trade"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.close_perp_trade_long(
                price=data["price"],
                trade_mint=data["trade_mint"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error closing perp long trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class OpenPerpTradeLongTool(BaseTool):
    name: str = "open_perp_trade_long"
    description: str = """
    Opens a perpetual long trade.

    Input: A JSON string with:
    {
        "price": "float, entry price for the trade",
        "collateral_amount": "float, amount of collateral",
        "collateral_mint": "string, optional, mint address of the collateral",
        "leverage": "float, optional, leverage factor",
        "trade_mint": "string, optional, token mint address",
        "slippage": "float, optional, slippage tolerance"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.open_perp_trade_long(
                price=data["price"],
                collateral_amount=data["collateral_amount"],
                collateral_mint=data.get("collateral_mint"),
                leverage=data.get("leverage"),
                trade_mint=data.get("trade_mint"),
                slippage=data.get("slippage")
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error opening perp long trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class OpenPerpTradeShortTool(BaseTool):
    name: str = "open_perp_trade_short"
    description: str = """
    Opens a perpetual short trade.

    Input: A JSON string with:
    {
        "price": "float, entry price for the trade",
        "collateral_amount": "float, amount of collateral",
        "collateral_mint": "string, optional, mint address of the collateral",
        "leverage": "float, optional, leverage factor",
        "trade_mint": "string, optional, token mint address",
        "slippage": "float, optional, slippage tolerance"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.open_perp_trade_short(
                price=data["price"],
                collateral_amount=data["collateral_amount"],
                collateral_mint=data.get("collateral_mint"),
                leverage=data.get("leverage"),
                trade_mint=data.get("trade_mint"),
                slippage=data.get("slippage")
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error opening perp short trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")
    
class Create3LandCollectionTool(BaseTool):
    name: str = "create_3land_collection"
    description: str = """
    Creates a 3Land NFT collection.

    Input: A JSON string with:
    {
        "collection_symbol": "string, symbol of the collection",
        "collection_name": "string, name of the collection",
        "collection_description": "string, description of the collection",
        "main_image_url": "string, optional, URL of the main image",
        "cover_image_url": "string, optional, URL of the cover image",
        "is_devnet": "bool, optional, whether to use devnet"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.create_3land_collection(
                collection_symbol=data["collection_symbol"],
                collection_name=data["collection_name"],
                collection_description=data["collection_description"],
                main_image_url=data.get("main_image_url"),
                cover_image_url=data.get("cover_image_url"),
                is_devnet=data.get("is_devnet", False),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error creating 3land collection: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class Create3LandNFTTool(BaseTool):
    name: str = "create_3land_nft"
    description: str = """
    Creates a 3Land NFT.

    Input: A JSON string with:
    {
        "item_name": "string, name of the NFT",
        "seller_fee": "float, seller fee percentage",
        "item_amount": "int, number of NFTs to mint",
        "item_symbol": "string, symbol of the NFT",
        "item_description": "string, description of the NFT",
        "traits": "Any, NFT traits",
        "price": "float, optional, price of the NFT",
        "main_image_url": "string, optional, URL of the main image",
        "cover_image_url": "string, optional, URL of the cover image",
        "spl_hash": "string, optional, SPL hash identifier",
        "pool_name": "string, optional, pool name",
        "is_devnet": "bool, optional, whether to use devnet",
        "with_pool": "bool, optional, whether to include a pool"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.create_3land_nft(
                item_name=data["item_name"],
                seller_fee=data["seller_fee"],
                item_amount=data["item_amount"],
                item_symbol=data["item_symbol"],
                item_description=data["item_description"],
                traits=data["traits"],
                price=data.get("price"),
                main_image_url=data.get("main_image_url"),
                cover_image_url=data.get("cover_image_url"),
                spl_hash=data.get("spl_hash"),
                pool_name=data.get("pool_name"),
                is_devnet=data.get("is_devnet", False),
                with_pool=data.get("with_pool", False),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error creating 3land NFT: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class CreateDriftUserAccountTool(BaseTool):
    name: str = "create_drift_user_account"
    description: str = """
    Creates a Drift user account with an initial deposit.

    Input: A JSON string with:
    {
        "deposit_amount": "float, amount to deposit",
        "deposit_symbol": "string, symbol of the asset to deposit"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.create_drift_user_account(
                deposit_amount=data["deposit_amount"],
                deposit_symbol=data["deposit_symbol"],
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error creating Drift user account: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DepositToDriftUserAccountTool(BaseTool):
    name: str = "deposit_to_drift_user_account"
    description: str = """
    Deposits funds into a Drift user account.

    Input: A JSON string with:
    {
        "amount": "float, amount to deposit",
        "symbol": "string, symbol of the asset",
        "is_repayment": "bool, optional, whether the deposit is a loan repayment"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.deposit_to_drift_user_account(
                amount=data["amount"],
                symbol=data["symbol"],
                is_repayment=data.get("is_repayment"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error depositing to Drift user account: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")
    
class WithdrawFromDriftUserAccountTool(BaseTool):
    name: str = "withdraw_from_drift_user_account"
    description: str = """
    Withdraws funds from a Drift user account.

    Input: A JSON string with:
    {
        "amount": "float, amount to withdraw",
        "symbol": "string, symbol of the asset",
        "is_borrow": "bool, optional, whether the withdrawal is a borrow request"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.withdraw_from_drift_user_account(
                amount=data["amount"],
                symbol=data["symbol"],
                is_borrow=data.get("is_borrow"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error withdrawing from Drift user account: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class TradeUsingDriftPerpAccountTool(BaseTool):
    name: str = "trade_using_drift_perp_account"
    description: str = """
    Executes a trade using a Drift perpetual account.

    Input: A JSON string with:
    {
        "amount": "float, trade amount",
        "symbol": "string, market symbol",
        "action": "string, 'long' or 'short'",
        "trade_type": "string, 'market' or 'limit'",
        "price": "float, optional, trade execution price"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.trade_using_drift_perp_account(
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
                trade_type=data["trade_type"],
                price=data.get("price"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error trading using Drift perp account: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class CheckIfDriftAccountExistsTool(BaseTool):
    name: str = "check_if_drift_account_exists"
    description: str = """
    Checks if a Drift user account exists.

    Input: None.
    Output:
    {
        "exists": "bool, whether the Drift user account exists",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            exists = await self.solana_kit.check_if_drift_account_exists()
            return {
                "exists": exists,
                "message": "Success"
            }
        except Exception as e:
            return {
                "exists": None,
                "message": f"Error checking Drift account existence: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DriftUserAccountInfoTool(BaseTool):
    name: str = "drift_user_account_info"
    description: str = """
    Retrieves Drift user account information.

    Input: None.
    Output:
    {
        "account_info": "dict, account details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            account_info = await self.solana_kit.drift_user_account_info()
            return {
                "account_info": account_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "account_info": None,
                "message": f"Error fetching Drift user account info: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetAvailableDriftMarketsTool(BaseTool):
    name: str = "get_available_drift_markets"
    description: str = """
    Retrieves available markets on Drift.

    Input: None.
    Output:
    {
        "markets": "dict, list of available Drift markets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            markets = await self.solana_kit.get_available_drift_markets()
            return {
                "markets": markets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "markets": None,
                "message": f"Error fetching available Drift markets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class StakeToDriftInsuranceFundTool(BaseTool):
    name: str = "stake_to_drift_insurance_fund"
    description: str = """
    Stakes funds into the Drift insurance fund.

    Input: A JSON string with:
    {
        "amount": "float, amount to stake",
        "symbol": "string, token symbol"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.stake_to_drift_insurance_fund(
                amount=data["amount"],
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error staking to Drift insurance fund: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class RequestUnstakeFromDriftInsuranceFundTool(BaseTool):
    name: str = "request_unstake_from_drift_insurance_fund"
    description: str = """
    Requests unstaking from the Drift insurance fund.

    Input: A JSON string with:
    {
        "amount": "float, amount to unstake",
        "symbol": "string, token symbol"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.request_unstake_from_drift_insurance_fund(
                amount=data["amount"],
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error requesting unstake from Drift insurance fund: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class UnstakeFromDriftInsuranceFundTool(BaseTool):
    name: str = "unstake_from_drift_insurance_fund"
    description: str = """
    Completes an unstaking request from the Drift insurance fund.

    Input: A JSON string with:
    {
        "symbol": "string, token symbol"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.unstake_from_drift_insurance_fund(
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error unstaking from Drift insurance fund: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DriftSwapSpotTokenTool(BaseTool):
    name: str = "drift_swap_spot_token"
    description: str = """
    Swaps spot tokens on Drift.

    Input: A JSON string with:
    {
        "from_symbol": "string, token to swap from",
        "to_symbol": "string, token to swap to",
        "slippage": "float, optional, allowed slippage",
        "to_amount": "float, optional, desired amount of the output token",
        "from_amount": "float, optional, amount of the input token"
    }
    Output:
    {
        "transaction": "dict, swap transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.drift_swap_spot_token(
                from_symbol=data["from_symbol"],
                to_symbol=data["to_symbol"],
                slippage=data.get("slippage"),
                to_amount=data.get("to_amount"),
                from_amount=data.get("from_amount"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error swapping spot token on Drift: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftPerpMarketFundingRateTool(BaseTool):
    name: str = "get_drift_perp_market_funding_rate"
    description: str = """
    Retrieves the funding rate for a Drift perpetual market.

    Input: A JSON string with:
    {
        "symbol": "string, market symbol (must end in '-PERP')",
        "period": "string, optional, funding rate period, either 'year' or 'hour' (default: 'year')"
    }
    Output:
    {
        "funding_rate": "dict, funding rate details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            funding_rate = await self.solana_kit.get_drift_perp_market_funding_rate(
                symbol=data["symbol"],
                period=data.get("period", "year"),
            )
            return {
                "funding_rate": funding_rate,
                "message": "Success"
            }
        except Exception as e:
            return {
                "funding_rate": None,
                "message": f"Error getting Drift perp market funding rate: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftEntryQuoteOfPerpTradeTool(BaseTool):
    name: str = "get_drift_entry_quote_of_perp_trade"
    description: str = """
    Retrieves the entry quote for a perpetual trade on Drift.

    Input: A JSON string with:
    {
        "amount": "float, trade amount",
        "symbol": "string, market symbol (must end in '-PERP')",
        "action": "string, 'long' or 'short'"
    }
    Output:
    {
        "entry_quote": "dict, entry quote details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            entry_quote = await self.solana_kit.get_drift_entry_quote_of_perp_trade(
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
            )
            return {
                "entry_quote": entry_quote,
                "message": "Success"
            }
        except Exception as e:
            return {
                "entry_quote": None,
                "message": f"Error getting Drift entry quote of perp trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftLendBorrowApyTool(BaseTool):
    name: str = "get_drift_lend_borrow_apy"
    description: str = """
    Retrieves the lending and borrowing APY for a given symbol on Drift.

    Input: A JSON string with:
    {
        "symbol": "string, token symbol"
    }
    Output:
    {
        "apy_data": "dict, lending and borrowing APY details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            apy_data = await self.solana_kit.get_drift_lend_borrow_apy(
                symbol=data["symbol"]
            )
            return {
                "apy_data": apy_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "apy_data": None,
                "message": f"Error getting Drift lend/borrow APY: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class CreateDriftVaultTool(BaseTool):
    name: str = "create_drift_vault"
    description: str = """
    Creates a Drift vault.

    Input: A JSON string with:
    {
        "name": "string, vault name",
        "market_name": "string, market name format '<name>-<name>'",
        "redeem_period": "int, redeem period in blocks",
        "max_tokens": "int, maximum number of tokens",
        "min_deposit_amount": "float, minimum deposit amount",
        "management_fee": "float, management fee percentage",
        "profit_share": "float, profit share percentage",
        "hurdle_rate": "float, optional, hurdle rate",
        "permissioned": "bool, optional, whether the vault is permissioned"
    }
    Output:
    {
        "vault_details": "dict, vault creation details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            vault_details = await self.solana_kit.create_drift_vault(
                name=data["name"],
                market_name=data["market_name"],
                redeem_period=data["redeem_period"],
                max_tokens=data["max_tokens"],
                min_deposit_amount=data["min_deposit_amount"],
                management_fee=data["management_fee"],
                profit_share=data["profit_share"],
                hurdle_rate=data.get("hurdle_rate"),
                permissioned=data.get("permissioned"),
            )
            return {
                "vault_details": vault_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_details": None,
                "message": f"Error creating Drift vault: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class UpdateDriftVaultDelegateTool(BaseTool):
    name: str = "update_drift_vault_delegate"
    description: str = """
    Updates the delegate address for a Drift vault.

    Input: A JSON string with:
    {
        "vault": "string, vault address",
        "delegate_address": "string, new delegate address"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.update_drift_vault_delegate(
                vault=data["vault"],
                delegate_address=data["delegate_address"],
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error updating Drift vault delegate: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class UpdateDriftVaultTool(BaseTool):
    name: str = "update_drift_vault"
    description: str = """
    Updates an existing Drift vault.

    Input: A JSON string with:
    {
        "vault_address": "string, address of the vault",
        "name": "string, vault name",
        "market_name": "string, market name format '<name>-<name>'",
        "redeem_period": "int, redeem period in blocks",
        "max_tokens": "int, maximum number of tokens",
        "min_deposit_amount": "float, minimum deposit amount",
        "management_fee": "float, management fee percentage",
        "profit_share": "float, profit share percentage",
        "hurdle_rate": "float, optional, hurdle rate",
        "permissioned": "bool, optional, whether the vault is permissioned"
    }
    Output:
    {
        "vault_update": "dict, vault update details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            vault_update = await self.solana_kit.update_drift_vault(
                vault_address=data["vault_address"],
                name=data["name"],
                market_name=data["market_name"],
                redeem_period=data["redeem_period"],
                max_tokens=data["max_tokens"],
                min_deposit_amount=data["min_deposit_amount"],
                management_fee=data["management_fee"],
                profit_share=data["profit_share"],
                hurdle_rate=data.get("hurdle_rate"),
                permissioned=data.get("permissioned"),
            )
            return {
                "vault_update": vault_update,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_update": None,
                "message": f"Error updating Drift vault: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftVaultInfoTool(BaseTool):
    name: str = "get_drift_vault_info"
    description: str = """
    Retrieves information about a specific Drift vault.

    Input: A JSON string with:
    {
        "vault_name": "string, name of the vault"
    }
    Output:
    {
        "vault_info": "dict, vault details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            vault_info = await self.solana_kit.get_drift_vault_info(
                vault_name=data["vault_name"]
            )
            return {
                "vault_info": vault_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_info": None,
                "message": f"Error retrieving Drift vault info: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")
    
class DepositIntoDriftVaultTool(BaseTool):
    name: str = "deposit_into_drift_vault"
    description: str = """
    Deposits funds into a Drift vault.

    Input: A JSON string with:
    {
        "amount": "float, amount to deposit",
        "vault": "string, vault address"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.deposit_into_drift_vault(
                amount=data["amount"],
                vault=data["vault"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error depositing into Drift vault: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class RequestWithdrawalFromDriftVaultTool(BaseTool):
    name: str = "request_withdrawal_from_drift_vault"
    description: str = """
    Requests a withdrawal from a Drift vault.

    Input: A JSON string with:
    {
        "amount": "float, amount to withdraw",
        "vault": "string, vault address"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.request_withdrawal_from_drift_vault(
                amount=data["amount"],
                vault=data["vault"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error requesting withdrawal from Drift vault: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class WithdrawFromDriftVaultTool(BaseTool):
    name: str = "withdraw_from_drift_vault"
    description: str = """
    Withdraws funds from a Drift vault after a withdrawal request.

    Input: A JSON string with:
    {
        "vault": "string, vault address"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.withdraw_from_drift_vault(
                vault=data["vault"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error withdrawing from Drift vault: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DeriveDriftVaultAddressTool(BaseTool):
    name: str = "derive_drift_vault_address"
    description: str = """
    Derives the Drift vault address from a given name.

    Input: A JSON string with:
    {
        "name": "string, vault name"
    }
    Output:
    {
        "vault_address": "string, derived vault address",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            vault_address = await self.solana_kit.derive_drift_vault_address(
                name=data["name"]
            )
            return {
                "vault_address": vault_address,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_address": None,
                "message": f"Error deriving Drift vault address: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class TradeUsingDelegatedDriftVaultTool(BaseTool):
    name: str = "trade_using_delegated_drift_vault"
    description: str = """
    Executes a trade using a delegated Drift vault.

    Input: A JSON string with:
    {
        "vault": "string, vault address",
        "amount": "float, trade amount",
        "symbol": "string, market symbol",
        "action": "string, either 'long' or 'short'",
        "trade_type": "string, either 'market' or 'limit'",
        "price": "float, optional, trade execution price"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.trade_using_delegated_drift_vault(
                vault=data["vault"],
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
                trade_type=data["trade_type"],
                price=data.get("price")
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error trading using delegated Drift vault: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")
    
class FlashOpenTradeTool(BaseTool):
    name: str = "flash_open_trade"
    description: str = """
    Opens a flash trade using the Solana Agent toolkit API.

    Input: A JSON string with:
    {
        "token": "string, the trading token",
        "side": "string, either 'buy' or 'sell'",
        "collateralUsd": "float, collateral amount in USD",
        "leverage": "float, leverage multiplier"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.flash_open_trade(
                token=data["token"],
                side=data["side"],
                collateral_usd=data["collateralUsd"],
                leverage=data["leverage"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error opening flash trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class FlashCloseTradeTool(BaseTool):
    name: str = "flash_close_trade"
    description: str = """
    Closes a flash trade using the Solana Agent toolkit API.

    Input: A JSON string with:
    {
        "token": "string, the trading token",
        "side": "string, either 'buy' or 'sell'"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction = await self.solana_kit.flash_close_trade(
                token=data["token"],
                side=data["side"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error closing flash trade: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class ResolveAllDomainsTool(BaseTool):
    name: str = "resolve_all_domains"
    description: str = """
    Resolves all domain types associated with a given domain name.

    Input: A JSON string with:
    {
        "domain": "string, the domain name to resolve"
    }
    Output:
    {
        "tld": "string, the resolved domain's TLD",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            domain_tld = await self.solana_kit.resolve_all_domains(data["domain"])
            return {"tld": domain_tld, "message": "Success"} if domain_tld else {"message": "Domain resolution failed"}
        except Exception as e:
            return {"message": f"Error resolving domain: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class GetOwnedDomainsForTLDTool(BaseTool):
    name: str = "get_owned_domains_for_tld"
    description: str = """
    Retrieves the domains owned by the user for a given TLD.

    Input: A JSON string with:
    {
        "tld": "string, the top-level domain (TLD)"
    }
    Output:
    {
        "domains": "list of strings, owned domains under the TLD",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            owned_domains = await self.solana_kit.get_owned_domains_for_tld(data["tld"])
            return {"domains": owned_domains, "message": "Success"} if owned_domains else {"message": "No owned domains found"}
        except Exception as e:
            return {"message": f"Error fetching owned domains: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class GetAllDomainsTLDsTool(BaseTool):
    name: str = "get_all_domains_tlds"
    description: str = """
    Retrieves all available top-level domains (TLDs).

    Input: No input required.
    Output:
    {
        "tlds": "list of strings, available TLDs",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            tlds = await self.solana_kit.get_all_domains_tlds()
            return {"tlds": tlds, "message": "Success"} if tlds else {"message": "No TLDs found"}
        except Exception as e:
            return {"message": f"Error fetching TLDs: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class GetOwnedAllDomainsTool(BaseTool):
    name: str = "get_owned_all_domains"
    description: str = """
    Retrieves all domains owned by a given user.

    Input: A JSON string with:
    {
        "owner": "string, the owner's public key"
    }
    Output:
    {
        "domains": "list of strings, owned domains",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            owned_domains = await self.solana_kit.get_owned_all_domains(data["owner"])
            return {"domains": owned_domains, "message": "Success"} if owned_domains else {"message": "No owned domains found"}
        except Exception as e:
            return {"message": f"Error fetching owned domains: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
    
def create_solana_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaBalanceTool(solana_kit=solana_kit),
        SolanaTransferTool(solana_kit=solana_kit),
        SolanaDeployTokenTool(solana_kit=solana_kit),
        SolanaTradeTool(solana_kit=solana_kit),
        SolanaFaucetTool(solana_kit=solana_kit),
        SolanaStakeTool(solana_kit=solana_kit),
        SolanaPumpFunTokenTool(solana_kit=solana_kit),
        SolanaCreateImageTool(solana_kit=solana_kit),
        SolanaGetWalletAddressTool(solana_kit=solana_kit),
        SolanaTPSCalculatorTool(solana_kit=solana_kit),
        SolanaFetchPriceTool(solana_kit=solana_kit),
        SolanaTokenDataTool(solana_kit=solana_kit),
        SolanaTokenDataByTickerTool(solana_kit=solana_kit),
        SolanaMeteoraDLMMTool(solana_kit=solana_kit),
        SolanaRaydiumBuyTool(solana_kit=solana_kit),
        SolanaRaydiumSellTool(solana_kit=solana_kit),
        SolanaCreateGibworkTaskTool(solana_kit=solana_kit),
        SolanaSellUsingMoonshotTool(solana_kit=solana_kit),
        SolanaBuyUsingMoonshotTool(solana_kit=solana_kit),
        SolanaPythGetPriceTool(solana_kit=solana_kit),
        SolanaHeliusGetBalancesTool(solana_kit=solana_kit),
        SolanaHeliusGetAddressNameTool(solana_kit=solana_kit),
        SolanaHeliusGetNftEventsTool(solana_kit=solana_kit),
        SolanaHeliusGetMintlistsTool(solana_kit=solana_kit),
        SolanaHeliusGetNFTFingerprintTool(solana_kit=solana_kit),
        SolanaHeliusGetActiveListingsTool(solana_kit=solana_kit),
        SolanaHeliusGetNFTMetadataTool(solana_kit=solana_kit),
        SolanaHeliusGetRawTransactionsTool(solana_kit=solana_kit),
        SolanaHeliusGetParsedTransactionsTool(solana_kit=solana_kit),
        SolanaHeliusGetParsedTransactionHistoryTool(solana_kit=solana_kit),
        SolanaHeliusCreateWebhookTool(solana_kit=solana_kit),
        SolanaHeliusGetAllWebhooksTool(solana_kit=solana_kit),
        SolanaHeliusGetWebhookTool(solana_kit=solana_kit),
        SolanaHeliusEditWebhookTool(solana_kit=solana_kit),
        SolanaHeliusDeleteWebhookTool(solana_kit=solana_kit),
        SolanaFetchTokenReportSummaryTool(solana_kit=solana_kit),
        SolanaFetchTokenDetailedReportTool(solana_kit=solana_kit),
        SolanaGetPumpCurveStateTool(solana_kit=solana_kit),
        SolanaCalculatePumpCurvePriceTool(solana_kit=solana_kit),
        SolanaBuyTokenTool(solana_kit=solana_kit),
        SolanaSellTokenTool(solana_kit=solana_kit),
        SolanaSNSGetAllDomainsTool(solana_kit=solana_kit),
        SolanaSNSRegisterDomainTool(solana_kit=solana_kit),
        SolanaSNSGetFavouriteDomainTool(solana_kit=solana_kit),
        SolanaSNSResolveTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetsByAuthorityTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetsByCreatorTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetTool(solana_kit=solana_kit),
        SolanaMintMetaplexCoreNFTTool(solana_kit=solana_kit),
        SolanaDeployCollectionTool(solana_kit=solana_kit),
        SolanaDeBridgeCreateTransactionTool(solana_kit=solana_kit),
        SolanaDeBridgeCheckTransactionStatusTool(solana_kit=solana_kit),
        SolanaDeBridgeExecuteTransactionTool(solana_kit=solana_kit),
        SolanaCybersCreateCoinTool(solana_kit=solana_kit),
        SolanaGetTipAccounts(solana_kit=solana_kit),
        SolanaGetRandomTipAccount(solana_kit=solana_kit),
        SolanaGetBundleStatuses(solana_kit=solana_kit),
        SolanaSendBundle(solana_kit=solana_kit),
        SolanaGetInflightBundleStatuses(solana_kit=solana_kit),
        SolanaSendTxn(solana_kit=solana_kit),
        BackpackCancelOpenOrdersTool(solana_kit=solana_kit),
        BackpackCancelOpenOrderTool(solana_kit=solana_kit),
        BackpackGetBorrowLendPositionsTool(solana_kit=solana_kit),
        BackpackGetBorrowPositionHistoryTool(solana_kit=solana_kit),
        BackpackGetDepthTool(solana_kit=solana_kit),
        BackpackGetFundingIntervalRatesTool(solana_kit=solana_kit),
        BackpackGetFundingPaymentsTool(solana_kit=solana_kit),
        BackpackGetHistoricalTradesTool(solana_kit=solana_kit),
        BackpackGetKlinesTool(solana_kit=solana_kit),
        BackpackGetMarkPriceTool(solana_kit=solana_kit),
        BackpackGetMarketsTool(solana_kit=solana_kit),
        BackpackGetOpenInterestTool(solana_kit=solana_kit),
        BackpackGetOpenOrdersTool(solana_kit=solana_kit),
        BackpackGetOrderHistoryTool(solana_kit=solana_kit),
        BackpackGetPnlHistoryTool(solana_kit=solana_kit),
        BackpackGetRecentTradesTool(solana_kit=solana_kit),
        BackpackGetSettlementHistoryTool(solana_kit=solana_kit),
        BackpackGetStatusTool(solana_kit=solana_kit),
        BackpackGetSupportedAssetsTool(solana_kit=solana_kit),
        BackpackGetSystemTimeTool(solana_kit=solana_kit),
        BackpackGetTickerInformationTool(solana_kit=solana_kit),
        BackpackGetTickersTool(solana_kit=solana_kit),
        BackpackGetUsersOpenOrdersTool(solana_kit=solana_kit),
        BackpackSendPingTool(solana_kit=solana_kit),
        BackpackExecuteBorrowLendTool(solana_kit=solana_kit),
        BackpackExecuteOrderTool(solana_kit=solana_kit),
        BackpackGetFillHistoryTool(solana_kit=solana_kit),
        BackpackGetAccountBalancesTool(solana_kit=solana_kit),
        BackpackRequestWithdrawalTool(solana_kit=solana_kit),
        BackpackGetAccountSettingsTool(solana_kit=solana_kit),
        BackpackUpdateAccountSettingsTool(solana_kit=solana_kit),
        BackpackGetCollateralInfoTool(solana_kit=solana_kit),
        BackpackGetAccountDepositsTool(solana_kit=solana_kit),
        BackpackGetOpenPositionsTool(solana_kit=solana_kit),
        BackpackGetBorrowHistoryTool(solana_kit=solana_kit),
        BackpackGetInterestHistoryTool(solana_kit=solana_kit),
        BackpackGetMarketTool(solana_kit=solana_kit),
        ClosePerpTradeLongTool(solana_kit=solana_kit),
        ClosePerpTradeShortTool(solana_kit=solana_kit),
        OpenPerpTradeLongTool(solana_kit=solana_kit),
        OpenPerpTradeShortTool(solana_kit=solana_kit),
        Create3LandCollectionTool(solana_kit=solana_kit),
        Create3LandNFTTool(solana_kit=solana_kit),
        CreateDriftUserAccountTool(solana_kit=solana_kit),
        DepositToDriftUserAccountTool(solana_kit=solana_kit),
        WithdrawFromDriftUserAccountTool(solana_kit=solana_kit),
        TradeUsingDriftPerpAccountTool(solana_kit=solana_kit),
        CheckIfDriftAccountExistsTool(solana_kit=solana_kit),
        DriftUserAccountInfoTool(solana_kit=solana_kit),
        GetAvailableDriftMarketsTool(solana_kit=solana_kit),
        StakeToDriftInsuranceFundTool(solana_kit=solana_kit),
        RequestUnstakeFromDriftInsuranceFundTool(solana_kit=solana_kit),
        UnstakeFromDriftInsuranceFundTool(solana_kit=solana_kit),
        DriftSwapSpotTokenTool(solana_kit=solana_kit),
        GetDriftPerpMarketFundingRateTool(solana_kit=solana_kit),
        GetDriftEntryQuoteOfPerpTradeTool(solana_kit=solana_kit),
        GetDriftLendBorrowApyTool(solana_kit=solana_kit),
        CreateDriftVaultTool(solana_kit=solana_kit),
        UpdateDriftVaultDelegateTool(solana_kit=solana_kit),
        UpdateDriftVaultTool(solana_kit=solana_kit),
        GetDriftVaultInfoTool(solana_kit=solana_kit),
        DepositIntoDriftVaultTool(solana_kit=solana_kit),
        RequestWithdrawalFromDriftVaultTool(solana_kit=solana_kit),
        WithdrawFromDriftVaultTool(solana_kit=solana_kit),
        DeriveDriftVaultAddressTool(solana_kit=solana_kit),
        TradeUsingDelegatedDriftVaultTool(solana_kit=solana_kit),
        FlashCloseTradeTool(solana_kit=solana_kit),
        FlashOpenTradeTool(solana_kit=solana_kit),
        ResolveAllDomainsTool(solana_kit=solana_kit),
        GetOwnedDomainsForTLDTool(solana_kit=solana_kit),
        GetAllDomainsTLDsTool(solana_kit=solana_kit),
        GetOwnedAllDomainsTool(solana_kit=solana_kit),
    ]

