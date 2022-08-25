from brownie import Storage,accounts,config

def read():
    print(Storage[-1])
    str=Storage[-1]
    print(str.retrieve())

def main():
    read()