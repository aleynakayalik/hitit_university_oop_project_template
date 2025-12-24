
from __future__ import annotations
from app.modules.module_2.base import PaymentMethod
from datetime import datetime
from typing import Any, Iterable, List, Optional

class CashPayment(PaymentMethod):#balance var limit yok
   def __init__(self, owner: str, balance: float, currency: str | None = None):
      if currency is None:
         currency = self.varsayilan_currency()  # currency verilmezse varsayılan kullanılır
      super().__init__(owner = owner, balance = balance, currency = currency,limit = None)
      
   #Ödeme yapılmadan önce yeterli bakiye var mı kontrol
   def authorize(self, amount: float) -> bool: #Abstract method override polymorphism
      if not self.tutar_gecerli_mi(amount): #girilen tutar geçerli mi diye bakıyoruz
         return False
      
      bakiye = self.get_balance()
      if bakiye is None:
         return False
      return bakiye >= amount
         
   
   #nakit ödeme işlemi
   def odeme_yap(self, amount: float) -> bool: #Abstract method override polymorphism
      if not self.authorize(amount):
         return False
      
      yeni_bakiye = self.get_balance() - amount
      self.set_balance(yeni_bakiye)
      return True
   
   #yapılan ödemenin iadesi
   def iade_yap(self, amount: float) -> bool: #Abstract method override
      if not self.tutar_gecerli_mi(amount):
         return False
      yeni_bakiye = (self.get_balance() or 0.0) + amount
      self.set_balance(yeni_bakiye)
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
   
   def __init__(self,owner: str,card_no: str,card_holder_name: str
                ,expiry_date: str,cvv: str,limit: float,currency: str  |None = None):
      
      #para birimi verilmezse varsayılan kullanılır
      if currency is None:
          currency = self.varsayilan_currency()
         
      super().__init__(owner = owner, currency = currency, balance = None, limit = limit)
       
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
         raise ValueError("Kart numarası sadece rakam içermeli.")
      if len(card_no) < 12 or len(card_no) > 19:
         raise ValueError("Kart numarası 12-19 haneli olmalıdır.")
      
      self.__card_no = card_no

   #kart sahini
   def get_card_holder_name(self) -> str:
      return self.__card_holder_name
   def set_card_holder_name(self, name: str) -> None:
      if not isinstance(name, str):
         raise ValueError("Kart sahibinin adı metin olmalıdır.")
      
      name= name.strip()
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
      
      expiry_date = expiry_date.strip()

      #MM/YY
      if len(expiry_date) != 5 or expiry_date[2] != "/":
         raise ValueError("Son kullanma tarihi MM/YY şeklinde olmalıdır.")
      
      ay, yil = expiry_date.split("/")

      if not ay.isdigit() or not yil.isdigit():
         raise ValueError("Son kullanma tarihi sayısal olmalıdır.")
      if not (1 <= int(ay) <= 12):
         raise ValueError("Ay 1 ile 12 arasında olmalıdır.")
      
      self.__expiry_date = expiry_date

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

      return limit >= amount

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

      yeni_limit = (self.get_limit() or 0.0) + amount
      self.set_limit(yeni_limit)
      return True

   @staticmethod
   def kart_tipi() -> str:
         return "Kredi Kartı"

   @classmethod
   def odeme_tipi(cls) -> str:
         return "Kredi Kartı"
      

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

   def __init__(self, owner: str, wallet_id: str, balance: float, aktif_mi: bool = True, currency: str | None = None):
      if currency is None:
         currency = self.varsayilan_currency()

      super().__init__(owner=owner, currency=currency, balance=balance, limit=None)

      self.__wallet_id = None
      self.__aktif_mi = None

      self.set_wallet_id(wallet_id)
      self.set_aktif_mi(aktif_mi)
   #Cüzdan id bilgisini döndürür -getter-
   def get_wallet_id(self) -> str:
      return self.__wallet_id
   #Cüzdan id bilgisini ayarlar -setter-
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
   
   #cüzdan id yi maskeler
   def masked_wallet_id(self) -> str:
      if len(self.__wallet_id) <= 4:
         return "****"
      return "*" * (len(self.__wallet_id) - 4) + self.__wallet_id[-4:]
   #cüzdan aktif mi bilgisini döndürür
   def get_aktif_mi(self) -> bool:
      return self.__aktif_mi
   def set_aktif_mi(self, aktif_mi: bool) -> None:
      if not isinstance(aktif_mi, bool):
         raise ValueError("aktif_mi True veya False olmalıdır.")
      self.__aktif_mi = aktif_mi

   def authorize(self, amount: float) -> bool:
      
      if not self.__aktif_mi: #Cüzdan aktif mi?
         return False

      if not self.tutar_gecerli_mi(amount): #Tutar geçerli mi?
         return False

      bakiye = self.get_balance()
      if bakiye is None: #Bakiye var mı?
         return False

      if bakiye >= amount: #Bakiye yetiyor mu?
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

