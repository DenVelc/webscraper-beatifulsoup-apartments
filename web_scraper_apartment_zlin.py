#!/usr/bin/env python
# coding: utf-8

# ### Závěrečný projekt - modul Python

# V tomto projektu proběhla analýza dat ze webové stránky `www.sreality.cz`, kde byla  získána  aktuální nabídka bytů ve Zlíně.
# Projekt se dělí na 3 části:
# 1. WebScraping - pomocí knihovny `BeautifulSoup` byly získány všechny aktuální inzerce bytů v daném městě. 
# - Byly získány  **tyto** informace: `URL odkaz bytu, rozměry bytu, kompozice bytu, cena bytu, lokace bytu (ulice + město)`
# 2. Datová analýza - ETL proces
# - V první fázi byl proveden processing dat tak, aby obsahoval příslušné datové typy, nenulové hodnoty a podobně.
# - Zprocesovaná a vyčištěná data byla vyexporotvána do `.csv` souboru.
# 3. Datová analýza
# - V třetí části byl do dataframe nahrán vyexportovaný `.csv` soubor s vyscrapovanými daty.
# - V této fázi byla provedna analýza dat, kde byly zodpovězeny tyto dotazy:
# - `Jaká je průměrná cena bytů?`
# - `Jaká je průměrná cena bytů pro každou kompozici (1+1, 2+1, atp.)?`
# - `Jaká je průměrná velikost bytu pro každou kompozici?`
# - `Existuje ulice, kde je vyšší koncentrace dražších bytů?`
# - `Jaký typ kompozice je v daném městě nejčastěji inzerovan?`
# - `Existují zde inzerce bytů, které stojí více, než 20.000,-? Pokud ano, jsou v této cenové hladině inzerovány i maximálně dvoupokojové byty (2+1/2+kk)?`
# - `Jaká je minimální a maximální cena inzerce pro každou kompozici bytu? Která kompozice má největší rozptyl mezi minimální a maximální inzerovanou cenou?`
# 

# ### WebScraping

# In[135]:


def ziskej_cenu_bytu(text: str) -> tuple[str, int]:
    cena = text.split()[2]
    metry = text.split()[3]

    return cena, metry

from bs4 import BeautifulSoup
import requests

strana = 1
byty_data = []

while True:
    data = requests.get(f'https://www.sreality.cz/hledani/pronajem/byty/zlin?strana={strana}').text
    soup = BeautifulSoup(data, 'html.parser')

    byty = soup.findAll('li', 'MuiGrid-root MuiGrid-item css-l1328q') #Zde hledám byty na stránce, společné znaky.

    for byt in byty:
        odkaz = byt.find('a', 'MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways css-1c7vz4z')['href']
        #Ačkovy tag mi našel konkrétní detail bytu.
        info_byty = byt.find('div', 'MuiBox-root css-n6y9a7') #Div tag mi našel souhrnné informace (kompo,cena, ulice)
        if info_byty is None:
            continue
        byt_detail = info_byty.find('p',  'MuiTypography-root MuiTypography-body1 css-13ztabn').text #Kompozice
        rozmery, kompozice = ziskej_cenu_bytu(byt_detail)
        ulice_kompozice = info_byty.findAll('p', 'MuiTypography-root MuiTypography-body1 css-13ztabn') #Ulice
        ulice = ulice_kompozice[1].text #Ulice_kompozice má stejný tag jako ulice, je zapotřebí indexovat.
        cena = info_byty.find('p', 'MuiTypography-root MuiTypography-body1 css-1ndcg2e').text #Cena
        print(cena)
        byt_objekt = {
            'Cena': cena,
            'Kompozice bytu': kompozice,
            'Rozměry bytu': rozmery,
            'Lokace': ulice
        }

        byty_data.append(byt_objekt)

    button = soup.find('button', 'MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedInherit MuiButton-sizeMedium MuiButton-outlinedSizeMedium MuiButton-colorInherit MuiButton-root MuiButton-outlined MuiButton-outlinedInherit MuiButton-sizeMedium MuiButton-outlinedSizeMedium MuiButton-colorInherit css-lp5ywq').text

    if button != 'Další stránka':
        print('Již zde není žádná další strana. Končím')
        break        

    strana += 1

    print(f'Scrapuju stránku č. {strana}')


