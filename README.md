# Základné informácie o projekte:
- vytvorili sme si full-stack single-page aplikáciu, pomocou ktorej vieme vytvoriť grafické prostredie GUI ako webovú stránku a pomocou nej vie používateľ zobraziť VES súbor ako obrázok
- táto webová stránka prostredníctvom JavaScriptu komunikuje s webovým serverom používajúcim Flask naprogramovaným v Pythone
- ten spracuje HTTP požiadavku a vráti hotový PNG obrázok
# Návod ako spustiť projekt:
- vytvorite priečinok pre projekt
- vytvorite súbor main.py a vložiť nasledovný obsah
- spustite príkazový riadok a prejsť do vytvoreného priečinku cez príkaz cd
- prejdite do jednotky (drive) G: cd /D G:
- prejdite o priečinok vyššie: cd ..
- prejdite do priečinka foo: cd foo
- spustite nasledovné príkazy

 1. py -3 -m venv venv
 2. venv\Scripts\activate
 3. pip install Flask
 4. python -m pip install --upgrade Pillow

5. set FLASK_APP=main.py
 6. flask run


![127 0 0 1_5000_](https://user-images.githubusercontent.com/80895765/115831272-aa178700-a411-11eb-9775-02b1be3d8514.png)
