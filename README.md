# Luganodes-Task   Ethereum Deposit Tracker

An Ethereum Deposit Tracker that logs all deposits over a contract and creates Telegram alerts. Comes with a grafana dashboard for better visualisation.

## Requirements
- python==3.12.2 
- prometheus
- grafana

## Installation

Clone the GitHub repository 

```bash
git clone https://github.com/pearguacamole/Luganodes-SDE-Task.git
```
Move into the project directory and open a terminal window inside the directory

Create a python virtual environment using venv and then activate the virtual environment

```bash
python -m venv nodes
source node/bin/activate
```
Once this is done we will be able to see '(nodes)' at the start of the command line before the username, after which we can install all the packages required for the application to work

```bash
pip install -r requirements.txt
```
Once this is done the environment is ready

## config.py

Before we can run the application we need to populate the config.py file. Once you open config file it will look something like this - 
```python
#Replace <<API Key here>> place holder with alchemy key
RPC_ENDPOINT = 'https://eth-mainnet.g.alchemy.com/v2/<<API Key here>>'
#check example below
#RPC_ENDPOINT = 'https://eth-mainnet.g.alchemy.com/v2/BRVNfqEubNMJJfypmMCsggWcwM-JefkA'
BEACON_DEPOSIT_CONTRACT = '0x8149745670881d99700078ede5903A1A7beBe262'


#replace <<Password Here>> placeholder with mongodb password
MONGO_URI = 'mongodb+srv://kushagra:<<Password Here>>@luganode.ftepf.mongodb.net/?'
# See the example below here the password is wordpass
#MONGO_URI = 'mongodb+srv://kushagra:wordpass@luganode.ftepf.'
MONGO_DB_NAME = 'eth_deposits'
MONGO_COLLECTION_NAME = 'deposits'

# replace the placeholders with required token and chatid
TELEGRAM_TOKEN = '<<telegram bot token>>'
TELEGRAM_CHAT_ID = '<<telegram chatid>>'
```
We now need to correctly populate all of these values - 
#### RPC_ENDPOINT
You will need to create an alchemy key. This can be done by following this [tutorial](https://www.alchemy.com/support/how-to-create-a-new-alchemy-api-key). Just keep in mind you need to key for Ethereum Mainnet do don't disable it during configuration. Once you have the key you can replace the <<API Key here>> placeholder with your api key. Follow the example given in the file.

#### BEACON_DEPOSIT_CONTRACT
This is the contract over which the transaction will be monitored is our case it will be "0x00000000219ab540356cBB839Cbe05303d7705Fa".

#### MONGO_URI
You need to create an account on [mongo cloud](https://cloud.mongodb.com/), you can follow these [steps](https://scribehow.com/shared/Creating_and_Managing_a_New_MongoDB_Atlas_Project__9AIzqzr8T6-8ch8zvmrXoQ). Once you have the uri replace the placeholder in it with your selected username and password. And then replace the example uri with the correct one.

#### TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
 You will need to generate these two using @BotFather the instruction to generate these can be found in this [gist](https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a0). Once generated replace the placeholders and save the file.


## Prometheus
You will need Prometheus to get data from python and send it to Grafana. It can be downloaded form [here](https://prometheus.io/download/). Once downloaded unzip the file, and replace the contents of prometheus.yml inside the directory with the prometheus.yml in the repository.
```bash
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
      
  - job_name: 'eth_deposit_tracker'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:8000'] 
```
You can copy past form here too, just put it inside the prometheus.yml that was downloaded with prometheus. Finally open the terminal in the extracted directory and use the following command to run it.
```bash
./prometheus --config.file=prometheus.yml
```
Leave it running

## Grafana
For Macos, run 
```bash
brew install grafana
```
after installation run 
```bash
brew services start grafana
```

For other operating systems you can follow the [documentation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/).

Once the installation is complete and service has started in the background you can access it at 
```bash
localhost:3000
```
For first time login both user_id and password is 'admin'.

## Running the application
Once the above setup is complete you can start the application. To do that
- cd into the directory where you git cloned the project.
- Initialise the virtual environment If you haven't already
```bash
source node/bin/activate
```
- Run main.py using the command
```bash
python main.py
```
- Now you should be able to see the logs the first three should appear like 
```txt
2024-09-10 22:37:51,985 [INFO] Connected to Ethereum node
2024-09-10 22:37:52,120 [INFO] Prometheus metrics available at http://localhost:8000
2024-09-10 22:37:52,437 [INFO] Started monitoring deposits on Beacon Deposit Contract
```
- Once you see this it means that the application has started successfully
- Once there is a deposit logs about it will appear along with alerts over telegram.
#### Grafana
Once the application is up and running you can monitor it using grafana.
- In your web browser open 'localhost:3000:
- Login in using user name and password, default is 'admin' for both
- Once grafana is open, go into dashboard section and select import dashboard
- You'll be prompted to choose a Json file
- Select the "luganodes dash-1725984554946.json" file from the project directory.
- Follow the prompts and choose Prometheus as data handler
- You will now be able to see the dashboard with live tracking of errors encountered by the application and total deposits logged.