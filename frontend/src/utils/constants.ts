import { ShoppingListItem } from "./types";

const categories: string[] = [
    "fruits and vegetables",
    "meat",
    "diary",
    "dry goods",
    "alcohols",
    "medicine",
    "pet goods",
    "baby goods",
    "domestic detergents",
    "ready-cook meals",
    "hygiene",
    "coffee & tea",
    "frozen foods",
    "garden and tinkering",
    "bread",
    "preserves",
    "spices, sauces, additives",
    "fishes and seafood",
    "sweets and snacks",
    "fats",
    "water and drinks",
    "dried fruit and nuts",
    "fresh herbs",
    "canned food",
    "other"
];

const units: string[] = ["pcs", "pkgs", "kg", "g", "l", "ml"];

const defaultItem: ShoppingListItem = {
    id: -1,
    product: '',
    quantity: '',
    unit: '',
    category: '',
    note: '',
    completed: false
};

export { categories, units, defaultItem };
