menu_data = {
    "restaurants": [
        {
            "name": "Punjabi Tadka",
            "rating": 4.5,
            "delivery_time": "25-35 min",
            "menu": {
                "Butter Chicken": 320,
                "Chicken Biryani": 280,
                "Paneer Butter Masala": 260,
                "Naan": 40,
                "Garlic Naan": 50,
                "Jeera Rice": 120
            }
        },
        {
            "name": "Mumbai Spice",
            "rating": 4.3,
            "delivery_time": "20-30 min",
            "menu": {
                "Butter Chicken": 340,
                "Veg Biryani": 220,
                "Dal Makhani": 180,
                "Naan": 45,
                "Roti": 35
            }
        }
    ]
}

def get_all_menus():
    return menu_data