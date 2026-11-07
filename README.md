# HypeRadar

Automatikusan frissülő magyar popkultúra és gaming magazin. Az éles oldal: https://kolamark.github.io/hyperadar/. Ha még nincs alkalmas hír, három külön jelölt bemutató írás látható.

## Kipróbálás

Az `index.html` közvetlenül böngészőben megnyitható. A keresés, a rovatváltás és a mintacikkek megnyitása kliensoldalon működik.

Az RSS-jelöltek gyűjtéséhez Python 3.11+ szükséges:

```bash
python3 scripts/collect.py
```

A konfigurált feedek URL-jei a `config/feeds.json` fájlban találhatók. A script csak címet, eredeti linket, rovatot és dátumot gyűjt a `data/candidates.json` fájlba; nem vesz át cikkeket vagy képeket, nem ír magyar hírt, és nem publikál. A jelöltekhez az eredeti oldalt és elsődleges forrásokat szerkesztőnek kell ellenőriznie.

Az `.github/workflows/collect.yml` napi tíz budapesti helyi időpontra van ütemezve: 06:17, 08:17, 10:17, 12:17, 14:17, 16:17, 18:17, 20:17, 22:17 és 23:17. Kézzel is indítható a GitHub Actions felületén. A GitHub ütemezése késhet vagy egy futás kimaradhat, ezért az időpontok célok, nem garantált megjelenési időpontok. Hibás feed esetén a napló jelzi a problémát.

## Automatikus cikkek és közzététel

A `scripts/publish.py` két különböző forrás egyező történeténél letölti a teljes hozzáférhető cikkek szövegét. A modell a közös tényeket magyarul fogalmazza meg, és előre kivágott, számozott forrásrészletek közül választ bizonyítékot. A pontos idézetet és a forráslinket a kód illeszti az állításokhoz. A magyar nyelvi kapu a címet, bevezetőt és törzset vizsgálja; a kiadási tesztek ezt is ellenőrzik. A kód ellenőrzi, hogy ez a részlet valóban szerepel-e a letöltött szövegben. Ezután külön, alapértelmezésben `gpt-4.1` modellel futó ellenőrzés a cím, a bevezető és a törzs minden mondatához konkrét bizonyítékazonosítót kér. Csak teljes, minden mondatot támogató audit esetén jelenhet meg a tervezet. A szemantikai ellenőrzés továbbra is tévedhet. Az érzékeny, vitatott és hiányosan alátámasztott témákat kihagyja. Nem használ idegen képeket. Futásonként legfeljebb két, naponként legfeljebb 15 cikk készülhet; a 10–15 cikk **cél, nem garantált darabszám**.

Az automatikus íráshoz a repó **Settings → Secrets and variables → Actions → New repository secret** menüjében `OPENAI_API_KEY` nevű titkot kell beállítani. A kulcs nélkül a forrásgyűjtés fut, a cikkírás nem. Az API-használat költséggel jár; a modell a workflow `OPENAI_MODEL` változójával cserélhető. A generálás legfeljebb hat modellkérést indít egy futásban; az audit minden eljutó tervezethez további modellkérést használ, így az API-költség magasabb lehet. Az ellenőrző modell az `OPENAI_AUDIT_MODEL` környezeti változóval cserélhető. A rövid cikk minimuma 90 szó, két bizonyítékhoz kötött bekezdéssel.

A workflow a jóváhagyás nélkül létrejött cikkeket közvetlenül az `articles.json` fájlba menti, majd GitHub Pages-re telepíti az olvasói oldalt. Ehhez a repó Settings → Pages alatt a **GitHub Actions** közzétételi forrást kell kiválasztani. A repóba írt bot-commit önmagában nem indít új workflow-t, ezért a kiadás ugyanannak a futásnak a része. A nyilvános GitHub Pages oldal címe: https://kolamark.github.io/hyperadar/.

Az `articles.json` az automatikusan ellenőrzött, publikus cikkek adatforrása. A jelenlegi weboldal csak üres fájl esetén jelenít meg bemutató tartalmat. Az RSS-jelöltek soha nem kerülnek automatikusan az olvasói felületre.

## Szerkesztői jóváhagyás

Az `editorial.html` megmarad kézi javításhoz, de az automatikus hírekhez nem kell jóváhagyás. A kézi jóváhagyás gomb egy teljes `articles.json` fájlt **letölt**; nem módosítja automatikusan a repót. A `.github/workflows/validate.yml` ellenőrzi az adatok szerkezetét. A mechanikus ellenőrzés nem helyettesíti az emberi szerkesztőt; az automatikus rendszer tévedhet, ezért a megjelent hírek utólagos ellenőrzése és javítása fontos.

Az oldal jelenlegi privát előnézete a Sites tárhelyén fut, amely külön forrásból kerül telepítésre. Az előnézet a GitHubon publikált cikkadatokat olvassa; a weboldal kinézetének módosításához külön Site-telepítés kell.

## Következő fejlesztési szakasz

- Több releváns, egymástól független forrás és pontosabb történetcsoportosítás a napi darabszám javításához.
- Saját, megosztható cikkoldalak és jogtisztán használható illusztrációk.
- Utólagos javítási és visszavonási napló, futási és API-költségfigyelés.

A jelenlegi automatikus folyamat nem garantál napi 10–15 cikket. Az új, számozott forrásrészletekkel a korábbi idézetmásolási hiba megszűnt, de két éles próbában egy-egy cikk tartalmi pontatlanságot mutatott. A #SaveMassEffect írást visszavontuk, és kizártuk ugyanazokat a forráslinkeket az újrapublikálásból; a Zelda-cikket elsődleges Nintendo-forrással és szűkebb, ellenőrzött állításokkal javítottuk. Azóta erősebb, minden mondathoz konkrét bizonyítékot kérő audit fut. A 2026. november 7-i utolsó próba 658 jelöltből 18 történetcsoportot talált, tíz teszten átment, és nem publikált új cikket: hat tervezetet az audit utasított el. Az automatikus tényellenőrzés továbbra sem ad hibamentességi garanciát.

## Szerkesztési alapelv

Forrásmegjelölés nem jelent újraközlési vagy képfelhasználási engedélyt. A rendszer nem publikál ellenőrizetlen állítást, másolt szöveget vagy tisztázatlan jogú képet. Érzékeny témák emberi jóváhagyást igényelnek.
