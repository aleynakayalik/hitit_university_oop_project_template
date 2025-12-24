
from __future__ import annotations
from typing import Any, Dict, Optional

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
    
    def kullaniciya_gore_listele(self, owner: str) -> list:
        return self.sahibine_gore_listele(owner)

    def list_by_owner(self, owner: str) -> list:
        return self.sahibine_gore_listele(owner)

    def list_all(self) -> list:
        return self.tumunu_listele()

    def id_ile_getir(self, id: int):
        return self.id_ile_bul(id)

    def get_by_id(self, id: int):
        return self.id_ile_bul(id)
    

#yapılan ödeme işlemlerini bellekte saklayan repository
class InMemoryTransactionRepository:

    def __init__(self) -> None:
        self.__islemler: dict[int,Any] = {}
        self.__siradaki_id: int = 1   # otomatik id vermek için sayaç

    #işlem sahini döndürür
    def __islem_sahibi(self, islem) -> str | None:
        get_owner = getattr(islem, "get_owner", None)
        if callable(get_owner):
            try:
                s = get_owner()
                return s.strip() if isinstance(s, str) and s.strip() else None
            except Exception:
                return None
        return None

    #işlem durumu(BAŞARILI/BAŞARISIZ) döndürür
    def __islem_durumu(self, islem) -> str | None:
        get_status = getattr(islem, "get_status", None)
        if callable(get_status):
            try:
                d = get_status()
                return d.strip().upper() if isinstance(d, str) and d.strip() else None
            except Exception:
                return None
        return None
    
    #yeni bir ödeme işlemini repositorye ekler
    def ekle(self, islem) -> int:
        if islem is None:
            raise ValueError("işlem boş olamaz.")
        get_id = getattr(islem, "get_id", None)
        if callable(get_id):
            try:
                islem_id = get_id()
            except Exception:
                islem_id = None
        else:
            islem_id = getattr(islem, "id", None)


        # id yoksa otomatik ver
        if islem_id is None or (isinstance(islem_id, int) and islem_id == 0):
            islem_id = self.__siradaki_id
            self.__siradaki_id += 1

            set_id = getattr(islem, "set_id", None)
            if callable(set_id):
                set_id(islem_id)
            else:
                setattr(islem, "id", islem_id)

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
    
    #Servis uyumu için ALIAS metotlar

    def kullaniciya_gore_listele(self, owner: str) -> list:
        return self.sahibine_gore_listele(owner)

    def list_by_owner(self, owner: str) -> list:
        return self.sahibine_gore_listele(owner)

    def list_all(self) -> list:
        return self.tumunu_listele()

    def list_by_status(self, status: str) -> list:
        return self.duruma_gore_listele(status)



# Yemekhane menüsündeki ürünleri bellekte tutar.
# Ürünlerin hangi günlerde çıkacağını (1-5) destekler.
class InMemoryMenuRepository:
    def __init__(self) -> None:
        self.__urunler: dict[int, object] = {}
        self.__siradaki_id: int = 1  # otomatik id için sayaç

    # Ürün aktif mi kontrolü.
    def __aktif_mi(self, urun) -> bool:
        get_av = getattr(urun, "get_is_available", None) ## MenuItem için doğru yol: getter
        if callable(get_av):
            try:
                return bool(get_av())
            except Exception:
                return False
    # Getter yoksa (başka objeler için) fallback
        deger = getattr(urun, "available", None)
        if isinstance(deger, bool):
            return deger
        deger = getattr(urun, "aktif_mi", None)
        if isinstance(deger, bool):
            return deger

        return False

    # Menü ürününü repository'e ekler.
    def ekle(self, menu_urunu) -> int:
        if menu_urunu is None:
            raise ValueError("Menü ürünü boş olamaz.")

        urun_id = getattr(menu_urunu, "id", None)

        # id yoksa otomatik ver
        if urun_id is None:
            urun_id = self.__siradaki_id
            self.__siradaki_id += 1
            set_id = getattr(menu_urunu, "set_id", None)
            if callable(set_id):
                try:
                    set_id(urun_id)
                except Exception:
                    try:
                        setattr(menu_urunu, "id", urun_id)
                    except Exception:
                        pass
            else:
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
    #test ile bağladım
    def add(self, item):
        return self.ekle(item)   


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
            get_cat = getattr(urun, "get_category", None)
            if callable(get_cat):
                urun_kat = get_cat()
            else:
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
            gunler = None
            get_days = getattr(urun, "get_available_days", None)
            if callable(get_days):
                try:
                    gunler = get_days()
                except Exception:
                    gunler = None
            else:
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
    
    def id_ile_getir(self, urun_id: int):
        for item in self.tumunu_listele():
            if item.get_id() == urun_id:
                return item
        return None

    def sil(self, urun_id: int) -> bool:
        # A) liste ise:
        if hasattr(self, "_items") and isinstance(self._items, list):
            once = len(self._items)
            self._items = [x for x in self._items if x.get_id() != urun_id]
            return len(self._items) != once

        # B) dict ise:
        if hasattr(self, "_items") and isinstance(self._items, dict):
            return self._items.pop(urun_id, None) is not None

        raise RuntimeError("Repo iç yapısı bulunamadı. _items list/dict değil.")

    def aktif_pasif_yap(self, urun_id: int, aktif: bool) -> bool:
        item = self.id_ile_getir(urun_id)
        if item is None:
            return False
        item.set_active(aktif)          
        return True

    def fiyat_guncelle(self, urun_id: int, yeni_fiyat: float) -> bool:
        item = self.id_ile_getir(urun_id)
        if item is None:
            return False
        item.set_price(yeni_fiyat)     
        return True
    



