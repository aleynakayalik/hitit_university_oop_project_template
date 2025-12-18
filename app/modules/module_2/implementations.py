from app.modules.module_2.base import PaymentMethod

class CashPayment(PaymentMethod):#balance var limit yok
   def __init__(self, owner: str, balance: float, currency: str = None):
      if currency is None:
         currency = self.varsayilan_currency()  # currency verilmezse varsayılan kullanılır
      super().__init(owner = owner, balance = balance, currency = currency,limit = None)
      
      #Ödeme yapılmadan önce yeterli bakiye var mı kontrol
      def authorize(self, amount: float) -> bool: #Abstract method override
         if not self.tutar_gecerli_mi(amount): #girilen tutar geçerli mi diye bakıyoruz
            return False
         bakiye = self.get_balance()
         if bakiye is None:
            return False
         #Bakiyemiz, ödemek istediğimiz tutardan büyük ya da eşitse ödeme yapılabilir
         if bakiye >= amount:
            return True
         return False
      
      #nakit ödeme işlemi
      def odeme_yap(self, amount: float) -> bool: #Abstract method override
         if not self.authorize(amount):
            return False
         
         yeni_bakiye = self.get_balance() - amount
         self.set_balance(yeni_bakiye)
         return True
      
      #yapılan ödemenin iadesi
      def iade_yap(self, amount: float) -> bool: #Abstract method override
         if not self.tutar_gecerli_mi(amount):
            return False
         yeni_bakiye = (self.get_balance() or 0) + amountself.set_balance(yeni_bakiye)
         return True
      
      #ödeme yöntemi nakit mi kontrolü
      @staticmethod
      def nakit_mi() -> bool:
         return True
      
      #sınıf hakkında kısa bilgi
      @classmethod
      def odeme_tipi(cls) -> str:
         return "Nakit Ödeme"
      
      
class CreditCardPayment(PaymentMethod): #limit kullanılır balance kullanılmaz
   
   def __init__(self,owner: str,card_no: str,card_holder_name: str,expiry_date: str,cvv: str,limit: float,currency: str = None):
      #para birimi verilmezse varsayılan kullanılır
      if currency is None:
          currency = self.varsayilan_currency()
         
      super().__ini__(owner = owner, currency = currency, balance = None, limit = limit)
       
      #kredi kartına özeller
      self.__card_no = None
      self.__card_holder_name = None
      self.__expiry_date = None
      self.__cvv = None

      #setterlar ile doğrulayarak atama
      self.set_card_no(card_no)
      self.set_card_holder_name(card_holder_name)
      self.set_expiry_date(expiry_date)
      self.set_cvv(cvv)

      #kart numarası
      def get_card_no(self) -> str:
         return self.__card_no
      def set_card_no(self, card_no: str) -> None:
         if not isinstance(card_no,str):
            raise ValueError("Kart numarası metin olmalıdır.")
         
         card_no = card_no.strip().replace(" ","")
         
         if not card_no.isdigit():
            raise ValueError("Kartt numarası sadece rakam içermeli.")
         if len(card_no) < 12 and len(card_no) > 19:
            raise ValueError("Kart numarası 12-19 haneli olmalıdır.")
         
         self.__card_no = card_no

      #kart sahini
      def get_card_holder_name(self) -> str:
         return self.__card_holder_name
      def set_card_holder_name(self, name: str) -> None:
         if not isinstance(name, str):
            raise ValueError("Kart sahibinin adı metin olmalıdır.")
         
         name= name.stript()
         if name =="":
            raise ValueError("Kart sahibinin adı boş olamaz.")
         if len(name) < 3 :
            raise ValueError("Kart sahibinin adı çok kısa.")
         self.__card_holder_name = name

      #son kullanma tarihi cvv
      def get_expiry_date(self) -> str:
         return self.__expiry_date
      def set_expiry_date(self, expiry_date: str) -> None:
         if not isinstance(expiry_date, str):
            raise ValueError("Son kullanma tarihi metin olmalıdır.")
         
         expiry_date = expiry_date.stript()

         #MM/YY
         if len(expiry_date) != 5 or expiry_date[2] != "/":
            raise ValueError("Son kullanma tarihi MM/YY şeklinde olmalıdır.")
         
         ay, yil = expiry_date.split("/")

         if not ay.isdigit() or not yil.isdigit():
            raise ValueError("Son kullanma tarihi sayısal olmalıdır.")
         if not (1 <= int(ay) <= 12):
            raise ValueError("Ay 1 ile 12 arasında olmalıdır.")
         
         self.__expiry_dare = expiry_date

      #cvv
      def get_cvv(self) -> str:
        return self.__cvv

      def set_cvv(self, cvv: str) -> None:
         if not isinstance(cvv, str):
            raise ValueError("CVV metin olmalıdır.")

         cvv = cvv.strip()

         if not cvv.isdigit():
            raise ValueError("CVV sadece rakam olmalıdır.")
         if len(cvv) not in (3, 4):
            raise ValueError("CVV 3 veya 4 haneli olmalıdır.")

         self.__cvv = cvv

      #Kart numarasını ekranda gizli göstermek için
      def masked_card_no(self) -> str:
         return "*" * (len(self.__card_no) - 4) + self.__card_no[-4:]
      
      #ödeme işlemleri
      def authorize(self, amount: float) -> bool: #Tutar geçerli mi
         if not self.tutar_gecerli_mi(amount):
            return False

         limit = self.get_limit()
         if limit is None:
            return False

         if limit >= amount:
            return True

         return False

      def odeme_yap(self, amount: float) -> bool:
         # Önce kontrol ediyor
         if not self.authorize(amount):
            return False

         # Limitten düş
         yeni_limit = self.get_limit() - amount
         self.set_limit(yeni_limit)

         return True

      def iade_yap(self, amount: float) -> bool:
         if not self.tutar_gecerli_mi(amount):
            return False

         yeni_limit = (self.get_limit() or 0) + amount
         self.set_limit(yeni_limit)

         return True

      @staticmethod
      def kart_tipi() -> str:
          return "Kredi Kartı"

      @classmethod
      def odeme_tipi(cls) -> str:
          return "Credit Card"
         

      def get_info(self) -> str:
          return (
            f"{self.__class__.__name__} | "
            f"Kişi: {self.get_owner()} | "
            f"Kart Sahibi: {self.__card_holder_name} | "
            f"Kart: {self.masked_card_no()} | "
            f"SKT: {self.__expiry_date} | "
            f"Limit: {self.kullanilabilir_tutar():.2f}"
        )


