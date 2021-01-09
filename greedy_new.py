import copy
#dictionary format: [usability per weight index (initially 0), needed parts, weight in grams (initially), usability]
products = {"Notebook Office 13": [0, 205, 2451, 40],
            "Notebook Office 14": [0, 420, 2978, 35],
            "Notebook outdoor": [0, 450, 3625, 80],
            "Mobiltelefon Büro": [0, 60, 717, 30],
            "Mobiltelefon outdoor": [0, 157, 988, 60],
            "Mobiltelefon Heavy-Duty": [0, 220, 1220, 65],
            "Tablet Büro klein": [0, 620, 1405, 40],
            "Tablet Büro groß": [0, 250, 1455, 40],
            "Tablet outdoor klein": [0, 540, 1690, 45],
            "Tablet outdoor groß": [0, 370, 1980, 68]
            }

#this function takes one input array as described above and calculates the profitability index for this element and writes it at index 0 of the list;
#converts weights from grams to kg
def calculate_profitability_index(dict):
    for key, value in products.items():
        value[2] = value[2]/1000
        value[0] = value[3]/(value[2]) # calculating the profitability per kg


#turns profitability index positive again (was negative during calculation)
def turn_profitability_positive(dict):
    for key, value in dict.items():
        if value[0] < 0:
            value[0] = - value[0]

#gets key in dictionary with maximum profitability with respect to the available unit number and weight
def get_max_key(base_info, capacity):
    while True:
        current_max_key = max(base_info, key=base_info.get)
        temp_value = base_info.get(current_max_key) #best maximum value guess, needs to be checked whether it fits in our truck

        if temp_value[0] < 0:
            return 0

        if temp_value[2] < capacity and temp_value[0] >= 0 and temp_value[1] > 0:
            #if enough capacity is available, return the key of the dict entry with max profitability
            return current_max_key
        else:
            temp_value[0] = - temp_value[0] #to make sure it will not be detected as max during the max finding process, will be reversed at the end
            base_info[current_max_key] = temp_value

#function for loading the empty transporter, first parameter load capacity in kg, second parameter weight of the driver, third parameter: available products dict
def load_transporter(capacity, weight, product_info):
    #create an empty dictionary as loading list and inventory dictionary
    loading_list = {}

    # code to fill loading list
    capacity_greedy = capacity - weight
    usability = 0

    #loading process with greedy algorithm
    while True:
        #finding the key with the current maximum usability and get the value array for it with fitting weight
        current_max_key = get_max_key(product_info,capacity_greedy) #returns 0 when no fitting element can be found
        if current_max_key == 0:
            break

        current_max_value = product_info.get(current_max_key)

        #if blocks for faster loading (loads 100, 10, 1 in a row)
        loading_keys = loading_list.keys() #gets the keys of the loading list to check whether there is already an entry with specified key

        n = [100,10,1]

        for elem in n:
            if current_max_value[2]*elem < capacity_greedy and current_max_value[1] >= elem:
                if current_max_key in loading_keys:
                    loading_list[current_max_key] += elem
                    capacity_greedy = capacity_greedy - (current_max_value[2] * elem)
                    current_max_value[1] = current_max_value[1] - elem
                    usability += current_max_value[3] * elem
                else:
                    loading_list[current_max_key] = elem
                    capacity_greedy = capacity_greedy - (current_max_value[2] * elem)
                    current_max_value[1] = current_max_value[1] - elem
                    usability += current_max_value[3] * elem

    turn_profitability_positive(product_info)
    return loading_list, usability

#perform loading comparison
#initializing product lists, usabilities and loading lists
calculate_profitability_index(products)
#deep copies are needed here because of Python design priciples
product_list1 = copy.deepcopy(products)
product_list2 = copy.deepcopy(products)
usability_1 = 0
usability_2 = 0
usability_3 = 0
usability_4 = 0
total_usability_1 = 0
total_usability_2 = 0
loadinglist_1 = {}
loadinglist_2 = {}
loadinglist_3 = {}
loadinglist_4 = {}

#case 1
loadinglist_1, usability_1 = load_transporter(1100, 85.7, product_list1)
loadinglist_2, usability_2 = load_transporter(1100, 72.4, product_list1)
total_usability_1 = usability_1 + usability_2

#case 2
loadinglist_3, usability_3 = load_transporter(1100, 72.4, product_list2)
loadinglist_4, usability_4 = load_transporter(1100, 85.7, product_list2)
total_usability_2 = usability_3 + usability_4

if total_usability_1 > total_usability_2:
    print("Gesamtnutzen: " + str(total_usability_1) + " Nutzeinheiten")
    print("Ladungsliste 1. LKW: " + str(loadinglist_1))
    print("Ladungsliste 2. LKW: " + str(loadinglist_2))
else:
    print("Gesamtnutzen: " + str(total_usability_2) + " Nutzeinheiten")
    print("Ladungsliste 1. LKW: " + str(loadinglist_3))
    print("Ladungsliste 2. LKW: " + str(loadinglist_4))