#Yemekhane menüsündeki tek bir ürünü temsil eden entity sınıfı
class MenuItem:
   def __init__(self, id: int, name: str, price: float, category: str,is_available: bool = True,
                tags: list[str] | None = None, available_days: list[int] | None = None):
      self.__id = None
      self.__name = None
      self.__price = None
      self.__category = None
      self.__is_available = None
      self.__tags = None
      self.__available_days = None

      self.set_id(id)
      self.set_name(name)
      self.set_price(price)
      self.set_category(category)
      self.set_is_available(is_available)
      self.set_tags(tags)
      self.set_available_days(available_days)

   #Ürün id bilgisini döndürür
   def get_id(self) -> int:
      return self.__id
   #Ürün id bilgisini ayarlar
   def set_id(self, id: int) -> None:
      if not isinstance(id, int) or id <= 0:
         raise ValueError("MenuItem id pozitif bir tamsayı olmalıdır.")
      self.__id = id

   #Ürün adını döndürür
   def get_name(self) -> str:
      return self.__name
   #Ürün adını ayarlar
   def set_name(self, name: str) -> None:
      if not isinstance(name, str):
         raise ValueError("Ürün adı metin olmalıdır.")
      name = name.strip()
      if len(name) < 2:
         raise ValueError("Ürün adı en az 2 karakter olmalıdır.")
      self.__name = name

   #Ürün fiyatını döndürür
   def get_price(self) -> float:
      return self.__price
   #Ürün fiyatını ayarlar
   def set_price(self, price: float) -> None:
      if not isinstance(price, (int, float)):
         raise ValueError("Ürün fiyatı sayısal olmalıdır.")
      price = float(price)
      if price <= 0:
         raise ValueError("Ürün fiyatı 0'dan büyük olmalıdır.")
      self.__price = price

   #Ürün kategorisini döndürür
   def get_category(self) -> str:
      return self.__category
   #Ürün kategorisini ayarlar
   def set_category(self, category: str) -> None:
      if not isinstance(category, str):
         raise ValueError("Kategori metin olmalıdır.")
      category = category.strip()
      if len(category) < 3:
         raise ValueError("Kategori en az 3 karakter olmalıdır.")
      self.__category = category

   #Ürünün menüde aktif olup olmadığını döndürür
   def get_is_available(self) -> bool:
      return self.__is_available
   #Ürünün menüde aktif olup olmadığını ayarlar
   def set_is_available(self, is_available: bool) -> None:
      if not isinstance(is_available, bool):
         raise ValueError("is_available True veya False olmalıdır.")
      self.__is_available = is_available

   #Ürün etiketlerini döndürür
   def get_tags(self) -> list[str]:
      return list(self.__tags)
   #Ürün etiketlerini ayarlar
   def set_tags(self, tags: list[str] | None) -> None:
      if tags is None:
         self.__tags = []
         return
   
      if not isinstance(tags, list):
         raise ValueError("tags bir liste olmalıdır.")
      
      temiz_tags = []
      for tag in tags:
         if not isinstance(tag, str):
            raise ValueError("tags listesi sadece metin içermelidir.")
         tag = tag.strip()
         if tag != "":
            temiz_tags.append(tag.lower())

      self.__tags = temiz_tags

   #Ürünün servis edleceği günleri döndürür (1=Pzt,2=Salı,...,5=Cuma)
   def get_available_days(self) -> list[int]:
      return list(self.__available_days)
   #Ürünün servis edileceği günleri ayarlar (1-5 arası int liste)
   def set_available_days(self, available_days: list[int] | None) -> None:
      if available_days is None:
         available_days = [1, 2, 3, 4, 5]

      if (not isinstance(available_days, list)
        or not all(isinstance(d, int) for d in available_days)
        or any(d < 1 or d > 5 for d in available_days)):
         raise ValueError("available_days 1-5 arasında int liste olmalı.")

   
      self.__available_days = sorted(set(available_days))

   #Bu ürün verilen günde menüde var mı kontrol eder
   def gununde_var_mi(self, day: int) -> bool:
      return isinstance(day, int) and day in self.__available_days
   
   #Ürün bilgisini yazdırır
   def get_info(self) -> str:
       durum = "var" if self.__is_available else "yok"
       tags_txt = ",".join(self.__tags) if self.__tags else "-"
       gunler_txt = ",".join(str(d) for d in self.__available_days) if self.__available_days else "-"
       return (
            f"MenuItem(id={self.__id}, "
            f"name='{self.__name}', "
            f"price={self.__price:.2f}, "
            f"category='{self.__category}', "
            f"available={durum}, "
            f"available_days=[{gunler_txt}], "
            f"tags=[{tags_txt}])"
        )

   #Fiyatın geçerli olup olmadığını kontrol eder
   @staticmethod
   def fiyat_gecerli_mi(price: float) -> bool:
      return isinstance(price, (int, float)) and float(price) > 0
   
   #Gün numarasını gün adına çevirir (1=Pzt ... 5=Cuma)
   @staticmethod
   def gun_adi(day: int) -> str:
      gunler= {1: "Pazartesi", 2: "Salı", 3: "Çarşamba", 4: "Perşembe", 5: "Cuma"}
      return gunler.get(day, "Geçersiz Gün")
   
   
   #Örnek bir menü ürünü döndürür
   @classmethod
   def ornek_urun(cls) -> "MenuItem":
      return cls(
            id=1,
            name="Hamburger",
            price=10.0,
            category="Main",
            is_available=True,
            tags=["fast-food", "et"],
            available_days=[1, 3, 5]
        )

