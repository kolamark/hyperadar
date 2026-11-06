# HypeRadar

Magyar popkultúra és gaming magazin fejlesztés alatt. Az `index.html` a jelenlegi, mobilbarát bemutató oldal. A három mintacikk egyértelműen demóként van megjelölve, és nem aktuális hír.

## Kipróbálás

Az `index.html` közvetlenül böngészőben megnyitható. A keresés, a rovatváltás és a mintacikkek megnyitása kliensoldalon működik.

Az RSS-jelöltek gyűjtéséhez Python 3.11+ szükséges:

```bash
python3 scripts/collect.py
```

A konfigurált feedek URL-jei a `config/feeds.json` fájlban találhatók. A script csak címet, eredeti linket, rovatot és dátumot gyűjt a `data/candidates.json` fájlba; nem vesz át cikkeket vagy képeket, nem ír magyar hírt, és nem publikál. A jelöltekhez az eredeti oldalt és elsődleges forrásokat szerkesztőnek kell ellenőriznie.

Az `.github/workflows/collect.yml` minden órában ellenőrzi a budapesti helyi időt, és a 06, 08, 10, 12, 14, 16, 18, 20, 22 és 23 órás időablakban lefuttatja a gyűjtést. Kézzel is indítható a GitHub Actions felületén. A GitHub ütemezése késhet, ezért ez **legfeljebb tíz célzott ellenőrzési ablak**, nem garantáltan pontos időpontban lefutó szolgáltatás. Hibás feed esetén a napló jelzi a problémát.

Az `articles.json` az ellenőrzött és jóváhagyott, publikus cikkek adatforrása. A jelenlegi weboldal addig bemutató tartalmat jelenít meg, amíg a fájl üres. Az RSS-jelöltek soha nem kerülnek automatikusan az olvasói felületre.

## Szerkesztői jóváhagyás

Az `editorial.html` a privát előnézeten nyitható meg. A GitHubon gyűjtött jelölteket beolvassa, és a szerkesztő saját magyar cikket írhat. Kötelező a forrás, a legalább 120 szavas szöveg és a négy szerkesztői nyilatkozat. A jóváhagyás gomb egy teljes `articles.json` fájlt **letölt**; nem módosítja automatikusan a repót. A fájlt a GitHub repó gyökerében lévő `articles.json` helyére kell feltölteni, lehetőleg pull requestként. A `.github/workflows/validate.yml` ellenőrzi az adatok szerkezetét és a szerkesztőségi minimumokat. A mechanikus ellenőrzés nem helyettesíti a tény- és jogellenőrzést.

Az oldal jelenlegi privát előnézete a Sites tárhelyén fut, amely külön forrásból kerül telepítésre. A GitHubon frissített cikkfájl **nem frissíti automatikusan ezt az előnézetet**; a telepítést jelenleg külön el kell végezni. A GitHub Pages automatikus kiadásához külön tárhely-beállítás szükséges.

## Következő fejlesztési szakasz

- Tartós adatbázis, szerkesztőségi admin és jóváhagyási folyamat.
- Több forrás, eredeti bejelentések, duplikációk és relevancia szerinti csoportosítás.
- Bizonyítékhoz kötött magyar cikkgenerálás; képjogok, források és állítások ellenőrzése.
- Megbízhatóbb időzítés és futásnapló, költségkorláttal.
- Az oldal dinamikus cikkfolyama és önálló, megosztható cikkoldalak.

A jelenlegi oldal privát előnézete: https://hyperadar-magazin.kolarovszki-mark.chatgpt.site

## Szerkesztési alapelv

Forrásmegjelölés nem jelent újraközlési vagy képfelhasználási engedélyt. A rendszer nem publikál ellenőrizetlen állítást, másolt szöveget vagy tisztázatlan jogú képet. Érzékeny témák emberi jóváhagyást igényelnek.
