# Discord Server Cloner v3

Discord sunucularını kopyalamak için gelişmiş araç. Kategoriler, kanallar, roller ve emojileri tamamen kopyalar.

## Ozellikler

- Sunucu profili (isim + ikon) kopyalama
- Kategori, kanal (text/voice) kopyalama
- Rol kopyalama
- Emoji kopyalama
- Anlik progress bar
- Tek tusla y/n cevaplama (Enter gerekmez)
- Ayarlari kaydetme

## Kurulum

```bash
git clone https://github.com/Memati8383/discord_server_cloner.git
cd discord_server_cloner
python main.py
```

## Kullanim

1. Discord hesabina gir, tokenini al
2. `python main.py` ile baslat
3. Tokeni gir (ilk seferde kaydedilir)
4. Ayarlari yap (hangi ogeler kopyalansin)
5. Hedef sunucu ID'sini gir (önce bos sunucu olustur)
6. Kaynak sunucu ID'sini gir
7. Otomatik kopyalama baslar

## Token Alma

1. Tarayicida `discord.com` ac, hesabina gir
2. F12 -> Network sekmesi
3. Sayfayi yenile, herhangi bir istege tikla
4. Request Headers > `authorization:` degeri tokenin

## Uyari

- Self-bot kullanimi Discord ToS'a aykiri, hesabin banlanabilir
- **Yan hesap** ile kullanman tavsiye edilir
- Tokenini kimseyle paylasma

## Gereksinimler

- Python 3.8+
- discord.py-self, rich, aiohttp (otomatik kurulur)