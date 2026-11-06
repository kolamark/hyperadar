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

## Automatikus cikkek és közzététel

A `scripts/publish.py` két különböző forrás egyező történeténél letölti a teljes hozzáférhető cikkek szövegét. A modell a közös tényeket magyarul fogalmazza meg, minden lényeges állításhoz visszaadja a pontos forrást és egy szó szerinti bizonyító részletet. A kód ellenőrzi, hogy ez a részlet valóban szerepel-e a letöltött szövegben. Az érzékeny, vitatott és hiányosan alátámasztott témákat kihagyja. Nem használ idegen képeket. Futásonként legfeljebb két, naponként legfeljebb 15 cikk készülhet; a 10–15 cikk **cél, nem garantált darabszám**.

Az automatikus íráshoz a repó **Settings → Secrets and variables → Actions → New repository secret** menüjében `OPENAI_API_KEY` nevű titkot kell beállítani. A kulcs nélkül a forrásgyűjtés fut, a cikkírás nem. Az API-használat költséggel jár; a modell a workflow `OPENAI_MODEL` változójával cserélhető. A cikkírás legfeljebb négy modellkérést indít egy futásban.

A workflow a jóváhagyás nélkül létrejött cikkeket közvetlenül az `articles.json` fájlba menti, majd GitHub Pages-re telepíti az olvasói oldalt. Ehhez a repó Settings → Pages alatt a **GitHub Actions** közzétételi forrást kell kiválasztani. A repóba írt bot-commit önmagában nem indít új workflow-t, ezért a kiadás ugyanannak a futásnak a része. A privát Sites előnézet a GitHubon lévő cikkfájlt olvassa, így új Site-telepítés nélkül meg tudja jeleníteni a friss cikkeket. A nyilvános GitHub Pages oldal címe a Pages beállítása után várhatóan `https://kolamark.github.io/hyperadar/`.

Az `articles.json` az ellenőrzött és jóváhagyott, publikus cikkek adatforrása. A jelenlegi weboldal addig bemutató tartalmat jelenít meg, amíg a fájl üres. Az RSS-jelöltek soha nem kerülnek automatikusan az olvasói felületre.

## Szerkesztői jóváhagyás

Az `editorial.html` megmarad kézi javításhoz, de az automatikus hírekhez nem kell jóváhagyás. A kézi jóváhagyás gomb egy teljes `articles.json` fájlt **letölt**; nem módosítja automatikusan a repót. A `.github/workflows/validate.yml` ellenőrzi az adatok szerkezetét. A mechanikus ellenőrzés nem helyettesíti az emberi szerkesztőt; az automatikus rendszer tévedhet, ezért a megjelent hírek utólagos ellenőrzése és javítása fontos.

Az oldal jelenlegi privát előnézete a Sites tárhelyén fut, amely külön forrásból kerül telepítésre. Az előnézet a GitHubon publikált cikkadatokat olvassa; a weboldal kinézetének módosításához külön Site-telepítés kell.

## Következő fejlesztési szakasz

- Tartós adatbázis, szerkesztőségi admin és jóváhagyási folyamat.
- Több forrás, eredeti bejelentések, duplikációk és relevancia szerinti csoportosítás.
- Bizonyítékhoz kötött magyar cikkgenerálás; képjogok, források és állítások ellenőrzése.
- Megbízhatóbb időzítés és futásnapló, költségkorláttal.
- Az oldal dinamikus cikkfolyama és önálló, megosztható cikkoldalak.

A jelenlegi oldal privát előnézete: https://hyperadar-magazin.kolarovszki-mark.chatgpt.site

## Szerkesztési alapelv

Forrásmegjelölés nem jelent újraközlési vagy képfelhasználási engedélyt. A rendszer nem publikál ellenőrizetlen állítást, másolt szöveget vagy tisztázatlan jogú képet. Érzékeny témák emberi jóváhagyást igényelnek.
