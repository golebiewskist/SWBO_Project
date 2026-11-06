# EventHub: System Zarządzania Wydarzeniami (SWBO)

> **Platforma społecznościowa do planowania, publikowania i koordynacji wydarzeń**  
> **Autor:** Stanisław Gołębiewski  
> **Stos:** Python 3, Django 5, PostgreSQL 17 / SQLite, Docker, Bootstrap, FontAwesome  

---

## 📌 O Projekcie

**EventHub** to aplikacja webowa zaprojektowana do kompleksowej obsługi wydarzeń i spotkań. System oferuje zaawansowany model uprawnień i ról użytkowników, harmonogramowanie imprez, kategoryzację oraz system zaproszeń.

---

## 🛠️ Funkcjonalności

- **Model Ról i Uprawnień (`users/models.py`):**
  - Rozszerzony profil użytkownika (`UserProfile`) ze specjalnymi uprawnieniami organizatora (`can_create_events`).
  - Bezpieczna rejestracja, edycja profilu, zmiana haseł.
- **Zarządzanie Wydarzeniami (`EventHub/models.py`):**
  - Tworzenie, edycja i publikowanie wydarzeń z określeniem daty rozpoczęcia, lokalizacji, limitu miejsc i statusu.
  - Kolorystyczne tagowanie kategorii wydarzeń.
- **Wyszukiwanie i Filtrowanie:**
  - Dynamiczne wyszukiwanie po tytułach, opisach i kategoriach.
- **Gotowość do wdrożenia:**
  - Skonteneryzowane środowisko z bazą danych PostgreSQL 17 (`docker-compose.yaml`).

---

## 🚀 Uruchomienie

### Docker Compose:
```bash
docker compose up -d --build
```
Aplikacja dostępna pod adresem: `http://localhost:8000`
