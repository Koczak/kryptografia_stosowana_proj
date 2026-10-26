MATERIAŁY DO KURSU:
   
Wykłady Ostatnia modyfikacja: B. Sawicki 20.01.2025 13:07
Architektura kryptowaluty. Wyzwania i algorytmy. Przykład SimpleCoin. https://github.com/sawickib/simplecoin/
Podstawy współczesnej kryptografii. Wprowadzenie do teorii informacji. Liczby losowe. Entropia. Szyfr doskonały.
Kryptograficzne funkcje skrótu.
Losowanie i szyfrowanie (algorytmy strumieniowe)
Algorytmy asymetryczne. Artmetyka modularna
Algorytmy asymetryczne: Szyfr plecakowy. RSA.
Algorytmy asymetryczne: Elgamal - szyfrowanie, podpis
Algorytmy asymetryczne: Artmetyka punktów na krzywych eliptycznych.
Algorytmy asymetryczne: ECC.
Podpis cyfrowy. Dystrybucja kluczy publicznych.
Protokoły uzgadniania kluczy, dzielenia tajemnicy i inne
Algorytmy szyfrowania symetrycznego, blokowego.
Protokoły uwierzytelniania użytkowników i systemów.
Szyfrowanie homomorficzne.
Wprowadzenie do kryptografii opartej na kratach.
1.	egz2024_0.pdf (44,3 kb)	B. Sawicki, 20.01.2025 13:02	
2.	Notatki2022.zip (14815,2 kb)	B. Sawicki, 6.02.2022 17:55	
   
Projekt własnej kryptowaluty (Aktualizacja: 06.10.2026) Ostatnia modyfikacja: P. Zawadzki 6.10.2026 11:34
Założenia
Budujemy system kryptowaluty, który będzie implementował podstawowy zestaw funkcji w oparciu o technologię rejestru rozproszonego i łańcucha bloków (blockchain).

Technologia
Zalecamy wykorzystanie środowiska języka JavaScript, ale możliwe są również inne rozwiązania (np. Python).

Komunikacja z użytkownikiem może być zrealizowana w dowolny sposób i nie będzie przedmiotem oceny.

Niezbędne jest natomiast oddzielenie węzła sieci (Node) od portfela (Wallet), który jest klientem węzła sieci i przy jego pomocy komunikuje się z nią.

Organizacja
Praca samodzielnie. Repozytorium kodu musi być dostępne na GitHub-ie, a kamienie milowe oznaczone odpowiednimi tagami: MILESTONE_1, MILESTONE_2, MILESTONE_3, MILESTONE_4.
Spotkania oceniające kamienie milowe są realizowane w trybie stacjonarnym. W pozostałych tygodniach terminy konsultacyjne.

Zasady oceny
Każdy etap oceniany będzie w skali 0-10 pkt.
Dodatkowe 10 pkt zostanie przyznane na podstawie sprawozdania końcowego.
Sumaryczna ocena to maks. 50 pkt.

Hrmonogram
Sieć peer-to-peer i bezpieczny portfel (10p) [27.10.2026 r.]
Tworzenie cyfrowych tożsamości
Bezpieczne przechowywanie kluczy w cyfrowym portfelu
Uruchomienie i rejestracja węzła sieci (nawiązanie komunikacji z innymi węzłami)
Prosty łańcuch bloków (10p) [17.11.2026 r.]
Tylko jeden górnik
Tworzenie bloków
Ustalenie protokołu wymiany danych o nowych blokach
Implementacja weryfikacji bloków pobieranych od innych węzłów
Transakcje przekazania środków (10p) [08.12.2026 r.]
Tworzenie transakcji.
Pierwszą transakcją w bloku powinna być transakcja coinbase tworząca nowe "monety"
Osiągnięcie konsensusu metodą proof-of-work
Walidacja transakcji pod kątem double-spending
Obliczanie aktualnych sald na kontach
Kopanie asynchroniczne (10p) [12.01.2027 r.]
Wielu górników
Obsługa forków oraz orphan block
Eksperyment: jak sieć zachowa się, gdy złośliwy węzeł będzie wymuszać tworzenie forków?
Sprawozdanie końcowe (10p) [26.01.2027 r.]
Sprawozdanie końcowe z projektu w formie pliku PDF powinno zostać umieszczone do piętnastego tygodnia w systemie ISOD. Powinno zawierać następujące elementy:

ogólna architektura i funkcjonalność systemu,
przedstawienie algorytmów kryptograficznych zastosowanych w projekcie (długości kluczy, implementacje, itp.) oraz uzasadnienia dla takiego wyboru,
wyniki analiz bezpieczeństwa i symulacji jego zachowania podczas różnych zaburzeń (ataków);
przykładowe scenariusze:

nieuczciwy węzeł,
grupa węzłów działająca w zmowie,
awaria łącza danych,
ogromna dysproporcja pomiędzy zasobami węzłów,
skuteczny atak na jeden algorytm kryptograficzny,
awaria danych w jednym z węzłów,
zgubienie hasła do klucza prywatnego
Celem sprawozdania jest obiektywne przeanalizowanie implementacji. Liczba ataków zakończonych sukcesem nie obniża oceny ze sprawozdania.
Ocenie podlega natomiast np. jakość przeprowadzonych testów oraz ich liczba.

Pomocna literatura
[1] Jimmy Song, "Zrozumieć Bitcoin - Programowanie kryptowalut od podstaw", wyd. O'Reilly / Helion, 2020﻿
[2] Lauri Hartikka, "Naivecoin: a tutorial for building a cryptocurrency", URL: https://lhartikk.github.io/
[3] Satoshi Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System", URL: https://bitcoin.org/bitcoin.pdf

Informacje z karty przedmiotu:
(Poniższe dane możliwe są do edycji tylko w karcie przedmiotu przez kierownika przedmiotu.)
Link do aktualnej karty przedmiotu: Aktualna karta przedmiotu