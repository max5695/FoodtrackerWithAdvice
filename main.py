import requests
import json
import random



def get_personal_data():
    data = {}
    data['name'] = input("Geben Sie Ihren Namen ein: ")
    data['alter'] = int(input("Geben Sie Ihr Alter ein: "))
    data['groesse'] = int(input("Geben Sie Ihre Größe in cm ein: "))
    data['gewicht'] = int(input("Geben Sie Ihr Gewicht in kg ein: "))
    return data



def get_food_data():
    food_list = []
    while True:
        food_name = input("Geben Sie den Namen der Nahrung ein: ")
        search_response = requests.get(f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food_name}&search_simple=1&action=process&json=1")
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data['count'] > 0:
                product_id = search_data['products'][0]['id']
                response = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{product_id}.json")
                if response.status_code == 200:
                    product_data = response.json()
                    if product_data['status'] == 1:
                        product = product_data['product']
                        food = {
                            'name': product.get('product_name', 'Unbekannt'),
                            'kalorien': int(product['nutriments'].get('energy-kcal_100g', 0)),
                            'vitamine': [v for v in product['nutriments'] if 'vitamin' in v]
                        }
                        food_list.append(food)
                        print(f"Nahrungsmittel {food['name']} hinzugefügt.")
                    else:
                        print("Produkt nicht gefunden.")
                else:
                    print("Fehler beim Abrufen der Produktdaten.")
            else:
                print("Kein Produkt mit diesem Namen gefunden.")
        else:
            print("Fehler bei der Produktsuche.")
        
        another = input("Möchten Sie eine weitere Nahrung eingeben? (ja/nein): ").strip().lower()
        if another != 'ja':
            break
    return food_list


def calculate_calorie_limit(personal_data):
    # Beispielhafte Berechnung der Kaloriengrenze basierend auf Alter, Größe und Gewicht
    # Dies ist eine vereinfachte Formel und sollte an die tatsächlichen Bedürfnisse angepasst werden
    grundumsatz = 10 * personal_data['gewicht'] + 6.25 * personal_data['groesse'] - 5 * personal_data['alter'] + 5
    aktivitaetsfaktor = 1.55  # Beispielhafter Aktivitätsfaktor für eine durchschnittliche Tätigkeit (mäßige Bewegung/Sport an 3-5 Tagen pro Woche)
    kaloriengrenze = grundumsatz * aktivitaetsfaktor
    return kaloriengrenze


def get_random_recommendation(vitamin):
    recommendations = {
        'vitamin_a': ['Karotten', 'Süßkartoffeln', 'Spinat', 'Kürbis'],
        'vitamin_b1': ['Vollkornprodukte', 'Schweinefleisch', 'Hülsenfrüchte', 'Nüsse'],
        'vitamin_c': ['Orangen', 'Paprika', 'Brokkoli', 'Erdbeeren'],
        'vitamin_d': ['Sonnenlicht', 'Fisch', 'Eier', 'Pilze'],
    }
    return random.choice(recommendations.get(vitamin, ['Keine Empfehlung verfügbar']))


def evaluate_data(personal_data, food_data):
    total_calories = sum(item['kalorien'] for item in food_data)
    all_vitamins = {vit for item in food_data for vit in item['vitamine']}
    
    vitamin_deficiencies = [vit for vit in ['vitamin_a', 'vitamin_b1', 'vitamin_c', 'vitamin_d'] if vit not in all_vitamins]

    kaloriengrenze = calculate_calorie_limit(personal_data)

    print(f"Hallo {personal_data['name']}!")
    print(f"Sie haben insgesamt {total_calories} Kalorien konsumiert.")
    print(f"Ihre individuelle Kaloriengrenze beträgt {kaloriengrenze:.2f} Kalorien.")
    if total_calories > kaloriengrenze:
        print("Sie haben zu viele Kalorien konsumiert!")
    else:
        print("Ihr Kalorienkonsum ist im grünen Bereich.")

    if vitamin_deficiencies:
        print("Sie haben einen Mangel an folgenden Vitaminen:")
        for vit in vitamin_deficiencies:
            recommendation = get_random_recommendation(vit)
            print(f"{vit.capitalize()}: {recommendation}")
    else:
        print("Sie haben alle notwendigen Vitamine konsumiert.")




def main():
    print("Willkommen beim Foodtracker!")
    
    personal_data_input = get_personal_data()
    with open('personal_data.json', 'w') as f:
        json.dump(personal_data_input, f)
    
    print("\nNahrungseingabe:")
    food_data_input = get_food_data()

    print("\nAuswertung:")
    evaluate_data(personal_data_input, food_data_input)



if __name__ == "__main__":
    main()
