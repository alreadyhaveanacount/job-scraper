## Basic imports

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union

## Setting up constants

user_headers = { # To mimic a real browser
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
}

work_regimes = {"Remote", "Hybrid", "On-site"}
contract_types = {"Part-time", "Full-time", "Contract"}

WEEKS_PER_YEAR = 52

## Helper function
def extract_text(tag, default_result: Union[str, None] =None) -> Union[str, None] :
    return default_result if tag is None else tag.get_text(strip=True)

def notation_to_int(notation: str) -> int:
    num = 0

    if notation.endswith("k"):
        num = int(float(notation[:-1])) * 1000
    elif notation.endswith("m"):
        num = int(float(notation[:-1])) * 1000000
    else:
        num = int(notation)

    return num

def to_hourly_salary(contract, pay_rate, average_pay):
    if pay_rate == "Hour": return average_pay

    hours_per_week = 40 if contract == "Full-time" else 20

    if pay_rate == "Month":
        return round(average_pay / (4 * hours_per_week))

    if pay_rate == "Year":
        return round(average_pay / (WEEKS_PER_YEAR * hours_per_week))

    return None

## Main function

def load_page(buffer: List[Dict], specifics: Dict[str, Union[str, List[str]]]={}) -> None:
    to_add = "?"

    for key, value in specifics.items():
        if isinstance(value, list):
            for item in value:
                to_add += f"{key}={item}&"
        else:
            to_add += f"{key}={value}&"

    try:
        response = requests.get("https://remote.com/jobs/all" + to_add, headers=user_headers)
        response.raise_for_status() # Creates an error if STATUS != 200
    except requests.RequestException as e:
        print("[ERROR] Failed to fetch data: " + e)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("article")

    for job in jobs:
        salary_range = extract_text(job.find("span", class_="sc-a6d70f3d-0 ercMyp"))

        min_salary, max_salary = [None, None] if salary_range is None else map(notation_to_int, salary_range.split(" ")[0:3:2])

        pay_rate = extract_text(job.find("span", class_="sc-a6d70f3d-0 bqpWGD"))

        job_data = {
            "Company Name": extract_text(job.find("span", class_="sc-a6d70f3d-0 cWvlWe"), "CONFIDENTIAL COMPANY"),
            "Function": extract_text(job.find("span", class_="sc-a6d70f3d-0 fsvfbz")),
            "Is Quick Apply?": "No",
            "Contract": None,
            "Minimal Salary": min_salary,
            "Maximum Salary": max_salary,
            "Average Hourly Salary": None,
            "Pay Rate": None if pay_rate is None else pay_rate[1:].capitalize(),
            "Regime": None,
            "Reference Link": "https://remote.com" + job.find("a", class_="sc-a093e03f-0 sc-a093e03f-1 krjhEa gZaGuL sc-31ccc88a-0 jZmZlq")["href"]
        }

        job_attrs = job.find("ul", class_="sc-226ef401-0 cIJpWb sc-86bf8474-0 iMxrtA")

        if job_attrs is None: job_attrs = job.find("div", class_="sc-226ef401-0 jKiWdu sc-d573d29-0 hmYLJn").find_all("li")

        for attr in job_attrs:
            text = attr.text

            if text == "Quick apply": job_data["Is Quick Apply?"] = "Yes"
            if text in work_regimes: job_data["Regime"] = text
            if text in contract_types: job_data["Contract"] = text
        
        if min_salary is not None and max_salary is not None:
            job_data["Average Hourly Salary"] = to_hourly_salary(job_data["Contract"][1:], job_data["Pay Rate"], round((min_salary + max_salary) / 2, 2))

        buffer.append(job_data)