#Kullanıcının oluşturduğu siparişi temsil eden entity sınıfı
class Order:
   def __init__(self, id: int, owner: str, items: list[MenuItem], currency: str = "TRY",
                created_at : datetime | None = None, status: str = "SİPARİŞ OLUŞTURULDU",
                notes: str = "", discount_rate: float = 0.0,paid_amount: float =0.0):
      
      self.__id = None
      self.__owner = None
      self.__items = None
      self.__currency = None
      self.__created_at = None
      self.__status = None
      self.__notes = None
      self.__discount_rate = None
      self.__paid_amount = None

      self.set_id(id)
      self.set_owner(owner)
      self.set_items(items)
      self.set_currency(currency)
      self.set_created_at(created_at)
      self.set_status(status)
      self.set_notes(notes)
      self.set_discount_rate(discount_rate)
      self.set_paid_amount(paid_amount)

   #Sipariş id bilgisini döndürür
   def get_id(self) -> int:
      return self.__id
   #Sipariş id bilgisini ayarlar
   def set_id(self, id: int) -> None:
      if not isinstance(id, int) or id <= 0:
         raise ValueError("Order id pozitif bir tamsayı olmalıdır.")
      self.__id = id

   #Siparişi veren kullanıcıyı döndürür
   def get_owner(self) -> str:
      return self.__owner
   #Siparişi veren kullanıcıyı ayarlar
   def set_owner(self, owner: str) -> None:
      if not isinstance(owner, str):
         raise ValueError("owner metin olmalıdır.")
      owner = owner.strip()
      if owner == "":
         raise ValueError("owner boş olamaz.")
      if len(owner) < 2:
         raise ValueError("owner çok kısa.")
      self.__owner = owner

   #Siparişteki ürün listesini döndürür
   def get_items(self) -> list[MenuItem]:
      return list(self.__items)
   #Siparişteki ürün listesini ayarlar
   def set_items(self, items: list[MenuItem]) -> None:
      if not isinstance(items, list):
         raise ValueError("items bir liste olmalıdır.")
      if len(items) == 0:
         raise ValueError("Sipariş boş olamaz (en az 1 ürün olmalı).")

      kontrol_listesi = []
      for item in items:
         if not isinstance(item, MenuItem):
               raise ValueError("items listesi sadece MenuItem içermelidir.")
         kontrol_listesi.append(item)

      self.__items = kontrol_listesi

   #Siparişin para birimini döndürür
   def get_currency(self) -> str:
      return self.__currency
   #Siparişin para birimini ayarlar
   def set_currency(self, currency: str) -> None:
      if not isinstance(currency, str):
         raise ValueError("currency metin olmalıdır.")
      currency = currency.strip().upper()
      if currency == "":
         raise ValueError("currency boş olamaz.")
      self.__currency = currency

   #Sipariş oluşturulma tarihini döndürür
   def get_created_at(self) -> datetime:
      return self.__created_at
   #Sipariş oluşturulma tarihini ayarlar (verilmezse şimdiki zaman)
   def set_created_at(self, created_at: datetime | None) -> None:
      if created_at is None:
         self.__created_at = datetime.now()
         return
      if not isinstance(created_at, datetime):
         raise ValueError("created_at datetime olmalıdır.")
      self.__created_at = created_at

   #Sipariş durumunu döndürür
   def get_status(self) -> str:
      return self.__status
   #Sipariş durumunu ayarlar
   def set_status(self, status: str) -> None:
      if not isinstance(status, str):
         raise ValueError("status metin olmalıdır.")
      status = status.strip().upper()
      if status == "":
         raise ValueError("status boş olamaz.")
      self.__status = status

   #Sipariş notunu döndürür
   def get_notes(self) -> str:
      return self.__notes
   #Sipariş notunu ayarlar
   def set_notes(self, notes: str) -> None:
      if not isinstance(notes, str):
         raise ValueError("notes metin olmalıdır.")
      self.__notes = notes.strip()

   #Sipariş indirimi oranını döndürür
   def get_discount_rate(self) -> float:
      return self.__discount_rate
   #Sipariş indirimi oranını ayarlar
   def set_discount_rate(self, discount_rate: float) -> None:
      if not isinstance(discount_rate, (int, float)):
         raise ValueError("discount_rate sayısal olmalıdır.")
      discount_rate = float(discount_rate)
      if discount_rate < 0 or discount_rate > 0.8:
         raise ValueError("discount_rate 0 ile 0.8 arasında olmalıdır.")
      self.__discount_rate = discount_rate

   #Sipariş için ödenen tutarı döndürür
   def get_paid_amount(self) -> float:
      return self.__paid_amount
   #Sipariş için ödenen tutarı ayarlar
   def set_paid_amount(self, paid_amount: float) -> None:
      if not isinstance(paid_amount, (int, float)):
         raise ValueError("paid_amount sayısal olmalıdır.")
      paid_amount = float(paid_amount)
      if paid_amount < 0:
         raise ValueError("paid_amount negatif olamaz.")
      self.__paid_amount = paid_amount

   #Sipariş toplam tutarını (indirimsiz) hesaplar
   def toplam_tutar(self) -> float:
      toplam = 0.0
      for item in self.__items:
         toplam += item.get_price()
      return toplam

   #Sipariş indirim tutarını hesaplar
   def indirim_tutari(self) -> float:
      return self.toplam_tutar() * self.__discount_rate

   #Siparişin ödenmesi gereken tutarını hesaplar
   def odenecek_tutar(self) -> float:
      return self.toplam_tutar() - self.indirim_tutari()

   #Siparişe ürün ekler
   def urun_ekle(self, item: MenuItem) -> None:
      if not isinstance(item, MenuItem):
         raise ValueError("Eklenecek ürün MenuItem olmalıdır.")
      self.__items.append(item)

   #Siparişten ürün çıkarır (id ile)
   def urun_cikar(self, item_id: int) -> bool:
      if not isinstance(item_id, int) or item_id <= 0:
         raise ValueError("item_id pozitif integer olmalıdır.")

      for i in range(len(self.__items)):
         if self.__items[i].get_id() == item_id:
               self.__items.pop(i)
               return True
      return False

   #Siparişte belirli bir ürün var mı kontrol eder
   def contains_item(self, item_id: int) -> bool:
      if not isinstance(item_id, int) or item_id <= 0:
         return False
      for item in self.__items:
         if item.get_id() == item_id:
               return True
      return False

   #Siparişin kısa bilgisini döndürür
   def get_info(self) -> str:
      return(
            f"Order(id={self.__id}, owner='{self.__owner}', status={self.__status}, "
            f"item_count={len(self.__items)}, total={self.toplam_tutar():.2f}, "
            f"discount={self.__discount_rate:.2f}, payable={self.odenecek_tutar():.2f}, "
            f"paid={self.__paid_amount:.2f} {self.__currency}, created_at={self.__created_at})"
      )
   
   #Sipariş id geçerli mi kontrol eder
   @staticmethod
   def id_gecerli_mi(order_id: int) -> bool:
      return isinstance(order_id, int) and order_id > 0

   #Demo için örnek sipariş döndürür
   @classmethod
   def ornek_siparis(cls, owner: str) -> "Order":
      return cls(
            id=1,
            owner=owner,
            items=[MenuItem.ornek_urun()],
            currency="TRY",
            status="SİPARİŞ OLUŞTURULDU",
            notes="Acısız olsun",
            discount_rate=0.20,
            paid_amount=0.0
      )

