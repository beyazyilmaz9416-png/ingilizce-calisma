import streamlit as st
import random
import os

st.set_page_config(page_title="İngilizce Çalışması", page_icon="📚", layout="wide")

KELIME_DOSYA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kelimeler.txt')

st.markdown("""
<style>
    .soru { font-size: 26px; font-weight: bold; color: #2980b9; text-align: center; padding: 20px; }
    .mod  { font-size: 18px; text-align: center; color: #8e44ad; font-weight: bold; margin-bottom: 8px; }
    .skor { font-size: 15px; text-align: center; color: #2c3e50; margin-bottom: 10px; }
    input { autocomplete: off !important; }
</style>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('input').forEach(i => i.setAttribute('autocomplete','off'));
    });
</script>
""", unsafe_allow_html=True)


def kelime_yukle():
    soru = {}
    try:
        with open(KELIME_DOSYA, 'r', encoding='utf-8') as f:
            for satir in f:
                satir = satir.strip()
                if ':' in satir:
                    ing, tur = satir.split(':', 1)
                    ing = ing.strip().lower()
                    tur = tur.strip().lower()
                    if ing and tur:
                        soru[ing] = tur
    except:
        soru = {'hello': 'merhaba', 'world': 'dünya'}
    return soru


def kelime_kaydet(kelimeler):
    with open(KELIME_DOSYA, 'w', encoding='utf-8') as f:
        for ing, tur in kelimeler.items():
            f.write(f"{ing}:{tur}\n")


def yeni_soru_sec():
    s = st.session_state
    s.sonuc = ""
    s.sonuc_tipi = ""
    s.cevap_verildi = False

    if s.tekrar_modu:
        if not s.yanlis_kelimeler:
            s.tekrar_bitti = True
            return
        ing = random.choice(list(s.yanlis_kelimeler.keys()))
        # tekrar modunda ing→tur sor
        s.mevcut_soru = ing
        s.dogru_cevap = s.yanlis_kelimeler[ing]
        return

    if s.soru_no > 50 and s.mod == "ing_tur":
        s.mod = "tur_ing"
        s.soru_no = 1

    if s.soru_no > 50 and s.mod == "tur_ing":
        s.oyun_bitti = True
        return

    ing = random.choice(list(s.kelimeler.keys()))
    tur = s.kelimeler[ing]

    if s.mod == "ing_tur":
        s.mevcut_soru = ing      # ekranda İngilizce
        s.dogru_cevap = tur      # beklenen cevap Türkçe
    else:
        s.mevcut_soru = tur      # ekranda Türkçe
        s.dogru_cevap = ing      # beklenen cevap İngilizce


def state_baslat():
    if 'baslatildi' not in st.session_state:
        st.session_state.baslatildi = True
        st.session_state.kelimeler = kelime_yukle()
        st.session_state.dogru = 0
        st.session_state.yanlis = 0
        st.session_state.bos = 0
        st.session_state.soru_no = 1
        st.session_state.mod = "ing_tur"
        st.session_state.tekrar_modu = False
        st.session_state.yanlis_kelimeler = {}
        st.session_state.sonuc = ""
        st.session_state.sonuc_tipi = ""
        st.session_state.oyun_bitti = False
        st.session_state.tekrar_bitti = False
        st.session_state.cevap_verildi = False
        st.session_state.mevcut_soru = ""
        st.session_state.dogru_cevap = ""
        st.session_state.input_key = 0
        yeni_soru_sec()


def cevabi_isle(cevap):
    s = st.session_state
    cevap = cevap.strip().lower()
    if not cevap:
        return False

    dogru_cevaplar = [c.strip() for c in s.dogru_cevap.split(',')]

    if cevap in dogru_cevaplar:
        s.dogru += 1
        s.sonuc = "✅ Doğru!"
        s.sonuc_tipi = "success"
        if s.tekrar_modu and s.mevcut_soru in s.yanlis_kelimeler:
            del s.yanlis_kelimeler[s.mevcut_soru]
    else:
        s.yanlis += 1
        s.sonuc = f"❌ Yanlış! Doğru cevap: **{s.dogru_cevap}**"
        s.sonuc_tipi = "error"
        if not s.tekrar_modu:
            s.yanlis_kelimeler[s.mevcut_soru] = s.dogru_cevap

    if not s.tekrar_modu:
        s.soru_no += 1
        if s.yanlis >= 20:
            s.oyun_bitti = True
            return True

    s.cevap_verildi = True
    s.input_key += 1
    return True


