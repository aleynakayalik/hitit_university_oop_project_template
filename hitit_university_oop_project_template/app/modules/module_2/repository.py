from __future__ import annotations
from typing import Any, Dict

#Kullanıcıların ödeme yöntemlerini veritabenı varmış gibi RAM de saklar
class InMemoryPaymentRepository:
    def __init__(self) -> None:
        self.__odeme_yontemleri: Dict[int, Any] = {}
        self.__siradaki_id: int = 1  #repo otomatik id versin diye sayaç

    #ödeme yönteminin sahibini bulur
    def __odeme_sahibi(self, odeme_yontemi) -> str |  None:
        if odeme_yontemi is None:
            return None
        #base classdaki get_owner()
        get_owner = getattr(odeme_yontemi, "get_owner", None)
        if callable(get_owner):
            try:
                sahip = get_owner()
                if isinstance(sahip, str) and sahip.strip() != "":
                    return sahip.strip()
            except Exception:
                pass

        #direkt owner attribute u
        sahip = getattr(odeme_yontemi, "owner", None)
        if isinstance(sahip, str) and sahip.strip() != "":
            return sahip.strip()
        
        return None
    #ödeme yönteminin idsini döndürür yoksa none
    def __odeme_id(self, odeme_yontemi) -> int | None:
        odeme_id = getattr(odeme_yontemi, "id", None)
        if isinstance(odeme_id, int):
            return odeme_id
        return None
    #ödeme yöntemini repositorye ekler
    def ekle(self, odeme_yontemi) -> int:
        if odeme_yontemi is None:
            raise ValueError("ödeme yöntemi boş olamaz.")
        
        sahip = self.__odeme_sahibi(odeme_yontemi)
        if sahip is None:
            raise ValueError("ödeme yönteminin bir sahibi olmalıdır.")
        
        odeme_id = self.__odeme_id(odeme_yontemi)

        #id yoksa otamatik ver
        if odeme_id is None:
            odeme_id = self.__siradaki_id
            self.__siradaki_id += 1
            try:
                setattr(odeme_yontemi,"id", odeme_id)
            except Exception:
                pass
        
        if odeme_id <= 0:
            raise ValueError("ödeme yöntemi id'si pozitif olmalıdır.")
        
        if odeme_id in self.__odeme_yontemleri:
            raise ValueError("bu id ile kayıtlı bir ödeme yöntemi zaten var")
        
        self.__odeme_yontemleri[odeme_id] = odeme_yontemi
        return odeme_id
    
    #sistemdeki tüm ödeme yöntemlerini döndürür
    def tumunu_listele(self) -> list:
        return list(self.__odeme_yontemleri.values())
    
    #belirli bir kullanıcıya ait ödeme yöntemlerini döndürür
    def sahibine_gore_listele(self, sahip: str) -> list:
        if not isinstance(sahip, str) or sahip.strip() == "":
            raise ValueError("sahip bilgisi boş olamaz")

        sahip = sahip.strip()
        sonuc = []

        for odeme in self.__odeme_yontemleri.values():
            if self.__odeme_sahibi(odeme) == sahip:
                sonuc.append(odeme)

        return sonuc
    
    #verilen id ye sahip ödeme yöntemini döndürür
    def id_ile_bul(self, id: int):

        if not isinstance(id, int) or id <= 0:
            raise ValueError("id pozitif bir sayı olmalıdır.")

        return self.__odeme_yontemleri.get(id)
    

#yapılan ödeme işlemlerini bellekte saklayan repository
class InMemoryTransactionRepository:

    def __init__(self) -> None:
        self.__islemler: dict[int,Any] = {}
        self.__siradaki_id: int = 1   # otomatik id vermek için sayaç

    #işlem sahini döndürür
    def __islem_sahibi(self, islem) -> str | None:
        sahip = getattr(islem, "owner", None)
        if isinstance(sahip, str) and sahip.strip() != "":
            return sahip.strip()
        return None
    
    #işlem durumu(BAŞARILI/BAŞARISIZ) döndürür
    def __islem_durumu(self, islem) -> str | None:
        durum = getattr(islem, "status", None)
        if isinstance(durum, str) and durum.strip() != "":
            return durum.strip().upper()
        return None
    
    #yeni bir ödeme işlemini repositorye ekler
    def ekle(self, islem) -> int:
        if islem is None:
            raise ValueError("işlem boş olamaz.")
        islem_id = getattr(islem, "id", None)

        #id yoksa otomatik ver
        if islem_id is None:
            islem_id = self.__siradaki_id
            self.__siradaki_id += 1
            try:
                setattr(islem, "id", islem_id)
            except Exception:
                pass

        if not isinstance(islem_id, int) or islem_id <= 0:
            raise ValueError("İşlem id'si pozitif bir sayı olmalıdır.")

        if islem_id in self.__islemler:
            raise ValueError("Bu id ile kayıtlı bir işlem zaten var.")

        if self.__islem_sahibi(islem) is None:
            raise ValueError("İşlemin bir sahibi (owner) olmalıdır.")

        self.__islemler[islem_id] = islem
        return islem_id
    #tüm işlemleri döndürür
    def tumunu_listele(self) -> list:
        return list(self.__islemler.values())
    #Belirli bir kullanıcıya ait işlemleri döndürür.
    def sahibine_gore_listele(self, sahip: str) -> list:
        
        if not isinstance(sahip, str) or sahip.strip() == "":
            raise ValueError("Sahip bilgisi boş olamaz.")

        sahip = sahip.strip()
        sonuc = []

        for islem in self.__islemler.values():
            if self.__islem_sahibi(islem) == sahip:
                sonuc.append(islem)

        return sonuc
    #İşlem durumuna(BASARILI / BASARISIZ göre filtreleme yapar.
    def duruma_gore_listele(self, durum: str) -> list:
      
        if not isinstance(durum, str) or durum.strip() == "":
            raise ValueError("Durum bilgisi boş olamaz.")

        durum = durum.strip().upper()
        sonuc = []

        for islem in self.__islemler.values():
            if self.__islem_durumu(islem) == durum:
                sonuc.append(islem)

        return sonuc
             