#Yapılan ödeme işlemini kayıt altına alan entity sınıfı
class PaymentTransaction:
   
   #Ödeme işlemi kaydı oluşturur
   def __init__(self,id: int,owner: str,order_id: int,amount: float,currency: str,status: str,method_type: str,
        failure_reason: str = "",created_at: datetime | None = None):
        self.__id = None
        self.__owner = None
        self.__order_id = None
        self.__amount = None
        self.__currency = None
        self.__status = None
        self.__method_type = None
        self.__failure_reason = None
        self.__created_at = None

        self.set_id(id)
        self.set_owner(owner)
        self.set_order_id(order_id)
        self.set_amount(amount)
        self.set_currency(currency)
        self.set_status(status)
        self.set_method_type(method_type)
        self.set_failure_reason(failure_reason)
        self.set_created_at(created_at)

   #İşlem id bilgisini döndürür
   def get_id(self) -> int:
      return self.__id
   #İşlem id bilgisini ayarlar
   def set_id(self, id: int) -> None:
      if not isinstance(id, int) or id < 0:
         raise ValueError("Transaction id negatif olamaz. (0 = repo atayacak)")
      self.__id = id

   #İşlemi yapan kullanıcıyı döndürür
   def get_owner(self) -> str:
      return self.__owner
   #İşlemi yapan kullanıcıyı ayarlar
   def set_owner(self, owner: str) -> None:
      if not isinstance(owner, str):
         raise ValueError("owner metin olmalıdır.")
      owner = owner.strip()
      if owner == "":
         raise ValueError("owner boş olamaz.")
      self.__owner = owner

   #İlgili sipariş id'sini döndürür
   def get_order_id(self) -> int:
      return self.__order_id
   #İlgili sipariş id'sini ayarlar
   def set_order_id(self, order_id: int) -> None:
      if not isinstance(order_id, int) or order_id < 0:
         raise ValueError("order_id negatif olamaz. (0 = bilinmiyor)")
      self.__order_id = order_id
      
   #Ödenen tutarı döndürür
   def get_amount(self) -> float:
      return self.__amount
   #Ödenen tutarı ayarlar
   def set_amount(self, amount: float) -> None:
      if not isinstance(amount, (int, float)):
         raise ValueError("amount sayısal olmalıdır.")
      amount = float(amount)
      if amount <= 0:
         raise ValueError("amount 0'dan büyük olmalıdır.")
      self.__amount = amount

   #Para birimini döndürür
   def get_currency(self) -> str:
      return self.__currency
   #Para birimini ayarlar
   def set_currency(self, currency: str) -> None:
      if not isinstance(currency, str):
         raise ValueError("currency metin olmalıdır.")
      currency = currency.strip().upper()
      if currency == "":
         raise ValueError("currency boş olamaz.")
      self.__currency = currency

   #İşlem durumunu döndürür
   def get_status(self) -> str:
      return self.__status
   #İşlem durumunu ayarlar (BAŞARILI/BAŞARISIZ)
   def set_status(self, status: str) -> None:
      if not isinstance(status, str):
         raise ValueError("status metin olmalıdır.")
      status = status.strip().upper()
      if status not in {"BAŞARILI", "BAŞARISIZ"}:
         raise ValueError("status 'BAŞARILI' veya 'BAŞARISIZ' olmalıdır.")
      self.__status = status

   #Kullanılan ödeme yöntemi tipini döndürür
   def get_method_type(self) -> str:
      return self.__method_type
   #Kullanılan ödeme yöntemi tipini ayarlar
   def set_method_type(self, method_type: str) -> None:
      if not isinstance(method_type, str):
         raise ValueError("method_type metin olmalıdır.")
      method_type = method_type.strip()
      if method_type == "":
         raise ValueError("method_type boş olamaz.")
      self.__method_type = method_type

   #Başarısızlık sebebini döndürür
   def get_failure_reason(self) -> str:
      return self.__failure_reason
   #Başarısızlık sebebini ayarlar (başarılıysa boş olabilir)
   def set_failure_reason(self, reason: str) -> None:
      if not isinstance(reason, str):
         raise ValueError("failure_reason metin olmalıdır.")
      self.__failure_reason = reason.strip()

   #İşlem zamanını döndürür
   def get_created_at(self) -> datetime:
      return self.__created_at

   #İşlem zamanını ayarlar (verilmezse şimdiki zaman)
   def set_created_at(self, created_at: datetime | None) -> None:
      if created_at is None:
         self.__created_at = datetime.now()
         return
      if not isinstance(created_at, datetime):
         raise ValueError("created_at datetime olmalıdır.")
      self.__created_at = created_at

   #İşlemin başarılı olup olmadığını döndürür
   def basarili_mi(self) -> bool:
      return self.__status == "BAŞARILI"
   #İşlemin kısa bilgisini döndürür
   def get_info(self) -> str:
      sebep = "-" if self.__failure_reason == "" else self.__failure_reason
      return (
            f"PaymentTransaction(id={self.__id}, owner='{self.__owner}', order_id={self.__order_id}, "
            f"amount={self.__amount:.2f} {self.__currency}, status={self.__status}, "
            f"method_type='{self.__method_type}', reason='{sebep}', created_at={self.__created_at})"
      )

   #Transaction id geçerli mi kontrol eder
   @staticmethod
   def id_gecerli_mi(tx_id: int) -> bool:
      return isinstance(tx_id, int) and tx_id >= 0
   
   @classmethod
   def basarili(cls, owner: str, amount: float, currency: str, method_type: str,
        order_id: int = 0, id: int = 0, created_at: datetime | None = None,) -> "PaymentTransaction":
      return cls(id=id, owner=owner, order_id=order_id, amount=amount, currency=currency,
            status="BAŞARILI", method_type=method_type, failure_reason="", created_at=created_at,)

   @classmethod
   def basarisiz(cls, owner: str, amount: float, currency: str, method_type: str,
        reason: str, order_id: int = 0, id: int = 0, created_at: datetime | None = None,) -> "PaymentTransaction":
      return cls(id=id, owner=owner, order_id=order_id, amount=amount, currency=currency,
            status="BAŞARISIZ", method_type=method_type, failure_reason=reason, created_at=created_at,)
   
   
   #Başarılı bir ödeme işlemi oluşturur
   @classmethod
   def basarili_islem(cls,id: int, owner: str, order_id: int, amount: float,
                      currency: str, method_type: str) -> "PaymentTransaction":
      return cls(id=id, owner=owner, order_id=order_id, amount=amount, currency=currency,
               status="BAŞARILI", method_type=method_type, failure_reason="")

 

