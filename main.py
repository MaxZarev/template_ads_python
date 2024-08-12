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

    for profile, password in zip(profiles, passwords):
        ads = Ads(profile, password=password)
        ads.metamask.auth_metamask()
        activity(ads)
        ads.close_browser()
        sleep_random(5, 10)


def activity(ads: Ads):
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


if __name__ == '__main__':
    main()
