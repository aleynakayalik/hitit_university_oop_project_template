

from __future__ import annotations

from datetime import datetime

from app.modules.module_2.implementations import (
    MenuItem,
    CafeteriaService,
    CashPayment,
    CreditCardPayment,
    OnlineWalletPayment,
)
from app.modules.module_2.repository import (
    InMemoryMenuRepository,
    InMemoryPaymentRepository,
    InMemoryTransactionRepository,
)


def _sep(title: str = "") -> None:
    print("\n" + "=" * 60)
    if title:
        print(title)
        print("-" * 60)


def _goster(items) -> None:
    for x in items:
        print(" -", x)


def main() -> None:
    _sep("MODÜL 2 - ÖDEME / YEMEKHANE DEMO")

    #Repo'ları oluştur (veritabanı varmış gibi RAM'de tutuyorum)
    menu_repo = InMemoryMenuRepository()
    payment_repo = InMemoryPaymentRepository()
    tx_repo = InMemoryTransactionRepository()

    #Servisi oluştur
    service = CafeteriaService(
        menu_repo=menu_repo,
        payment_repo=payment_repo,
        transaction_repo=tx_repo,
    )

    #Menüye ürünleri ekle (haftalık menü mantığı: available_days 1-5)
    _sep("MENÜYE ÜRÜN EKLEME")
    menu_repo.add(MenuItem(ad="Mercimek Çorbası", fiyat=25.0, kategori="Çorba", available_days=[1, 2, 3, 4, 5]))
    menu_repo.add(MenuItem(ad="Tavuk Sote", fiyat=70.0, kategori="Ana Yemek", available_days=[1, 3, 5]))
    menu_repo.add(MenuItem(ad="Pilav", fiyat=30.0, kategori="Yan Ürün", available_days=[1, 2, 3, 4, 5]))
    menu_repo.add(MenuItem(ad="Ayran", fiyat=12.0, kategori="İçecek", available_days=[1, 2, 3, 4, 5]))
    menu_repo.add(MenuItem(ad="Salata", fiyat=18.0, kategori="Yan Ürün", available_days=[2, 4]))

    print("Menüye ürünler eklendi. (Toplam:", len(menu_repo.list_all(only_available=False)), ")")

    #Menü listeleme (gün filtresi + aktif)
    _sep("MENÜ LİSTELEME (GÜN=1)")
    bugun = 1
    menu_gun1 = service.menu_listele(day=bugun)
    _goster(menu_gun1)

    #Ödeme yöntemlerini oluştur 
    _sep("ÖDEME YÖNTEMLERİ OLUŞTURMA (SUBCLASS)")
    owner = "Ali"
    cash = CashPayment(owner=owner, currency="TRY", balance=60)  # düşük bakiye
    card = CreditCardPayment(owner=owner, currency="TRY", limit=500, card_no="1234-5678-9012-3456")
    wallet = OnlineWalletPayment(owner=owner, currency="TRY", balance=250, wallet_id="WLT-001")

    # Polimorfizm: hepsi PaymentMethod ama farklı sınıflar
    payment_methods = [cash, card, wallet]
    print("Polimorfizm listesi (PaymentMethod listesi):")
    for m in payment_methods:
        # get_type yoksa sınıf adını basar
        tip = getattr(m, "get_type", None)
        print(" -", tip() if callable(tip) else m.__class__.__name__, "| owner:", m.get_owner())

    # Repo'ya ödeme yöntemlerini kaydet
    _sep("ÖDEME YÖNTEMLERİNİ REPO'YA KAYDETME")
    # Repo metot isimleri farklı olabilir, o yüzden güvenli şekilde deniyoruz.
    for pm in payment_methods:
        if hasattr(payment_repo, "add"):
            payment_repo.add(pm)
        elif hasattr(payment_repo, "ekle"):
            payment_repo.ekle(pm)
    print("Ödeme yöntemleri kaydedildi (varsa).")

    #Sipariş oluştur (ürün id'leri ile)
    _sep("SİPARİŞ OLUŞTURMA")
    # Menü repo id'leri genelde 1..N olur. Aşağıdaki id'ler tutmazsa
    # menü listelemede bastığın id'lere göre değiştir.
    item_ids = [1, 2, 4]  # çorba + tavuk + ayran
    order = service.siparis_olustur(owner=owner, item_ids=item_ids)

    print("Sipariş oluşturuldu:")
    print(" - Sipariş Sahibi:", getattr(order, "owner", owner))
    print(" - Ürün sayısı:", len(getattr(order, "items", [])))
    print(" - Toplam Tutar:", order.toplam_tutar(), getattr(order, "currency", "TRY"))

    #YETERSİZ bakiye ile ödeme dene (authorize başarısız örneği)
    _sep("ÖDEME DENEMESİ (YETERSİZ BAKİYE) - CASH")
    try:
        tx_fail = service.odeme_al(order, cash)
        print("İşlem sonucu (exception yok):", getattr(tx_fail, "status", "BİLİNMİYOR"))
        print(" - amount:", getattr(tx_fail, "amount", None))
        print(" - method:", getattr(tx_fail, "method_type", cash.__class__.__name__))
    except Exception as e:
        print("Ödeme başarısız (beklenen):", str(e))

    #Uygun ödeme yöntemi seç (serviste varsa)
    _sep("UYGUN ÖDEME YÖNTEMİ SEÇME (VARSA)")
    sec = getattr(service, "uygun_odeme_yontemi_sec", None)
    if callable(sec):
        uygun = sec(owner=owner, amount=order.toplam_tutar())
        print("Servis uygun yöntem seçti:", uygun.__class__.__name__)
    else:
        print("Bu projede uygun_odeme_yontemi_sec metodu yoksa sorun değil (opsiyonel).")

    #BAŞARILI ödeme yap (kredi kartı ya da cüzdan ile)
    _sep("ÖDEME DENEMESİ (BAŞARILI) - CARD")
    try:
        tx_ok = service.odeme_al(order, card)
        print("Ödeme başarılı gibi görünüyor.")
        print(" - status:", getattr(tx_ok, "status", "BİLİNMİYOR"))
        print(" - owner:", getattr(tx_ok, "owner", owner))
        print(" - amount:", getattr(tx_ok, "amount", None))
        print(" - currency:", getattr(tx_ok, "currency", "TRY"))
        print(" - method:", getattr(tx_ok, "method_type", card.__class__.__name__))
        print(" - created_at:", getattr(tx_ok, "created_at", datetime.now()))
    except Exception as e:
        print("Burada başarısız olduysa card limitini yükselt:", str(e))

    #İşlem geçmişi listele / raporlama (owner / durum)
    _sep("İŞLEM GEÇMİŞİ (OWNER=Ali)")
    gecmis = getattr(service, "islem_gecmisi", None)
    if callable(gecmis):
        liste = gecmis(owner=owner)
        if not liste:
            print("Kayıt yok.")
        else:
            for tx in liste:
                print(
                    f"- id={getattr(tx, 'id', '-')}"
                    f" | owner={getattr(tx, 'owner', '-')}"
                    f" | amount={getattr(tx, 'amount', '-')}"
                    f" | status={getattr(tx, 'status', '-')}"
                    f" | method={getattr(tx, 'method_type', '-')}"
                )
    else:
        # servis metodu yoksa repo üzerinden göster
        tum = tx_repo.list_all() if hasattr(tx_repo, "list_all") else []
        print("Serviste islem_gecmisi yok -> repo list_all ile gösteriyorum.")
        for tx in tum:
            print(
                f"- id={getattr(tx, 'id', '-')}"
                f" | owner={getattr(tx, 'owner', '-')}"
                f" | amount={getattr(tx, 'amount', '-')}"
                f" | status={getattr(tx, 'status', '-')}"
                f" | method={getattr(tx, 'method_type', '-')}"
            )

    _sep("DEMO BİTTİ")


if __name__ == "__main__":
    main()
