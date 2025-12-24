# app/modules/module_2/demo.py
from __future__ import annotations

from typing import List

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
    InMemoryPaymentRepository,
    InMemoryTransactionRepository,
)

try:
    from app.modules.module_2.repository import InMemoryOrderRepository
except Exception:
    class InMemoryOrderRepository:
        def __init__(self) -> None:
            self.__siparisler = {}
            self.__siradaki_id = 1

        def yeni_id(self) -> int:
            yeni = self.__siradaki_id
            self.__siradaki_id += 1
            return yeni

        def ekle(self, siparis) -> int:
            if siparis is None:
                raise ValueError("Sipariş boş olamaz.")

            get_owner = getattr(siparis, "get_owner", None)
            owner = get_owner() if callable(get_owner) else getattr(siparis, "owner", None)
            if not isinstance(owner, str) or not owner.strip():
                raise ValueError("Siparişin sahibi (owner) olmalıdır.")

            get_id = getattr(siparis, "get_id", None)
            sid = get_id() if callable(get_id) else getattr(siparis, "id", None)

            if sid is None or (isinstance(sid, int) and sid == 0):
                sid = self.yeni_id()
                set_id = getattr(siparis, "set_id", None)
                if callable(set_id):
                    set_id(sid)
                else:
                    setattr(siparis, "id", sid)

            if not isinstance(sid, int) or sid <= 0:
                raise ValueError("Sipariş id'si pozitif olmalıdır.")
            if sid in self.__siparisler:
                raise ValueError("Bu id ile kayıtlı sipariş zaten var.")

            self.__siparisler[sid] = siparis
            return sid

        def id_ile_getir(self, siparis_id: int):
            if not isinstance(siparis_id, int) or siparis_id <= 0:
                raise ValueError("siparis_id pozitif int olmalıdır.")
            return self.__siparisler.get(siparis_id)

        def tumunu_listele(self) -> list:
            return list(self.__siparisler.values())

        def kullaniciya_gore_listele(self, owner: str) -> list:
            if not isinstance(owner, str) or not owner.strip():
                raise ValueError("owner boş olamaz.")
            owner = owner.strip()

            sonuc = []
            for s in self.__siparisler.values():
                get_owner = getattr(s, "get_owner", None)
                o = get_owner() if callable(get_owner) else getattr(s, "owner", None)
                if isinstance(o, str) and o.strip() == owner:
                    sonuc.append(s)
            return sonuc

        # Alias metotlar
        def add(self, siparis) -> int:
            return self.ekle(siparis)

        def get_by_id(self, siparis_id: int):
            return self.id_ile_getir(siparis_id)

        def list_all(self) -> list:
            return self.tumunu_listele()

        def list_by_owner(self, owner: str) -> list:
            return self.kullaniciya_gore_listele(owner)

        def guncelle(self, siparis) -> None:
            get_id = getattr(siparis, "get_id", None)
            sid = get_id() if callable(get_id) else getattr(siparis, "id", None)
            if not isinstance(sid, int) or sid <= 0:
                raise ValueError("Güncellenecek siparişin id'si geçersiz.")
            if sid not in self.__siparisler:
                raise ValueError("Güncellenecek sipariş repo'da yok.")
            self.__siparisler[sid] = siparis

        def update(self, siparis) -> None:
            self.guncelle(siparis)


# ---------------------------
#   YARDIMCI EKRAN / INPUT
# ---------------------------
def _sep() -> None:
    print("\n" + "=" * 70)