def on_input_change():
    s = st.session_state
    deger = s.get(f"cevap_{s.input_key}", "").strip()
    if s.cevap_verildi:
        yeni_soru_sec()
        s.input_key += 1
    elif deger:
        cevabi_isle(deger)


def gec():
    s = st.session_state
    s.bos += 1
    s.sonuc = f"⏭ Geçtiniz. Doğru cevap: **{s.dogru_cevap}**"
    s.sonuc_tipi = "warning"
    if not s.tekrar_modu:
        s.yanlis_kelimeler[s.mevcut_soru] = s.dogru_cevap
        s.soru_no += 1
    s.cevap_verildi = True
    s.input_key += 1


def yeniden_basla():
    s = st.session_state
    s.dogru = 0
    s.yanlis = 0
    s.bos = 0
    s.soru_no = 1
    s.mod = "ing_tur"
    s.tekrar_modu = False
    s.yanlis_kelimeler = {}
    s.oyun_bitti = False
    s.tekrar_bitti = False
    s.sonuc = ""
    s.sonuc_tipi = ""
    s.cevap_verildi = False
    s.input_key += 1
    yeni_soru_sec()


def yanlis_tekrar():
    s = st.session_state
    s.dogru = 0
    s.yanlis = 0
    s.bos = 0
    s.tekrar_modu = True
    s.oyun_bitti = False
    s.tekrar_bitti = False
    s.sonuc = ""
    s.cevap_verildi = False
    s.input_key += 1
    yeni_soru_sec()


# ── BAŞLAT ────────────────────────────────────────────────────────────────
state_baslat()
s = st.session_state

# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ➕ Kelime Ekle")
    yeni_ing = st.text_input("İngilizce", key="yeni_ing", placeholder="örn: apple").strip().lower()
    yeni_tur = st.text_input("Türkçe", key="yeni_tur", placeholder="örn: elma").strip().lower()

    if st.button("Ekle", use_container_width=True, type="primary"):
        if yeni_ing and yeni_tur:
            if yeni_ing not in s.kelimeler:
                s.kelimeler[yeni_ing] = yeni_tur
                kelime_kaydet(s.kelimeler)
                st.success(f"✅ '{yeni_ing}: {yeni_tur}' eklendi!")
            else:
                st.warning(f"'{yeni_ing}' zaten mevcut.")
        else:
            st.error("Her iki alanı da doldurun.")

    st.divider()
    st.markdown("## ✏️ Kelime Düzenle / Sil")
    if s.kelimeler:
        secili = st.selectbox("Kelime seç", options=sorted(s.kelimeler.keys()), key="secili_kelime")
        duzenle_tur = st.text_input("Türkçe karşılık", value=s.kelimeler.get(secili, ""), key="duzenle_tur")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Güncelle", use_container_width=True):
                if duzenle_tur.strip():
                    s.kelimeler[secili] = duzenle_tur.strip().lower()
                    kelime_kaydet(s.kelimeler)
                    st.success("Güncellendi!")
                else:
                    st.error("Boş bırakılamaz.")
        with col_b:
            if st.button("Sil", use_container_width=True):
                del s.kelimeler[secili]
                kelime_kaydet(s.kelimeler)
                st.rerun()

    st.divider()
    st.caption(f"📖 Toplam kelime: {len(s.kelimeler)}")


