import matplotlib.pyplot as plt

def aylik_enflasyon_grafik(data, year):
    aylar = [row[0] for row in data]
    degerler = [row[1] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(aylar, degerler, marker='o')
    plt.title(f"{year} Aylık Enflasyon Oranları")
    plt.xlabel("Ay")
    plt.ylabel("Enflasyon (%)")
    plt.grid(True)

    dosya_adi = f"enflasyon_{year}.png"
    plt.savefig(dosya_adi)
    plt.close()

    return dosya_adi
