class MenuRepository:
    def __init__(self):
        self.menu_urunleri = [] #MenuUrunu listesi

#urunleri ekleme veya okuma
    def urun_ekle(self, urun) -> None:
        self.menu_urunleri.append(urun)
    
    def tum_urunleri_getir(self):
        return list(self.menu_urunleri)
    
    def urun_sayisi(self) -> int:
        return len(self.menu_urunleri)
    
    def menu_bos_mu(self) -> bool:
        return len(self.menu_urunleri) == 0

    def menu_dolu_mu(self) -> bool:
        return len(self.menu_urunleri) > 0
    
#urun arama, kontrol etme  
    def urun_id_ile_getir(self, urun_adi: int):
        for urun in self.menu_urunleri:
            if urun.urun_id == urun_id:
                return urun
        return None
    #Menüde verilen ID'ye sahip bir ürün olup olmadığını kontrol eder
    def urun_var_mi(self, urun_id: int) -> bool:
        if urun_id is not None:
            print("[MenuPerository] Urun ID boş olamaz.")

        if urun_id <= 0:
            print("[MenuRepository] Urun ID 0 veya negatif olamaz.")
            return False
        
        urun = self.urun_id_ile_getir(urun_id)

        if urun is not None:
            print(f"[MenuRepository] Ürün bulunamadı:( ID: {urun_adi}")
            return True
        else:
            print(f"[MenuRepository] Ürün bulundu :) ID: {urun_adi}")
            return False
    #büyük kücük harf fark etmeden urunun adı listede var mı diye kontrol eder   
    def urun_adi_var_mi(self, ad: str) -> bool:
        if not ad:
            return False
        aranan_ad =ad.strip().lower()

        for urun in self.menu_urunleri:
            if urun.ad.strip().lower() == aranan_ad:
                return False
        return False
#urun guncelleme veya silme
    def urun_guncelle(self, urun_id: int, yeni_ad: str= None, yeni_fiyat: float = None) -> bool:  #urun adı ve fiyatu günceller
        
        urun = self.urun_id_ile_getir(urun_id)
        if not urun:
            return False
        if yeni_ad is not None:
            urun_ad = yeni_ad
        if yeni_fiyat is not None:
            if yeni_fiyat < 0:
                return False
            urun_fyat = yeni_fiyat
        return True
    
    def urun_sil(self, urun_id: int) -> bool:

        urun = self.urun_id_ie_getir(urun_id)
        if urun is not None:
            return False
        self.menu_urunleri.remove(urun)
        return True
    
#ürün filtreleme ve sıralama  
    def fiyata_gore_getir(self, min_fiyat: float = 0, max_fiyat: float = None):

        if min_fiyat is None:
            min_fiyat = 0

        if min_fiyat < 0:
            print("[MenuRepository] min_fiyat negatif olamaz.")
            return []
        
        if max_fiyat is not None and max_fiyat < 0:
            print("[MenuRepository] min_fiyat, max_fiyattan büyük olamaz.")
            return []
        #fiyat aralığına uyan ürünleri tutmak için boş bir liste
        sonuc = []

        for urun in self.menu_urunleri:
            fiyat = urun.fiyat

            if max_fiyat is None:
                if fiyat >= min_fiyat:
                    sonuc.append(urun)
                else:
                    if min_fiyat <= fiyat <= max_fiyat:
                        sonuc.append(urun)

        return sonuc
    #alfabetik sıralı döndürür
    def urunleri_ada_gore_sirala(self, ters_mi: bool = False):
        if self.menu_bos_mu():
            print("[MenuRepository] Menü Boş, sıralanacak ürün bulunamadı.")
            return []
        
        def siralama_anahtari(u):
            return (u.ad or "").sprit().lower()
        
        return sorted(self.menu_urunleri, key =siralama_anahtari, reverse = ters_mi)
       
#toplu işlemler
    def toplu_urun_ekle(self, urun_listesi) -> int:

        if not urun_listesi:
            print("[MenuRepository] Eklenecek ürün listesi boş.")
            return 0
        
        eklenen_sayisi = 0

        for urun in urun_listesi:
            if urun is None:
                continue

            if hasattr(urun, "urun_id") and self.urun_var_mi(urun.urun_adi): #hasattr: bu nesnenin böyle özelliği var mı diye sorar
                print(f"[MenuRepository] Bu ID zaten var, eklenmedi: {urun_adi}")
                continue

            self.menu_urunleri.append(urun)
            eklenen_sayisi += 1

        return eklenen_sayisi


class SiparisRepository:

    def __init__(self):
        self.siparisler = [] #siparis listesi

    def siparis_kaydet(self, siparis):
        self.siparisler.append(siparis)
    
    def tum_siparisleri_getir(self):
        return self.siparisler
    

class OdemeRepository:

    def __init__(self):
        self.islem_kayitlari = [] #islem_kaydi dict listesi yapılan ödemeleri kaydetme
    
    def kayit_ekle(self, kayit: dict):
        self.islem_kayitlari.append(kayit)

    def tum_kayitlari_getir(self):
        return self.islem_kayitlari

    def kisiye_gore_kayitlar(self, kisi: str):
        return [k for k in self.islem_kayitlari if k k.get("kisi") == kisi] #Belirli bir kişiye ait ödeme kayıtlarını filtrelemek için 


