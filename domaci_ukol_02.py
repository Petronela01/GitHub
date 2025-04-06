import requests
import json

#Cast 1 vyhledani informaci na zaklade ICO 
zadane_ico = input("Zadej ICO:")
web_adresa = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/" + zadane_ico
response = requests.get(web_adresa) 
firma = response.json()
#print(firma)
obchodni_nazev = firma["obchodniJmeno"]
adresa = firma["sidlo"]["textovaAdresa"]
print(f"Pro ICO {zadane_ico} se jedna o {obchodni_nazev} se sidlem na adrese {adresa}.")

#Cast 2 vyhledani na zaklade nazvu, ci casti nazvu + Bonus dodani pravni formy 

nazev_subjektu = input("Zadej nazev subjektu: ")
web_adresa_vyhledat = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
data = '{"obchodniJmeno": "' + nazev_subjektu + '"}'
res = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat", headers=headers, data=data)
subjekt = res.json()
pocet_subjektu = subjekt["pocetCelkem"]
print(f"Nalezenych subjektu:{pocet_subjektu}")

ekonomicke_subjekty = subjekt["ekonomickeSubjekty"]
seznam_hledanych_subjektu = []
for line in ekonomicke_subjekty:
    seznam_hledanych_subjektu.append([line["ico"], line["obchodniJmeno"], line["pravniForma"]])

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
data = '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'
res = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat", headers=headers, data=data)
polozkyCiselniku = res.json()

def find_legal_form( kod: str, polozkyCiselniku) -> str:
     for polozka_ciselniku in polozkyCiselniku["ciselniky"][0]["polozkyCiselniku"]:
         if polozka_ciselniku["kod"] == kod:
             return polozka_ciselniku["nazev"][0]["nazev"]

for item in seznam_hledanych_subjektu:
    ico = item[0]
    nazev = item[1]
    pravni_forma = item[2]
    print(ico + ', ' + nazev + ', ' + find_legal_form(pravni_forma,polozkyCiselniku))
