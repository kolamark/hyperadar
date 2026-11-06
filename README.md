# HypeRadar

Magyar popkultúra és gaming magazin fejlesztés alatt. Az `index.html` a jelenlegi, mobilbarát bemutató oldal. A három mintacikk egyértelműen demóként van megjelölve, és nem aktuális hír.

## Kipróbálás

Az `index.html` közvetlenül böngészőben megnyitható. A keresés, a rovatváltás és a mintacikkek megnyitása kliensoldalon működik.

Az RSS-jelöltek gyűjtéséhez Python 3.11+ szükséges:

```bash
python3 scripts/collect.py
```

A konfigurált feedek URL-jei a `config/feeds.json` fájlban találhatók. A script csak címet, eredeti linket, rovatot és dátumot gyűjt a `data/candidates.json` fájlba; nem vesz át cikkeket vagy képeket, nem ír magyar hírt, és nem publikál. A jelöltekhez az eredeti oldalt és elsődleges forrásokat szerkesztőnek kell ellenőriznie.

## Következő fejlesztési szakasz

- Tartós adatbázis, szerkesztőségi admin és jóváhagyási folyamat.
- Több forrás, eredeti bejelentések, duplikációk és relevancia szerinti csoportosítás.
- Bizonyítékhoz kötött magyar cikkgenerálás; képjogok, források és állítások ellenőrzése.
- Napi tíz időzített ellenőrzés Europe/Budapest időzónában, futásnaplóval és költségkorláttal.
- Az oldal dinamikus cikkfolyama és önálló, megosztható cikkoldalak.

A jelenlegi oldal privát előnézete: https://hyperadar-magazin.kolarovszki-mark.chatgpt.site

## Szerkesztési alapelv

Forrásmegjelölés nem jelent újraközlési vagy képfelhasználási engedélyt. A rendszer nem publikál ellenőrizetlen állítást, másolt szöveget vagy tisztázatlan jogú képet. Érzékeny témák emberi jóváhagyást igényelnek.
