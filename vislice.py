import bottle
import model
import sys
import os


PISKOT_ZADNJA_IGRA = "zadnjaigra"
ZADNJA_IGRA_KODA = "blazno skrivna koda"

TIPKOVNICA = [
    "QWERTZUIOPŠ",
    "ASDFGHJKLČŽ",
    "YXCVBNM"
]

vislice = model.Vislice()


@bottle.get("/img/<file>")
def staticne_slike(file):
    return bottle.static_file(file, root="img")


@bottle.get("/favicon.ico")
def favicon():
    """
    Poskrbimo za ikonico, ki se pokaže v brskalniku v zavihku levo od imena.
    """
    return bottle.static_file("favicon.ico", root="img")


@bottle.get("/oblikovanje/<file>")
def staticni_css(file):
    return bottle.static_file(file, root="oblikovanje")


@bottle.get("/")
def osnovno():
    ime_piskota = "povratek"
    ja = "ja"
    if bottle.request.get_cookie(ime_piskota) == ja:
        pozdrav = "Me veseli, da se spet srečava!"
    else:
        # shranimo piskotek
        bottle.response.set_cookie(ime_piskota, ja)
        pozdrav = "Živjo, hitro odigraj svojo prvo igro :)"
    return bottle.template("index", pozdrav=pozdrav)


# @bottle.post("/igra/")
# def nova_igra():
#     nov_id = vislice.nova_igra()
#     return bottle.redirect(f"/igra/{nov_id}")


# @bottle.post("/igra/")
# @bottle.get("/igra/")
@bottle.route("/igra/", method=["GET", "POST"])
def trenutna_igra():
    id_igre = int(bottle.request.get_cookie(PISKOT_ZADNJA_IGRA, secret=ZADNJA_IGRA_KODA))
    print("ID IGRE: ", id_igre)
    crka = bottle.request.forms.crka.upper()  # avtomatsko odkorida v unicode
    if crka:
        if preveri_vnos(crka):
            vislice.ugibaj(id_igre, crka)
        else:
            return f"<p>To ni dovoljena črka: {crka}</p>"
    igra = vislice.igre[id_igre][0]
    return bottle.template("igra", igra=igra, tipkovnica=TIPKOVNICA)


# @bottle.post("/nova_igra/")
# @bottle.get("/nova_igra/")
@bottle.route("/nova_igra/", method=["GET", "POST"])
def nova_igra_s_piskotki():
    nov_id = vislice.nova_igra()
    bottle.response.set_cookie(PISKOT_ZADNJA_IGRA, str(nov_id), path="/", secret=ZADNJA_IGRA_KODA)
    return bottle.redirect("/igra/")


@bottle.get("/igra/<id_igre:int>")
def pokazi_igro(id_igre):
    return bottle.template("igra", id_igre=id_igre, igra=vislice.igre[id_igre][0], tipkovnica=TIPKOVNICA)


def preveri_vnos(crka):
    return len(crka) == 1 and ("A" <= crka <= "Z" or crka in "ČŽŠ")


@bottle.post('/igra/<id_igre:int>')
def ugibaj(id_igre):
    # Namesto
    # crka = bottle.request.forms.getunicode('crka').upper()
    # raje preprosto napisemo
    crka = bottle.request.forms.crka.upper()  # avtomatsko odkorida v unicode
    if preveri_vnos(crka):
        vislice.ugibaj(id_igre, crka)
        return pokazi_igro(id_igre)
    else:
        return f"<p>To ni dovoljena črka: {crka}</p>"


# @bottle.get("/pretekle_igre/")
@bottle.post("/pretekle_igre/")
def pokazi_pretekle_igre():
    koncane = []
    for id_igre, (_, status) in vislice.igre.items():
        if status in [model.ZMAGA, model.PORAZ]:
            koncane.append(id_igre)
    return bottle.template("pretekle_igre", koncane_igre=koncane)


if sys.argv[1] == "local":
    bottle.run(host='localhost', port=8080, debug=True)
else:
    bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
