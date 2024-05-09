def sembol_tablosu_olustur(girdi_dosyasi):
    sembol_tablosu = {}
    locctr = 0
    baslangic_adresi = None

    # Girdi dosyasından tüm satırları okuma
    with open(girdi_dosyasi, 'r') as dosya:
        satirlar = dosya.readlines()

    # Ara dosya oluşturma ve işleme başlama
    with open('ara_dosya.txt', 'w') as ara_dosya:
        baslangic_bulundu = False

        for satir in satirlar:
            satir = satir.strip()

            if not satir or satir.startswith('.'):  # Yorum satırlarını ve boş satırları geç
                continue

            bolumler = satir.split()
            if not baslangic_bulundu:
                if bolumler[1] == 'START':
                    locctr = int(bolumler[2], 16)
                    baslangic_adresi = locctr
                    ara_dosya.write(f'{hex(locctr)[2:].upper()} {satir}\n')
                    baslangic_bulundu = True
                else:
                    raise ValueError("Dosya 'START' komutu ile başlamalı")
                continue

            if bolumler[1] == 'END':
                ara_dosya.write(f'{satir}\n')
                break

            etiket = bolumler[0] if len(bolumler) == 3 else None
            islem_kodu = bolumler[1] if etiket else bolumler[0]
            operand = bolumler[2] if etiket else bolumler[1]

            # Etiket işleme ve sembol tablosuna ekleme
            if etiket:
                if etiket in sembol_tablosu:
                    raise ValueError(f'Tekrar eden sembol hatası: {etiket}')
                sembol_tablosu[etiket] = hex(locctr)[2:].upper()

            # 'locctr' güncelleme
            if islem_kodu in ('WORD', 'RESW', 'RESB'):
                locctr += 3 if islem_kodu == 'WORD' else int(operand) * (3 if islem_kodu == 'RESW' else 1)
            elif islem_kodu == 'BYTE':
                if operand.startswith('X'):
                    locctr += (len(operand) - 3) // 2
                elif operand.startswith('C'):
                    locctr += len(operand) - 3
                else:
                    raise ValueError(f'Geçersiz BYTE formatı: {operand}')
            else:
                locctr += 3  # Diğer durumlar için sabit uzunluk

            ara_dosya.write(f'{hex(locctr)[2:].upper()} {satir}\n')

    # Sembol tablosunu dosyaya yazma
    with open('sembol_tablosu.txt', 'w') as sembol_dosya:
        for sembol, adres in sembol_tablosu.items():
            sembol_dosya.write(f'{sembol} {adres}\n')

# Kullanıcı arayüzü
if __name__ == "__main__":
    girdi_dosyasi = input("Lütfen girdi dosyasının adını giriniz: ")
    try:
        sembol_tablosu_olustur(girdi_dosyasi)
        print('Sembol tablosu oluşturuldu')
    except Exception as hata:
        print(f'Hata: {hata}')