#Yemekhane ve ödeme süreçlerini yöneten servis sınıfı
class CafeteriaService:

   def __init__(self, menu_repo: Any, order_repo: Any, tx_repo: Any, payment_repo: Any) -> None:
      self._menu_repo = menu_repo
      self._order_repo = order_repo
      self._tx_repo = tx_repo
      self._payment_repo = payment_repo

   #1-5 arası günü yazıya çevirir.
   @staticmethod
   def gun_adi(gun: int) -> str:
      return {
            1: "Pazartesi",
            2: "Salı",
            3: "Çarşamba",
            4: "Perşembe",
            5: "Cuma",
      }.get(gun, "Bilinmeyen Gün")

   #Repo dönüşünü güvenli şekilde listeye çevirir.
   @staticmethod
   def _liste_yap(obj: Any) -> list:
        
        if obj is None:
            return []
        if isinstance(obj, list):
            return obj
        if isinstance(obj, tuple):
            return list(obj)
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, dict):
            return list(obj.values())
        if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
            return list(obj)
        return [obj]
   
   #Servis genelinde varsayılan para birimi.
   @classmethod
   def varsayilan_para_birimi(cls) -> str:
      return "TRY"
   #Repo üzerinde metot adları farklı olsa da uygun olanı çağırır.
   def _repo_cagir(self, repo: Any, aday_islemleri: list[str], *args, **kwargs):
      for ad in aday_islemleri:
         fn = getattr(repo, ad, None)
         if callable(fn):
            return fn(*args, **kwargs)
      raise AttributeError(f"Repo içinde beklenen metot yok: {aday_islemleri}")
   

   def _yeni_siparis_id(self) -> int:
    # 1) Repo sayaç metodu varsa
      for ad in ["yeni_id", "next_id", "siradaki_id", "get_next_id"]:
         fn = getattr(self._order_repo, ad, None)
         if callable(fn):
            yeni = fn()
            if isinstance(yeni, int) and yeni > 0:
                  return yeni

      # 2) Yoksa mevcut siparişlerden max+1
      try:
         mevcut = self._repo_cagir(self._order_repo, ["tumunu_listele", "list_all"])
         mevcut_list = self._liste_yap(mevcut)
      except Exception:
         mevcut_list = [] 

      en_buyuk = 0
      for o in mevcut_list:
         get_id = getattr(o, "get_id", None)
         if callable(get_id):
            try:
                  val = get_id()
                  if isinstance(val, int) and val > en_buyuk:
                     en_buyuk = val
            except Exception:
                  pass

      return en_buyuk + 1


