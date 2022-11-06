"""Small webcrawler app using python to list out the jobs listed on infopark.in"""
from sys import argv as arg
import requests
from bs4 import BeautifulSoup

from colorama import Fore

import urllib3


def get_jobs(url, command):
    """This function is to store crawled job list into a file
     and also displays in the terminal"""
    urllib3.disable_warnings()
    res = requests.get(url, verify=False, timeout=1)
    soup = BeautifulSoup(res.content, features="lxml")
    heads = soup.findAll("div", attrs={"class": "company-list"})
    job_list = {}
    jobs = {}
    for head in heads:
        company_name = head.find_all("div")[1].text
        dates = head.find_all("div")[2].text
        links = head.a['href']
        job_list[head.find("a").text] = company_name, dates, links

    for key, val in job_list.items():
        if command in key.lower() or command in val[0].lower():
            company_name = val[0].capitalize()
            last_date = val[1]
            link = val[2]
            jobs[key.capitalize()] = "Company: "+company_name,"Last date : "+last_date, "Link to apply: "+link
    if jobs:
        with open("job_list.txt", "w", encoding="utf-8") as file:
            for key, val in jobs.items():
                print(Fore.CYAN+f"\n{key}: {val}\n\n")
                file.write(f"{key}: {val} \n\n")
        print(Fore.GREEN + "\nCrawling successfull!\n")
    else:
        print(
            Fore.RED
            + "\nSomething went wrong, please check the entry details carefully!!\n"
        )


def main():
    """Main function where the program starts"""
    if len(arg) > 1 and arg[1] != "":
        command = arg[1]
        get_jobs("https://infopark.in/companies/job-search", command)
    else:
        print(Fore.RED + "\nError : Please enter the job designation to crawl!!\n")


if __name__ == "__main__":
    main()
