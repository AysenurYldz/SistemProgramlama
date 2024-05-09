# SIC Assembly Program İşleyici ve Sembol Tablosu Oluşturucu
### Ayşenur Yıldız B200109026

Bu Python betiği, SIC (Simplified Instructional Computer) assembly programlarını işleyen ve sembol tablosu oluşturan bir araçtır. 
İlk geçiş algoritması kullanılarak, girdi olarak verilen SIC assembly program dosyasını okur, sembol tablosunu oluşturur ve 
ara dosyaya yazarak programın başlangıç ve bitiş adreslerini belirler.

## Kullanım

Programı çalıştırmak için terminal üzerinden programın olduğu dosyaı kaynak alıp main.py dosyasını çalıştırın.

# Örnek Kullanım
```python
(base)bt@a$ conda actıvate env1
(base)bt@a$ python3 main.py
Lütfen girdi dosyasının adını giriniz: girdi.txt
Sembol tablosu oluşturuldu
```

Program, sembol tablosunu oluşturacak ve sembol_tablosu.txt dosyasına yazacaktır. Ayrıca, ara dosya ara_dosya.txt içinde geçici bir işlem dosyası oluşturacaktır.

```python
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

```

## Program Açıklaması

Bu Python programı, bir SIC/XE assembly programındaki sembollerin bellek adreslerini hesaplayarak sembol tablosunu oluşturur. 
İşlevselliğini adım adım açıklamak için aşağıdaki adımları takip edebiliriz:

sembol_tablosu_olustur fonksiyonu, girdi olarak aldığı dosyadaki SIC/XE assembly kodunu işleyerek sembol tablosunu oluşturur.
sembol_tablosu adlı boş bir sözlük oluşturulur. Bu sözlük, sembollerin bellek adreslerini saklamak için kullanılacaktır.
locctr ve baslangic_adresi adlı değişkenler sıfıra eşitlenir. locctr, programın bellek adresini tutar. baslangic_adresi, programın başlangıç adresini tutar.
Girdi dosyası (girdi_dosyasi) okunur ve her satır satirlar adlı bir liste içinde saklanır.
ara_dosya.txt adında bir dosya oluşturulur ve yazma modunda açılır. Bu dosyaya işlenmiş her satır yazılacaktır.
baslangic_bulundu adlı bir bayrak oluşturulur ve başlangıç adresinin bulunup bulunmadığını belirlemek için kullanılır. Başlangıç adresi bulunduğunda bu bayrak True olarak ayarlanır.
Satırlar üzerinde döngü oluşturulur. Her satır işlenirken önce boşluklar ve yorum satırları kontrol edilir (strip ve `startswith('.')). Boş veya yorum satırıysa işleme devam edilmez.
Başlangıç adresi henüz bulunmadıysa (not baslangic_bulundu), satırın ikinci bölümüne (bolumler[1]) bakarak başlangıç adresi kontrol edilir. Eğer satırın ikinci bölümü 'START' ise, programın başlangıç adresi (locctr) olarak belirtilen adres (bolumler[2]) atanır. Başlangıç adresi bulunduktan sonra, ara dosyaya başlangıç satırı yazılır ve baslangic_bulundu bayrağı True olarak ayarlanır.
Eğer başlangıç adresi bulunduysa, işlenecek komutlar incelenir. Satırın ilk bölümü bir etiketi temsil ediyorsa, bu etiket sembol tablosuna eklenir. Ardından, işlem kodu ve operand belirlenir.
locctr güncellenir. Eğer işlem kodu 'WORD', 'RESW' veya 'RESB' ise, bellek adresi 3 artırılır veya operandın değerine göre artırılır. Eğer işlem kodu 'BYTE' ise, operandın formatına göre bellek adresi güncellenir. Diğer durumlarda ise bellek adresi sabit olarak 3 artırılır.
Ara dosyaya işlenmiş satır ve güncellenmiş bellek adresi yazılır.
Eğer işlenen satırın işlem kodu 'END' ise, döngü sonlandırılır ve ara dosyaya 'END' satırı yazılır.
Sembol tablosu, sembol_tablosu.txt adında bir dosyaya yazılır. Bu dosyaya her bir sembol ve onun bellek adresi yazılır.
Kullanıcı arayüzü bölümünde, kullanıcıdan girdi dosyasının adı alınır. sembol_tablosu_olustur fonksiyonu çağrılır ve sembol tablosu oluşturulduktan sonra kullanıcıya bilgi verilir veya hata durumunda hata mesajı gösterilir.

## Örnek Girdi
Girdi dosyası, SIC assembly programını içermelidir. Örnek bir girdi dosyası aşağıdaki gibi olabilir:

```assembly
FIRST    START    1000
         LDA      FIRST
         STA      ALPHA
         LDCH     #5
         STCH     C1
         J        LOOP
ALPHA    BYTE     C'EOF'
C1       RESB     1
LOOP     J        LOOP
         END      FIRST
```
		 
START 1000: Programın başlangıç adresini belirtir. Bellek boyutu üzerinde bir etkisi yoktur.
LDA FIRST: FIRST etiketindeki bellek hücresindeki değeri yükler ve akümülatöre (A) kaydeder. Bu bir Format 3 komutudur (3 byte).
STA ALPHA: Akümülatördeki değeri ALPHA etiketindeki bellek hücresine kaydeder. Bu da bir Format 3 komutudur (3 byte).
LDCH #5: Akümülatöre 5 değerini yükler ve en düşük byte'ına kaydeder. Bu da bir Format 3 komutudur (3 byte).
STCH C1: Akümülatörün en düşük byte'ını C1 etiketindeki bellek hücresine kaydeder. Bu da bir Format 3 komutudur (3 byte).
J LOOP: Programı LOOP etiketine atlattığı sonsuz bir döngü oluşturur. Bu da bir Format 3 komutudur (3 byte).
ALPHA BYTE C'EOF': ALPHA etiketine 'EOF' karakter dizisini (End of File) atar. 'EOF' karakter dizisi için 3 byte (her karakter 1 byte).
C1 RESB 1: C1 etiketine 1 byte'lık boş bellek alanı ayrılır.
LOOP J LOOP: Programı tekrar LOOP etiketine atlar, sonsuz bir döngü oluşturur. Bu da bir Format 3 komutudur (3 byte).
END FIRST: Programın sonunu belirtir. Bellek boyutu üzerinde bir etkisi yoktur.		 
		 

## Çıktı
Program, sembol tablosunu ve ara dosyayı oluşturacak ve çıktı olarak program uzunluğunu verecektir. Ayrıca, oluşturulan 
sembol tablosu sembol_tablosu.txt dosyasına yazılacaktır. Ara dosya, geçici bir işlem dosyasıdır ve kullanıcı tarafından kullanılmaz.

FIRST — 1000 (Program başlangıç adresi)
ALPHA — 100F (BYTE talimatından önce toplam 15 byte talimat var)
C1 — 1012 (ALPHA'dan sonra 3 byte)
LOOP — 1013 (C1'den sonra 1 byte)

Örnek sembol tablosu çıktısı:
```assembly

ALPHA — 100F 
C1 — 1012 
LOOP — 1013 
```
