# DeFi Deposit Research

## Topics
**SAC-DAPP-2025** How long is the average DeFi deposit? Our [work](https://ieeexplore.ieee.org/document/10646464) in DAPPS 2024 suggested that mandating a minimum deposit time for DeFi protocols will prevent flashloan hacks. Readers asked if this would have a negative impact for user experience. This work, accepted to [SAC DAPP](https://www.cas-blockchain-certification.com/en/acm-sac-dapp-track) 2025 as a poster, takes a first step towards answering this. We show that most users deposit assets for several blocks, at least in some cases. A more involved study is coming to overcome the limitations of this poster -- stay tuned!

## Setup and Tips
One-time setup might look like this (some libraries may no longer be needed):

```
sudo apt install python3.12-venv
python3 -m venv my-venv
my-venv/bin/pip3 install web3
my-venv/bin/pip3 install matplotlib
my-venv/bin/pip3 install numpy
my-venv/bin/pip3 install python-dotenv
my-venv/bin/pip3 install argparse
my-venv/bin/pip3 install pandas
```

Prior to running code (`python3 main.py`) in the correct directory, copy a `.env` file over from somewhere appropriate, then
```
source my-venv/bin/activate
```
