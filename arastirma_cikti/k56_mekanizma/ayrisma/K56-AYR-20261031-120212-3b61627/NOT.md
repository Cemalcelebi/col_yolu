# GEÇERSİZ koşu (commit 3b61627) — yalnız kayıt için saklandı

Kod incelemesi (31 Ekim) bu koşuda iki sorun buldu: (1) İÇ dizi tablosundaki "kesilme nedeni" dönem dışı (2024) etiketli günün getirisine bakıyordu
(betimleyici, karar sütunu değil, ama İÇ → BAĞIMSIZ dolaylı erişim); (2) koşu özeti JSON'u yazılırken çöktü, SON.json oluşmadı. Geçerli koşu ayrisma/SON.json.