# In[136]:


df.to_csv('Velcovsky_zdrojová_data.csv', index=False, encoding='utf-8')


# ### Datová analýza

# In[32]:


import pandas as pd
df = pd.read_csv('Velcovsky_zdrojová_data.csv')


# In[33]:


df['Čistá cena'] = (
    df['Cena'].str.replace(r'\D', '', regex=True)  
    .replace('', None)  # Nahrazení prázdných hodnot hodnotou None
    .dropna()  # Odstranění prázdných řádků
    .astype(int)  # Převod na číslo
)
# Odstranění řádků, kde je prázdná hodnota. V případě nabídky pronájmu se jedná o "Cena na vyžádání".
df = df.dropna(subset=['Čistá cena'])
df.head()



# Jaká je průměrná cena bytů nabízených bytů

# In[34]:


prumerna_cena = df['Čistá cena'].mean().round(2)
rozmery = ", ".join(df['Rozměry bytu'].unique())

print(f'Průměrná cena pronájmu v lokalitě Zlín je {prumerna_cena} Kč. Mezi jednotlivé dispozice patří: {rozmery}.')


# Seskupení podle 'Rozměry bytu' a výpočet průměrné ceny

# In[35]:


prumerna_cena = df.groupby('Rozměry bytu')['Čistá cena'].mean().round(2).reset_index()
prumerna_cena_sorted = prumerna_cena.sort_values('Čistá cena', ascending=False)