# Yemekhane menüsündeki ürünleri bellekte tutar.
# Ürünlerin hangi günlerde çıkacağını (1-5) destekler.
class InMemoryMenuRepository:
    def __init__(self) -> None:
        self.__urunler: dict[int, object] = {}
        self.__siradaki_id: int = 1  # otomatik id için sayaç

    # Ürün aktif mi kontrolü.
    def __aktif_mi(self, urun) -> bool:
        deger = getattr(urun, "available", None)
        if deger is None:
            deger = getattr(urun, "aktif_mi", None)

        return bool(deger) if isinstance(deger, bool) else False

    # Menü ürününü repository'e ekler.
    def ekle(self, menu_urunu) -> int:
        if menu_urunu is None:
            raise ValueError("Menü ürünü boş olamaz.")

        urun_id = getattr(menu_urunu, "id", None)

        # id yoksa otomatik ver
        if urun_id is None:
            urun_id = self.__siradaki_id
            self.__siradaki_id += 1
            try:
                setattr(menu_urunu, "id", urun_id)
            except Exception:
                pass

        if not isinstance(urun_id, int) or urun_id <= 0:
            raise ValueError("Menü ürünü id'si pozitif int olmalıdır.")

        if urun_id in self.__urunler:
            raise ValueError("Bu id ile kayıtlı bir menü ürünü zaten var.")

        self.__urunler[urun_id] = menu_urunu
        return urun_id

    # ID ile menü ürününü bulur. Yoksa None döner.
    def id_ile_getir(self, id: int):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id pozitif int olmalıdır.")
        return self.__urunler.get(id)

    # Menüdeki tüm ürünleri döndürür.
    def tumunu_listele(self) -> list:
        return list(self.__urunler.values())

    # Sadece aktif olan ürünleri döndürür.
    def aktifleri_listele(self) -> list:
        sonuc = []
        for urun in self.__urunler.values():
            if self.__aktif_mi(urun):
                sonuc.append(urun)
        return sonuc

    # Tek fonksiyonla listeleme isteyen servisler için 
    def listele(self, sadece_aktif: bool = True) -> list:
        return self.aktifleri_listele() if sadece_aktif else self.tumunu_listele()

    # Kategoriye göre filtreler (örn: 'ana yemek', 'içecek').
    def kategoriye_gore_listele(self, kategori: str) -> list:
        if not isinstance(kategori, str) or kategori.strip() == "":
            raise ValueError("Kategori boş olamaz.")

        kategori = kategori.strip().lower()
        sonuc = []

        for urun in self.__urunler.values():
            urun_kat = getattr(urun, "category", None)
            if isinstance(urun_kat, str) and urun_kat.strip().lower() == kategori:
                sonuc.append(urun)

        return sonuc

    # Haftanın gününe göre ürünleri döndürür.
    def gune_gore_listele(self, gun: int, sadece_aktif: bool = True) -> list:
        if not isinstance(gun, int) or gun < 1 or gun > 5:
            raise ValueError("Gün 1-5 arasında olmalıdır.")

        sonuc = []

        for urun in self.__urunler.values():
            # available_days listesi var mı?
            gunler = getattr(urun, "available_days", None)

            eslesti = False
            if isinstance(gunler, list) and all(isinstance(d, int) for d in gunler):
                eslesti = gun in gunler
            else:
                # tek gün alanı (day / available_day)
                tek_gun = getattr(urun, "day", None)
                if tek_gun is None:
                    tek_gun = getattr(urun, "available_day", None)
                if isinstance(tek_gun, int):
                    eslesti = (tek_gun == gun)

            if not eslesti:
                continue

            if sadece_aktif and not self.__aktif_mi(urun):
                continue

            sonuc.append(urun)

        return sonuc




