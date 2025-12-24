# tests/module_2/test_module_2.py
import pytest

from app.modules.module_2.base import PaymentMethod
from app.modules.module_2.implementations import (
    CashPayment,
    CreditCardPayment,
    OnlineWalletPayment,
    MenuItem,
    Order,
    PaymentTransaction,
    CafeteriaService,
)
from app.modules.module_2.repository import (
    InMemoryMenuRepository,
    InMemoryOrderRepository,
    InMemoryPaymentRepository,
    InMemoryTransactionRepository,
)


# -------------------------
# Fixtures
# -------------------------
@pytest.fixture()
def repos():
    menu_repo = InMemoryMenuRepository()
    order_repo = InMemoryOrderRepository()
    tx_repo = InMemoryTransactionRepository()
    pay_repo = InMemoryPaymentRepository()
    return menu_repo, order_repo, tx_repo, pay_repo


@pytest.fixture()
def service(repos):
    menu_repo, order_repo, tx_repo, pay_repo = repos

    # menü doldur
    menu_repo.ekle(MenuItem(1, "Çorba", 20.0, "corba", True, tags=["vegan"], available_days=[1, 3, 5]))
    menu_repo.ekle(MenuItem(2, "Pilav", 30.0, "ana", True, tags=["klasik"], available_days=[1, 2, 3, 4, 5]))
    menu_repo.ekle(MenuItem(3, "Ayran", 10.0, "icecek", True, tags=["sut"], available_days=[1, 2, 3, 4, 5]))
    menu_repo.ekle(MenuItem(4, "Pasif Ürün", 99.0, "ana", False, tags=["x"], available_days=[1]))

    return CafeteriaService(menu_repo=menu_repo, order_repo=order_repo, tx_repo=tx_repo, payment_repo=pay_repo)


# -------------------------
# Base / Abstract
# -------------------------
def test_paymentmethod_abstract_oldugu_icin_orneklenemez():
    with pytest.raises(TypeError):
        PaymentMethod(owner="Ali", currency="TRY")


def test_paymentmethod_balance_ve_limit_ayni_anda_verilemez():
    # Abstract olduğu için direkt PaymentMethod üzerinden yapamayız.
    # Bu kural PaymentMethod.__init__ içinde: alt sınıfı kullanarak tetikleyelim.
    with pytest.raises(ValueError):
        # CashPayment balance verir, ama biz burada base'e ulaşmak için "limit" de geçmek zorundayız,
        # CashPayment izin vermez. O yüzden bu testi base'e özel bir dummy sınıfla yapıyoruz.
        class Dummy(PaymentMethod):
            def authorize(self, amount: float) -> bool:
                return True

            def odeme_yap(self, amount: float) -> bool:
                return True

            def iade_yap(self, amount: float) -> bool:
                return True

        Dummy(owner="Ali", currency="TRY", balance=10, limit=10)


# -------------------------
# Payment yöntemleri
# -------------------------
def test_cashpayment_authorize_yeterli_bakiye():
    p = CashPayment(owner="Mehmet", balance=100, currency="TRY")
    assert p.authorize(50) is True
    assert p.authorize(150) is False


def test_cashpayment_odeme_yap_bakiye_duser():
    p = CashPayment(owner="Mehmet", balance=100, currency="TRY")
    assert p.odeme_yap(40) is True
    assert p.get_balance() == 60.0


def test_creditcard_authorize_limit_yeterli():
    cc = CreditCardPayment(
        owner="Mehmet",
        card_no="123456789012",
        card_holder_name="MEHMET YILMAZ",
        expiry_date="12/30",
        cvv="123",
        limit=200,
        currency="TRY",
    )
    assert cc.authorize(150) is True
    assert cc.authorize(250) is False


def test_creditcard_odeme_yap_limit_duser():
    cc = CreditCardPayment(
        owner="Mehmet",
        card_no="123456789012",
        card_holder_name="MEHMET YILMAZ",
        expiry_date="12/30",
        cvv="123",
        limit=200,
        currency="TRY",
    )
    assert cc.odeme_yap(50) is True
    assert cc.get_limit() == 150.0


def test_onlinewallet_pasifken_authorize_false():
    w = OnlineWalletPayment(owner="Mehmet", wallet_id="CUZDAN01", balance=100, aktif_mi=False, currency="TRY")
    assert w.authorize(10) is False


def test_onlinewallet_authorize_yeterli_bakiye():
    w = OnlineWalletPayment(owner="Mehmet", wallet_id="CUZDAN01", balance=100, aktif_mi=True, currency="TRY")
    assert w.authorize(50) is True
    assert w.authorize(150) is False


# -------------------------
# MenuItem / Order
# -------------------------
def test_menuitem_gun_adi():
    assert MenuItem.gun_adi(1) == "Pazartesi"
    assert MenuItem.gun_adi(5) == "Cuma"
    assert MenuItem.gun_adi(99) == "Geçersiz Gün"


def test_menu_repo_gune_gore_listele(service):
    # Pazartesi (1) menüsünde 1,2,3 var; 4 pasif ama gün=1 olduğu için sadece_aktif=True iken gelmemeli
    items = service.menuyu_goster(1, sadece_aktif=True)
    ids = sorted([u.get_id() for u in items])
    assert ids == [1, 2, 3]


