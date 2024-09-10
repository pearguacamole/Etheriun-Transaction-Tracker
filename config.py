#Replace <<API Key here>> place holder with alchemy key
RPC_ENDPOINT = 'https://eth-mainnet.g.alchemy.com/v2/<<API Key here>>'
#check example below
#RPC_ENDPOINT = 'https://eth-mainnet.g.alchemy.com/v2/BRVNfqEubNMJJfypmMCsggWcwM-JefkA'
BEACON_DEPOSIT_CONTRACT = '0x8149745670881d99700078ede5903A1A7beBe262'


#replace <<Password Here>> placeholder with mongodb password
MONGO_URI = 'mongodb+srv://kushagra:<<Password Here>>@luganode.ftepf.mongodb.net/?retryWrites=true&w=majority&appName=luganode'
# See the example below here the password is wordpass
#MONGO_URI = 'mongodb+srv://kushagra:wordpass@luganode.ftepf.mongodb.net/?retryWrites=true&w=majority&appName=luganode'
MONGO_DB_NAME = 'eth_deposits'
MONGO_COLLECTION_NAME = 'deposits'

# replace the placeholders with required token and chatid
TELEGRAM_TOKEN = '<<telegram bot token>>'
TELEGRAM_CHAT_ID = '<<telegram chatid>>'
