# AccuMop

### Systém pro kontrolu akumulace pojistných rizik. Celý proces se skládá z přípravy dat (SAS), jejich úpravy (Python) a následné vizualizace (Streamlit).

## Myšlenka

Tento přístup pro sledování akumulace rizika spočívá v rozdělení sledované plochy na síť stejně rozlehlých území. V našem případě sledujeme akumulaci rizika v České republice, kterou rozdělujeme na síť čtverců o přibližné rozloze 1 km<sup>2</sup>. V každém čtverci výsledné matice získáme hodnotu mezi 0 a 1, která bude představovat míru akumulace rizika v dané oblasti.

## Příprava dat - SAS

Zásadní hodnotou pro výslednou míru akumulace rizika je očekávaná škoda za dané riziko na jednotlivých objektech. Proto vycházíme z tabulky, kde máme pro každý objekt umístěn na mapě, tedy s hodnotami `longitude` a `lalitude`, hodnotu `očekávané škody` a dále `rizikovou zónu`.

Dále nadefinujeme čtvercovou síť přes námi sledovanou oblast a každou lokaci z původní tabulky přiřadíme do příslušného čtverce.

Pro dané riziko vypočteme v každém čtverci sumu očekávaných škod daného rizika přes všechny pojištěné objekty (v našem případě budovy), které spadají do rizikové zóny připouštějící výskyt velké škody daného rizika. Tímto způsobem dostaneme matici hodnot, které pronásobením maximální hodnou matice dostaneme do rozmezí mezi 0 a 1.

## Úprava a vizualizace dat - Python, Streamlit

Získaná data již můžeme zobrazit přímo na mapě tak, že červenější body v zobrazené matici odpovídají hodnotám bližším 1, tedy území s větší akumulací rizika.

![image](pics\original_pic.PNG)

Problémem je, že takto mohou vzniknout čtvercové oblasti, pro které nebudeme mít dostatečká data, tedy nepojištěné objekty, nicméně z mapy vidíme, že v okolních oblastech máme velkou akumulaci rizika. Tento problém vyřeší pomocí upraveného algoritmu, který se používá k rozmazání obrázků.

Chceme tedy získat novou matici hodnot, která bude vycházet z té původní, ale v každém čtverci matice bude brát v ůvahu také hodnoty okolních čtverců. Čím je však okolní oblast dál, tím menší váhu pro hodnotu v aktuálním čtverci by měla mít. Od určité vzdálenosti již vzájemný vliv jednotlivých oblastí nepřipouštíme (výchozí hodnota jsou 3 km).

![image](pics\blur_pic.PNG)

Pokud $s_n$ je hodnotu čtverce v nové matici, $s_o$ je hodnota čverce ve staré matici, $d$ je Euklidovská vzdálenost čtverců a $p$ je volitelná hodnota (výchozí hodnota je 1), pak vzorec pro výpočet hodnot v nové matici by se dal tedy zapsat takto:

$$s_{n} = \sum\frac{s_{o}}{\left( 1+d \right)^{p}}$$

Po tomto procesu však ještě vzniká problém s tím, že v některých případech se nám mohou dostat nenulové, případně i vysoké hodnoty do čtverců, kde všechny budovy spadají do bezrizikové zóny (například místo u řeky, ale na kopci). To vyřešíme tak, že všechny takové hodnoty v nové matici převedeme na 0 a poté opět všechny hodnoty matice vydělíme maximální hodnotou matice, aby macimální hodnotou byla hodnota 1.

![image](pics\final_pic.PNG)

Výsledek můžeme opět zobrazit na mapě a využít ho v dalších procesech.
