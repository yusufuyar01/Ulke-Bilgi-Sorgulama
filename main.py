
import requests

URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"


def ulke_sorgula(ulke_adi):
    try:
        response = requests.get(URL, timeout=20)
        response.raise_for_status()

        ulkeler = response.json()
        aranan = ulke_adi.casefold()

        ulke = None

        for item in ulkeler:
            isimler = [
                item.get("name", {}).get("common", ""),
                item.get("name", {}).get("official", "")
            ]

            isimler += [
                bilgi.get("common", "")
                for bilgi in item.get("translations", {}).values()
            ]

            if any(isim.casefold() == aranan for isim in isimler if isim):
                ulke = item
                break

        if ulke is None:
            print("Ülke bulunamadı.")
            return

        print("\n========== ÜLKE BİLGİLERİ ==========")
        print("Ülke:", ulke["name"]["common"])
        print("Resmi adı:", ulke["name"]["official"])
        print("Başkent:", ", ".join(ulke.get("capital", [])) or "Bilinmiyor")
        print("Bölge:", ulke.get("region", "Bilinmiyor"))
        print("Nüfus:", f"{ulke.get('population', 0):,}")

        print("\nPara birimleri:")
        for kod, bilgi in ulke.get("currencies", {}).items():
            print(f"{kod}: {bilgi['name']} ({bilgi.get('symbol', '')})")

        print("\nDiller:")
        for dil in ulke.get("languages", {}).values():
            print(dil)

        print("====================================")

    except requests.exceptions.RequestException as hata:
        print("Veriler alınamadı:", hata)


def main():
    while True:
        ulke_adi = input(
            "\nÜlke adını girin (Çıkış için q): "
        ).strip()

        if ulke_adi.casefold() == "q":
            print("Program kapatılıyor...")
            break

        if ulke_adi:
            ulke_sorgula(ulke_adi)
        else:
            print("Lütfen bir ülke adı girin.")


if __name__ == "__main__":
    main()