# ── ANA EKRAN ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#ff4b4b; color:white; text-align:center; padding:12px; border-radius:8px; font-size:18px; font-weight:bold; margin-bottom:10px;'>
    ⚠️ DİKKAT: Tarayıcınızın otomatik çeviri özelliğini KAPATIN!
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#2c3e50;'>📚 İNGİLİZCE ÇALIŞMASI</h2>", unsafe_allow_html=True)

if s.tekrar_modu:
    mod_text = "🔁 YANLIŞ KELİMELER TEKRARI"
elif s.mod == "ing_tur":
    mod_text = "🇬🇧 İNGİLİZCE → TÜRKÇE"
else:
    mod_text = "🇹🇷 TÜRKÇE → İNGİLİZCE"

st.markdown(f"<div class='mod'>{mod_text}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='skor'>✅ Doğru: {s.dogru} &nbsp;|&nbsp; ❌ Yanlış: {s.yanlis} &nbsp;|&nbsp; ⏭ Boş: {s.bos}</div>", unsafe_allow_html=True)
st.divider()

# Oyun bitti
if s.oyun_bitti:
    if s.dogru >= 80:
        mesaj = "🏆 MÜKEMMEL! Çok başarılısınız!"
    elif s.dogru >= 60:
        mesaj = "👍 İYİ! Devam edin!"
    else:
        mesaj = "📖 Daha çok çalışmanız gerekiyor."
    st.success(mesaj)
    st.info(f"Toplam Doğru: {s.dogru} | Toplam Yanlış: {s.yanlis} | Toplam Boş: {s.bos}")
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 Yeniden Başla", on_click=yeniden_basla, use_container_width=True)
    with col2:
        if s.yanlis_kelimeler:
            st.button("🔁 Yanlışları Tekrarla", on_click=yanlis_tekrar, use_container_width=True)
    st.stop()

# Tekrar bitti
if s.tekrar_bitti:
    st.success(f"🎉 Tüm yanlış kelimeleri doğru yaptınız! Doğru: {s.dogru} | Yanlış: {s.yanlis}")
    st.button("🔄 Ana Menüye Dön", on_click=yeniden_basla, use_container_width=True)
    st.stop()

# ── SORU ──────────────────────────────────────────────────────────────────
if s.tekrar_modu:
    soru_text = f"TEKRAR: '{s.mevcut_soru}' ne demek?"
elif s.mod == "ing_tur":
    soru_text = f"{s.soru_no}. '{s.mevcut_soru}' ne demek?"
else:
    soru_text = f"{s.soru_no}. '{s.mevcut_soru}' İngilizcesi?"

st.markdown(f"<div class='soru'>{soru_text}</div>", unsafe_allow_html=True)

# Sonuç göster
if s.cevap_verildi:
    if s.sonuc_tipi == "success":
        st.success(s.sonuc)
    elif s.sonuc_tipi == "error":
        st.error(s.sonuc)
    else:
        st.warning(s.sonuc)
    st.caption("Enter'a basarak sonraki soruya geçebilirsiniz.")

# autocomplete kapalı input
st.markdown("""
<style>
    input[data-testid="stTextInput"] { autocomplete: off !important; }
</style>""", unsafe_allow_html=True)

st.text_input(
    "Cevap",
    key=f"cevap_{s.input_key}",
    label_visibility="collapsed",
    placeholder="Cevabınızı yazıp Enter'a basın..." if not s.cevap_verildi else "Sonraki soru için Enter'a basın...",
    on_change=on_input_change,
    autocomplete="off"
)

col1, col2, col3 = st.columns(3)
with col1:
    if s.cevap_verildi:
        if st.button("▶ Sonraki Soru", use_container_width=True, type="primary"):
            yeni_soru_sec()
            s.input_key += 1
            st.rerun()
    else:
        if st.button("✅ Cevapla", use_container_width=True, type="primary"):
            cevabi_isle(s.get(f"cevap_{s.input_key}", ""))
            st.rerun()
with col2:
    if st.button("⏭ Geç", use_container_width=True, on_click=gec):
        pass
with col3:
    if st.button("🔄 Yeniden Başla", use_container_width=True, on_click=yeniden_basla):
        pass
