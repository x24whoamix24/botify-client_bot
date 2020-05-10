
from rakuten_seller.rakuten_seller import RakutenSeller 

SPORT_PRODUCTS_SHEET_NUMBER = 4

def main():
    
    user = "PrimeValue"
    rakuten_token = "8bcfa56fed804c19a0c6747fd8346230"
    seller = RakutenSeller(user, rakuten_token)
    sheet_name = "Materiel_de_Sport"
    config_folder = "./config/"
    config_files = ["client_secret.json"]
    seller.connectToSheet(sheet_name, config_folder, config_files )

    products = [
        ('https://www.aliexpress.com/item/4000311599150.html?spm=a2g0o.productlist.0.0.2ba572c5PQ0MlL&algo_pvid=afdd8978-9dc5-4cee-8fa7-a95a158ff1ea&algo_expid=afdd8978-9dc5-4cee-8fa7-a95a158ff1ea-0&btsid=0be3746c15889349959208477e4e32&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_', 674824960, 'https://fr.shopping.rakuten.com/offer/buy/674824960/11-pieces-de-resistance-pour-exercices-fitness-gym-yoga-ou-de-pilates-abdos-bandes-definies.html')
        ]
    seller.start_browser()
    print ("importing {} ".format(products))
    for p in products:
        
        ali_url, product_id, rakuten_url = p
        print ("now importing {} ".format(p))
        try:
            seller.importProduct("Sport product", ali_url, product_id, rakuten_url, SPORT_PRODUCTS_SHEET_NUMBER)
        except Exception as e:
            print("faild to import {}, because: {}".format(p, e))
        
    seller.stop_browser()
    print("finished importing products")                                                                                       
    

if (__name__ == "__main__"):
    main()