from matplotlib import pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(prumerna_cena_sorted['Rozměry bytu'], prumerna_cena_sorted['Čistá cena'], color='skyblue', edgecolor='black')
plt.title('Average price of apartments according to availability in the city of Zlín', fontsize=16)
plt.xlabel('Disposition of renting an apartment', fontsize=14)
plt.ylabel('Rental price in CZK', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


# Existuje ulice, kde je vyšší koncentrace dražších bytů? Varianta A)

# In[36]:


ulice = df.groupby('Lokace')['Čistá cena'].agg(['max','count'])

def clean_data(ulice):
    # Seřadit podle sloupce: 'max' (sestupně)
    ulice = ulice.sort_values(['max'], ascending=[False])
    return ulice
ulice_clean = clean_data(ulice.copy())
ulice_clean.head()# Odpověď: Luhačovice


# Existuje ulice, kde je vyšší koncentrace dražších bytů? Varianta B)
# 

# In[37]:


# Seskupení podle 'Lokace' a výpočet agregovaných hodnot
lokace_statistiky = df.groupby('Lokace')['Čistá cena'].agg(['mean', 'count', 'max']).round(2)

# Seřazení podle průměrné ceny (od nejdražší)
lokace_statistiky = lokace_statistiky.sort_values(by='max', ascending=False)

# Výpis lokalit s více než 2 byty a průměrnou cenou nad 20 000 Kč
drazsi_lokace = lokace_statistiky[(lokace_statistiky['max'] > 20000) & (lokace_statistiky['count'] > 2)]

print(f'Lokalita s nejvyšší koncentrací dražších bytů, dle zadaných parametrů více než 2 byty a průměrnou cenou nad 20 000 Kč je lokalita:')
drazsi_lokace


# In[38]:


import plotly.express as px

drazsi_lokace = pd.DataFrame({
    "Lokalita": [
        "Luhačovice",
        "třída Tomáše Bati (Zlín)",
        "ulice Smetanova (Zlín)",
        "třída Svobody (Zlín-Malenovice)"
    ],
    "Průměrná cena (Kč)": [
        20877,
        15502.67,
        19333.33,
        14897.5
    ]
})

drazsi_lokace["Latitude"] = [49.1007, 49.2202, 49.2237, 49.2009]
drazsi_lokace["Longitude"] = [17.7592, 17.6659, 17.6689, 17.5898]

data_lokace = drazsi_lokace.copy()

fig = px.scatter_mapbox(
    data_lokace,
    lat="Latitude",
    lon="Longitude",
    size="Průměrná cena (Kč)",
    hover_name="Lokalita",
    title="Průměrná cena pronájmu v Kč",
    zoom=9,
    mapbox_style="open-street-map"
)

fig.show()


# Jaký typ kompozice je v daném městě nejčastěji inzerovan?
# Největší počet nabízených bytů je s rozlohou 45m2 (celkem 12 inzerovaných). 
# Odpověď: Pravděpodobnou příčinou může být převis nabídky malometrážních bytů, které nejsou prioritní poptávkou rodin s dětmi. Alternativně může být vyšší poptávka po menších bytech od mladých lidí nebo jednotlivců.

# In[39]:


kompo = df['Kompozice bytu'].value_counts().reset_index()
def categorize(kompo):
    if kompo < 45:
        return "Do 45 m²"
    elif 45 <= kompo <= 70:
        return "45-70 m²"
    else:
        return "Nad 70 m²"

kompo['Kategorie'] = kompo['Kompozice bytu'].apply(categorize)
kompo_final = kompo.groupby('Kategorie')['count'].sum()

print(kompo_final)


# In[40]:


plt.figure(figsize=(15, 10))

plt.bar(kompo_final.index, kompo_final.values, color='skyblue', edgecolor='black')

# Přidání hodnot nad sloupce
for i, v in enumerate(kompo_final.values):
    plt.text(i, v + 1, str(v), ha='center', fontsize=14, fontweight='bold')

plt.xlabel('Category of apartments', fontsize=14)
plt.ylabel('Count of apartments', fontsize=14)
plt.title('Count of apartments by (m²)', fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


# Existují zde inzerce bytů, které stojí více, než 20.000,-? Pokud ano, jsou v této cenové hladině inzerovány i maximálně dvoupokojové byty (2+1/2+kk)?

# In[41]:


# Filtrace bytů s cenou vyšší než 20 000 Kč
byty_nad_20000 = df[df['Čistá cena'] > 20000]
# Zjištění, zda existují byty s dispozicemi 2+1 nebo 2+kk v této cenové hladině
dva_pokoje = byty_nad_20000[byty_nad_20000['Rozměry bytu'].isin(['2+1', '2+kk'])]

dva_pokoje


# Jaká je minimální a maximální cena inzerce pro každou kompozici bytu. Která kompozice má největší rozptyl mezi minimální a maximální inzerovanou cenou?
# 

# In[42]:


min_max_inzerce = df.groupby('Rozměry bytu')['Čistá cena'].agg(['min','max'])
min_max_inzerce = min_max_inzerce.sort_values(['max'])

rozptyl = min_max_inzerce.assign(rozptyl=lambda x: x['max'] - x['min'])
rozptyl


# Jaké je  minimální a maximální cena inzerce pro každou kompozici bytu? Která kompozice má největší rozptyl mezi minimální a maximální inzerovanou cenou?
# 

# In[43]:


# Seskupení podle 'Rozměry bytu' a výpočet minimální, maximální ceny a rozptylu
kompozice_stat = (
    df.groupby('Rozměry bytu')['Čistá cena']
    .agg(['min', 'max'])  # Výpočet minimální a maximální ceny
    .assign(rozptyl=lambda x: x['max'] - x['min'])  # Přidání sloupce pro rozptyl
)

nejvetsi_rozptyl = kompozice_stat[kompozice_stat['rozptyl'] == kompozice_stat['rozptyl'].max()]
print("Kompozice bytů s největším rozptylem:")
print(nejvetsi_rozptyl)

