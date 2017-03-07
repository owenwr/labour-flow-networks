Obtaining the Data
————————————————————

Data is not uploaded to GitHub since it is sensitive.
Contact project author, Owen Riddall, for access to data.
Omar Guerrero also has access, contact him via his website: http://oguerr.com/

Organisation of Data Folders
—————————————————————————————
Folders must be organized like this for code in project to work.

16-12-2016-Mega
    |
    |— dates_birth.csv			< file containing firm birth dates
    |- dates_death.csv			< file containing firm death dates
    |- flows				< directory containing worker flows for year year
    |    |- flows_1988-1989.csv		< filenames in this form
    |- geography			< directory containing firm geographical classification for each year
    |    |- kkunta_1988.csv		< filenames in this form
    |- industrial-classification	< directory containing firm industrial classification for each year
    |    |- maak_1988.csv		< filenames in this form
    |- profits				< directory containing firm profits for each year
    |    |- profits_1988.csv		< filenames in this form
    |- sizes				< directory containing firm sizes for each year
    |    |- sizes_1988.csv		< filenames in this form

File Format
————————————
A brief description of the files’ format and content.

Filename: dates_birth
Column format: firm id | year of birth

Filename: dates_death
Column format: firm id | year of death

Filename: flows/flows_initialYear_finalYear
Column format: origin firm | destination firm | total flows

Filename: profits/profits_year
Column format: firm id | net profits in Euros

Filename: sizes/sizes_year
Column format: firm id | number of reported employees

Filename: geography/kkunta_year
Column format: firm id | kunta code (geographical region code)
Regions (http://tilastokeskus.fi/meta/luokitukset/maakunta/001-2016/index_en.html)
01	Uusimaa
02	Varsinais-Suomi
04	Satakunta
05	Kanta-Häme
06	Pirkanmaa
07	Päijät-Häme
08	Kymenlaakso
09	South Karelia
10	Etelä-Savo
11	Pohjois-Savo
12	North Karelia
13	Central Finland
14	South Ostrobothnia
15	Ostrobothnia
16	Central Ostrobothnia
17	North Ostrobothnia
18	Kainuu
19	Lapland
21	Åland

Filename: industrial-classification/maak_year
Column format: firm id | maak code (industrial classification code)


*** notes
- Origin: Omar Guerrero extracted from Statistics Finland
- [Omar Guerrero] I think that the firm sizes need to be divided by 10, so fractional sizes are permitted since this quantity is an average reported over several weeks during the year.
- 