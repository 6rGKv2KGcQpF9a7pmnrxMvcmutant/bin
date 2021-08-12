import json
import re
from time import sleep
import subprocess as sp
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# TODO add some argparse magic to control where the screenshot gets made
# import argparse
# def parse_commandline():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-s",
#         "--longer",
#         dest="ex_arg",  # optional, would default to args.longer
#         help="The help text.",
#     )
#     parser.add_argument(
#         "-b",
#         "--bool_flag",
#         action="store_true",
#         dest="ex_arg2",  # optional, would default to args.bool_flag
#         help="help text",
#     )
#     return parser.parse_args()


def get_creds(id_: str):
    """Function to get login information for an account using Bitwarden CLI."""
    out: str = sp.check_output(["bw", "get", "item", id_])  # get password for PS
    json_out: dict = json.loads(out)
    user: str = json_out["login"]["username"]
    passwd: str = json_out["login"]["password"]
    return (user, passwd)


def main():
    # FIXME refactor so that the nested functions are no longer nested,
    # parameterize the driver, and then return it when they're done
    def login(user, passwd):
        ## first log in
        sleep(2)
        username_box = driver.find_element_by_id("fieldAccount")
        username_box.send_keys(user)
        sleep(1)
        password_box = driver.find_element_by_id("fieldPassword")
        password_box.send_keys(passwd)
        sleep(1)
        login_box = driver.find_element_by_id("btn-enter-sign-in")
        login_box.click()

    def get_tbls():
        ## navigate to the year schedule tab
        sched_btn = driver.find_element_by_id("btn-yearSched")
        sched_btn.click()
        ## save the tables (regex to make tables tab separated)
        tbls: list = driver.find_elements_by_xpath("//div/table")
        regex = r"(.*?\(Sp\))\s(S\d)\s(\w+-\d+)\s(.*?)\s(\w+,.*?)\s([A-Z]\d{3})\s(\d{2}/\d{2}/\d{4})\s(\d{2}/\d{2}/\d{4})"
        subst = "\\1\\t\\2\\t\\3\\t\\4\\t\\5\\t\\6\\t\\7\\t\\8"
        sem_1_tbl: str = "\n".join(
            re.sub(regex, subst, tbls[0].text, 0, re.MULTILINE).split("\n")[2:-1]
        )
        sem_2_tbl: str = "\n".join(
            re.sub(regex, subst, tbls[1].text, 0, re.MULTILINE).split("\n")[2:-1]
        )
        return (sem_1_tbl, sem_2_tbl)

    def get_sched_ss(classes: str, ss_fname):
        # FIXME fix this func so that it refreshes after entering in a set of classes
        entry_box = driver.find_element_by_xpath("//textarea[@id='powerschool-entry']")
        entry_box.send_keys(classes)
        update_btn = driver.find_element_by_xpath("//button[1]")
        update_btn.click()
        schedule = driver.find_element_by_xpath("//div[@id='areaToPrint']")
        schedule.screenshot(ss_fname)

    ps_url: str = "https://sis.imsa.edu"  # powerschool
    moe_url: str = "https://george.moe/imsa-scheduler/"
    user, passwd = get_creds("a38b8012-16a6-4371-bc9c-ad130147f398")
    options = Options()
    options.headless = True
    with Firefox(options=options) as driver:
        driver.implicitly_wait(10)
        driver.get(ps_url)
        login(user, passwd)
        classes_s1, classes_s2 = get_tbls()
        driver.get(moe_url)
        get_sched_ss(classes_s1, "semester-1-sched.png")
        get_sched_ss(classes_s2, "semester-2-sched.png")


if __name__ == "__main__":
    main()
