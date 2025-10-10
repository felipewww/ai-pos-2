from models.delivery_point import DeliveryPoint

# todo
# cada veiculo só pode fazer 2 entregas prioritárias, pois entre elas vai entregar os comuns mais proximos
# e após elas entregará os remainings
points_oriente_priority = [
    # oriente
    DeliveryPoint(
        title="R. Joaquim de Paula, 200-320 - Cidade Morumbi",
        lat=-23.246790,
        lng=-45.900543,
        is_priority=True,
    ),
    DeliveryPoint(
        title="Praça Victor Hugo, 91-1 - Jardim Oriente",
        lat=-23.240570,
        lng=-45.900794,
        is_priority=True,
    ),
    DeliveryPoint(
        title="Rua Yoshikatsu Iida, 12-344 - Res. Sol Nascente",
        lat=-23.245235,
        lng=-45.892470,
        is_priority=True,
    ),
    DeliveryPoint(
        title="R. George Washington, 130-218 - Jardim Oriente",
        lat=-23.240570,
        lng=-45.899422,
        is_priority=True,
    ),

    #satelite
    DeliveryPoint(
        title="rua pedro tursi, 301",
        lat=-23.222092,
        lng=-45.885470,
        is_priority=True,
    ),
    DeliveryPoint(
        title="rua nazaré, 829",
        lat=-23.232030,
        lng=-45.889525,
        is_priority=True,
    ),
    DeliveryPoint(
        title="R. Divinópolis, 2-196 - Bosque dos Eucaliptos",
        lat=-23.237525,
        lng=-45.890879,
        is_priority=True,
    ),
    DeliveryPoint(
        title="R. Ipiau, 162-408 - Jardim Satélite",
        lat=-23.230846,
        lng=-45.888061,
        is_priority=True,
    ),
]

points_oriente = [
    # Oriente
    DeliveryPoint(
        title="R. das Chácaras, 374-428 - Jardim Oriente",
        lat=-23.242545,
        lng=-45.893361,
    ),
    DeliveryPoint(
        title="R. Osaka, 158-222 - Jardim Oriente",
        lat=-23.243112,
        lng=-45.895900,
    ),
    DeliveryPoint(
        title="R. Fusanobu Yokota, 126-206 - Jardim Terras do Sul",
        lat=-23.246538,
        lng=-45.896060,
    ),
    DeliveryPoint(
        title="R. Guilherme Marconi, 50-110 - Jardim Oriente",
        lat=-23.242839,
        lng=-45.902075,
    ),
    DeliveryPoint(
        title="R. Marcelo Carlos Pereira, 68-128 - Cidade Morumbi",
        lat=-23.245886,
        lng=-45.899743,
    ),
    DeliveryPoint(
        title="R. Benedito Batista Campos, 79-45 - Cidade Morumbi",
        lat=-23.248008,
        lng=-45.904042,
    ),
    DeliveryPoint(
        title="R. Lenine Rebelo, 115-1 - Jardim Sul",
        lat=-23.248786,
        lng=-45.893156,
    ),
    DeliveryPoint(
        title="R. Sol Nascente, 30-236 - Res. Sol Nascente",
        lat=-23.245046,
        lng=-45.897090,
    ),


    # Satelite
    DeliveryPoint(
        title="rua Polar, 100",
        lat=-23.220456,
        lng=-45.893967,
    ),
    DeliveryPoint(
        title="rua aldebaram, 2",
        lat=-23.225819,
        lng=-45.888817,
    ),

    DeliveryPoint(
        title="rua scorpius, 800",
        lat=-23.225839,
        lng=-45.894160,
    ),
    DeliveryPoint(
        title="rua joao de paula, 189",
        lat=-23.230275,
        lng=-45.895791,
    ),
    DeliveryPoint(
        title="rua tijuca, 442",
        lat=-23.228829,
        lng=-45.881087,
    ),
    DeliveryPoint(
        title="R. San Marino, 81-169 - Jardim America",
        lat=-23.231288,
        lng=-45.895774,
    ),
    DeliveryPoint(
        title="R. Osvaldo Faria, 365-191 - Jardim Satélite",
        lat=-23.226893,
        lng=-45.879383,
    ),
    DeliveryPoint(
        title="R. Pleiades, 111-1 - Jardim Satélite",
        lat=-23.221031,
        lng=-45.895959,
    ),
    DeliveryPoint(
        title="R. Maranduba, 2-156 - Jardim Satélite",
        lat=-23.232992,
        lng=-45.881497,
    ),

    DeliveryPoint(
        title="R. Vírgem, 377-175 - Jardim Satélite",
        lat=-23.225325,
        lng=-45.886689,
    ),
    DeliveryPoint(
        title="R. Crater, 437-231 - Jardim Satélite",
        lat=-23.227301,
        lng=-45.891361,
    ),
    DeliveryPoint(
        title="R. Cisne, 179-1 - Jardim Satélite",
        lat=-23.221202,
        lng=-45.891324,
    ),
    DeliveryPoint(
        title="R. Newton Viêira Novaes, 2-170 - Bosque dos Eucaliptos",
        lat=-23.241682,
        lng=-45.882831,
    ),
]
