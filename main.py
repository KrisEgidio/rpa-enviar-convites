from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox

def main():
    load_dotenv()
    company_id = os.getenv("COMPANY_LINKEDIN_ID")
    network_url = f"https://www.linkedin.com/company/{company_id}/admin/feed/posts/?invite=true"
    driver = webdriver.Edge()
    start_bot(driver, network_url)

def get_login_data():
    """
    Cria uma janela para input de dados do login

    :return: user, password
    """
    def on_login_button_click():
        user = user_var.get()
        password = password_var.get()
        window.destroy()  # Fecha a janela
        return user, password

    window = tk.Tk()
    window.title("Login")

    # Crie rótulos para os campos de entrada
    label_user = tk.Label(window, text="Usuário:")
    label_password = tk.Label(window, text="Senha:")

    # Crie variáveis de controle para os campos de entrada
    user_var = tk.StringVar()
    password_var = tk.StringVar()

    # Crie campos de entrada vinculados às variáveis de controle
    entry_user = tk.Entry(window, textvariable=user_var)
    entry_password = tk.Entry(window, show="*", textvariable=password_var)  # A senha é exibida como asteriscos

    button = tk.Button(window, text="Login", command=on_login_button_click)

    # Coloque os widgets na janela
    label_user.pack()
    entry_user.pack()
    label_password.pack()
    entry_password.pack()
    button.pack()

    # Inicie a janela
    window.mainloop()

def login_to_linkedin(driver):
    """
    void
    Aguardar o usuário logar.
    """
    driver.get("https://www.linkedin.com/login")

    ## Verificando se o usuário está logado ##
    current_url = driver.current_url
    while 'feed' not in current_url:
        time.sleep(1)
        current_url = driver.current_url
    print("Logged in successfully")


def send_requests_to_users(driver, network_url):
    """
    void
    Envia convites para os usuários da rede obtendo a quantidade de convite disponíveis e realizando o cálculo para enviar a quantidade correta.
    """

    driver.get(network_url)
    time.sleep(2)

    ## Obtendo a quantidade de convites disponíveis para enviar ##
    size = driver.find_element(By.XPATH, "//span[@class='t-14 t-black--light']//span[@class='t-bold']").text
    sends = int(size.split("/")[0])



    ## Obtendo a quantidade vezes que vai clicar no botão de carregar mais usuários ##
    if sends >= 20:
        show_more = round((sends - 20) / 10)
    else:
        show_more = 0

    more_results_button = driver.find_element(By.XPATH,
                                              "//button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']")

    ## Clicando no botão de carregar mais usuários ##
    if show_more > 0:
        for i in range(show_more):
            more_results_button = driver.find_element(By.XPATH,
                                                      "//button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']")
            more_results_button.click()
            time.sleep(2)

    ## Selecionando os usuários ##
    for i in range(sends):
        checkbox = driver.find_elements(By.XPATH,
                                        "//input[@class='ember-checkbox ember-view']")
        driver.execute_script("arguments[0].click();", checkbox[i])

    time.sleep(2)

    ## Enviando os convites ##
    send_button = driver.find_element(By.XPATH,
                                      "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
    send_button.click()
    time.sleep(5)
    print("Requests sent successfully")


def take_a_screenshot(driver):
    """
    void
    Tira um print da tela e salva na pasta resource.
    """
    loc_time = time.localtime()
    time_string = time.strftime("%m/%d/%Y", loc_time)
    driver.save_screenshot(time_string + "_screenshot.png")


def start_bot(driver, network_url):
    """
    void
    Inicia o bot.
    """
    try:
        print("Bot started")
        login_to_linkedin(driver)
        send_requests_to_users(driver, network_url)
        driver.quit()
    except Exception as e:
        print(f"Something went wrong {e}")
        # take_a_screenshot(driver)
        time.sleep(10000000)
        ##driver.quit()


main()