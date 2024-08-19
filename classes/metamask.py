from typing import TYPE_CHECKING

from selenium.common import TimeoutException

from utils import sleep_random, generate_password
from utils import write_text_to_file

if TYPE_CHECKING:
    from classes.ads import Ads


class Metamask:
    chains = {
        "Linea ANKR": {
            "Network name": "Linea ANKR",
            "New RPC URL": "https://rpc.ankr.com/linea",
            "Chain ID": 59144,
            "Currency Symbol": "ETH",
        },
        "BSC": {
            "Network name": "BSC",
            "New RPC URL": "https://bsc-pokt.nodies.app",
            "Chain ID": 56,
            "Currency Symbol": "BNB",
        },

    }

    def __init__(self, ads, password: str = None, seed: str = None):
        self._url = "chrome-extension://kfffndnaofmhjgfjincifaloeplkongj/home.html"
        self.ads: Ads = ads
        self.password = password
        self.seed = seed

    def open_metamask(self):
        """
        Открывает metamask
        :return:
        """
        self.ads.open_url(self._url)

    def create_wallet(self):
        """
        Создает кошелек в metamask
        :return:
        """
        self.open_metamask()
        sleep_random()
        self.ads.click_element("//input[@data-testid='onboarding-terms-checkbox']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='onboarding-create-wallet']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='metametrics-no-thanks']")

        # генерируем пароль и вводим в 2 поля
        password = generate_password()
        self.ads.input_text("//input[@data-testid='create-password-new']", password)
        sleep_random()
        self.ads.input_text("//input[@data-testid='create-password-confirm']", password)
        sleep_random()
        self.ads.click_element("//input[@data-testid='create-password-terms']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='create-password-wallet']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='secure-wallet-recommended']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='recovery-phrase-reveal']")
        seed = []
        for i in range(12):
            xpath = f"//div[@data-testid='recovery-phrase-chip-{i}']"
            word = self.ads.get_text(xpath)
            seed.append(word)
        sleep_random()
        self.ads.click_element("//button[@data-testid='recovery-phrase-next']")
        sleep_random()
        for i in range(12):
            self.ads.input_text(f"//input[@data-testid='recovery-phrase-input-{i}']", seed[i], timeout=1)
            sleep_random()
        sleep_random()
        self.ads.click_element("//button[@data-testid='recovery-phrase-confirm']")
        sleep_random(3, 5)
        self.ads.click_element("//button[@data-testid='onboarding-complete-done']")

        sleep_random()
        self.ads.click_element("//button[@data-testid='pin-extension-next']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='pin-extension-done']")
        sleep_random(3, 3)
        self.ads.click_element("//button[@data-testid='popover-close']", 5)
        sleep_random()

        self.ads.click_element("//button[@data-testid='account-options-menu-button']")
        sleep_random()

        self.ads.click_element("//button[@data-testid='account-list-menu-details']")
        sleep_random()

        address = self.ads.get_text("//button[@data-testid='address-copy-button-text']/span/div")
        sleep_random()

        seed_str = " ".join(seed)

        write_text_to_file("new_wallets.txt", f"{self.ads.profile_number} {address} {password} {seed_str}")

    def auth_metamask(self) -> None:
        """
        Авторизует в metamask
        :return:
        """
        self.open_metamask()
        self.ads.input_text("//input[@data-testid='unlock-password']", self.password, 3)
        self.ads.click_element("//button[@data-testid='unlock-submit']", 3)
        sleep_random(3, 5)
        self.ads.click_element("//button[@data-testid='popover-close']", 5)
        if not self.ads.find_element("//li[@data-testid='home__nfts-tab']", 5):
            raise Exception("Metamask auth failed")

    def import_wallet(self):
        """
        Импортирует кошелек в metamask
        :return:
        """
        self.open_metamask()

        seed_list = self.seed.split(" ")
        if not self.password:
            self.password = generate_password()

        if self.ads.find_element("//button[@data-testid='onboarding-create-wallet']", 5):
            self.ads.click_element("//input[@data-testid='onboarding-terms-checkbox']")
            sleep_random()
            self.ads.click_element("//button[@data-testid='onboarding-import-wallet']")
            self.ads.click_element("//button[@data-testid='metametrics-no-thanks']")
            for i, word in enumerate(seed_list):
                self.ads.input_text(f"//input[@data-testid='import-srp__srp-word-{i}']", word)
            self.ads.click_element("//button[@data-testid='import-srp-confirm']")
            self.ads.input_text("//input[@data-testid='create-password-new']", self.password)
            self.ads.input_text("//input[@data-testid='create-password-confirm']", self.password)
            sleep_random()
            self.ads.click_element("//input[@data-testid='create-password-terms']")
            self.ads.click_element("//button[@data-testid='create-password-import']")

            sleep_random(3, 5)
            self.ads.click_element("//button[@data-testid='onboarding-complete-done']")

            sleep_random()
            self.ads.click_element("//button[@data-testid='pin-extension-next']")
            sleep_random()
            self.ads.click_element("//button[@data-testid='pin-extension-done']")
            sleep_random(3, 3)
            self.ads.click_element("//button[@data-testid='popover-close']", 5)
            sleep_random()
        else:
            self.ads.click_element("//a[text()='Forgot password?']", 5)
            for i, word in enumerate(seed_list):
                self.ads.input_text(f"//input[@data-testid='import-srp__srp-word-{i}']", word)
            self.ads.input_text("//input[@data-testid='create-vault-password']", self.password)
            self.ads.input_text("//input[@data-testid='create-vault-confirm-password']", self.password)
            self.ads.click_element("//button[@data-testid='create-new-vault-submit-button']")
            sleep_random(3, 3)
            self.ads.click_element("//button[@data-testid='popover-close']", 5)

        self.ads.click_element("//button[@data-testid='account-options-menu-button']")
        sleep_random()

        self.ads.click_element("//button[@data-testid='account-list-menu-details']")
        sleep_random()

        address = self.ads.get_text("//button[@data-testid='address-copy-button-text']/span/div")
        sleep_random()

        write_text_to_file("new_wallets.txt", f"{self.ads.profile_number} {address} {self.password} {self.seed}")

    def connect(self):
        """
        Подтверждает подключение к metamask
        :return:
        """
        try:
            current_tab = self.ads.driver.current_window_handle
            sleep_random(2.5, 3.5)

            for _ in range(20):
                target_tab = self.ads.find_tab("notification.html#connect")
                if target_tab:
                    self.ads.driver.switch_to.window(target_tab)
                    sleep_random(1.5, 2.5)
                    self.ads.click_element("//button[@data-testid='page-container-footer-next']")
                    self.ads.click_element("//button[@data-testid='page-container-footer-next']")
                    sleep_random(1.5, 2.5)
                    self.ads.driver.switch_to.window(current_tab)
                    sleep_random(1.5, 2.5)
                    return
                sleep_random(2.5, 3.5)
            raise TimeoutException(f"{self.ads.profile_number} Metamask connect timeout")
        except Exception as ex:
            print(f"{self.ads.profile_number} Error metamask connect: {ex}")

    def sign(self):
        """
        Подтверждает подпись в metamask
        :return:
        """
        try:
            current_tab = self.ads.driver.current_window_handle
            sleep_random(2.5, 3.5)

            for _ in range(20):
                target_tab = self.ads.find_tab("#confirm-transaction")
                if target_tab:
                    self.ads.driver.switch_to.window(target_tab)
                    sleep_random(2.5, 3.5)
                    self.ads.click_element("//button[@data-testid='page-container-footer-next']")
                    sleep_random(0.5, 1.5)
                    self.ads.driver.switch_to.window(current_tab)
                    sleep_random(2.5, 3.5)
                else:
                    sleep_random(2.5, 3.5)
        except Exception as ex:
            print(f"{self.ads.profile_number} Error metamask sign: {ex}")

    def send_tx(self):
        """
        Подтверждает отправку транзакции в metamask
        :return:
        """
        current_tab = self.ads.driver.current_window_handle
        for _ in range(15):
            sleep_random(2.5, 3.5)

            for _ in range(20):
                target_tab = self.ads.find_tab("#confirm-transaction")
                if target_tab:
                    self.ads.driver.switch_to.window(target_tab)
                    sleep_random(2.5, 3.5)
                    if button_switch := self.ads.find_element("//button[text()='Switch network' or text()='Сменить сеть']", 1):
                        button_switch.click()
                        sleep_random(3, 5)
                        continue
                    else:
                        break
                sleep_random(2.5, 3.5)

            self.ads.click_element("//button[@data-testid='page-container-footer-next']")
            sleep_random(1.5, 2.5)
            self.ads.driver.switch_to.window(current_tab)
            sleep_random(1.5, 2.5)
            return

    def select_chain(self, chain: str):
        """
        Выбирает сеть в metamask
        :param chain: название сети как в метамаске
        :return:
        """
        if chain == self.ads.get_text("//button[@data-testid='network-display']/child::span"):
            return
        self.ads.click_element("//button[@data-testid='network-display']")
        if self.ads.find_element(f"//p[text()='{chain}']", 3):
            self.ads.click_element(f"//p[text()='{chain}']")
        else:
            self.ads.click_element("//button[@aria-label='Закрыть' or @aria-label='Close']")
            self.set_chain(chain)
    def set_chain(self, chain: str):
        """
        Добавляет новую сеть в metamask
        :param chain: название сети
        :return:
        """
        chain_name = self.chains[chain]["Network name"]
        rpc = self.chains[chain]["New RPC URL"]
        chain_id = str(self.chains[chain]["Chain ID"])
        currency = self.chains[chain]["Currency Symbol"]
        self.ads.open_url(self._url+"#settings/networks/add-network")
        sleep_random(1, 3)
        self.ads.input_text("//input[@data-testid='network-form-network-name']", text=chain_name)
        self.ads.input_text("//input[@data-testid='network-form-rpc-url']", text=rpc)

        self.ads.input_text("//input[@data-testid='network-form-chain-id']", text=chain_id)
        self.ads.input_text("//input[@data-testid='network-form-ticker-input']", text=currency)
        sleep_random(1, 3)
        self.ads.click_element("//button[text()='Save' or text()='Сохранить']")
        self.ads.click_element("//h6[contains(text(), 'Switch to') or contains(text(), 'Сменить на')]")
