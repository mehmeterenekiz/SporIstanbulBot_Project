Günlük hayatımda karşılaştığım bir soruna çözüm bulmak amacıyla Python üzerinde OpenCV ve Selenium gibi güçlü kütüphanleri kullanarak gerçekleştirdiğim bir bot projesidir.

Bu Projede daha öncesinden edinilen görüntü işleme ile ilgi bilgi birkimi web siteler üzerinde botlara karşı önlem amacıyla kullanılan Captcha doğrulama kodlarını aşmak için kullanıldı ve başarılı bir şekilde gerçekleştirildi. Eğer istenirse ekran kartı ile entegre bir şekilde çalışılarak metni görselde okuma işlemi daha hızlı yapılabilir.

İlgili Captchalarda görüntü işleme işlemleri uygulandıktan sonra PaddleOcr gibi yazıları okumaya olanak sağlayan yapay zeka kullanılarak görseldeki metin başarılı bir şekilde okundu.

Görselden okunan kod Selenium kütüphanesindeki fonksiyonlar yardımıyla doğrulama kodu alanına yazdırıldı, ilgili rezervasyon işlemleri yapıldı ve ödeme sisteminde kart bilgileri girilerek ödeme aşaması tamamlandı.

İlerleyen zamanlarda daha otamatik bir şekilde çalışabilmek adına banka tarafından cep telefonuna gönderilen doğrulama kodunu bota aktarabilmek için bir api geliştirilecektir.
