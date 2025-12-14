# app/modules/module_2/implementations.py
from app.modules.module_2.base import BaseClass2

class Base2SubClass1(BaseClass2):
    def method2(self):
        print(f"Sinif Attribute: {self.base2Attribute}")

class Base2SubClass2(BaseClass2):
    def method2(self):
        print(f"Sinif Attribute: {self.base2Attribute}")



from app.modules.module_2.base import OdemeYontemi 

class KrediKartiOdeme(OdemeYontemi): ##subclass
    def __init__(self, kisi: str, bakiye: float, para_birimi: str, card_no,card_name: str,cvv: int):
     super().__init(kisi, bakiye, para_birimi)
     self.card_no = card_no
     self.card_name = card_name
     self.cvv = cvv #attribute

    def yeterli_bakiye_mi(self,tutar: float) -> bool:
       return self.bakiye >= tutar
    
    def odeme(self, tutar: float) -> bool:
        if self.yeterli_bakiye_mi(tutar):
            self.bakiye -= tutar
            print(f"Kart ödemesi BAŞARILI: {tutar} {self.para_birimi}")
            return True
        else:
           print("Kart Ödemesi BAŞARISIZ : Yetersiz Bakiye")
        return False

class NakitOdeme(OdemeYontemi):
   def __init__(self, kisi: str, bakiye: float, para_birimi: str = "TL"):
      super().__init__(kisi, bakiye, para_birimi)
      self.fis_no = 0    
      self.gunluk_islem_sayisi = 0

   def yetkilendir(self, tutar: float) -> bool:   #kasadki nakit parayı kontrol ediyor
      return self.bakiye >= tutar
   def odeme_yap(self, tutar: float) -> bool:
      if self.yetkilendir(tutar):
         self.bakiye -= tutar
         self.fis_no += 1
         self.gunluk_islem_sayisi += 1
         print( f"[Nakit] Ödeme başarılı | Tutar: {tutar} {self.para_birimi} | "
                f"Fiş No: {self.fis_no} | Günlük İşlem: {self.gunluk_islem_sayisi} | "
                f"Kalan Bakiye: {self.bakiye}")
         return True
      
      print("Nakit ödeme BAŞARISIZ: Yetersiz nakit")
      return False
      
class OnlineCuzdanOdeme(OdemeYontemi):
   def __init__(self, isim:str, bakiye: float, para_birimi: str = "TL", hesap_id: str = ""):
      super().__init__(kisi, bakiye, para_birimi)
      self.hesap_id = hesap_id
      self.basarisiz_denem_sayisi = 0
      self.toplam_islem_sayisi = 0
    
   def yetkilendir(self, tutar: float) -> bool:
      return self.bakiye>= tutar
   def odeme_yap(self, tutar: float) -> bool:
      if self.yetkilendir(tutar):
         self.bakiye -= tutar
         self.toplam_islem_sayisi += 1
         print(
    f"""

----------------------------------
Hesap ID          : {self.hesap_id}
Ödenen Tutar      : {tutar} {self.para_birimi}
Toplam İşlem Sayısı: {self.toplam_islem_sayisi}
Kalan Bakiye      : {self.bakiye} {self.para_birimi}
----------------------------------
""")
         return True
      
      self.basarisiz_deneme_sayisi += 1
      print(
            f"""
[Online Cüzdan] Ödeme Başarısız
Cüzdan Adı: {self.cuzdan_adi}
Başarısız Deneme Sayısı: {self.basarisiz_deneme_sayisi}
""")
      return False

class OdemeYonetimi:
   def odeme_yap(self,odeme_yontemi, tutar): #attiribute
      if tutar <=0:
         print("Geçersiz ödeme tutarı.")
         return False
      
      yetkili_mi = odeme_yontemi.yetkilendir(tutar) #otomatik olarak yetkilendir metodunu çalıştırıyor
      if not yetkili_mi:
         print("Ödeme yetkilendirilemedi.")
         return False
      
      odeme_basalili_mi = odeme_yontemi.odeme_yap(tutar)
      if odeme_basalili_mi:
         print("Ödeme işlemi başarıyla tamamandı.")
         return True
      
      print("Ödeme işleminde beklenmeyen bir hata oluştu!!")
      return False

         



    

