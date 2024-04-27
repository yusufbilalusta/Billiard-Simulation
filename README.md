# Top Simülasyonu Projesi

Bu proje, bir masaüstü simülasyonu oluşturmak için Python kullanarak bir dizi sınıf içerir. Simülasyon, bir masa üzerindeki topların hareketini modellemektedir.

## Kurulum

1. Projeyi bilgisayarınıza klonlayın:

    ```bash
    git clone https://github.com/kullanici/adresi.git
    ```

2. Gerekli kütüphaneleri yükleyin:

    ```bash
    pip install numpy matplotlib
    ```

## Kullanım

- `Base`, `Intermediate`, `Advanced` ve `Expert` olmak üzere dört farklı sınıf bulunmaktadır. Her biri farklı yetenek düzeylerini temsil eder.

- Simülasyon başlatmak için herhangi bir sınıfın `Simulation` metodunu çağırın. Örneğin:

    ```python
    from top_simulasyonu import Intermediate

    sim = Intermediate()
    sim.Simulation(limit=500, duration=0.1, name="IntermediateOutput")
    ```

- `limit` parametresi, simülasyonun kaç adım süreceğini belirtir.
- `duration` parametresi, her adımın ne kadar süreceğini belirtir.
- `name` parametresi, çıktı dosyasının adını belirtir.

## Katkılar

Katkı yapmak isterseniz, lütfen yeni bir dal oluşturun ve değişikliklerinizle birlikte ana dalı birleştirme talebi (pull request) gönderin. Değişikliklerinizin kabul edilmesi için uygun testlerin geçmesine ve kodun proje standartlarına uygun olmasına dikkat edin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
