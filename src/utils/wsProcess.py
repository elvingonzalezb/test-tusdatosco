from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import utils.mongoTransaction
from enum import Enum

class TypeSearch(Enum):
    DEMANDANTE = "demandante"
    DEMANDADO = "demandado"

# Función para determinar el tipo de búsqueda y escribir en el campo de entrada correspondiente
def validate_search(driver, type_search, num_document):
    # Determinar el tipo de búsqueda
    if type_search == TypeSearch.DEMANDANTE:
        value_search = num_document #"0968599020001"
        type_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="cedulaActor"]')
    elif type_search == TypeSearch.DEMANDADO:
        value_search = num_document #"1791251237001"
        type_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="cedulaDemandado"]')

    # Escribir el valor en el campo de entrada
    type_input.send_keys(value_search)
def process_causes(num_document, type_search):
    # Configuration
    opts = Options()
    opts.add_argument("user-agent=Mozilla/125.0.2 Chrome/124.0.6367.91")
    #opts.add_argument("--headless")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=opts
    )

    urlSearch = 'https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros'

    try:
        driver.get(urlSearch)
        sleep(3)
        # Realizar la búsqueda según el tipo
        type_search = TypeSearch.DEMANDANTE
        validate_search(driver, type_search, num_document)

        # Esperar a que el botón de búsqueda esté habilitado para hacer clic en él
        boton_search = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Enviar formulario"]')
        boton_search.click()
        
        # Demora necesaria
        sleep(5)

        # Obtener el número total de registros encontrados
        cant_register = driver.find_element(By.CSS_SELECTOR, '.cantidadMovimiento').text
        cant_register = int(cant_register.split(':')[-1].strip())
        
        # Obtener el número de documento del actor/ofendido
        num_document = driver.find_element(By.CSS_SELECTOR, 'div.ng-star-inserted strong').find_element(By.XPATH, './following-sibling::span').text
    
        # Inicializar data
        data_process = {
            "numDocument": num_document,
            "numRegistros": cant_register,
            "type": type_search,
            "causas": []
        }     

        count_page = 1
        # Proceso de guardar y actualizar página por página
        while True:
            # Obtener todos los elements de la clase 'causa-individual'
            elements_causa = driver.find_elements(By.CSS_SELECTOR, '.causa-individual')

            # Iterar sobre los elements para obtener la información
            for element in elements_causa:
                causa = {}
                causa["entryDate"] = element.find_element(By.CLASS_NAME, 'fecha').text
                causa["numProcess"] = element.find_element(By.CLASS_NAME, 'numero-proceso').text
                causa["actionInfraction"] = element.find_element(By.CLASS_NAME, 'accion-infraccion').text
                causa["idMovement"] = element.find_element(By.CSS_SELECTOR, 'div.detalle a').get_attribute('aria-label').split()[-1]
                
                data_process["causas"].append(causa)   

            # Obtener el número de documento
            num_document = driver.find_element(By.CSS_SELECTOR, 'div.ng-star-inserted strong').find_element(By.XPATH, './following-sibling::span').text

            # Call connection
            collection_name = "causas"
            collection = mongoTransaction.connect_to_mongodb(collection_name)

            new_causas = data_process["causas"]
            mongoTransaction.update_data(collection, num_document, new_causas)      
            print("Successful registration of the page", count_page) 
            count_page += 1
            
            # Esperar a que el botón de siguiente esté presente y visible
            try:
                #boton_siguiente = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Página siguiente"]')))
                boton_siguiente = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Página siguiente"]')))
                # Ir a nueva pagina
                boton_siguiente.click()
                print("Advancing to the next page:", count_page)
                sleep(3)
            except NoSuchElementException:
                print("There are no more pages")
                break
            except Exception as e:
                print("An error occurred when clicking on the next page button:", e)
                break

    except NoSuchElementException as e:
        print("Element not found:", e)

    except Exception as e:
        print("An error occurred:", e)
        
    driver.quit()


process_causes("1791251237001", "demandado")