from django.db import models


class ItemCategory(models.TextChoices):
    FRUITS_VEGETABLES = "fruits and vegetables"
    MEAT = "meat"
    DAIRY = "dairy"
    DRY_GOODS = "dry goods"
    ALCOHOLS = "alcohols"
    MEDICINE = "medicine"
    PET_GOODS = "pet goods"
    BABY_GOODS = "baby goods"
    DOMESTIC_DETERGENTS = "domestic detergents"
    READY_COOK_MEALS = "ready-cook meals"
    HYGIENE = "hygiene"
    COFFEE_TEA = "coffee & tea"
    FROZEN_FOODS = "frozen foods"
    GARDEN_TINKER = "garden and tinkering"
    BREAD = "bread"
    PRESERVES = "preserves"
    SPICES = "spices, sauces, additives"
    FISH = "fishes and seafood"
    SWEETS = "sweets and snacks"
    FATS = "fats"
    DRINKS = "water and drinks"
    NUTS = "dried fruit and nuts"
    HERBS = "fresh herbs"
    CANS = "canned food"
    OTHER = "other"


class ItemUnit(models.TextChoices):
    PIECES = "pcs"
    PACKAGES = "pkgs"
    KILOGRAM = "kg"
    GRAM = "g"
    LITER = "l"
    MILLILITER = "ml"