def _metin_al(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print(" Boş bırakılamaz.")


def _secim_al(prompt: str, secenekler: set[str]) -> str:
    while True:
        s = input(prompt).strip().lower()
        if s in secenekler:
            return s
        print(" Geçersiz seçim.")


def _evet_hayir_al(prompt: str) -> bool:
    while True:
        s = input(prompt).strip().lower()
        if s in {"e", "evet", "yes", "y"}:
            return True
        if s in {"h", "hayır", "hayir", "no", "n"}:
            return False
        print(" Lütfen e/h (evet/hayır) gir.")


def _ad_soyad_al(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if not s:
            print(" Boş bırakılamaz.")
            continue

        for ch in s:
            if ch == " ":
                continue
            if not ch.isalpha():
                print("Ad soyad sadece harf ve boşluk içermeli. (Sayı/işaret yok)")
                break
        else:
            parcalar = [p for p in s.split() if p]
            if len(parcalar) < 2:
                print(" Lütfen ad ve soyad gir. (Örn: Aleyna Kayalık)")
                continue
            return s


def _isim_harf_al(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if not s:
            print(" Boş bırakılamaz.")
            continue

        for ch in s:
            if ch == " ":
                continue
            if not ch.isalpha():
                print(" Sadece harf ve boşluk gir. (Sayı/işaret yok)")
                break
        else:
            if len(s.replace(" ", "")) < 3:
                print(" Çok kısa. En az 3 harf olmalı.")
                continue
            return s


def _int_al(prompt: str, min_deger: int | None = None, max_deger: int | None = None) -> int:
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
        except Exception:
            print(" Tam sayı gir.")
            continue
        if min_deger is not None and v < min_deger:
            print(f" En az {min_deger} olmalı.")
            continue
        if max_deger is not None and v > max_deger:
            print(f" En fazla {max_deger} olmalı.")
            continue
        return v


def _float_al(prompt: str, min_deger: float | None = None) -> float:
    while True:
        s = input(prompt).strip().replace(",", ".")
        try:
            v = float(s)
        except Exception:
            print(" Sayı gir.")
            continue
        if min_deger is not None and v < min_deger:
            print(f" En az {min_deger} olmalı.")
            continue
        return v


# ---------------------------
#   ÇIKTI FORMATLAMA (OKUNAKLI)
# ---------------------------
def _para(x: float) -> str:
    try:
        return f"{float(x):.2f} TRY"
    except Exception:
        return f"{x} TRY"


def _siparis_yazdir(order) -> None:
    oid = getattr(order, "get_id", lambda: getattr(order, "id", "-"))()
    owner = getattr(order, "get_owner", lambda: getattr(order, "owner", "-"))()
    status = getattr(order, "get_status", lambda: getattr(order, "status", "-"))()
    created_at = getattr(order, "get_created_at", lambda: getattr(order, "created_at", "-"))()

    toplam = getattr(order, "toplam_tutar", lambda: 0.0)()
    indirim_orani = getattr(order, "get_discount_rate", lambda: 0.0)()
    indirim_tutar = getattr(order, "indirim_tutari", lambda: 0.0)()
    odenecek = getattr(order, "odenecek_tutar", lambda: toplam)()
    paid = getattr(order, "get_paid_amount", lambda: 0.0)()

    items = getattr(order, "get_items", lambda: [])()
    notes = getattr(order, "get_notes", lambda: "")()

    _sep()
    print("🧾 SİPARİŞ OLUŞTURULDU")
    print(f"• Sipariş No   : {oid}")
    print(f"• Kişi         : {owner}")
    print(f"• Durum        : {status}")
    print(f"• Tarih        : {created_at}")

    print("\n Ürünler")
    if not items:
        print("  - (ürün yok)")
    else:
        for u in items:
            uid = getattr(u, "get_id", lambda: getattr(u, "id", "-"))()
            ad = getattr(u, "get_name", lambda: getattr(u, "name", "-"))()
            fiyat = getattr(u, "get_price", lambda: getattr(u, "price", 0.0))()
            print(f"  - [{uid}] {ad} ({_para(fiyat)})")

    print("\n Özet")
    print(f"• Toplam       : {_para(toplam)}")
    try:
        if indirim_orani and float(indirim_orani) > 0:
            print(f"• İndirim Oranı : %{int(float(indirim_orani) * 100)}")
            print(f"• İndirim Tutar : {_para(indirim_tutar)}")
    except Exception:
        pass
    print(f"• Ödenecek     : {_para(odenecek)}")
    print(f"• Ödenen       : {_para(paid)}")

    if isinstance(notes, str) and notes.strip():
        print("\n Not")
        print(f"• {notes.strip()}")


def _odeme_sonucu_yazdir(tx) -> None:
    tid = getattr(tx, "get_id", lambda: getattr(tx, "id", "-"))()
    owner = getattr(tx, "get_owner", lambda: getattr(tx, "owner", "-"))()
    order_id = getattr(tx, "get_order_id", lambda: getattr(tx, "order_id", "-"))()
    amount = getattr(tx, "get_amount", lambda: getattr(tx, "amount", 0.0))()
    status = getattr(tx, "get_status", lambda: getattr(tx, "status", "-"))()
    method = getattr(tx, "get_method_type", lambda: getattr(tx, "method_type", "-"))()
    reason = getattr(tx, "get_failure_reason", lambda: getattr(tx, "failure_reason", ""))()
    created_at = getattr(tx, "get_created_at", lambda: getattr(tx, "created_at", "-"))()

    _sep()
    print(" ÖDEME SONUCU")
    print(f"• İşlem No     : {tid}")
    print(f"• Kişi         : {owner}")
    print(f"• Sipariş No   : {order_id}")
    print(f"• Tutar        : {_para(amount)}")
    print(f"• Yöntem       : {method}")
    print(f"• Durum        : {status}")
    print(f"• Tarih        : {created_at}")

    if isinstance(reason, str) and reason.strip() and reason != "-":
        print(f"• Sebep        : {reason.strip()}")


def _islemleri_liste_yazdir(baslik: str, islemler: list) -> None:
    _sep()
    print(baslik)
    if not islemler:
        print("• Kayıt yok.")
        return

    for tx in islemler:
        tid = getattr(tx, "get_id", lambda: getattr(tx, "id", "-"))()
        order_id = getattr(tx, "get_order_id", lambda: getattr(tx, "order_id", "-"))()
        amount = getattr(tx, "get_amount", lambda: getattr(tx, "amount", 0.0))()
        status = getattr(tx, "get_status", lambda: getattr(tx, "status", "-"))()
        method = getattr(tx, "get_method_type", lambda: getattr(tx, "method_type", "-"))()
        created_at = getattr(tx, "get_created_at", lambda: getattr(tx, "created_at", "-"))()
        reason = getattr(tx, "get_failure_reason", lambda: getattr(tx, "failure_reason", ""))()

        print(f"\n İşlem #{tid}")
        print(f"• Sipariş No : {order_id}")
        print(f"• Tutar      : {_para(amount)}")
        print(f"• Yöntem     : {method}")
        print(f"• Durum      : {status}")
        print(f"• Tarih      : {created_at}")
        if isinstance(reason, str) and reason.strip() and reason != "-":
            print(f"• Sebep      : {reason.strip()}")


def _kalan_tutar_yazdir(owner: str, nakit: CashPayment, kart: CreditCardPayment, cuzd: OnlineWalletPayment) -> None:
    _sep()
    print(" Kalan Tutar Özeti")

    print("\n Nakit")
    print(f"• Kişi        : {owner}")
    print(f"• Para Birimi : {nakit.get_currency()}")
    print(f"• Bakiye      : {_para(nakit.kullanilabilir_tutar())}")

    print("\n Kredi Kartı")
    try:
        kart_no = getattr(kart, "masked_card_no", lambda: "-")()
    except Exception:
        kart_no = "-"
    print(f"• Kişi        : {owner}")
    print(f"• Kart        : {kart_no}")
    print(f"• Para Birimi : {kart.get_currency()}")
    print(f"• Kalan Limit : {_para(kart.kullanilabilir_tutar())}")

    print("\n Online Cüzdan")
    try:
        w_id = getattr(cuzd, "masked_wallet_id", lambda: "-")()
    except Exception:
        w_id = "-"
    try:
        durum = "Aktif" if cuzd.get_aktif_mi() else "Pasif"
    except Exception:
        durum = "-"
    print(f"• Kişi        : {owner}")
    print(f"• Cüzdan      : {w_id}")
    print(f"• Durum       : {durum}")
    print(f"• Para Birimi : {cuzd.get_currency()}")
    print(f"• Bakiye      : {_para(cuzd.kullanilabilir_tutar())}")


# ---------------------------
#   SİSTEM OLUŞTURMA (GÜVENLİ)
# ---------------------------
def _kart_olustur_guvenli(owner: str, kart_limit: float) -> CreditCardPayment:
    # Kart başlığı sadece 1 kere gözüksün (yanlış girip tekrar denese bile)
    ilk_sefer = True
    while True:
        if ilk_sefer:
            _sep()
            print("Kredi Kartı Bilgileri")
            ilk_sefer = False

        card_no = _metin_al("Kart No (12-19 hane, sadece rakam): ").strip().replace(" ", "")
        card_holder = _isim_harf_al("Kart Sahibi Adı: ")
        expiry = _metin_al("SKT (MM/YY): ").strip()
        cvv = _metin_al("CVV (3-4 hane): ").strip()

        try:
            return CreditCardPayment(
                owner=owner,
                card_no=card_no,
                card_holder_name=card_holder,
                expiry_date=expiry,
                cvv=cvv,
                limit=kart_limit,
                currency="TRY",
            )
        except Exception as e:
            print(f" Kart bilgileri hatalı: {e}")
            tekrar = _evet_hayir_al("Kart bilgilerini tekrar girmek ister misin? (e/h): ")
            if not tekrar:
                print(" Kart olmadan devam ediliyor (limit=0).")
                return CreditCardPayment(
                    owner=owner,
                    card_no="123456789012",
                    card_holder_name="KART YOK",
                    expiry_date="01/30",
                    cvv="000",
                    limit=0.0,
                    currency="TRY",
                )


def _cuzdan_olustur_guvenli(owner: str, cuzd_bakiye: float) -> OnlineWalletPayment:
    ilk_sefer = True
    while True:
        if ilk_sefer:
            _sep()
            print("Online Cüzdan Bilgileri")
            ilk_sefer = False

        wallet_id = _metin_al("Cüzdan ID (en az 6 karakter, boşluk yok): ").strip()
        aktif = _evet_hayir_al("Cüzdan aktif mi? (e/h): ")

        try:
            return OnlineWalletPayment(
                owner=owner,
                wallet_id=wallet_id,
                balance=cuzd_bakiye,
                aktif_mi=aktif,
                currency="TRY",
            )
        except Exception as e:
            print(f" Cüzdan bilgileri hatalı: {e}")
            tekrar = _evet_hayir_al("Cüzdan bilgilerini tekrar girmek ister misin? (e/h): ")
            if not tekrar:
                print("⚠️ Cüzdan olmadan devam ediliyor (bakiye=0, pasif).")
                return OnlineWalletPayment(
                    owner=owner,
                    wallet_id="CUZDAN00",
                    balance=0.0,
                    aktif_mi=False,
                    currency="TRY",
                )


# ---------------------------
#   MENÜ / ÖDEME AKIŞI
# ---------------------------
def _urunleri_yaz(items: List[MenuItem]) -> None:
    if not items:
        print(" Menüde ürün yok.")
        return
    for u in items:
        print(f"- ID:{u.get_id()} | {u.get_name()} | {u.get_category()} | {u.get_price():.2f} TRY")


def _odeme_yontemi_sec(nakit: CashPayment, kart: CreditCardPayment, cuzd: OnlineWalletPayment):
    _sep()
    print(" Ödeme Yöntemi Seç")
    print("1) Nakit")
    print("2) Kredi Kartı")
    print("3) Online Cüzdan")
    sec = _secim_al("Seçim (1/2/3): ", {"1", "2", "3"})
    if sec == "1":
        return nakit
    if sec == "2":
        return kart
    return cuzd


def _tx_repo_ekle(servis: CafeteriaService, tx: PaymentTransaction) -> None:
    repo = getattr(servis, "_tx_repo", None)
    if repo is None:
        return
    fn = getattr(repo, "ekle", None) or getattr(repo, "add", None)
    if callable(fn):
        fn(tx)


def _order_repo_guncelle(servis: CafeteriaService, order: Order) -> None:
    repo = getattr(servis, "_order_repo", None)
    if repo is None:
        return
    fn = getattr(repo, "guncelle", None) or getattr(repo, "update", None)
    if callable(fn):
        try:
            fn(order)
        except Exception:
            pass


def _odeme_akisi(
    servis: CafeteriaService,
    owner: str,
    order: Order,
    nakit: CashPayment,
    kart: CreditCardPayment,
    cuzd: OnlineWalletPayment,
) -> None:
    tutar = order.odenecek_tutar() if hasattr(order, "odenecek_tutar") else order.toplam_tutar()

    while True:
        yontem = _odeme_yontemi_sec(nakit, kart, cuzd)

        # authorize
        try:
            yetki = yontem.authorize(tutar)
        except Exception as e:
            yetki = False
            hata = str(e)
        else:
            hata = ""

        if not yetki:
            tx = PaymentTransaction.basarisiz(
                owner=order.get_owner(),
                amount=tutar,
                currency=getattr(yontem, "get_currency", lambda: "TRY")(),
                method_type=yontem.__class__.__name__,
                reason=("Yetkilendirme başarısız." + (f" {hata}" if hata else "")),
                order_id=order.get_id(),
            )
            _tx_repo_ekle(servis, tx)
            _odeme_sonucu_yazdir(tx)

            print(" Ödeme başarısız: Yetersiz bakiye/limit veya yetkilendirme sorunu.")
            if not _evet_hayir_al("Başka yöntemle tekrar denensin mi? (e/h): "):
                # ödeme bitti (başarısız) → bakiye özeti yazdır
                _kalan_tutar_yazdir(owner, nakit, kart, cuzd)
                break
            continue

        # odeme_yap
        try:
            ok = yontem.odeme_yap(tutar)
            if ok is False:
                raise ValueError("Ödeme yöntemi ödemeyi reddetti.")
        except Exception as e:
            tx = PaymentTransaction.basarisiz(
                owner=order.get_owner(),
                amount=tutar,
                currency=getattr(yontem, "get_currency", lambda: "TRY")(),
                method_type=yontem.__class__.__name__,
                reason=f"Ödeme sırasında hata: {e}",
                order_id=order.get_id(),
            )
            _tx_repo_ekle(servis, tx)
            _odeme_sonucu_yazdir(tx)

            print(" Ödeme başarısız.")
            if not _evet_hayir_al("Başka yöntemle tekrar denensin mi? (e/h): "):
                _kalan_tutar_yazdir(owner, nakit, kart, cuzd)
                break
            continue

        # basarili
        tx = PaymentTransaction.basarili(
            owner=order.get_owner(),
            amount=tutar,
            currency=getattr(yontem, "get_currency", lambda: "TRY")(),
            method_type=yontem.__class__.__name__,
            order_id=order.get_id(),
        )
        _tx_repo_ekle(servis, tx)

        # sipariş güncelle
        try:
            order.set_status("PAID")
            order.set_paid_amount(tutar)
        except Exception:
            pass
        _order_repo_guncelle(servis, order)

        _odeme_sonucu_yazdir(tx)
        print("ÖDEME BAŞARILI!")

        # ödeme sonrası bakiye özeti
        _kalan_tutar_yazdir(owner, nakit, kart, cuzd)
        break


def _menuyu_repo_doldur(menu_repo: InMemoryMenuRepository) -> None:
    menu_repo.ekle(MenuItem(1, "Mercimek Çorbası", 18.0, "corba", True, tags=["vegan"], available_days=[1, 3, 5]))
    menu_repo.ekle(MenuItem(2, "Pilav", 22.0, "ana", True, tags=["glutensiz"], available_days=[1, 2, 3, 4, 5]))
    menu_repo.ekle(MenuItem(3, "Tavuk Sote", 55.0, "ana", True, tags=["protein"], available_days=[2, 4]))
    menu_repo.ekle(MenuItem(4, "Makarna", 30.0, "ana", True, tags=["klasik"], available_days=[1, 3]))
    menu_repo.ekle(MenuItem(5, "Ayran", 10.0, "icecek", True, tags=["sut"], available_days=[1, 2, 3, 4, 5]))
    menu_repo.ekle(MenuItem(6, "Salata", 16.0, "yan", True, tags=["hafif"], available_days=[2, 3, 5]))


# ---------------------------
#   MAIN
# ---------------------------
def main() -> None:
    _sep()
    print("Akıllı Kampüs - Modül 2 (Yemekhane / Sipariş / Ödeme)")

    owner = _ad_soyad_al("Ad Soyad : ")

    _sep()
    print("Başlangıç Para Bilgileri (Bu miktarlardan ödeme oldukça düşecek)")
    nakit_bakiye = _float_al("Nakit bakiye (TRY): ", min_deger=0.0)
    kart_limit = _float_al("Kredi kartı limiti (TRY): ", min_deger=0.0)
    cuzd_bakiye = _float_al("Online cüzdan bakiye (TRY): ", min_deger=0.0)

    # Repo'lar
    menu_repo = InMemoryMenuRepository()
    order_repo = InMemoryOrderRepository()
    tx_repo = InMemoryTransactionRepository()
    pay_repo = InMemoryPaymentRepository()

    _menuyu_repo_doldur(menu_repo)

    # Ödeme yöntemleri (kart bilgisi SADECE 1 kere burada sorulur)
    nakit = CashPayment(owner=owner, balance=nakit_bakiye, currency="TRY")
    kart = _kart_olustur_guvenli(owner, kart_limit)
    cuzd = _cuzdan_olustur_guvenli(owner, cuzd_bakiye)

    pay_repo.ekle(nakit)
    pay_repo.ekle(kart)
    pay_repo.ekle(cuzd)

    servis = CafeteriaService(menu_repo=menu_repo, order_repo=order_repo, tx_repo=tx_repo, payment_repo=pay_repo)

    # Ana döngü
    while True:
        _sep()
        print("Ne yapmak istiyorsun?")
        print("1) Okul yemeği (Haftalık menü)")
        print("2) Sipariş ver (ürün seç)")
        print("3) Çıkış")
        ana = _secim_al("Seçim (1/2/3): ", {"1", "2", "3"})

        if ana == "3":
            break

        if ana == "1":
            _sep()
            gun = _int_al("Hangi gün? (1=Pzt ... 5=Cuma): ", 1, 5)
            gun_adi = servis.gun_adi(gun)
            items = servis.menuyu_goster(gun, sadece_aktif=True)

            _sep()
            print(f" {gun_adi} Menüsü")
            _urunleri_yaz(items)

            toplam = sum(u.get_price() for u in items)
            print(f"\n Menü Toplam: {_para(toplam)}")

            uygun = _evet_hayir_al("Bu menü sizin için uygun mu? (e/h): ")
            if not uygun:
                print("↩ Ana menüye dönülüyor...")
                continue

            if not items:
                print(" Bugün için menü boş, ödeme yapılamaz.")
                continue

            urun_idleri = [u.get_id() for u in items]
            order = servis.siparis_olustur(owner=owner, urun_idleri=urun_idleri)

            _siparis_yazdir(order)
            _odeme_akisi(servis, owner, order, nakit, kart, cuzd)
            continue

        if ana == "2":
            _sep()
            print("Aktif Ürünler (Seçmek için ID kullanacaksın)")
            tum_aktif = servis.menu_listele(sadece_aktif=True)
            _urunleri_yaz(tum_aktif)

            if not tum_aktif:
                print(" Aktif ürün yok, sipariş veremezsin.")
                continue

            _sep()
            secim_txt = _metin_al("İstediğin ürün ID'leri (virgülle) örn: 2,5 : ")
            try:
                urun_idleri = [int(x.strip()) for x in secim_txt.split(",") if x.strip() != ""]
            except Exception:
                print(" ID'ler sayı olmalı.")
                continue

            if not urun_idleri:
                print(" En az 1 ürün seçmelisin.")
                continue

            secilen_items: List[MenuItem] = []
            try:
                for uid in urun_idleri:
                    u = servis.urun_getir(uid)
                    if u is None:
                        raise ValueError(f"Ürün bulunamadı: {uid}")
                    secilen_items.append(u)
            except Exception as e:
                print(f" Hata: {e}")
                continue

            _sep()
            print(" Seçilenler:")
            _urunleri_yaz(secilen_items)
            toplam = sum(u.get_price() for u in secilen_items)
            print(f"\nToplam: {_para(toplam)}")

            indirim_istiyor = _evet_hayir_al("Öğrenci indirimi %10 ister misin? (e/h): ")
            ind_oran = 0.10 if indirim_istiyor else 0.0

            notlar = input("Sipariş notu (boş bırakabilirsin): ").strip()

            onay = _evet_hayir_al("Siparişi oluşturup ödemeye geçelim mi? (e/h): ")
            if not onay:
                print("↩ Ana menüye dönülüyor...")
                continue

            try:
                order = servis.siparis_olustur(owner=owner, urun_idleri=urun_idleri)
            except Exception as e:
                print(f" Sipariş oluşturulamadı: {e}")
                continue

            try:
                if ind_oran > 0:
                    order.set_discount_rate(ind_oran)
                if notlar:
                    order.set_notes(notlar)
            except Exception:
                pass

            _siparis_yazdir(order)
            print(f"\n Ödenecek Tutar (indirime göre): {_para(order.odenecek_tutar())}")

            _odeme_akisi(servis, owner, order, nakit, kart, cuzd)
            continue

    # Demo sonu raporlar
    _islemleri_liste_yazdir(" İşlem Geçmişi (Tümü)", servis.islemleri_listele())
    _islemleri_liste_yazdir(" Sadece Başarılı İşlemler", servis.basarili_islemler())
    _islemleri_liste_yazdir(f" {owner} için İşlemler", servis.islemleri_listele(owner=owner))

    _kalan_tutar_yazdir(owner, nakit, kart, cuzd)

    _sep()
    print(" Demo bitti.")


if __name__ == "__main__":
    main()
