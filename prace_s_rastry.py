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
# Muzete vyuzit i jiny soubor, nejlepe vyrez multispektralniho snimku
soubor = 'S2A_T33UVR_20180703T101029.tif'

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
pass

# Vypište datovy typ objektu
pass

# 2. Čtení metadat rasteru (stavove attributy otevreneho objektu dataset)

# Vypište stavový atribut `ds.closed`
pass
# Vypište mod datasetu pomocí atributu `ds.mode`
pass

# Metadata (vlastnosti) datasetu - take atributy objektu
# Vypište počet kanalu v datasetu pomocí atribut `ds.count`
pass
# Vypište šířku pole v datasetu pomocí atribut `ds.width`
pass
# Vypište výšku pole v datasetu pomocí atribut `ds.width`
pass

# Rasterio dataset má atribut meta, který poskytuje souhrnné informace včetně parametrů geotransformace
# Vytvořte proměnnou meta z atributu `ds.width`
pass
# Jaký datový typ je proměnná meta
pass
# Vypište jednotlivé paramtery z proměnné meta
pass

# Indexy kanálu/pásem lze získat z atributu `ds.index`
# Vypište je
pass
# a jejich datove typy pomocí atributu `ds.dtypes`
pass
# Jaká je radiometrická hloubka pásem Sentinel-2?

# Georeferencovani rasteru
# Vypište minimální ohraničující obdélník (Bbox) datasetu z atributu `ds.bounds`
pass
# Vypište souřadnice levého horního rohu rasteru z atributu `ds.bounds.left`
pass

# Bbox je ziskan z geoprostorovych transformacnich atributu
# ... afinní transformační matice, která mapuje umístění pixelů v souřadnicích (col, row) na prostorové pozice (x, y)
# Vypište atribut geotransformace `ds.transform`
pass

# Součin této matice a tuple(0, 0), souřadnic sloupce a řádku levého horního rohu datové sady,
# je prostorová poloha levého horního rohu.
#  ds.transform * (0,0)

# Vypište souřadnice levého horního rohu
pass
# Vypište souřadnice pravého dolního rohu
# Součin geotransformační matice a tuple(šířky, výšky) je prostorová poloha levého horního rohu
pass

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
pass
# Rasterio metoda .read() vrátí pole hodnot typu NumPy. Je to tak? Ověřte.
pass
#

# Jaký datový typ je použit pro jednotlivé hodnoty pole? Numpy atribut `.dtype`
pass

# Indexování honot v NumPy je podobné seznamu
lst = [3, 6, 2, 8, 9]
# první prvek má hodnotu
print(lst[0])
# poslední
print(lst[-1])

# adresovani hodnot NumPy 2D pole je: B1[výška, šířka]
# Proč?

# Mějme tyto indexy pole
x_ix = 100; y_ix = 150
# Zjistěte hodnotu v těchto indexových souřadnicích
pass

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
pass
# Ověřte datový typ
pass
# Vypište minimální a maximální hodnotu pomocí metod `.min()` a `.max()`
pass

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
meta['count'] = 1
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

