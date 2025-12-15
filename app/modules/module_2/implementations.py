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
   def __init__(self, kisi: str, bakiye: float, para_birimi: str, kart_numarası: str = "" ,kart_ismi: str = "",cvv: int =0):
     super().__init__(kisi, bakiye, para_birimi)
     self.kart_numarasi = kart_numarasi
     self.kart_ismi = kart_ismi
     self.cvv = cvv #attribute

   def yetkilendir(self, tutar: float) -> bool:
    return self.yeterli_bakiye_mi(tutar)
   def odeme_yap(self, tutar: float) -> bool:
      if not self.yetkilendir(tutar):
         #işlem kaydı oluşturma
         kayit = self.islem_kaydi(tutar = tutar , sonuc = False , aciklama = "Kredi Kartı ödemesi reddedildi : YETERSİZ BAKİYE")
         print("[Kredi Kartı] Ödeme başarısız :(")
         print(kayit)
         return False
      self.bakiye_dus(tutar)
      #işlem kaydı oluşturma
      kayit = self.islem_kaydi(tutar = tutar, sonuc = True, aciklama = "[Kredi Kartı] ile yapılan İŞLEM BAŞARILI :)")
      print(
            f"""

        KREDİ KARTI ÖDEMESİ
----------------------------------
Kart No   : {self.kart_numarasi}
Kart Adı  : {self.kart_ismi}
Tutar     : {tutar} {self.para_birimi}
Kalan     : {self.bakiye} {self.para_birimi}
----------------------------------
"""
        )
      print(self.ozet_bilgi())
      print("İşlem Kaydı : ",kayit)
      return True
    

class NakitOdeme(OdemeYontemi):
   def __init__(self, kisi: str, bakiye: float, para_birimi: str = "TL"):
      super().__init__(kisi, bakiye, para_birimi)
      self.fis_no = 0    
      self.gunluk_islem_sayisi = 0

   def yetkilendir(self, tutar: float) -> bool:   #kasadki nakit parayı kontrol ediyor
      return self.yeterli_bakiye_mi(tutar)
   
   def odeme_yap(self, tutar: float) -> bool:
      if not self.yetkilendir(tutar):
         #işlem kaydı oluşturma
         kayit = self.islem_kaydi(tutar = tutar, sonuc = False, aciklama = "Nakit Ödeme reddedildi : YTERSİZ BAKİYE")
         print("[Nakit] ödeme başarısız")
         print(kayit)
         return False
      self.bakiye_dus(tutar)
      self.fis_no += 1
      self.gunluk_islem_sayisi += 1
      #işlem kaydı oluşturma
      kayit = self.islem_kaydi(tutar = tutar, sonuc = True, aciklama = "Nakit ödeme başarılı")
      print(
            f"""
           NAKİT ÖDEME
----------------------------------
Fiş No              : {self.fis_no}
Günlük İşlem Sayısı : {self.gunluk_islem_sayisi}
Ödenen Tutar        : {tutar} {self.para_birimi}
Kalan Bakiye        : {self.bakiye} {self.para_birimi}
----------------------------------
"""        )
      print(self.ozet_bilgi())
      print("işlem Kaydı:",kayit)
      return True

      
class OnlineCuzdanOdeme(OdemeYontemi):
   def __init__(self, isim:str, bakiye: float, para_birimi: str = "TL", hesap_id: str = ""):
      super().__init__(kisi, bakiye, para_birimi)
      self.hesap_id = hesap_id
      self.basarisiz_deneme_sayisi = 0
      self.toplam_islem_sayisi = 0
    
   def yetkilendir(self, tutar: float) -> bool:
      return self.yeterli_bakiye_mi(tutar)
   def odeme_yap(self, tutar: float) -> bool:
      if not self.yetkilendir(tutar):
            self.basarisiz_deneme_sayisi += 1
            #işlem kaydı oluşturma
            kayit = self.islem_kaydi(tutar=tutar, sonuc=False,aciklama="Online cüzdan ödeme reddedildi: yetersiz bakiye")
            
            print("[Online Cüzdan] Ödeme başarısız:(")
            print("Başarısız deneme sayısı:", self.basarisiz_deneme_sayisi)
            print(kayit)
            return False
      self.bakiye_dus(tutar)
      self.toplam_islem_sayisi += 1     
      #işlem kaydı oluşturma
      kayit = self.islem_kaydi(tutar = tutar, sonuc = True,aciklama = "Online cüzdan ödeme başarılı:)") 
      print(
            f"""
        ONLINE CÜZDAN ÖDEMESİ
----------------------------------
Hesap ID            : {self.hesap_id}
Ödenen Tutar        : {tutar} {self.para_birimi}
Toplam İşlem Sayısı : {self.toplam_islem_sayisi}
Kalan Bakiye        : {self.bakiye} {self.para_birimi}
----------------------------------
""")
      print(self.ozet_bilgi())
      print("İşlem Kaydı:", kayit)
      return True


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

         



    

