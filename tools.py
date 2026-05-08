from menu_data import get_all_menus
from crewai.tools import tool

@tool
def search_menu(item_name: str):
    """Search for items in all restaurants and return matching items with prices"""
    data = get_all_menus()
    results = []
    search_term = item_name.lower().strip()

    for restaurant in data["restaurants"]:
        for menu_item, price in restaurant["menu"].items():
            menu_lower = menu_item.lower()

            # Flexible matching
            if (search_term in menu_lower or menu_lower in search_term or any(word in menu_lower for word in search_term.split())):
                
                results.append({
                    "restaurant": restaurant["name"],
                    "item": menu_item,
                    "price": price,
                    "delivery_time": restaurant["delivery_time"],
                    "rating": restaurant["rating"]
                })

    if not results:
        return f"No matching item found for '{item_name}'"
    
    return str(results)


@tool
def get_full_menu(restaurant_name: str = None):
    """Return full menu of a restaurant or all restaurants"""
    data = get_all_menus()

    if restaurant_name:
        for res in data["restaurants"]:
            if restaurant_name.lower() in res["name"].lower():
                return f"Menu of {res['name']}:\n{res['menu']}"
        return f"Restaurant '{restaurant_name}' not found."
    
    return str(data)