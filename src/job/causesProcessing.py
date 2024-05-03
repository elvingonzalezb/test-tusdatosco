import asyncio
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import mongo

from enum import Enum

actor_o_ofendido = {
    "type_search": "demandante",
    "num_document": [
        "0968599020001",
        "0992339411001",
        "1791251237001",
        "0968599020001",
        "0968599020001",
        "0992339411001"
    ]
}

demandado_o_procesado = {
    "type_search": "demandado",
    "num_document": [
        "1791251237001",
        "0968599020001",
        "0968599020001",
        "0992339411001",
        "1791251237001",
        "0968599020001"
    ]
}

class TypeSearch(Enum):
    DEMANDANTE = "demandante"
    DEMANDADO = "demandado"

async def process_causes(num_document, type_search):
    print("Initiating process for:", type_search) 
    mongo.register_progress(num_document[0], 1, 1, "Starting process", "in progress")
    # Configuración del WebDriver
    opts = Options()
    opts.add_argument("user-agent=Mozilla/125.0.2 Chrome/124.0.6367.91")
    opts.add_argument("--headless")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=opts
    )

    urlSearch = 'https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros'

    try:
        driver.get(urlSearch)

        # Espera hasta que el campo de búsqueda esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="cedulaActor"]')))

        # Búsqueda y llenado del campo según el tipo de búsqueda
        type_input = None
        if type_search == TypeSearch.DEMANDANTE.value:
            type_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="cedulaActor"]')
        elif type_search == TypeSearch.DEMANDADO.value:
            type_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="cedulaDemandado"]')

        if type_input is not None:
            for document in num_document:
                try:
                    type_input.clear()
                    type_input.send_keys(document)

                    # Espera hasta que el botón de búsqueda esté habilitado
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Enviar formulario"]')))

                    boton_search = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Enviar formulario"]')
                    boton_search.click()

                    # Espera hasta que se carguen los resultados
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cantidadMovimiento')))

                    await asyncio.sleep(5)

                    cant_register = driver.find_element(By.CSS_SELECTOR, '.cantidadMovimiento').text
                    cant_register = int(cant_register.split(':')[-1].strip())

                    num_document_result = driver.find_element(By.CSS_SELECTOR, 'div.ng-star-inserted strong').find_element(By.XPATH, './following-sibling::span').text

                    data_process = {
                        "numDocument": num_document_result,
                        "numRegistros": cant_register,
                        "type": type_search,
                        "causas": []
                    }

                    count_page = 1
                    while True:
                        elements_causa = driver.find_elements(By.CSS_SELECTOR, '.causa-individual')

                        for element in elements_causa:
                            causa = {}
                            causa["entryDate"] = element.find_element(By.CLASS_NAME, 'fecha').text
                            causa["numProcess"] = element.find_element(By.CLASS_NAME, 'numero-proceso').text
                            causa["actionInfraction"] = element.find_element(By.CLASS_NAME, 'accion-infraccion').text
                            causa["idMovement"] = element.find_element(By.CSS_SELECTOR, 'div.detalle a').get_attribute('aria-label').split()[-1]

                            data_process["causas"].append(causa)

                        num_document_result = driver.find_element(By.CSS_SELECTOR, 'div.ng-star-inserted strong').find_element(By.XPATH, './following-sibling::span').text

                        collection_name = "causas"
                        collection = mongo.connect_to_mongodb(collection_name)

                        new_causas = data_process["causas"]                        
                        mongo.update_data(collection, num_document_result, new_causas)
                        print("Successful registration of the page", count_page, "Num Document", num_document_result)
                        mongo.register_progress(num_document_result, count_page, count_page, "Successful registration of the page", "success")
                        count_page += 1

                        try:
                            boton_siguiente = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Página siguiente"]')))
                            boton_siguiente.click()
                            mongo.register_progress(num_document_result, count_page, count_page)
                            print("Advancing to the next page:", count_page, "Num Document", num_document_result, "Advancing to the next page", "success")
                            await asyncio.sleep(3)
                        except NoSuchElementException:
                            print("There are no more pages")
                            mongo.register_progress(num_document_result, count_page, count_page, "Process completed", "no more pages")
                            break
                        except StaleElementReferenceException:
                            print("Stale element reference. Trying to continue with the next document.")
                            mongo.register_progress(num_document_result, count_page, count_page, "Stale element reference", "error")
                            break
                        except Exception as e:
                            print("An error occurred when clicking on the next page button:", e)
                            mongo.register_progress(num_document_result, count_page, count_page, "Error occurred", "error")
                            break
                except Exception as e:
                    print(f"An error occurred for document {document}: {e}")
                    continue  # Continuar con el siguiente documento en caso de error
        else:
            print("Type input not found")
    except NoSuchElementException as e:
        print("Element not found:", e)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Cerrar el WebDriver al finalizar
        driver.quit()

async def run_requests():
    tasks = []
    for data in [actor_o_ofendido, demandado_o_procesado]:
        num_documents = data["num_document"]
        type_search = data["type_search"]
        task = asyncio.create_task(process_causes(num_documents, type_search))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_requests())
