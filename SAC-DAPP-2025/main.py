from web3 import Web3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

start_time = datetime.now()
load_dotenv()


### CONFIG FOR DEBUGGING
showPlots = False
verbose = True

### CONFIG FOR PROTOCOLS
test = False # toggles compound test data; overwrites block range.
yearnv3dai = False
yearnv3usdt = False
yearnv3usdc = False
yearnv2dai = True
yearnv2weth = True
curve = True 
sturdy = True
sturdy2a = False # Same hack as Sturdy, but different contract
sturdy2b = False # Same hack as Sturdy, but different contract


## hints to self
# print(tx['input'].hex()) #jgorzny: use this to print the hex value without decoding. 

# Helper functions
def checkDepTx(tx, i):
    if i in curve_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(curve_deposit_function_selectors[0]) or 
             tx['input'].hex().startswith(curve_deposit_function_selectors[1]))):
            if verbose:
                print("Found a d tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in sturdy_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(sturdy_deposit_function_selectors[0]) or 
             tx['input'].hex().startswith(sturdy_deposit_function_selectors[1]))):
            if verbose:
                print("Found a d tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in sturdy_indexes2:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(sturdy_deposit_function_selectors2[0]) or 
             tx['input'].hex().startswith(sturdy_deposit_function_selectors2[1]))):
            if verbose:
                print("Found a d tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in yearn2_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(yearn2_deposit_function_selectors[0]) or 
             tx['input'].hex().startswith(yearn2_deposit_function_selectors[1]) or 
             tx['input'].hex().startswith(yearn2_deposit_function_selectors[2]))):
            if verbose:
                print("Found a d tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    else:
        if tx['to'] == smart_contract_addresses[i] and tx['input'].hex().startswith(deposit_function_selectors[i]):
            if verbose:
                print("Found a d tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    return False

def checkWitTx(tx, i):
    if i in yearn_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(yearn_withdrawal_function_selectors[0]) or 
             tx['input'].hex().startswith(yearn_withdrawal_function_selectors[1]) or
             tx['input'].hex().startswith(yearn_withdrawal_function_selectors[2]) or 
             tx['input'].hex().startswith(yearn_withdrawal_function_selectors[3]) or
             tx['input'].hex().startswith(yearn_withdrawal_function_selectors[4]) or 
             tx['input'].hex().startswith(yearn_withdrawal_function_selectors[5]))):
            if verbose:
                print("Found a w tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in curve_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(curve_withdrawal_function_selectors[0]) or 
             tx['input'].hex().startswith(curve_withdrawal_function_selectors[1]) or
             tx['input'].hex().startswith(curve_withdrawal_function_selectors[2]) or 
             tx['input'].hex().startswith(curve_withdrawal_function_selectors[3]))):
            if verbose:
                print("Found a w tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in sturdy_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(sturdy_withdrawal_function_selectors[0]) or 
             tx['input'].hex().startswith(sturdy_withdrawal_function_selectors[1]))):
            if verbose:
                print("Found a w tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in sturdy_indexes2:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(sturdy_withdrawal_function_selectors2[0]) or 
             tx['input'].hex().startswith(sturdy_withdrawal_function_selectors2[1]))):
            if verbose:
                print("Found a w tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    elif i in yearn2_indexes:
        if (tx['to'] == smart_contract_addresses[i] and 
            (tx['input'].hex().startswith(yearn2_withdrawal_function_selectors[0]) or 
             tx['input'].hex().startswith(yearn2_withdrawal_function_selectors[1]) or 
             tx['input'].hex().startswith(yearn2_withdrawal_function_selectors[2]) or 
             tx['input'].hex().startswith(yearn2_withdrawal_function_selectors[3]))):
            if verbose:
                print("Found a w tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    else:
        if tx['to'] == smart_contract_addresses[i] and tx['input'].hex().startswith(withdrawal_function_selectors[i]):
            if verbose:
                print("Found a w tx:", tx['hash'].hex())
                print(" to:", tx['to'])
                print(" from:", tx['from'])
                print(" input:", tx['input'].hex())
                print(" protocol:", protocol_names[i])
            transactions[i].append(tx)
            writeTX(tx, protocol_transaction_files[i])
            return True
    return False

def writeTX(tx, filename):
    with open(filename, "a") as file:
        file.write(tx['hash'].hex()+"\n")

def countTx(tx, i):
    if tx['to'] == smart_contract_addresses[i]:
        total_tx[i] = total_tx[i] + 1

def checkTx(tx, i):
    checkDepTx(tx, i)
    checkWitTx(tx, i)
    countTx(tx, i)

def isDeposit(tx, i):
    if i in curve_indexes:
        return (tx['input'].hex().startswith(curve_deposit_function_selectors[0]) or
                tx['input'].hex().startswith(curve_deposit_function_selectors[1]))
    elif i in sturdy_indexes:
        return (tx['input'].hex().startswith(sturdy_deposit_function_selectors[0]) or
                tx['input'].hex().startswith(sturdy_deposit_function_selectors[1]))
    elif i in sturdy_indexes2:
        return (tx['input'].hex().startswith(sturdy_deposit_function_selectors2[0]) or
                tx['input'].hex().startswith(sturdy_deposit_function_selectors2[1]))
    elif i in yearn2_indexes:
        return (tx['input'].hex().startswith(yearn2_deposit_function_selectors[0]) or
                tx['input'].hex().startswith(yearn2_deposit_function_selectors[1]) or
                tx['input'].hex().startswith(yearn2_deposit_function_selectors[2]))
    else:
        return tx['input'].hex().startswith(deposit_function_selectors[i])

def addOrAppend(map, key, value):
    if key in map.keys():
        map[key].append(value)
    else:
        map[key] = [value]

def blockNum(tx):
    return tx['blockNumber']

def split_transactions(transactions, i):
    from_map = {}
    for j in range(0, len(transactions)):
        tx = transactions[j]
        addOrAppend(from_map, tx['from'], tx)
    return from_map

def append_s_value(i, s, user):
    with open(protocol_s_files[i], "a") as file:
        file.write(user + "," + str(s) +"\n")

def process_tx_list_from_user(transactions, i, user):
    s = []
    d = 0
    w = 0
    lastDep = None

    for j in range(0, len(transactions)):
        tx = transactions[j]
        if(isDeposit(tx, i)):
            #print("Is deposit!")
            d = d + 1
            lastDep = tx
        else:
            #print("Is withdrawal")
            w = w + 1
            if lastDep != None:
                s_val = blockNum(tx) - blockNum(lastDep)
                s.append(s_val)
                append_s_value(i, s_val, user)
                lastDep = None
    if not isDeposit(transactions[0], i):
        s_val_a = max(1, blockNum(transactions[0]) - start_block)
        append_s_value(i, s_val_a, user)
        s.append(s_val_a)
    if isDeposit(transactions[len(transactions)-1], i):
        s_val_b = max(end_block - blockNum(transactions[len(transactions)-1]), 1)
        append_s_value(i, s_val_b, user)
        s.append(s_val_b)
    if verbose:
        print("s:", s)
        print("d:", d)
        print("w", w)
    return (s,d,w)

def process_transactions(transactions, i):
    w_all = 0
    d_all = 0
    s_all = []

    split_tx_list = split_transactions(transactions, i)
    X_p = len(split_tx_list.keys())
    for key in split_tx_list.keys():
        (s_temp, d_temp, w_temp) = process_tx_list_from_user(split_tx_list[key], i, key)
        w_all = w_all + w_temp
        d_all = d_all + d_temp
        s_all.extend(s_temp)


    t_all = d_all + w_all
    #compute average
    sum = 0
    small_d = s_all[0]
    big_d = s_all[0]
    for k in range(0, len(s_all)):
        sum = sum + s_all[k]
        if small_d > s_all[k]:
            small_d = s_all[k]
        if big_d < s_all[k]:
            big_d = s_all[k]
    a_all = sum / len(s_all)

    s_values[i] = s_all

    d_values[i]  = d_all
    w_values[i] = w_all

    with open(final_results_file, "a") as file:
        file.write(protocol_names[i] + " RESULTS ---------  \n")
        file.write("t_p: " + str(t_all) + "\n")
        file.write("d_p: " + str(d_all) + "\n")
        file.write("w_p: " + str(w_all) + "\n")
        file.write("a_p: " + str(a_all) + "\n")
        file.write("small_d_p: " + str(small_d) + "\n")
        file.write("big_d_p: " + str(big_d) + "\n")
        file.write("X_p: " + str(X_p) + "\n")

    if verbose:
        #print("s_all:", s_all)
        print("d_all:", d_all)
        print("w_all", w_all)
        print("t_all", t_all)
        print("a_all", a_all)
        print("small_d_p", small_d)
        print("big_d_p", big_d)
        print("X_p", X_p)

    return (d_all, w_all, t_all, a_all, small_d, big_d)

print("Hello world - SAC 2025")

# Connect to Ethereum node
infura_url = os.getenv("INFURA")
print("INFURA: ", infura_url)
web3 = Web3(Web3.HTTPProvider(infura_url))
print("Infura connected...")

### Setup global constants
#yearn v3 DAI example
#start_block = 20675579
#end_block = 20675585

#yearn v3 USDT example
#start_block = 20649185
#end_block = 20649200

##real test! 33945 blocks yearnv3usdt/curve # untested
#start_block = 20615255
#end_block = 20649200

#real test 3311 blocks - yearnv2 dai/weth
#start_block = 20587641
#end_block = 20590952

#first three days of the year - Infura credit test
#start_block = 18908895
#end_block = 18926895 # 6000/day * 3 + start_block

#Infura test
#start_block = 19699336
#end_block = 19699337

#Strudy test
#start_block = 19762877
#end_block = 19762879

# Real data - first 6 months of 2023
start_block = 16308190
end_block = 17595510

#Real data - first 6 months of the year
#start_block = 18908895
#end_block = 20215112
assert(end_block >= start_block)

useEnds = True
resumeExperiment = False
if useEnds:
    block_list = list(range(start_block, end_block))
else:
    #block_list = [20587642, 20590951] # update this as appropriate; should be increasing!
    if resumeExperiment:
        block_list = [18909634, 18917076, 18920217, 18924648, 18927676, 18933514, 18936101, 18937043, 18940061, 18980899, 18980907, 18981383, 18982001, 18986171, 18991473, 18992690, 18993461, 18993868, 18996867, 19005193, 19015596, 19021749, 19022195, 19024886, 19030163, 19031215, 19038703, 19048305, 19049789, 19050645, 19051284, 19054478, 19055381, 19059169, 19062785, 19065518, 19066189, 19071962, 19074542, 19077966, 19084134, 19087665, 19087680, 19091996, 19098049, 19098063, 19100585, 19100586, 19104834, 19115338, 19120648, 19121104, 19121108, 19122597, 19125532, 19126795, 19127512, 19129256, 19130559, 19132039, 19134802, 19150561, 19158012, 19163328, 19164569, 19169386, 19173921, 19201486, 19207694, 19211599, 19211599, 19211871, 19217852, 19219242, 19219476, 19221066, 19223159, 19224032, 19233681, 19235962, 19239599, 19253291, 19254000, 19261340, 19269301, 19288434, 19289785, 19291959, 19291993, 19295660, 19302026, 19304460, 19311265, 19317822, 19317932, 19318301, 19320540, 19321708, 19322165, 19333462, 19335854, 19335981, 19336163, 19336917, 19341215, 19342690, 19348154, 19348296, 19348576, 19355782, 19359932, 19365432, 19369834, 19369835, 19374225, 19376316, 19377923, 19388284, 19403774, 19407395, 19408962, 19409009, 19415108, 19419151, 19423658, 19430986, 19431907, 19441093, 19441124, 19441517, 19451330, 19451532, 19451961, 19455282, 19459195, 19461632, 19463543, 19463595, 19464463, 19471200, 19476718, 19476999, 19479506, 19481520, 19485142, 19486795, 19504461, 19504781, 19505123, 19511765, 19512804, 19513234, 19514517, 19515187, 19518426, 19520146, 19523409, 19532519, 19540010, 19541897, 19546069, 19552186, 19555867, 19555878, 19562596, 19572598, 19576424, 19580929, 19581458, 19581734, 19582169, 19583612, 19585655, 19585735, 19585792, 19590231, 19592080, 19592712, 19594242, 19597713, 19599417, 19599700, 19600076, 19600301, 19605454, 19611397, 19611412, 19612776, 19613617, 19619503, 19621851, 19622571, 19627232, 19633545, 19635436, 19646256, 19648601, 19648604, 19650322, 19650847, 19657151, 19657670, 19658091, 19667853, 19670458, 19670618, 19672098, 19675565, 19675661, 19676151, 19676158, 19676735, 19679242, 19679996, 19680986, 19683766, 19684687, 19684979, 19692631, 19693509, 19695421, 19695562, 19697125]
        for i in range(19699337,20215113):
            block_list.append(i)

        print("Sorting to be safe...")
        block_list.sort()
    start_block = block_list[0]
    end_block = block_list[len(block_list)-1]   
num_blocks = len(block_list)

print("Going from block " + str(start_block) + " to " + str(end_block) + " (" + str(num_blocks) + ")")

protocol_names = []
smart_contract_addresses = []
deposit_function_selectors = [] 
withdrawal_function_selectors = []
transactions = []
s_values = []
d_values = []
w_values = []
protocol_transaction_files = []
protocol_chart_files = []
protocol_s_files = []
total_tx = []
skipped_protocols = []
final_results_file = "results/all-final00.txt"


### This is for yearn v3
yearn_indexes = []
yearn_withdrawal_function_selectors = []
# withdraw (0xb460af94) withdraw (0xa318c1a4) withdraw (0xd81a09f6)
yearn_withdrawal_function_selectors.append('b460af94')
yearn_withdrawal_function_selectors.append('a318c1a4')
yearn_withdrawal_function_selectors.append('d81a09f6')
# redeem (0xba087652) redeem (0x06580f2d) redeem (0x9f40a7b3)
yearn_withdrawal_function_selectors.append('ba087652')
yearn_withdrawal_function_selectors.append('06580f2d')
yearn_withdrawal_function_selectors.append('9f40a7b3')

### This is for yearn v2
yearn2_indexes = []
yearn2_deposit_function_selectors = []
yearn2_withdrawal_function_selectors = []
# deposit (0xd0e30db0) deposit (0xb6b55f25) deposit (0x6e553f65)
yearn2_deposit_function_selectors.append('d0e30db0')
yearn2_deposit_function_selectors.append('b6b55f25')
yearn2_deposit_function_selectors.append('6e553f65')
# withdraw (0x3ccfd60b) withdraw (0x2e1a7d4d) withdraw (0x00f714ce) withdraw (0xe63697c8)
yearn2_withdrawal_function_selectors.append('3ccfd60b')
yearn2_withdrawal_function_selectors.append('2e1a7d4d')
yearn2_withdrawal_function_selectors.append('00f714ce')
yearn2_withdrawal_function_selectors.append('e63697c8')


curve_indexes = []
curve_deposit_function_selectors = []
#add_liquidity (0x0b4c7e4d) add_liquidity (0xee22be23)
curve_deposit_function_selectors.append('0b4c7e4d')
curve_deposit_function_selectors.append('ee22be23')
curve_withdrawal_function_selectors = []
#remove_liquidity (0x5b36389c) remove_liquidity (0x269b5581) remove_liquidity_one_coin (0xf1dc3cc9) remove_liquidity_one_coin (0x8f15b6b5)
curve_withdrawal_function_selectors.append('5b36389c')
curve_withdrawal_function_selectors.append('269b5581')
curve_withdrawal_function_selectors.append('f1dc3cc9')
curve_withdrawal_function_selectors.append('8f15b6b5')

sturdy_indexes = []
sturdy_deposit_function_selectors = []
#deposit (0xe8eda9df) depositYield (0xd6996185)
sturdy_deposit_function_selectors.append('e8eda9df')
sturdy_deposit_function_selectors.append('d6996185')
sturdy_withdrawal_function_selectors = []
#withdraw (0x69328dec) withdrawFrom (0x12ade5ad)
sturdy_withdrawal_function_selectors.append('69328dec')
sturdy_withdrawal_function_selectors.append('12ade5ad')

sturdy_indexes2 = []
sturdy_deposit_function_selectors2 = []
#depositCollateral (0xa5d5db0c) depositCollateralFrom (0x259f2d01)
sturdy_deposit_function_selectors2.append('a5d5db0c')
sturdy_deposit_function_selectors2.append('259f2d01')
sturdy_withdrawal_function_selectors2 = []
#withdrawCollateral (0xa5fdfc63) withdrawOnLiquidation (0x8954ff3f)
sturdy_withdrawal_function_selectors2.append('a5fdfc63')
sturdy_withdrawal_function_selectors2.append('8954ff3f')

print("Adding protocols...")
## Add protocols

if test:
    start_block = 20698669
    end_block = 20698670
    # example: 20698669 contains a transfer: https://etherscan.io/tx/0x2b220f4fd003bfd935ddc7fc075e428f1c2ccbfdda26f707c84449d73d07ca0e to Compound

    # Compound - test only (token) -- example
    print("Adding Compound...")
    print("Index:", len(protocol_names))
    protocol_names.append('Compound')
    # contract_address = '0xc00e94cb662c3520282e6f5717214004a7f26888' ## not formatted
    smart_contract_addresses.append('0xc00e94Cb662C3520282E6f5717214004A7f26888')
    # Function selector for `transfer(address,uint256)`
    deposit_function_selectors.append('a9059cbb') #jgorzny: avoid 0x because the `.hex()` function drops that anyway, when performing the `startswith` check.
    withdrawal_function_selectors.append('qqqqqqqq') #jgorzny: fake / temp
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/compound-tx.txt")
    protocol_chart_files.append("results/compound.png")
    protocol_s_files.append("data/compound-s.txt")

    # Compound2 - test only (token) -- example
    print("Adding Compound2...")
    print("Index:", len(protocol_names))
    protocol_names.append('Compound2')
    # contract_address = '0xc00e94cb662c3520282e6f5717214004a7f26888' ## not formatted
    smart_contract_addresses.append('0xc00e94Cb662C3520282E6f5717214004A7f26888')
    # Function selector for `transfer(address,uint256)`
    deposit_function_selectors.append('qqqqqqqq') #jgorzny: avoid 0x because the `.hex()` function drops that anyway, when performing the `startswith` check.
    withdrawal_function_selectors.append('a9059cbb') #jgorzny: fake / temp
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/compound2-tx.txt")
    protocol_chart_files.append("results/compound2.png")
    protocol_s_files.append("data/compound2-s.txt")

if yearnv3dai:
    #YearnV3 - DAI	0x028eC7330ff87667b6dfb0D94b954c820195336c	deposit (0x6e553f65)	0x028eC7330ff87667b6dfb0D94b954c820195336c	withdraw (0xb460af94) withdraw (0xa318c1a4) withdraw (0xd81a09f6)	N/A	12-Mar-2024	4.29M	Ethereum
    print("Adding Yearn V3 DAI...")
    print("Index:", len(protocol_names))
    protocol_names.append('Yearn V3 DAI (0x028eC)')
    smart_contract_addresses.append('0x028eC7330ff87667b6dfb0D94b954c820195336c')
    deposit_function_selectors.append('6e553f65') 
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- yearn is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/yearn-dai-tx.txt")
    protocol_chart_files.append("results/yearn-dai.png")
    protocol_s_files.append("data/yearn-dai-s.txt")
    yearn_indexes.append(len(protocol_names)-1) # special for yearn

if yearnv3usdt:
    #YearnV3 - USDT	0x310B7Ea7475A0B449Cfd73bE81522F1B88eFAFaa	deposit (0x6e553f65)	0x310B7Ea7475A0B449Cfd73bE81522F1B88eFAFaa	withdraw (0xb460af94) withdraw (0xa318c1a4) withdraw (0xd81a09f6)	N/A	23-Jul-2024
    print("Adding Yearn V3 USDT...")
    print("Index:", len(protocol_names))
    protocol_names.append('Yearn V3 USDT (0x310B7)')
    smart_contract_addresses.append('0x310B7Ea7475A0B449Cfd73bE81522F1B88eFAFaa')
    deposit_function_selectors.append('6e553f65') 
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- yearn is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/yearn-usdt-tx.txt")
    protocol_chart_files.append("results/yearn-usdt.png")
    protocol_s_files.append("data/yearn-usdt-s.txt")
    yearn_indexes.append(len(protocol_names)-1) # special for yearn

if yearnv3usdc:
    #YearnV3 - USDC	0xBe53A109B494E5c9f97b9Cd39Fe969BE68BF6204	deposit (0x6e553f65)	0xBe53A109B494E5c9f97b9Cd39Fe969BE68BF6204	withdraw (0xb460af94) withdraw (0xa318c1a4) withdraw (0xd81a09f6) redeem (0xba087652) redeem (0x06580f2d) redeem (0x9f40a7b3)	N/A	12-Mar-2024
    print("Adding Yearn V3 USDC...")
    print("Index:", len(protocol_names))
    protocol_names.append('Yearn V3 USDC (0xBe53A)')
    smart_contract_addresses.append('0xBe53A109B494E5c9f97b9Cd39Fe969BE68BF6204')
    deposit_function_selectors.append('6e553f65') 
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- yearn is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/yearn-usdc-tx.txt")
    protocol_chart_files.append("results/yearn-usdc.png")
    protocol_s_files.append("data/yearn-usdc-s.txt")
    yearn_indexes.append(len(protocol_names)-1) # special for yearn

if yearnv2dai:
    # YearnV2 - DAI	0xdA816459F1AB5631232FE5e97a05BBBb94970c95	deposit (0xd0e30db0) deposit (0xb6b55f25) deposit (0x6e553f65)	0xdA816459F1AB5631232FE5e97a05BBBb94970c95	withdraw (0x3ccfd60b) withdraw (0x2e1a7d4d) withdraw (0x00f714ce) withdraw (0xe63697c8)		10-Jul-2021
    print("Adding Yearn V2 DAI...")
    print("Index:", len(protocol_names))
    protocol_names.append('Yearn V2 DAI (0xdA816)')
    smart_contract_addresses.append('0xdA816459F1AB5631232FE5e97a05BBBb94970c95')
    deposit_function_selectors.append('6e553f65') #jgorzny: there are others -- yearnv2 is a special case
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- yearnv2 is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/yearnv2-dai-tx.txt")
    protocol_chart_files.append("results/yearnv2-dai.png")
    protocol_s_files.append("data/yearn2-dai-s.txt")
    yearn2_indexes.append(len(protocol_names)-1) # special for yearnv2

if yearnv2weth:
    #YearnV2 - WETH	0xa258C4606Ca8206D8aA700cE2143D7db854D168c	deposit (0xd0e30db0) deposit (0xb6b55f25) deposit (0x6e553f65)	0xa258C4606Ca8206D8aA700cE2143D7db854D168c	withdraw (0x3ccfd60b) withdraw (0x2e1a7d4d) withdraw (0x00f714ce) withdraw (0xe63697c8)		7-Jun-2021
    print("Adding Yearn V2 WETH...")
    print("Index:", len(protocol_names))
    protocol_names.append('Yearn V2 WETH (0xa258C)')
    smart_contract_addresses.append('0xa258C4606Ca8206D8aA700cE2143D7db854D168c')
    deposit_function_selectors.append('6e553f65') #jgorzny: there are others -- yearnv2 is a special case
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- yearnv2 is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/yearnv2-weth-tx.txt")
    protocol_chart_files.append("results/yearnv2-weth.png")
    protocol_s_files.append("data/yearn2-weth-s.txt")
    yearn2_indexes.append(len(protocol_names)-1) # special for yearnv2

if curve:
    #Curve	0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511	add_liquidity (0x0b4c7e4d) add_liquidity (0xee22be23)	0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511	remove_liquidity (0x5b36389c) remove_liquidity (0x269b5581) remove_liquidity_one_coin (0xf1dc3cc9) remove_liquidity_one_coin (0x8f15b6b5)	30-Jul-2023	24-Nov-2021
    print("Adding Curve...")
    print("Index:", len(protocol_names))
    protocol_names.append('Curve (0x8301A)')
    smart_contract_addresses.append('0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511')
    deposit_function_selectors.append('6e553f65')  #jgorzny: there are others -- curve is a special case
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- curve is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/curve-tx.txt")
    protocol_chart_files.append("results/curve.png")
    protocol_s_files.append("data/curve-s.txt")
    curve_indexes.append(len(protocol_names)-1) # special for curve

if sturdy:
    #Sturdy	0x9f72dc67cec672bb99e3d02cbea0a21536a2b657	deposit (0xe8eda9df) depositYield (0xd6996185)	0x9f72dc67cec672bb99e3d02cbea0a21536a2b657	withdraw (0x69328dec) withdrawFrom (0x12ade5ad)
    print("Adding Sturdy...")
    print("Index:", len(protocol_names))
    protocol_names.append('Sturdy (0x9f72D)')
    smart_contract_addresses.append('0x9f72DC67ceC672bB99e3d02CbEA0a21536a2b657')
    deposit_function_selectors.append('6e553f65')  #jgorzny: there are others -- sturdy is a special case
    withdrawal_function_selectors.append('b460af94') #jgorzny: there are others -- sturdy is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/sturdy-tx.txt")
    protocol_chart_files.append("results/sturdy.png")
    protocol_s_files.append("data/sturdy-s.txt")
    sturdy_indexes.append(len(protocol_names)-1) # special for sturdy

if sturdy2a:
    #Sturdy 0xa36be47700c079bd94adc09f35b0fa93a55297bc depositCollateral (0xa5d5db0c) depositCollateralFrom (0x259f2d01)
    # withdrawCollateral (0xa5fdfc63) withdrawOnLiquidation (0x8954ff3f)
    print("Adding Sturdy 2a...")
    print("Index:", len(protocol_names))
    protocol_names.append('Sturdy (0xa36BE)')
    smart_contract_addresses.append('0xa36BE47700C079BD94adC09f35B0FA93A55297bc')
    deposit_function_selectors.append('0xa5d5db0c')  #jgorzny: there are others -- sturdy2 is a special case
    withdrawal_function_selectors.append('0xa5fdfc63') #jgorzny: there are others -- sturdy2 is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/sturdy2a-tx.txt")
    protocol_chart_files.append("results/sturdy2a.png")
    protocol_s_files.append("data/sturdy2a-s.txt")
    sturdy_indexes2.append(len(protocol_names)-1) # special for sturdy

if sturdy2b:
    #Sturdy 0x6AE5Fd07c0Bb2264B1F60b33F65920A2b912151C depositCollateral (0xa5d5db0c) depositCollateralFrom (0x259f2d01)
    # withdrawCollateral (0xa5fdfc63) withdrawOnLiquidation (0x8954ff3f)
    print("Adding Sturdy 2b...")
    print("Index:", len(protocol_names))
    protocol_names.append('Sturdy (0x6AE5F)')
    smart_contract_addresses.append('0x6AE5Fd07c0Bb2264B1F60b33F65920A2b912151C')
    deposit_function_selectors.append('0xa5d5db0c')  #jgorzny: there are others -- sturdy2 is a special case
    withdrawal_function_selectors.append('0xa5fdfc63') #jgorzny: there are others -- sturdy2 is a special case
    transactions.append([])
    s_values.append([])
    d_values.append([])
    w_values.append([])
    total_tx.append(0)
    protocol_transaction_files.append("data/sturdy2b-tx.txt")
    protocol_chart_files.append("results/sturdy2b.png")
    protocol_s_files.append("data/sturdy2b-s.txt")
    sturdy_indexes2.append(len(protocol_names)-1) # special for sturdy

print("Protocols added!")
print("protocols:", protocol_names)
if verbose:
    print("contract addresses:", smart_contract_addresses)
    print("deposit function selectors:", deposit_function_selectors)
    print("withdrawal function selectors:", withdrawal_function_selectors)
assert(len(protocol_names) == len(smart_contract_addresses))
assert(len(protocol_names) == len(deposit_function_selectors))
assert(len(protocol_names) == len(withdrawal_function_selectors))


print("Setup completed.")
print("Iterating over blocks to collect transactions...")
block_count = 0;
# Iterate over blocks and transactions
for block_number in block_list:
    print("Block: ", block_number)
    block = web3.eth.get_block(block_number, full_transactions=True)
    for tx in block['transactions']:
        #print("tx:", tx)
        for i in range(0, len(protocol_names)):
            checkTx(tx, i) 
    block_count = block_count+1
    if block_count % 500 == 0:
        print("Processed " + str(block_count) + " blocks.")
print("Transactions collected.")

# check lists
for i in range(0, len(protocol_names)):
    print("Protocol:", protocol_names[i])
    print("Good transactions:", len(transactions[i]))
    if len(transactions[i]) == 0:
        skipped_protocols.append(i)
        print("--> " + protocol_names[i] + " will be skipped for analaysis!!!")
    print("All transactions:", total_tx[i])

print("Running algorithm 1 for protocols...")
for i in range(0, len(protocol_names)):
    if i in skipped_protocols:
        continue # skips analysis
    print(protocol_names[i])
    print(len(transactions[i]))
    process_transactions(transactions[i], i)

print("Filtering bad protocols...")
valid_protocol_names = []
valid_s_values = []
valid_d_values = []
valid_w_values = []
valid_protocol_chart_files = []
valid_total_tx = []
for i in range(0, len(protocol_names)):
    if i not in skipped_protocols:
        valid_protocol_names.append(protocol_names[i])
        valid_s_values.append(s_values[i])
        valid_d_values.append(d_values[i])
        valid_w_values.append(w_values[i])
        valid_protocol_chart_files.append(protocol_chart_files[i])
        valid_total_tx.append(total_tx[i])

print("Valid protocols:", valid_protocol_names)

print("Generating graph(s)...")

xtickplacements = []
for i in range(0, len(valid_protocol_names)):
    xtickplacements.append(i+1)

#Chart all on the same one
plt.boxplot(valid_s_values)
plt.title("Withdrawal Delay for All Protocols")
plt.xlabel("Protocol")
plt.xticks(xtickplacements, valid_protocol_names, rotation=45)

# Annotate whisker values
boxplot_dict = plt.boxplot(valid_s_values)
for whisker in boxplot_dict['whiskers']:
    x = whisker.get_xdata()
    y = whisker.get_ydata()
    # Add text at the start and end of the whiskers
    plt.text(x[0], y[0], f'{y[0]:.2f}', ha='center', va='bottom')
    plt.text(x[1], y[1], f'{y[1]:.2f}', ha='center', va='top')

# Annotate means
for i, data in enumerate(valid_s_values, start=1):
    mean_value = np.mean(data)
    plt.text(i, mean_value, f'{mean_value:.2f}', ha='center', va='bottom', color='red')


plt.tight_layout()  # Automatically adjusts the layout


plt.ylabel("Delay (blocks)")
plt.savefig("results/all.png")
# Show the plot
if showPlots:
    plt.show()
plt.clf()


for i in range(0, len(valid_protocol_names)):
    plt.boxplot(valid_s_values[i])

    # Add a title and labels (optional)
    plt.title("Withdrawal Delay for " + valid_protocol_names[i])
    #plt.xlabel(valid_protocol_names[i]) #unnecessary for a single protocol
    plt.xticks([1], [valid_protocol_names[i]], rotation=45)

    plt.ylabel("Delay (blocks)")
    plt.tight_layout()  # Automatically adjusts the layout

    plt.savefig(valid_protocol_chart_files[i])

    # Show the plot
    if showPlots:
        plt.show()
    plt.clf()


### Stacked bar chart:
    
# Data
categories = valid_protocol_names
group1 = valid_d_values
group2 = valid_w_values

othertx = []
for i in range(0, len(valid_protocol_names)):
    othertx.append(valid_total_tx[i]-valid_d_values[i]-valid_w_values[i])
group3 = othertx

# Position on x-axis (bar locations)
x = np.arange(len(categories))

# Create stacked bar chart
plt.bar(x, group1, label='Deposits')
plt.bar(x, group2, bottom=group1, label='Withdrawals')  # Stack group2 on top of group1
plt.bar(x, group3, bottom=np.array(group1) + np.array(group2), label='Other Tx')  # Stack group3 on top of group1 + group2

# Adding labels and title
plt.xlabel('Protocols')
plt.ylabel('Counts')
plt.title('Transaction Breakdown')
plt.xticks(x, categories, rotation=45)  # Label x-axis with category names

# Add legend
plt.legend()
plt.tight_layout()  # Automatically adjusts the layout

if showPlots:
    # Show the plot
    plt.show()

plt.savefig("results/all-stacked.png")
plt.clf()

end_time = datetime.now()

print("Finished!")
print("Start time:", start_time)
print("End time:", end_time)