#MENU
   #Tüm menüyü listeler (aktif filtreli / filtresiz).
   def menu_listele(self, sadece_aktif: bool = True) -> List[MenuItem]:
      sonuc = self._repo_cagir(self._menu_repo, ["listele", "list_all", "tumunu_listele"], sadece_aktif)
      return self._liste_yap(sonuc)
   
   #İstenen güne göre menüyü döndürür.
   def menuyu_goster(self, gun: int, sadece_aktif: bool = True) -> List[MenuItem]:
      sonuc = self._repo_cagir(self._menu_repo, ["gune_gore_listele"], gun, sadece_aktif)
      return self._liste_yap(sonuc)
   
   #ID ile menü ürünü getirir.
   def urun_getir(self, urun_id: int) -> Optional[MenuItem]:
      return self._repo_cagir(self._menu_repo, ["id_ile_getir", "get_by_id"], urun_id)
   
   #Kategoriye göre menü ürünlerini listeler
   def kategoriye_gore_menu(self, kategori: str, sadece_aktif: bool = True):
      items = self._menu_repo.kategoriye_gore_listele(kategori)

      if not sadece_aktif:
         return items

      sonuc = []
      for u in items:
         aktif = getattr(u, "aktif_mi", None)
         if aktif is None:
               aktif = getattr(u, "available", None)
         if aktif is True:
               sonuc.append(u)

      return sonuc

