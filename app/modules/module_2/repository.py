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


from datetime import datetime

class SiparisRepository:
    
    def __init__(self):
        self.siparisler = []   # Siparis nesneleri veya dict olabilir
        self._son_id = 0


    def _yeni_id_uret(self) -> int: #Her yeni siparişe otomatik ID vermek için.
        self._son_id += 1
        return self._son_id


    def siparis_ekle(self, siparis) -> int:
        """
        Yeni sipariş ekler.
        - siparis nesnesine siparis_id atar
        - siparisin tarihini yoksa atar
        - eklenen siparişin ID'sini döndürür
        """
        if siparis is None:
            print("[SiparisRepository] Boş sipariş eklenemez.")
            return -1

        # kişi bilgisi olmalı (bizim projede sipariş kime ait)
        if not hasattr(siparis, "kisi"):
            print("[SiparisRepository] Sipariş nesnesinde 'kisi' alanı yok.")
            return -1

        # id ver
        siparis_id = self._yeni_id_uret()
        siparis.siparis_id = siparis_id

        # tarih yoksa ekle
        if not hasattr(siparis, "tarih") or siparis.tarih is None:
            siparis.tarih = datetime.now()

        # durum yoksa default ver
        if not hasattr(siparis, "durum") or siparis.durum is None:
            siparis.durum = "olusturuldu"

        self.siparisler.append(siparis)
        print(f"[SiparisRepository] Sipariş eklendi. ID: {siparis_id} | Kişi: {siparis.kisi}")
        return siparis_id

    # ----------------- LİSTELEME -----------------

    def tum_siparisleri_getir(self):
        """
        Tüm siparişleri döndürür
        """
        return list(self.siparisler)

    def kisiye_gore_siparisleri_getir(self, kisi: str):
        """
        Belirli bir kişiye ait siparişleri döndürür
        """
        if kisi is None or len(kisi.strip()) == 0:
            return []

        kisi = kisi.strip()
        return [s for s in self.siparisler if getattr(s, "kisi", None) == kisi]

    def duruma_gore_siparisleri_getir(self, durum: str):
        """
        Siparişleri durumuna göre filtreler (olusturuldu/hazirlaniyor/teslim/iptal)
        """
        if durum is None or len(durum.strip()) == 0:
            return []

        durum = durum.strip().lower()
        return [s for s in self.siparisler if str(getattr(s, "durum", "")).lower() == durum]

    # ----------------- ARAMA -----------------

    def id_ile_siparis_getir(self, siparis_id: int):
        """
        ID ile sipariş bulur. Bulamazsa None döner.
        """
        if siparis_id is None or siparis_id <= 0:
            return None

        for s in self.siparisler:
            if getattr(s, "siparis_id", None) == siparis_id:
                return s
        return None

    def siparis_var_mi(self, siparis_id: int) -> bool:
        """
        ID'ye göre sipariş var mı kontrol eder
        """
        return self.id_ile_siparis_getir(siparis_id) is not None

    # ----------------- GÜNCELLEME -----------------

    def siparis_durumu_guncelle(self, siparis_id: int, yeni_durum: str) -> bool:
        """
        Siparişin durumunu günceller.
        Başarılıysa True, yoksa False
        """
        siparis = self.id_ile_siparis_getir(siparis_id)
        if siparis is None:
            print("[SiparisRepository] Sipariş bulunamadı.")
            return False

        if yeni_durum is None or len(yeni_durum.strip()) == 0:
            print("[SiparisRepository] Yeni durum boş olamaz.")
            return False

        siparis.durum = yeni_durum.strip().lower()
        print(f"[SiparisRepository] Sipariş durumu güncellendi. ID: {siparis_id} | Yeni Durum: {siparis.durum}")
        return True

    # ----------------- SİLME / İPTAL -----------------

    def siparis_sil(self, siparis_id: int) -> bool:
        """
        Siparişi listeden tamamen siler (çok kullanılmaz ama opsiyonel).
        """
        siparis = self.id_ile_siparis_getir(siparis_id)
        if siparis is None:
            return False

        self.siparisler.remove(siparis)
        return True

    def siparis_iptal_et(self, siparis_id: int) -> bool:
        """
        Siparişi silmek yerine iptal durumuna çeker (daha mantıklı).
        """
        return self.siparis_durumu_guncelle(siparis_id, "iptal")

    # ----------------- RAPORLAMA (Opsiyonel ama artı puan) -----------------

    def tarih_araligina_gore_getir(self, baslangic: datetime, bitis: datetime):
        """
        Belirli tarih aralığındaki siparişleri döndürür.
        """
        if baslangic is None or bitis is None:
            return []

        sonuc = []
        for s in self.siparisler:
            tarih = getattr(s, "tarih", None)
            if tarih is None:
                continue
            if baslangic <= tarih <= bitis:
                sonuc.append(s)

        return sonuc

    



