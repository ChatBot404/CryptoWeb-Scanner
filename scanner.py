#!/usr/bin/python3

import os

import bs4 #to scrape information from webpage
import regex as re
import requests
import socket
import requests.packages
from colorama import Fore
from colorama import Style

minerRegex = re.compile(r"coinhive.min.js|wpupdates.github.io/ping|cryptonight.asm.js|coin-hive.com|"
                        r"jsecoin.com|cryptoloot.pro|" r"webassembly.stream|ppoi.org|"
                        r"xmrstudio|webmine.pro|miner.start|allfontshere.press|upgraderservices.cf|vuuwd.com")

possibleMinerfiles = re.compile('upgraderservices.cf|vuuwd.com')


def header():
    print(f'\n{Fore.GREEN}==============================================={Style.RESET_ALL}\n')


def scan2():
    try:
        requests.get('http://' + line.strip(), verify=False, timeout=5)
    except requests.exceptions.SSLError or requests.exceptions.ConnectionError or requests.exceptions.Timeout:
        pass


requests.packages.urllib3.disable_warnings()


choice = input('Do you want to scan a single site? [y/n]')
if choice == "y" or choice == "Y":
    header()
    scansite = input("Enter the site to scan\n")

    try:
        print('the site is', scansite)
        scansite2 = requests.get('https://' + scansite)

        scan= scansite2.raise_for_status()
        print(scan)

        scansite3 = bs4.BeautifulSoup(scansite2.content, "html.parser")  #iterates, by sitting atop an html parser

        text = minerRegex

        final = scansite3.find("script", text)
        #print(scansite3.prettify())

        print(final)
        header()
    except ImportError:
        print('Could not connect')

else:
    #    print('multisite scanning not yet supported')
    multiscan = input("Provide a file containing the list of sites you want scanned: ")

    assert os.path.exists(multiscan), "I did not find the file at, " + str(multiscan)
    scanfile = open(multiscan, 'r')

    header()
    for line in scanfile:
        print('Scanning:' + line)
        try:
            #print('this line is', line, line.strip())
            multiscan2 = requests.get('https://' + line.strip())
            multiscan2.raise_for_status()
            multiscan3 = bs4.BeautifulSoup(multiscan2.text, "html.parser")
            multifinal = multiscan3.find("script", string=minerRegex)
            #            C:\Users\Chahat Bhatia\Desktop\Testing.txt
            #            verify= ssl.CERT_NONE, timeout=5
            #            if len(str(multifinal) > 16):
            #                print('  ==MINER FOUND==  ')
            #                print(multifinal)
            #                header()
            #            else:
            print(Fore.RED)
            print(multifinal)
            print(Style.RESET_ALL)
            header()
        except requests.exceptions.SSLError or requests.exceptions.ConnectionError or requests.exceptions.Timeout:
            pass
            print('Connection issues')
            header()

    scanfile.close()
