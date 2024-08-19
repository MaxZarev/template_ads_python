import random

from classes.ads import Ads

from utils import sleep_random, get_list_from_file


def create_wallets(profiles: list[int]):
    print("Создание кошельков")
    for profile in profiles:
        ads = Ads(profile)
        ads.metamask.create_wallet()
        ads.close_browser()
        sleep_random(5, 10)


def import_wallets(profiles: list[int], seeds: list[str]):
    print("Импорт кошельков")

    if not seeds:
        print("Список сид фраз пуст")
        return

    if len(seeds) != len(profiles):
        print("Количество сид фраз не совпадает с количеством профилей")
        return

    for profile, seed in zip(profiles, seeds):
        ads = Ads(profile, seed=seed)
        ads.metamask.import_wallet()
        ads.close_browser()
        sleep_random(5, 10)


def worker(profiles: list[int], passwords: list[str]):
    print("Автоматизация")
    if not passwords:
        print("Список паролей пуст")
        return

    if len(passwords) != len(profiles):
        print("Количество паролей не совпадает с количеством профилей")
        return

    work_data = dict(zip(profiles, passwords))

    random.shuffle(profiles)

    for profile in profiles:
        password = work_data[profile]
        ads = Ads(profile, password=password)
        ads.metamask.auth_metamask()
        activity(ads)
        ads.close_browser()
        sleep_random(5, 10)


def activity(ads: Ads):
    ads.metamask.select_chain("BSC")
    ads.open_url("pancakeswap.finance")
    if ads.find_element("//button[text()='Connect Wallet']", timeout=3):
        ads.click_element("//div[text()='Connect Wallet']")
        ads.click_element("//img[@src='https://assets.pancakeswap.finance/web/wallets/metamask.png']")
        ads.metamask.connect()

    ads.open_url("https://pancakeswap.finance/swap")
    ads.click_element("//div[@id='pair']")
    ads.click_element("//div[text()='USDT']")
    ads.input_text("//input[@title='Token Amount']", "100")
    ads.click_element("(//div[@id='pair'])[2]")
    ads.click_element("//h2[text()='Select a Token']/parent::div/parent::div/following-sibling::div/descendant::div[text()='BNB']")
    ads.metamask.send_tx()


    pass
    # todo: добавляем логику активности тут


def main():
    profiles = [int(profile) for profile in get_list_from_file("profiles.txt")]

    message = "Выберите тип работы? 1 - Создать новые кошельки, 2 - Импортировать кошельки, 3 - Автоматизация"
    response = input(message)

    if response == "1":
        create_wallets(profiles)

    if response == "2":
        seeds = get_list_from_file("seeds.txt")
        import_wallets(profiles, seeds)

    if response == "3":
        passwords = get_list_from_file("passwords.txt")
        worker(profiles, passwords)


main()
