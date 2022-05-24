import bottle
import model


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
    return bottle.template("index")


@bottle.post("/igra/")
def nova_igra():
    nov_id = vislice.nova_igra()
    return bottle.redirect(f"/igra/{nov_id}")


@bottle.get("/igra/<id_igre:int>")
def pokazi_igro(id_igre):
    return bottle.template("igra", id_igre=id_igre, igra=vislice.igre[id_igre][0], tipkovnica=TIPKOVNICA)


def preveri_vnos(crka):
    return len(crka) == 1 and ("A" <= crka <= "Z" or crka in "ČŽŠ")


@bottle.post('/igra/<id_igre:int>')
def ugibaj(id_igre):
    crka = bottle.request.forms.getunicode('crka').upper()
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


bottle.run(reloader=True, debug=True)
