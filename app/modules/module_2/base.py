
from __future__ import annotations  #type hint’lerin geç değerlendirilmesini sağlar ve class’lar arası referans hatalarını önler.
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    def __init__(self, owner: str, currency: str, balance: float | None = None, limit: float| None = None):
        self.__owner = None
        self.__currency = None
        self.__balance = None
        self.__limit = None

        self.set_owner(owner)
        self.set_currency(currency)

        #ikisi aynı anda doluysa karışmasın diye
        if balance is not None and limit is not None:
            raise ValueError("Aynı anda hem balance hem limit verilemez.")
             
        self.set_balance(balance)
        self.set_limit(limit)
    
    #ödeme yönteminin sahibini döndürür -getter-
    def get_owner(self) -> str:
        return self.__owner
    #ödeme yönteminin sahibini ayarlar -setter-
    def set_owner(self, owner: str) ->  None:
        if not isinstance(owner, str):
            raise ValueError("owner bir metin olmalıdır.")
        owner = owner.strip()
        if owner == "":
            raise ValueError("owner boş olamaz.")
        if len(owner) < 2:
            raise ValueError("owner en az 2 karakter olmalıdır.")
        self.__owner = owner
    
    #para birimini döndürür -getter-
    def get_currency(self) -> str:
        return self.__currency
    #para birimini ayarlar -setter-
    def set_currency(self, currency: str) -> None:
        if not isinstance(currency, str):
            raise ValueError("currency metin olmalıdır.")
        currency = currency.strip()
        if currency == "":
            raise ValueError("currency boş olamaz.")
        currency = currency.upper()
        if currency not in ["TRY","USD", "EUR"]:
            raise ValueError("Geçersiz para birimi.")
        self.__currency = currency
    
    #bakiye'yi döndürür -getter-
    def get_balance(self) -> float | None:
        return self.__balance
    #bakiye değerini ayarlar -setter-
    def set_balance(self, balance: float | None) -> None:
        if balance is None:
            self.__balance = None 
            return
        if not isinstance(balance, (int,float)):
            raise ValueError("balance sayı olmalıdır.")
        if balance < 0:
            raise ValueError("balance negatif olamaz.")
        
        self.__balance = float(balance)

    #limit değerini döndürür -getter-
    def get_limit(self) -> float | None:
        return self.__limit
    #limit değerini ayarlar -setter-
    def set_limit(self, limit: float | None) -> None:
        if limit is None:
            self.__limit = None
            return
        if not isinstance(limit, (int, float)):
            raise ValueError("limit sayı olmalıdır.")
        if limit < 0:
            raise ValueError("limit negatif olamaz.")
        self.__limit = float(limit)
    
    #öödeme yöntemiyle en fazla ne kadar ödenebilir
    def kullanilabilir_tutar(self) -> float:
        if self.__balance is not None:
            return self.__balance
        if self.__limit is not None:
            return self.__limit
        return 0.0
    
    #ödeme yapılmadan önce kontrol izin adımı
    @abstractmethod
    def authorize(self, amount: float) -> bool:
        pass
    
    #ödeme işlemi ve sonucu
    @abstractmethod
    def odeme_yap(self, amount: float) -> bool:
        pass
    
    #yapılan ödemenin iadesi gerçekleştirir
    @abstractmethod
    def iade_yap(self, amount: float) -> bool:
        pass

    #girilen tutar geçerli mi kontrol eder
    @staticmethod
    def tutar_gecerli_mi(amount: float) -> bool:
        if not isinstance(amount, (int,float)):
            return False
        if amount <= 0:
            return False
        return True
    
    #para birimi geçerli mi değil mi kontrol eder
    @staticmethod
    def para_birimi_gecerli_mi(currency: str) -> bool:
        if not isinstance(currency, str):
            return False
        currency = currency.strip().upper()

        if currency not in ["TRY", "USD","EUR"]:
            return False
        return True
    
    #varsayılan para birimini döndürür
    @classmethod
    def varsayilan_currency(cls) -> str:
        return "TRY"
    #kısa bilgi döndürür
    def get_info(self) -> str: 
        tip = self.__class__.__name__
        tutar = self.kullanilabilir_tutar()
        return f"{tip} | Kişi: {self.__owner} | Para Birimi: {self.__currency} | Kullanılabilir Tutar: {tutar}"
    
    



    

        
        