# Siparişleri (Order) veritabanı varmış gibi RAM'de tutan repository.
class InMemoryOrderRepository:
    # Repo içindeki siparişleri ve otomatik id sayacını hazırlar.
    def __init__(self) -> None:
        self.__siparisler: Dict[int, Any] = {}
        self.__siradaki_id: int = 1

    # Repo içindeki siparişten güvenli şekilde id çekmeye çalışır.
    def __siparis_id(self, siparis) -> Optional[int]:
        if siparis is None:
            return None

        get_id = getattr(siparis, "get_id", None)
        if callable(get_id):
            try:
                val = get_id()
                if isinstance(val, int):
                    return val
            except Exception:
                pass

        val = getattr(siparis, "id", None)
        return val if isinstance(val, int) else None

    # Repo içindeki siparişten güvenli şekilde owner çekmeye çalışır.
    def __siparis_sahibi(self, siparis) -> Optional[str]:
        if siparis is None:
            return None

        get_owner = getattr(siparis, "get_owner", None)
        if callable(get_owner):
            try:
                s = get_owner()
                if isinstance(s, str) and s.strip():
                    return s.strip()
            except Exception:
                pass

        s = getattr(siparis, "owner", None)
        if isinstance(s, str) and s.strip():
            return s.strip()

        return None

    # Repo'nun bir sonraki id'sini döndürür (servis bunu arıyor olabilir).
    def yeni_id(self) -> int:
        yeni = self.__siradaki_id
        self.__siradaki_id += 1
        return yeni

    # Siparişi repo'ya ekler, id yoksa otomatik id verir.
    def ekle(self, siparis) -> int:
        if siparis is None:
            raise ValueError("Sipariş boş olamaz.")

        sahip = self.__siparis_sahibi(siparis)
        if sahip is None:
            raise ValueError("Siparişin sahibi (owner) olmalıdır.")

        siparis_id = self.__siparis_id(siparis)

        # id yoksa (None veya 0 ise) otomatik ver
        if siparis_id is None or (isinstance(siparis_id, int) and siparis_id == 0):
            siparis_id = self.yeni_id()

            set_id = getattr(siparis, "set_id", None)
            if callable(set_id):
                try:
                    set_id(siparis_id)
                except Exception:
                    try:
                        setattr(siparis, "id", siparis_id)
                    except Exception:
                        pass
            else:
                try:
                    setattr(siparis, "id", siparis_id)
                except Exception:
                    pass

        if not isinstance(siparis_id, int) or siparis_id <= 0:
            raise ValueError("Sipariş id'si pozitif bir sayı olmalıdır.")

        if siparis_id in self.__siparisler:
            raise ValueError("Bu id ile kayıtlı sipariş zaten var.")

        self.__siparisler[siparis_id] = siparis
        return siparis_id

    # Verilen id'ye göre siparişi getirir (yoksa None).
    def id_ile_getir(self, siparis_id: int):
        if not isinstance(siparis_id, int) or siparis_id <= 0:
            raise ValueError("siparis_id pozitif int olmalıdır.")
        return self.__siparisler.get(siparis_id)

    # Repo'daki tüm siparişleri liste olarak döndürür.
    def tumunu_listele(self) -> list:
        return list(self.__siparisler.values())

    # Verilen kullanıcı adına göre siparişleri döndürür.
    def kullaniciya_gore_listele(self, owner: str) -> list:
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("owner boş olamaz.")

        owner = owner.strip()
        sonuc = []
        for s in self.__siparisler.values():
            if self.__siparis_sahibi(s) == owner:
                sonuc.append(s)
        return sonuc

    # Servis uyumu için alias: add.
    def add(self, siparis) -> int:
        return self.ekle(siparis)

    # Servis uyumu için alias: get_by_id.
    def get_by_id(self, siparis_id: int):
        return self.id_ile_getir(siparis_id)

    # Servis uyumu için alias: list_all.
    def list_all(self) -> list:
        return self.tumunu_listele()

    # Servis uyumu için alias: list_by_owner.
    def list_by_owner(self, owner: str) -> list:
        return self.kullaniciya_gore_listele(owner)

    # Opsiyonel: güncelleme gerekiyorsa aynı id üstüne yazar.
    def guncelle(self, siparis) -> None:
        siparis_id = self.__siparis_id(siparis)
        if siparis_id is None or not isinstance(siparis_id, int) or siparis_id <= 0:
            raise ValueError("Güncellenecek siparişin id'si geçersiz.")
        if siparis_id not in self.__siparisler:
            raise ValueError("Güncellenecek sipariş repo'da yok.")
        self.__siparisler[siparis_id] = siparis

    # Opsiyonel alias: update.
    def update(self, siparis) -> None:
        self.guncelle(siparis)