class OnlineWalletPayment(PaymentMethod): #balance ile çalışır

   def __init__(self, owner: str, wallet_id: str, balance: float, aktif_mi: bool = True, currency: str = None):
      if currency is None:
         currency = self.varsayilan_currency()

      super().__init__(owner=owner, currency=currency, balance=balance, limit=None)

      self.__wallet_id = None
      self.__aktif_mi = None

      self.set_wallet_id(wallet_id)
      self.set_aktif_mi(aktif_mi)

   def get_wallet_id(self) -> str:
      return self.__wallet_id

   def set_wallet_id(self, wallet_id: str) -> None:
      if not isinstance(wallet_id, str):
         raise ValueError("wallet_id metin olmalıdır.")
      wallet_id = wallet_id.strip()

      if wallet_id == "":
         raise ValueError("wallet_id boş olamaz.")
      if len(wallet_id) < 6:
         raise ValueError("wallet_id en az 6 karakter olmalıdır.")
      if " " in wallet_id:
         raise ValueError("wallet_id boşluk içeremez.")

      self.__wallet_id = wallet_id

   def masked_wallet_id(self) -> str:
      if len(self.__wallet_id) <= 4:
         return "****"
      return "*" * (len(self.__wallet_id) - 4) + self.__wallet_id[-4:]

    # --- AKTIF MI ---
   def get_aktif_mi(self) -> bool:
      return self.__aktif_mi

   def set_aktif_mi(self, aktif_mi: bool) -> None:
      if not isinstance(aktif_mi, bool):
         raise ValueError("aktif_mi True veya False olmalıdır.")
      self.__aktif_mi = aktif_mi

    # --- PAYMENT LOGIC ---
   def authorize(self, amount: float) -> bool:
        # 0) Cüzdan aktif mi?
      if not self.__aktif_mi:
         return False

        # 1) Tutar geçerli mi?
      if not self.tutar_gecerli_mi(amount):
         return False

        # 2) Bakiye var mı?
      bakiye = self.get_balance()
      if bakiye is None:
         return False

        # 3) Bakiye yetiyor mu?
      if bakiye >= amount:
         return True

      return False

   def odeme_yap(self, amount: float) -> bool:
      if not self.authorize(amount):
         return False

      yeni_bakiye = self.get_balance() - amount
      self.set_balance(yeni_bakiye)
      return True

   def iade_yap(self, amount: float) -> bool:
      if not self.tutar_gecerli_mi(amount):
         return False

      yeni_bakiye = (self.get_balance() or 0.0) + amount
      self.set_balance(yeni_bakiye)
      return True

   @staticmethod
   def wallet_id_gecerli_mi(wallet_id: str) -> bool:
      if not isinstance(wallet_id, str):
         return False
      
      wallet_id = wallet_id.strip()
      if wallet_id == "" or " " in wallet_id:
         return False
      return len(wallet_id) >= 6

   @classmethod
   def odeme_tipi(cls) -> str:
      return "Online Cüzdan"

   def get_info(self) -> str:
      durum = "Aktif" if self.__aktif_mi else "Pasif"
      return (
            f"{self.__class__.__name__} | Kişi: {self.get_owner()} | "
            f"Cüzdan: {self.masked_wallet_id()} | Durum: {durum} | "
            f"Para Birimi: {self.get_currency()} | Bakiye: {self.kullanilabilir_tutar():.2f}"
        )





 


   

   
         
"""
class OdemeYonetimi:
    def __init__(self):
        self.islem_gecmisi = []  # işlem kayıtlarını tutar

    def odeme_yap(self, odeme_yontemi, tutar: float) -> bool:
        if tutar <= 0:
            print("[Servis] Geçersiz ödeme tutarı.")
            return False

        #Ödeme işlemini başlatıyor (yetkilendirme + ödeme subclass içinde)
        sonuc = odeme_yontemi.odeme_yap(tutar) #polimorfizim örneği ödeme yönteminin türünden bağımsız olarak odeme_yap metodunu çağırmak

        #İşlem kaydı oluşturma (base class'tan)
        kayit = odeme_yontemi.islem_kaydi(
            tutar=tutar,
            sonuc=sonuc,
            aciklama="Servis üzerinden ödeme denemesi"
        )

        #Kayıtları saklamak için
        self.islem_gecmisi.append(kayit)

        if sonuc:
            print("[Servis] Ödeme başarıyla tamamlandı.")
        else:
            print("[Servis] Ödeme başarısız.")

        return sonuc

    def islem_gecmisini_listele(self):
        return self.islem_gecmisi
    
"""
class YemekhaneServisi:
   pass


    

