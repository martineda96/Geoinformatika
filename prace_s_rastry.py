#!/usr/bin/env python3

# Skriptovani procesu s rastery v Python
# 1. otevreni datasetu
# 2. cteni metadat rasteru
# 3. cteni dat rasteru do pole NumPy (numericky Python)
# 4. mapova algebra pomoci NumPy
# 5. zapis vysledku do noveho souboru vcetna nastaveni metadat vystupu

# Rasterio dokumentace
# https://rasterio.readthedocs.io

### Knihovny ###
import os
import rasterio
import numpy as np

### DATA ###
# nastavte cestu k ulozenemu souboru 'S2A_T33UVR_20180703T101029.tif'
cesta = 'T:\martineda\Geoinformatika\Rastery'
soubor = 'S2A_T33UVR_20180703T101029.tiff'

#lze taky overit cestu by os.listdir(cesta)
#pouzit zdvojena lomitka, jestli je problem v ceste \\Geoifnormatika\\Rastery

fn = os.path.join(cesta, soubor)
print(fn)
#taky jde os.path.isfile(fn) a napise to true (idealne)

### PRUZKUM RASTERU ###
# 1. Otevreni datasetu
# Funkce `rasterio.open()` přijímá řetězec cesty a vrací otevřený objekt datové sady.
# Rasterio otevře data pomocí ovladače GDAL.
# otevřete raster do proměnné ds

ds = rasterio.open(fn)
ds

# Vypište datovy typ objektu
print(type(ds))

# 2. Čtení metadat rasteru (stavove attributy otevreneho objektu dataset)

# Vypište stavový atribut `ds.closed`
ds.closed
# Vypište mod datasetu pomocí atributu `ds.mode`
ds.mode

# Metadata (vlastnosti) datasetu - take atributy objektu
# Vypište počet kanalu v datasetu pomocí atribut `ds.count`
ds.count #vypisuje pocet pasem

# Vypište šířku pole v datasetu pomocí atribut `ds.width`
ds.width #vrati pocet pixelu v rasteru na sirku
#CTRL + C v konzoli se vrátí z chybnýho stavu

# Vypište výšku pole v datasetu pomocí atribut `ds.height`
ds.height #vyska v pixelech
print(ds.width * ds.height) #pocet pixelu primitivne

# Rasterio dataset má atribut meta, který poskytuje souhrnné informace včetně parametrů geotransformace
# Vytvořte proměnnou meta z atributu `ds.width`
meta = ds.width
# Jaký datový typ je proměnná meta
type(meta)
# Vypište jednotlivé paramtery z proměnné meta
for k in meta:
    print(k,":", meta[k])

# Indexy kanálu/pásem lze získat z atributu `ds.index`
# Vypište je
ds.index
# a jejich datove typy pomocí atributu `ds.dtypes`
ds.dtypes
# Jaká je radiometrická hloubka pásem Sentinel-2?

# Georeferencovani rasteru
# Vypište minimální ohraničující obdélník (Bbox) datasetu z atributu `ds.bounds`
ds.bounds
# Vypište souřadnice levého horního rohu rasteru z atributu `ds.bounds.left`


# Bbox je ziskan z geoprostorovych transformacnich atributu
# ... afinní transformační matice, která mapuje umístění pixelů v souřadnicích (col, row) na prostorové pozice (x, y)
# Vypište atribut geotransformace `ds.transform`


# Součin této matice a tuple(0, 0), souřadnic sloupce a řádku levého horního rohu datové sady,
# je prostorová poloha levého horního rohu.
#  ds.transform * (0,0)

# Vypište souřadnice levého horního rohu
pass
# Vypište souřadnice pravého dolního rohu
# Součin geotransformační matice a tuple(šířky, výšky) je prostorová poloha levého horního rohu
#ds.transform*

# Souřadnicový referenční systém - CRS
# Vypište atribut CRS z yadatasetu pomocí `ds.crs`
pass
# Převeďte ho na EPSG string pomocí `ds.crs.to_string()` - jedná se již o metodu třídy rasterio
pass
# Převeďte do formátu Well Known Text pomocí `ds.crs.to_wkt()`
pass

### ČTENÍ DAT RASTERU ###
# Načtěte data z pásma 1 do proměnné B1 pomocí metody `read()` z data asetu ds
# index pásma: 1
B1 = ds.read(1) #indexa od 1 nikoliv od 0
# Rasterio metoda .read() vrátí pole hodnot typu NumPy. Je to tak? Ověřte.
type(B1)


