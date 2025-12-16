# app/modules/module_2/base.py
#from abc import ABC, abstractmethod

class BaseClass2(ABC):
    def __init__(self, parameter: str):
        self.base2Attribute = parameter

    @abstractmethod
    def method2(self) -> None:
        # model tanimii
        pass



from abc import ABC, abstractmethod

class OdemeYontemi(ABC):
    def __init__(self, kisi: str ,bakiye: float , para_birimi="TL"):  #attribute
        self.kisi = kisi 
        self.bakiye = bakiye       
        self.para_birimi = para_birimi

    @abstractmethod
    def yetkilendir(self, tutar: float) -> bool: #Ödeme yapılabilir mi kontrol eder
        pass

    @abstractmethod
    def odeme_yap(self, tutar: float) -> bool:  #Ödeme işlemini gerçekleştirir
        pass
    #her alt sınıfta farklı olduğu için
    @abstractmethod
    def odeme_tipi(self) -> str:
        pass
    

    #getter metotlar
    def get_bakiye(self):
        return self.bakiye
    
    def get_kisi(self):
        return self.kisi
    
    def get_para_birimi(self):
        return self.para_birimi
    
    #ortak metotlar

    def yeterli_bakiye_mi(self,tutar: float) -> bool:   #yeterli bakiye var mı kontrolu
        return self.bakiye >= tutar

    def bakiye_dus(self, tutar: float) -> None:
        self.bakiye -= tutar

    def bakiye_arttir(self, tutar: float) -> None:
        self.bakiye += tutar

    def ozet_bilgi(self) -> str:
        return (
            f"Kişi : {self.kisi}" |
            f"Bakiye : {self.bakiye} {self.para_birimi}" |
            f"Ödeme Yöntemi : {self.__class__.__name__}" |
            f"Ödeme Tipi : {self.odeme_tipi()}" #polimorfizm
        )
    #tüm ödeme yöntemleri için ortak olduğu için
    def islem_kaydi(self, tutar: float, sonuc: bool, aciklama: str = "") -> dict:
        return {
            "kisi": self.kisi,
            "odeme_tipi": self.odeme_tipi(), #polimorfizm Kredi Kartı şeklinde çıktı verir
            "sinif_adı": self.__class__.__name__, #teknik çıktı olur KrediKartiOdeme gibi
            "tutar": tutar,
            "para_birimi": self.para_birimi,
            "sonuc": sonuc,
            "aciklama": aciklama
        }
    
    