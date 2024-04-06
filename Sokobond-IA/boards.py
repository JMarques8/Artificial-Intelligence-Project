# This is used to map the "Atom Player" to the respective color and max_connection(bonds)
from constants import *

ATOM_MAPPING = {
    0: {
        'X' : [RED,1]
    },
    1: {
        'X' : [RED,1]
    },
    2: {
        'X' : [RED,1]
    },
    3: {
        'X' : [BLUE,2]
    },
    4: {
        'X' : [GREEN,3]
    },
    5: {
        'X' : [RED,1]
    },
    6: {
        'X' : [GREEN,3]
    },
    7: {
        'X' : [DARK_YELLOW,4]
    },
    8: {
        'X' : [GREEN,3]
    },
    9: {
        'X' : [DARK_YELLOW,4]
    },
    10: {
        'X' : [BLUE,2]
    }
}

BOARDS = {
    1: [
    "....................",
    "....................",
    "......######.........",
    "......#GGGH#.........",
    "......#GOGG#.........",
    "......#XGGG#.........", 
    "......######.........",
    "...................."  
    ],   

    10: [
    "....................",
    "....................",
    ".........######.....",
    ".........#GGGG#.....",
    "......####GGGG#.....",
    "......#GGGG#HG#.....",
    "......#GGGO#GG#.....",
    "......#GGGGGGG#.....",
    "......#GXGGGGG#.....",
    "......#GGGG####.....", 
    "......######........",
    "...................."  
    ],   

    2: [
    "....................",
    "....................",
    "....................",
    ".......######.......",
    ".......#HGGO#.......",
    ".......#GGGG#.......",
    ".......#XG###.......",
    ".......####.........",
    "....................",
    "....................",
    "....................",
    "....................",
    ],

    3: [
    "....................",
    "....................",
    "....................",
    "........#####.......",
    "......###GGG##......",
    "......#XGHGHG#......",
    "......###GGGG#......",
    "........#####.......",
    "....................",
    "....................",
    "....................",
    "....................",
    ],
    
    4: [
    "....................",
    "....................",
    "....................",
    "......#######.......",
    "......#GHGXG#.......",
    "......#GGGGG#.......",
    "......#GHGHG#.......",
    "......#######.......",
    "....................",
    "....................",
    "....................",
    "....................",   
    ],

    5: [
    "....................",
    "....................",
    "....................",
    "......#######.......",
    "......#GGOGG#.......",
    "......#GG#GG#.......",
    "......#GX#HG#.......",
    "......#GG#GG#.......",
    "......#GGOGG#.......",
    "......#######.......",
    "....................",
    "....................",   
    ],

    6: [
    "....................",
    "....................",
    "....................",
    "......#######.......",
    "......#GGGGG#.......",
    "......#GGGGG#.......",
    "......#H#H#H#.......",
    "......#GGGGG#.......",
    "......#GGXGG#.......",
    "......#######.......",
    "....................",
    "....................",   
    ],

    7:[
    "....................",
    "....................",
    "....................",
    ".......#######......",
    "......#GHGGGH##.....",
    "......#GGGXGGG#.....",
    "......##HGGGHG#.....",
    ".......#######......",
    "....................",
    "....................",
    "....................",
    "....................",   
    ],

    8:[
    "....................",
    "....................",
    "....................",
    "......########......",
    "......#GGGGGG#......",
    "......#GGGHGG#......",
    "......#OGHGGX#......",
    "......#GGGHGG#......",
    "......#GGGGGG#......",
    "......########......",
    "....................",
    "....................",   
    ],

    8:[
    "....................",
    "....................",
    "....................",
    "......########......",
    "......#GGGGGG#......",
    "......#GGGHGG#......",
    "......#OGHGGX#......",
    "......#GGGHGG#......",
    "......#GGGGGG#......",
    "......########......",
    "....................",
    "....................",   
    ],

    9:[
    "....................",
    "........###.........",
    ".......##X##........",
    "......##GGG##.......",
    ".....##GHGHG##......",
    ".....#GGGGGGG#......",
    ".....##GHGHG##......",
    "......##GGG##.......",
    ".......##G##........",
    "........###.........",
    "....................",
    "....................",   
    ],

    11:[
    "....................",
    "....................",
    "....................",
    "......#########.....",
    "......#GGGGGGG#.....",
    "......#GGHGHGG#.....",
    "......#GXGGGCG#.....",
    "......#GGHGHGG#.....",
    "......#GGGGGGG#.....",
    "......#########.....",
    "....................",
    "....................",   
    ]
}