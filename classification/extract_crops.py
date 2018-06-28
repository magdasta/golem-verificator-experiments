import optical_comparison.should_accept as should_accept

ok_thresholds = {
    "atom" : 1401,
    "barcelona" : 5125,
    "breakfast_room" : 3025,
    "bunkbed" : 6025,
    "car" : 1801,
    "cat" : 3825,
    "eco_light_bulb" : 1401,
    "french_woman" : 201,
    "glass" : 2900,
    "glass_material" : 4925,
    "habitacion" : 2825,
    "head" : 125,
    "interior" : 1001,
    "metal" : 425,
    "mug" : 3825,
    "office" : 3825,
    "plushy" : 4225,
    "ring" : 5725,
    "rocks" : 401,
    "sea" : 825,
    "shark" : 1201,
    "toughship" : 3225,
    "tree" : 425
}

not_ok_thresholds = {
    "atom" : 601,
    "barcelona" : 725,
    "breakfast_room" : 825,
    "bunkbed" : 1825,
    "car" : 401,
    "cat" : 1125,
    "eco_light_bulb" : 601,
    "french_woman" : 1,
    "glass" : 800,
    "glass_material" : 1925,
    "habitacion" : 1325,
    "head" : 85,
    "interior" : 401,
    "metal" : 25,
    "mug" : 1125,
    "office" : 1425,
    "plushy" : 1125,
    "ring" : 3125,
    "rocks" : 1,
    "sea" : 25,
    "shark" : 601,
    "toughship" : 725,
    "tree" : 25
}