def test_siparis_olustur_toplam_tutar(service):
    order = service.siparis_olustur("Mehmet", [1, 2])
    assert isinstance(order, Order)
    assert order.toplam_tutar() == 50.0
    assert order.odenecek_tutar() == 50.0


def test_siparis_olustur_pasif_urun_hata(service):
    with pytest.raises(ValueError):
        service.siparis_olustur("Mehmet", [4])  # pasif ürün


# -------------------------
# Transaction entity
# -------------------------
def test_transaction_basarili_basarisiz_factory():
    tx1 = PaymentTransaction.basarili(owner="Mehmet", amount=10, currency="TRY", method_type="CashPayment", order_id=1)
    assert tx1.get_status() == "BAŞARILI"
    assert tx1.basarili_mi() is True

    tx2 = PaymentTransaction.basarisiz(
        owner="Mehmet",
        amount=10,
        currency="TRY",
        method_type="CashPayment",
        reason="Yetersiz bakiye",
        order_id=1,
    )
    assert tx2.get_status() == "BAŞARISIZ"
    assert tx2.basarili_mi() is False
    assert "Yetersiz" in tx2.get_failure_reason()


# -------------------------
# Service ödeme akışı
# -------------------------
def test_odeme_al_basarili_olunca_tx_kaydi_ve_order_paid(service, repos):
    menu_repo, order_repo, tx_repo, pay_repo = repos

    # Ödeme yöntemlerini ekle
    nakit = CashPayment(owner="Mehmet", balance=200, currency="TRY")
    pay_repo.ekle(nakit)

    order = service.siparis_olustur("Mehmet", [1, 2])  # 50
    tx = service.odeme_al(order.get_id(), payment_method=nakit, otomatik_sec=False)

    assert isinstance(tx, PaymentTransaction)
    assert tx.get_status() == "BAŞARILI"
    assert tx.get_amount() == 50.0

    # tx repo kayıt kontrol
    txs = tx_repo.tumunu_listele()
    assert len(txs) == 1
    assert txs[0].get_status() == "BAŞARILI"

    # order durum ve ödenen tutar
    assert order.get_status() == "PAID"
    assert order.get_paid_amount() == 50.0


def test_odeme_al_yetki_yoksa_tx_basarisiz(service, repos):
    menu_repo, order_repo, tx_repo, pay_repo = repos

    # Yetersiz limitli kart
    kart = CreditCardPayment(
        owner="Mehmet",
        card_no="123456789012",
        card_holder_name="MEHMET YILMAZ",
        expiry_date="12/30",
        cvv="123",
        limit=10,
        currency="TRY",
    )
    pay_repo.ekle(kart)

    order = service.siparis_olustur("Mehmet", [1, 2])  # 50
    tx = service.odeme_al(order.get_id(), payment_method=kart, otomatik_sec=False)

    assert tx.get_status() == "BAŞARISIZ"
    assert "Yetkilendirme" in tx.get_failure_reason()

    txs = tx_repo.tumunu_listele()
    assert len(txs) == 1
    assert txs[0].get_status() == "BAŞARISIZ"

    # order paid olmamalı
    assert order.get_paid_amount() == 0.0
    assert order.get_status() != "PAID"


def test_odeme_al_otomatik_sec_uygun_yontem_secer(service, repos):
    _, _, tx_repo, pay_repo = repos

    # Sırayla: 1) yetersiz nakit 2) yeterli wallet
    nakit = CashPayment(owner="Mehmet", balance=10, currency="TRY")  # yetmez
    wallet = OnlineWalletPayment(owner="Mehmet", wallet_id="CUZDAN01", balance=200, aktif_mi=True, currency="TRY")

    pay_repo.ekle(nakit)
    pay_repo.ekle(wallet)

    order = service.siparis_olustur("Mehmet", [1, 2])  # 50

    tx = service.odeme_al(order.get_id(), payment_method=None, otomatik_sec=True)
    assert tx.get_status() == "BAŞARILI"
    assert tx.get_method_type() == "OnlineWalletPayment"

    # tx repo kaydı var
    assert len(tx_repo.tumunu_listele()) == 1


def test_islem_gecmisi_filtreleme(service, repos):
    _, _, tx_repo, pay_repo = repos

    nakit = CashPayment(owner="Mehmet", balance=200, currency="TRY")
    pay_repo.ekle(nakit)

    order1 = service.siparis_olustur("Mehmet", [1])  # 20
    service.odeme_al(order1.get_id(), payment_method=nakit, otomatik_sec=False)

    order2 = service.siparis_olustur("Mehmet", [2])  # 30
    service.odeme_al(order2.get_id(), payment_method=nakit, otomatik_sec=False)

    # owner filtre
    txs_owner = service.islemleri_listele(owner="Mehmet")
    assert len(txs_owner) == 2

    # başarılı filtre
    basarili = service.basarili_islemler()
    assert len(basarili) == 2
    assert all(t.get_status() == "BAŞARILI" for t in basarili)