#SİPARİŞ
   #Verilen ürün id’lerinden sipariş oluşturur ve repo’ya kaydeder
   def siparis_olustur(self, owner: str, urun_idleri: List[int]) -> Order:
      if not isinstance(owner, str) or not owner.strip():
         raise ValueError("owner boş olamaz.")
      if not isinstance(urun_idleri, list) or not urun_idleri:
         raise ValueError("Sipariş için en az 1 ürün seçmelisin.")

      items: List[MenuItem] = []
      for uid in urun_idleri:
         urun = self.urun_getir(uid)
         if urun is None:
            raise ValueError(f"Ürün bulunamadı: id={uid}")

         # MenuItem’ında aktiflik kontrolü
         get_av = getattr(urun, "get_is_available", None)
         if callable(get_av) and get_av() is False:
            raise  ValueError(f"Bu ürün şu an aktif değil: id={uid}")

         items.append(urun)

      yeni_id = self._yeni_siparis_id()

      order = Order(
         id=yeni_id,
         owner=owner.strip(),
         items=items,
         currency=self.varsayilan_para_birimi(),
         created_at=datetime.now(),
         status="SİPARİŞ OLUŞTURULDU",
      )

      self._repo_cagir(self._order_repo, ["ekle", "add"], order)
      return order


   #Sipariş id ile getirir.
   def siparis_getir(self, siparis_id: int) -> Optional[Order]:
      return self._repo_cagir(self._order_repo, ["id_ile_getir", "get_by_id"], siparis_id)
   #Siparişleri listeler
   def siparisleri_listele(self, owner: str | None = None) -> list[Order]:
      if owner and isinstance(owner, str) and owner.strip():
         sonuc = self._repo_cagir(self._order_repo, ["kullaniciya_gore_listele", "list_by_owner"], owner.strip())
         return self._liste_yap(sonuc)
      sonuc = self._repo_cagir(self._order_repo, ["tumunu_listele", "list_all"])
      return self._liste_yap(sonuc)

#ÖDEME YÖNTEMİ SEÇME
   #Ödeme yöntemlerini listeler (kullanıcıya göre / hepsi).
   def odeme_yontemleri(self, owner: str | None = None) -> list[PaymentMethod]: #polymorphism
      if owner and isinstance(owner, str) and owner.strip():
         sonuc = self._repo_cagir(self._payment_repo, ["kullaniciya_gore_listele", "list_by_owner"], owner.strip())
         return self._liste_yap(sonuc)
      sonuc = self._repo_cagir(self._payment_repo, ["tumunu_listele", "list_all"])
      return self._liste_yap(sonuc)

   #Kullanıcının ödeme yöntemleri içinde authorize(tutar) geçen ilk yöntemi seçer.
   #Polymorphism: Cash/CreditCard/Wallet hepsi PaymentMethod gibi davranır.
   def uygun_odeme_yontemi_sec(self, owner: str, tutar: float) -> PaymentMethod | None:
      
      yontemler = self.odeme_yontemleri(owner)

      for y in yontemler:
         try:
               if y.authorize(tutar):
                  return y
         except Exception: # bir yöntem bozuksa diğerini dene
               continue
      return None
   

