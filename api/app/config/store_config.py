STORE_ITEMS = {

    "medkit": {
        "name": "Medkit",
        "price": 200,
        "consumable": True,
        "effect": {"reputation": 5}
    },

    "coffee": {
        "name": "Coffee",
        "price": 50,
        "consumable": True,
        "effect": {"alignment": 2}
    },

    "energy_drink": {
        "name": "Energy Drink",
        "price": 100,
        "consumable": True,
        "effect": {"alignment": 1, "reputation": 1}
    },

    "public_donation": {
        "name": "Public Donation",
        "price": 700,
        "consumable": True,
        "effect": {"alignment": 6, "reputation": 4}
    },

    "dark_contract": {
        "name": "Dark Contract",
        "price": 1500,
        "consumable": True,
        "effect": {"alignment": -8, "reputation": 5}
    },

    # ======================
    # Permanent / Equipment
    # ======================

    "black_card": {
        "name": "Black Market Card",
        "price": 1000,
        "consumable": False,
        "effect": {"alignment": -5, "reputation": -3}
    },

    "training_manual": {
        "name": "Training Manual",
        "price": 500,
        "consumable": False,
        "effect": {"reputation": 3}
    },

    "ethics_book": {
        "name": "Ethics Handbook",
        "price": 300,
        "consumable": False,
        "effect": {"alignment": 4}
    },

    "luxury_watch": {
        "name": "Luxury Watch",
        "price": 1200,
        "consumable": False,
        "effect": {"reputation": 7}
    },

    "forged_id": {
        "name": "Forged Identity",
        "price": 800,
        "consumable": False,
        "effect": {"alignment": -4}
    }
}
