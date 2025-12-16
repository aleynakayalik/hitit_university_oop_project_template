
#
class MenuUrunu:
    def __init__(self, urun_id: int, ad: str, fiyat: float):
        self.urun_id = urun_id
        self.ad = ad
        self.fiyat = fiyat

class SepetKlemi:
    def __init__(self, urun: MenuUrunu, adet: int):
        self.urun = urun
        self.adet = adet

    def ara_toplam(self) -> float:
        return self.urun.fiyat * self.adet
    

class Siparis:
    def __init__(self, siparis_id: int, kisi: str):
        self.siparis_id = siparis_id
        self.kisi = kisi
        self.kalemler = []      # SepetKalemi listesi
        self.durum = "OLUSTURULDU"

    def urun_ekle(self, kalem: SepetKalemi) -> None:
        self.kalemler.append(kalem)
    def toplam_tutar(self) -> float:
        toplam = 0
        for kalem in self.kalemler:
            toplam += kalem.ara_toplam()
        return toplam