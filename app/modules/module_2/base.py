# app/modules/module_2/base.py
from abc import ABC, abstractmethod

class BaseClass2(ABC):
    def __init__(self, parameter: str):
        self.base2Attribute = parameter

    @abstractmethod
    def method2(self) -> None:
        # model tanimii
        pass



from abc import ABC, abstractmethod

class OdemeYontemi(ABC):
    def __init__(self, kisi,bakiye , para_birimi="TL"):
        self.kisi = kisi 
        self.bakiye = bakiye       
        self.para_birimi = para_birimi

    @abstractmethod
    def yetkilendir(self, tutar): #Ödeme yapılabilir mi kontrol eder
        pass

    @abstractmethod
    def odeme_yap(self, tutar):  #Ödeme işlemini gerçekleştirir
        pass
    

    #getter
    def get_bakiye(self):
        return self.bakiye
    
    def get_kisi(self):
        return self.kisi
    
    def get_para_birimi(self):
        return self.para_birimi
    
    #ortak metotlar

    def yeterli_bakiye_mi(self,tutar):   #yeterli bakiye var mı kontrolu
        return self.bakiye >= tutar

    def bakiye_guncellememe(self,tutar):
        self.bakiye = (self.bakiye - tutar)
        print(f"Mevcud bakiyeniz:{self.bakiye}")
        return self.bakiye
            
    """
    def bakiye_guncelle(self, tutar, islem):
        if islem == "odeme":
            self.bakiye -= tutar
        elif islem == "iade":
            self.bakiye += tutar

        return self.bakiye"""