class OdemeYontemiRepository:
    
    def __init__(self):
        self.odeme_yontemleri = [] # Tüm ödeme yöntemlerini burada tutuyoruz
        
        self._son_id = 0

    def _yeni_id_uret(self) -> int:
        self._son_id += 1
        return self._son_id

    def yontem_ekle(self, odeme_yontemi) -> int:
        
        if odeme_yontemi is None:
            print("[OdemeYontemiRepository] Boş ödeme yöntemi eklenemez.")
            return -1

        # Nesnenin üzerinde kişi bilgisi var mı? (yanlış nesne gelmesin)
        if not hasattr(odeme_yontemi, "kisi"):
            print("[OdemeYontemiRepository] Bu nesne ödeme yöntemi gibi görünmüyor (kisi yok).")
            return -1

        # ID veriyoruz
        yeni_id = self._yeni_id_uret()
        odeme_yontemi.yontem_id = yeni_id

        # Listeye ekliyoruz
        self.odeme_yontemleri.append(odeme_yontemi)

        print(f"[OdemeYontemiRepository] Ödeme yöntemi eklendi. ID: {yeni_id} | Kişi: {odeme_yontemi.kisi}")
        return yeni_id


    def tum_yontemleri_listele(self):
        return list(self.odeme_yontemleri)

    def kisiye_gore_yontemleri_listele(self, kisi: str):
        
        if kisi is None or len(kisi.strip()) == 0:
            print("[OdemeYontemiRepository] Kişi bilgisi boş olamaz.")
            return []

        kisi = kisi.strip()
        sonuc = []

        for y in self.odeme_yontemleri:
            if getattr(y, "kisi", None) == kisi:
                sonuc.append(y)

        return sonuc

    def kisi_yontem_sayisi(self, kisi: str) -> int:
        return len(self.kisiye_gore_yontemleri_listele(kisi))


    def id_ile_yontem_getir(self, yontem_id: int):
        
        if yontem_id is None or yontem_id <= 0:
            return None

        for y in self.odeme_yontemleri:
            if getattr(y, "yontem_id", None) == yontem_id:
                return y

        return None

    def yontem_var_mi(self, yontem_id: int) -> bool:
        yontem = self.id_ile_yontem_getir(yontem_id)
        return yontem is not None


    def yontem_sil(self, yontem_id: int) -> bool: #ID ile ödeme yöntemini siler. Silindiyse True, yoksa False döner.
        
        yontem = self.id_ile_yontem_getir(yontem_id)

        if yontem is None:
            print("[OdemeYontemiRepository] Silinecek yöntem bulunamadı.")
            return False

        self.odeme_yontemleri.remove(yontem)
        print(f"[OdemeYontemiRepository] Ödeme yöntemi silindi. ID: {yontem_id}")
        return True


    def odeme_tipine_gore_listele(self, odeme_tipi: str):
        
        if odeme_tipi is None or len(odeme_tipi.strip()) == 0:
            return []

        odeme_tipi = odeme_tipi.strip()
        sonuc = []

        for y in self.odeme_yontemleri:
            # bazı nesnelerde odeme_tipi metodu yoksa hata vermesin diye try
            try:
                if y.odeme_tipi() == odeme_tipi:
                    sonuc.append(y)
            except Exception:
                continue

        return sonuc

    def para_birimine_gore_listele(self, para_birimi: str): #Para birimine göre ödeme yöntemlerini listeler (TL / USD gibi).
    
        if para_birimi is None or len(para_birimi.strip()) == 0:
            return []

        para_birimi = para_birimi.strip().upper()
        sonuc = []

        for y in self.odeme_yontemleri:
            if getattr(y, "para_birimi", "").upper() == para_birimi:
                sonuc.append(y)

        return sonuc
  