#ÖDEME

   def odeme_al(self, siparis_id: int, payment_method: PaymentMethod | None = None,
            otomatik_sec: bool = True,) -> PaymentTransaction:
        
      order = self.siparis_getir(siparis_id)
      if order is None:
         raise ValueError("Sipariş bulunamadı.")
      
      order_owner = order.get_owner()
      # toplam tutar
      toplam = order.odenecek_tutar()

      # ödeme yöntemi seçimi
      secilen = payment_method
      if secilen is None and otomatik_sec:
         secilen = self.uygun_odeme_yontemi_sec(order.get_owner(), toplam)

      if secilen is None:
         # hiç yöntem yoksa bile tx kaydı düşelim
         tx = PaymentTransaction.basarisiz(
               owner=order.get_owner(),
               amount=toplam,
               currency=self.varsayilan_para_birimi(),
               method_type="Yok",
               reason="Uygun ödeme yöntemi bulunamadı.",
               order_id=order.get_id(),
         )
         self._repo_cagir(self._tx_repo, ["ekle", "add"], tx)
         return tx

      # authorize (bu ödeme yapılabilir mi? diye sorgulamak)
      try:
         yetki = secilen.authorize(toplam)
      except Exception as e:
         yetki = False
         hata = str(e)
      else:
         hata = ""

      if not yetki:
         tx = PaymentTransaction.basarisiz(
               owner=order.get_owner(),
               amount=toplam,
               currency=getattr(secilen, "get_currency", lambda: self.varsayilan_para_birimi())(),
               method_type=secilen.__class__.__name__,
               reason=("Yetkilendirme başarısız." + (f" {hata}" if hata else "")),
               order_id=order.get_id(),
         )
         self._repo_cagir(self._tx_repo, ["ekle", "add"], tx)
         return tx

      # ödeme yap
      try:
         ok = secilen.odeme_yap(toplam)
         if ok is False:
            raise ValueError("Ödeme yöntemi odemeyi reddetti.")
      except Exception as e:
         tx = PaymentTransaction.basarisiz(
               owner=order_owner,
               amount=toplam,
               currency=getattr(secilen, "get_currency", lambda: self.varsayilan_para_birimi())(),
               method_type=secilen.__class__.__name__,
               reason=f"Ödeme sırasında hata: {e}",
               order_id=order.get_id(),
         )
         self._repo_cagir(self._tx_repo, ["ekle", "add"], tx)
         return tx

      # başarılı tx
      tx = PaymentTransaction.basarili(
         owner=order.get_owner(),
         amount=toplam,
         currency=getattr(secilen, "get_currency", lambda: self.varsayilan_para_birimi())(),
         method_type=secilen.__class__.__name__,
         order_id=order.get_id(),
      )
      self._repo_cagir(self._tx_repo, ["ekle", "add"], tx)

      # siparişi ödenmiş işaretle 
      set_status = getattr(order, "set_status", None)
      if callable(set_status):
         set_status("PAID")

      set_paid = getattr(order, "set_paid_amount", None)
      if callable(set_paid):
         set_paid(toplam)

      # repo’da update metodu varsa çağır (opsiyonel)
      for upd in ["guncelle", "update"]:
         ufn = getattr(self._order_repo, upd, None)
         if callable(ufn):
               try:
                  ufn(order)
               except Exception:
                  pass

      return tx

#İŞLEM GEÇMİŞİ
   #İşlemleri listeler (kullanıcıya göre / tümü).
   def islemleri_listele(self, owner: str | None = None) -> list[PaymentTransaction]:
        
      if owner and isinstance(owner, str) and owner.strip():
         sonuc = self._repo_cagir(self._tx_repo, ["kullaniciya_gore_listele", "list_by_owner"], owner.strip())
         return self._liste_yap(sonuc)
      sonuc = self._repo_cagir(self._tx_repo, ["tumunu_listele", "list_all"])
      return self._liste_yap(sonuc)
   #Sadece başarılı işlemleri döndürür (repo destekliyorsa)
   def basarili_islemler(self) -> list[PaymentTransaction]: 
      try:
         sonuc = self._repo_cagir(self._tx_repo, ["duruma_gore_listele", "list_by_status"], "BAŞARILI")
         return self._liste_yap(sonuc)
      except Exception:
         # repo’da yoksa basit filtre
         txs = self.islemleri_listele()
         return [t for t in txs if getattr(t, "get_status", lambda: "")() == "BAŞARILI"]
