import argparse
import datetime as dt
import json
import subprocess as sp
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import tomli
from get_sched_ss import get_creds


def parse_commandline():
    parser = argparse.ArgumentParser(
        description="Program to automate the reporting of volunteer hours for IMSA using Selenium and TOML."
    )
    parser.add_argument(
        "-i",
        "--input_file",
        help="The TOML file to read as input containing the relevant information to be inputed in their fields. See ~/bin/mvhe/example.toml for an example.",
    )
    parser.add_argument(
        "-H",
        "--headful",
        help="Run the selenium webdriver in headful mode, opening the browser so that the user can see what's happening.",
        action="store_true",
    )
    return parser.parse_args()


def parse_toml(infile):
    with open(infile, "rb") as f:
        try:
            toml_dict: dict = tomli.load(f)
        except tomli.TOMLDecodeError:
            print(
                "The TOML in the input file appears to be invalid.\nCheck it with:\n\thttps://www.toml-lint.com/"
            )
            exit()
    return toml_dict


def input_date(driver, date):
    """Function to input the date into the helperhelper website.
    `driver` should be a selenium webdriver object
    `date` should be a datetime object."""
    url = "https://app.helperhelper.com/commitments/add-past/" + str(date)
    driver.get(url)
    return driver


def find_input_box_send_text(
    driver, xpath, to_send, clear_first=False, clear_manually=False, do_submit=False
):
    """Function to send text to a webdriver's input box. Supply the path of the
    input box using the `xpath` parameter, and the text to send with the
    `to_send` parameter.  If `clear_first` is set to true, the text box will be
    cleared first before inputting the text.  If, in conjunction with
    `clear_first` being true, `clear_manually` is set to true, the text box will
    be cleared with 5 presses of the backspace key.  If `do_submit` is set to
    true, then the driver will submit the form that the input box belongs to."""
    input_box = driver.find_element_by_xpath(xpath)
    if clear_first:
        if clear_manually:
            for i in range(5):
                input_box.send_keys(Keys.BACKSPACE)
        else:
            input_box.clear()
    input_box.send_keys(to_send)
    sleep(1)
    if do_submit:
        input_box.submit()
    return driver


def sel_from_dropdown(driver, xpath, to_send):
    dropdown_box = driver.find_element_by_xpath(xpath)
    dropdown_box.click()
    sleep(0.1)
    entry = driver.find_element_by_xpath(f"//div[text()='{to_send}']")
    entry.click()
    return driver


def enter_info(driver, info_dict: dict, do_submit=False):
    ## enter org name
    driver_ = find_input_box_send_text(
        driver,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[2]/div/label[2]/div/div/div/div/input",
        info_dict["name_of_organization"],
    )
    ## enter opp name
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[4]/div/label[2]/div/div/div/input",
        info_dict["name_of_opportunity"],
    )
    ## enter cat of need
    driver_ = sel_from_dropdown(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[5]/div/label[2]/div/div/div[1]/div",
        info_dict["category_of_need"],
    )
    ## enter start time
    st = driver_.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/table/tr/td[1]/div/label[2]/div/div/div[1]/input"
    )
    st.clear()
    # ind 0 = hr, ind 1 = min, ind 2 = AM or PM
    inp_time_list: list = info_dict["start_time"].replace(":", " ").split(" ")
    # first time will be to sel am/pm
    if inp_time_list[2] == "AM":
        driver_.find_element_by_xpath(
            "//div[@class='q-time__clock-circle fit']/../../../../../../div/div/div[text()='AM']"
        ).click()
    else:
        driver_.find_element_by_xpath(
            "//div[@class='q-time__clock-circle fit']/../../../../../../div/div/div[text()='PM']"
        ).click()
    st = driver_.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/table/tr/td[1]/div/label[2]/div/div/div[1]/input"
    )
    st.click()
    # second time will be to sel hr
    clk_popup_times_hr: list = driver.find_elements_by_xpath(
        "//div[@class='q-time__clock-circle fit']/div[*]"
    )
    for time in clk_popup_times_hr:
        if time.text == inp_time_list[0]:
            time.click()
            break
    # third time will be to sel min
    sleep(1)
    clk_popup_times_min: list = driver_.find_elements_by_xpath(
        "//div[@class='q-time__clock-circle fit']/div[*]"
    )
    for time in clk_popup_times_min:
        if time.text == inp_time_list[1]:
            time.click()
            break
    sleep(1)
    ## enter duration-hrs
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[7]/div/label[1]/label/div/div/div/input",
        info_dict["duration_hrs"],
        clear_first=True,
        clear_manually=True,
    )
    ## enter duration-min
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[7]/div/label[2]/label/div/div/div/input",
        info_dict["duration_mins"],
        clear_first=True,
        clear_manually=True,
    )
    ## enter coordtr name
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[9]/label[2]/div/div/div/input",
        info_dict["coordinator_first_and_last_name"],
    )
    ## enter coordtr email
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[10]/label[2]/div/div/div/input",
        info_dict["coordinator_email_address"],
    )
    ## enter coordtr phone num
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[11]/label[2]/div/div/div/input",
        info_dict["coordinator_mobile_phone_number"],
    )
    ## enter msg to coordtr
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[12]/label[2]/div/div/div/textarea",
        info_dict["msg_to_coordinator"],
    )
    ## enter service performed
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[13]/div[2]/div[1]/div/label[2]/div/div/div/textarea",
        info_dict["service_performed"],
    )
    ## enter serv cat type
    driver_ = sel_from_dropdown(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[13]/div[2]/div[2]/div/label[2]/div/div/div[1]/div",
        info_dict["service_category_type"],
    )
    ## enter how serv fulfill
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[13]/div[2]/div[3]/div/label[2]/div/div/div/textarea",
        info_dict["how_did_service"],
    )
    ## enter what was learned
    driver_ = find_input_box_send_text(
        driver_,
        "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/form/div[13]/div[2]/div[4]/div/label[2]/div/div/div/textarea",
        info_dict["what_learned_while"],
    )
    if do_submit:
        form_sub_btn = driver_.find_element_by_class_name("hhSubmitButton")
        form_sub_btn.click()
        sleep(3)
        ref_box = driver_.find_element_by_xpath("//textarea")
        ref_box.send_keys(info_dict["reflection"])
        ref_sub_btn = driver_.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/div/div[1]/div[1]/div/div/div[1]/div[1]/div[3]/div/button"
        )
        ref_sub_btn.click()
    return driver_


def main():
    ## variables
    args = parse_commandline()
    user, passwd = get_creds("b12fbfc7-e692-4ef1-9783-ad130147f399")
    url: str = "https://app.helperhelper.com/"
    if args.headful:
        driver = Firefox()
    else:
        options = Options()
        options.headless = True
        driver = Firefox(options=options)
    info_dict: dict = parse_toml(args.input_file)

    driver.implicitly_wait(10)
    driver.get(url)  # navigate to url
    ## send email initially
    driver = find_input_box_send_text(driver, "//div/input", user, do_submit=True)
    ## send password
    driver = find_input_box_send_text(
        driver, "//input[@type='password']", passwd, do_submit=True
    )
    sleep(2)
    ## get to the add commitment screen
    driver = input_date(driver, info_dict["start_date"])
    ## enter information
    driver = enter_info(driver, info_dict, do_submit=True)
    sleep(2)
    # return driver
    driver.quit()


if __name__ == "__main__":
    main()