# Jaký datový typ je použit pro jednotlivé hodnoty pole? Numpy atribut `.dtype`
B1.dtype

# Indexování honot v NumPy je podobné seznamu
lst = [3, 6, 2, 8, 9]
# první prvek má hodnotu
print(lst[0])
# poslední
print(lst[-1])

#x = 10, y = 20
B1[20 10]

#vybrat interval (trinact a jedenact uz to nebere)
B1[10:13 10:11]

# adresovani hodnot NumPy 2D pole je: B1[výška, šířka]
# Proč?

# Mějme tyto indexy pole
x_ix = 100; y_ix = 150
# Zjistěte hodnotu v těchto indexových souřadnicích
B1[150, 100]

# Indexovaní pomocí souřadnic
# Datové sady mají metodu `DatasetReader.index()` pro získání indexů pole odpovídajících bodům
# v georeferencovaném prostoru. Chcete-li získat hodnotu pro pixel 10 km východně a 5 km jižně
# od levého horního rohu datové sady, postupujte takto.

#  https://rasterio.readthedocs.io/en/stable/api/rasterio.io.html
# index(x, y)
# x (float) – x value in coordinate reference system
# y (float) – y value in coordinate reference system
# Returns: tuple (row index, col index)

x, y = (ds.bounds.left + 10000, ds.bounds.top - 5000)
radek, sloupec = ds.index(x, y)
print(f'Hodnota pole pro vybrany pixel je: {B1[radek, sloupec]}')

# Chceme-li získat prostorové souřadnice pixelu, použijte metodu DatasetReader.xy() datové sady.
# Příklad: souřadnice středu pole (obrazu) lze vypočítat takto.
print(f'Souradnice x, y stredu obrazovych dat: {ds.xy(ds.height // 2, ds.width // 2)}')

### Volitelné ###
# Okna pro čtení dat
# ((první_řádek, poslední_řádek), (první_sloupec, poslední_sloupec))
# Window(první_sloupec, první_řádek, šířka, výška)
with rasterio.open(os.path.join(cesta, soubor)) as cervene:
    B3 = cervene.read(1, window=((0, 100), (0, 200)))
print(f'Velikost  pole kanalu 3: {B3.shape}')

### 4. Mapová algebra pomocí NumPy ###
# Výpočet NDVI z dat Sentinel-2
RED = ds.read(3).astype(np.float32)
NIR = ds.read(4).astype(np.float32) 
print(f'Datovy typ cerveno pasma je: {RED.dtype}')

# Vypočťete index a výsledek uložte do proměnné NDVI
NDVI = (NIR - RED) / (NIR + RED) #(odrazivost vody - odraz chlorofilu)/norma
NDVI
# Ověřte datový typ
NDVI.dtype
# Vypište minimální a maximální hodnotu pomocí metod `.min()` a `.max()`
#Na GITu má doc. Brodsky info k NumPy v Jupyter Notebooku
NDVI.min()
NDVI.max()

# Více o NumPy? MLgeo

### 5. ZÁPIS RASTERU DO SOUBORU ###
# zapis https://rasterio.readthedocs.io/en/latest/topics/writing.html

# with rasterio.open(
#     './data/ndvi.tif',
#     'w',
#     driver='GTiff',
#     height=pole.shape[0],
#     width=pole.shape[1],
#     count=1,
#     dtype=pole.dtype,
#     crs='+proj=latlong',
#     transform=transform,
# ) as dst:
#     dst.write(1, pole)

# Připrava metadtat
# využijem metdata otevřeného souboru
meta = ds.meta
print(f'Metadata datasetu: {meta}')
# výstup: 32-bitová data!!!
# nastavíme atribut dtype na rasterio float32
meta["dtype"] = "float32"
# počet kanálů = 1
meta['count'] = 12
# komprese dat
# Rasterio používá GDAL jako 'backend'.
# Jaké kompresní metody jsou implementovány pod kterými zkratkami (kw)?
meta['compress'] = 'lzw'

# Zápis souboru
with rasterio.open(os.path.join(cesta, 'ndvi.tif'), 'w', **meta) as dst:
   dst.write_band(1, NDVI.astype(rasterio.float32))

# Ověření zápisu soubodu do FS a jeho velikosti
if os.path.isfile(os.path.join(cesta, 'ndvi.tif')):
    print('Soubor ndvi.tif je zapsan na disk.')
    print(f"Velikost souboru je: {os.path.getsize(os.path.join(cesta, 'ndvi.tif')) / 1000000} MB.")