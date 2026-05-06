"""Internal script - NOT shipped in repo. Generates generate_rolargesum.json with 100 candidates."""
import json
import random

random.seed(42)

# Template-uri pentru a varia text
TEMPLATES_PREFIX = [
    "Conform analiștilor politici, ",
    "Sursele oficiale au confirmat că ",
    "Într-un interviu difuzat la televiziune, ",
    "Documentul oficial arată că ",
    "Reporterii au observat că ",
    "Comunicatul de presă menționează că ",
    "Conform martorilor de la fața locului, ",
    "În declarația sa publică, ",
    "Datele recente indică faptul că ",
    "",  # uneori fără prefix
]

DOMAINS = [
    "https://digi24.ro/stiri/{cat}/{slug}",
    "https://hotnews.ro/{cat}/{slug}",
    "https://cotidianul.md/2024/{m}/{slug}",
    "https://www.jurnal.md/ro/news/{cat}/{slug}",
    "https://g4media.ro/{cat}/{slug}",
    "https://adevarul.ro/{cat}/{slug}",
    "https://stirileprotv.ro/{cat}/{slug}",
    "https://libertatea.ro/{cat}/{slug}",
    "https://gandul.ro/{cat}/{slug}",
    "https://stiripesurse.ro/{cat}/{slug}",
    "https://www.agerpres.ro/{cat}/{slug}",
    "https://www.mediafax.ro/{cat}/{slug}",
]

CATEGORIES = ["politica", "economie", "social", "justitie", "externe", "sport", "cultura", "sanatate", "educatie"]
MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


def make_doc_id(idx):
    domain = random.choice(DOMAINS)
    cat = random.choice(CATEGORIES)
    slug = f"articol-{idx:04d}"
    m = random.choice(MONTHS)
    return domain.format(cat=cat, slug=slug, m=m)


# (expresie_în_text, propoziție_completă, id_DERC)
# Mix: figurative + literal + variații
DATA = [
    # ===== POZITIVE FIGURATIVE - "a pune bețe în roate" =====
    ("pune bețe în roate", "Opoziția pune bețe în roate guvernului la fiecare proiect important votat în această sesiune.", "derc_001023"),
    ("au pus bețe în roate", "Senatorii au pus bețe în roate proiectului de lege fiscală încă din prima ședință a comisiei.", "derc_001023"),
    ("punea bețe în roate", "Ministerul punea bețe în roate proiectului de digitalizare de luni întregi, conform raportului.", "derc_001023"),
    ("pun bețe în roate", "Aleșii pun bețe în roate fiecărei reforme propuse de coaliție în ultimele șase luni.", "derc_001023"),

    # ===== POZITIVE - "a tăia frunză la câini" =====
    ("tăiat frunză la câini", "Funcționarii primăriei au tăiat frunză la câini ani la rând, fără să rezolve problemele de bază.", "derc_002145"),
    ("taie frunză la câini", "Studenții taie frunză la câini în campus, în loc să se concentreze pe studiu, conform rectorului.", "derc_002145"),
    ("tăind frunză la câini", "Angajații își petrec zilele tăind frunză la câini, deși proiectul are termen limită apropiat.", "derc_002145"),

    # ===== POZITIVE - "a trage pe sfoară" =====
    ("trași pe sfoară", "Investitorii străini au fost trași pe sfoară cu promisiuni de profit care nu s-au materializat.", "derc_003401"),
    ("a tras pe sfoară", "Fostul director a tras pe sfoară angajații cu salarii promise dar niciodată plătite integral.", "derc_003401"),
    ("trage pe sfoară", "Compania trage pe sfoară clienții cu reclame înșelătoare despre produsele bancare oferite.", "derc_003401"),

    # ===== POZITIVE - "a băga mâna în foc" =====
    ("bagă mâna în foc", "Avocatul apărării a spus că bagă mâna în foc pentru nevinovăția clientului în acest dosar.", "derc_006117"),
    ("băgat mâna în foc", "Procurorul a băgat mâna în foc pentru integritatea echipei sale în ancheta complexă.", "derc_006117"),
    ("băgăm mâna în foc", "Băgăm mâna în foc pentru acest candidat, a declarat purtătorul de cuvânt al partidului.", "derc_006117"),

    # ===== POZITIVE - "a da cu piciorul" =====
    ("dat cu piciorul", "Mijlocașul a dat cu piciorul unei oferte de cinci milioane de euro de la o echipă din Premier League.", "derc_005233"),
    ("dă cu piciorul", "Politicianul dă cu piciorul oricărei propuneri venite din partea opoziției, fără analiză.", "derc_005233"),

    # ===== POZITIVE - "a face din țânțar armăsar" =====
    ("făcut din țânțar armăsar", "Premierul a făcut din țânțar armăsar dintr-o discuție tehnică, escaladând tensiunea inutilă.", "derc_008291"),
    ("face din țânțar armăsar", "Presa face din țânțar armăsar fiecare incident minor implicând personalități publice.", "derc_008291"),

    # ===== POZITIVE - "a-i pica fisa" =====
    ("picat fisa", "După trei ore de explicații, abia atunci i-a picat fisa secretarului de stat în privința consecințelor.", "derc_009103"),
    ("îi pică fisa", "Greu îi pică fisa parlamentarului mediu când vine vorba de dosare juridice complicate.", "derc_009103"),

    # ===== POZITIVE - "a se da peste cap" =====
    ("dat peste cap", "Antrenorul s-a dat peste cap să motiveze echipa înaintea finalei, organizând antrenamente speciale.", "derc_011398"),
    ("se dă peste cap", "Echipa se dă peste cap să termine proiectul european la termenul stabilit prin contract.", "derc_011398"),

    # ===== POZITIVE - "a pune punctul pe i" =====
    ("pus punctul pe i", "Liderul de partid a pus punctul pe i într-un discurs care a clarificat poziția oficială față de reformă.", "derc_012445"),
    ("pune punctul pe i", "Procurorul șef pune punctul pe i la conferința de presă programată pentru mâine dimineața.", "derc_012445"),

    # ===== POZITIVE - "a închide ochii" =====
    ("închis ochii", "Guvernul a închis ochii la abuzurile companiei de stat timp de mai mulți ani, susțin sursele.", "derc_015234"),
    ("închide ochii", "Comisia de etică închide ochii la conflictele de interese din interiorul instituției.", "derc_015234"),

    # ===== POZITIVE - "a trage un semnal de alarmă" =====
    ("tras un semnal de alarmă", "Bruxelles-ul a tras un semnal de alarmă privind ritmul lent al reformelor judiciare în țară.", "derc_014567"),
    ("trag un semnal de alarmă", "Specialiștii trag un semnal de alarmă în privința deficitului bugetar tot mai accentuat.", "derc_014567"),

    # ===== POZITIVE - "a vorbi în dodii" =====
    ("vorbit în dodii", "Deputatul a vorbit în dodii la tribună, derutând până și colegii săi de partid.", "derc_016078"),
    ("vorbește în dodii", "Politicianul vorbește în dodii la fiecare conferință, evitând răspunsurile clare la întrebări.", "derc_016078"),

    # ===== POZITIVE - "a pune umărul" =====
    ("pus umărul", "Profesorii au pus umărul la organizarea evenimentului, deși nu erau plătiți suplimentar.", "derc_017145"),
    ("pune umărul", "Comunitatea pune umărul la reconstruirea bisericii distruse de incendiul din ianuarie.", "derc_017145"),

    # ===== POZITIVE - "a da apă la moară" =====
    ("dat apă la moară", "Atacantul a marcat un gol care a dat apă la moară comentatorilor critici ai antrenorului.", "derc_018291"),
    ("dă apă la moară", "Această decizie dă apă la moară celor care susțin retragerea sprijinului european.", "derc_018291"),

    # ===== POZITIVE - "a prinde cu mâța în sac" =====
    ("prins cu mâța în sac", "Procurorii au prins cu mâța în sac un funcționar care primea mită în biroul instituției.", "derc_019402"),
    ("prinde cu mâța în sac", "DNA-ul prinde cu mâța în sac doi oficiali ai unei primării din provincie săptămâna trecută.", "derc_019402"),

    # ===== POZITIVE - "a se face foc și pară" =====
    ("făcut foc și pară", "Vedeta s-a făcut foc și pară când a aflat că imaginile au apărut pe rețelele sociale fără acord.", "derc_020156"),
    ("se face foc și pară", "Clientul se face foc și pară de fiecare dată când i se refuză rambursarea produsului defect.", "derc_020156"),

    # ===== POZITIVE - "a bate apa în piuă" =====
    ("bat apa în piuă", "Analiștii au atras atenția că măsurile guvernului bat apa în piuă fără un plan coerent.", "derc_021034"),
    ("bate apa în piuă", "Comisia bate apa în piuă cu raporturi formale, dar nu produce nicio schimbare reală.", "derc_021034"),

    # ===== POZITIVE - "a rămâne cu buza umflată" =====
    ("rămas cu buza umflată", "Pacienții cronici au rămas cu buza umflată după ce noul program de compensare a fost amânat.", "derc_022178"),
    ("rămân cu buza umflată", "Beneficiarii rămân cu buza umflată după ce ministerul a suspendat plățile anunțate anterior.", "derc_022178"),

    # ===== POZITIVE - "a sări ca ars" =====
    ("sărit ca ars", "Ministrul finanțelor a sărit ca ars la întrebarea privind deficitul real al bugetului trecut.", "derc_023089"),
    ("sare ca ars", "Liderul opoziției sare ca ars de fiecare dată când se aduce vorba despre averea sa personală.", "derc_023089"),

    # ===== POZITIVE - "a face zile fripte" =====
    ("făcut zile fripte", "Femeia a făcut zile fripte fostului soț, conform mărturiilor depuse la procesul de divorț.", "derc_025401"),
    ("fac zile fripte", "Vecinii fac zile fripte familiei nou mutate, depunând zeci de plângeri la asociația de proprietari.", "derc_025401"),

    # ===== POZITIVE - "a bate palma" =====
    ("bătut palma", "Liderii partidelor au bătut palma asupra unui acord de guvernare după negocieri maraton de zece ore.", "derc_032145"),
    ("bate palma", "Investitorul bate palma cu primăria pentru un parteneriat public-privat de 50 de milioane.", "derc_032145"),

    # ===== POZITIVE - "a-și freca palmele" =====
    ("freacă palmele", "Concurența își freacă palmele după acest scandal financiar care lovește în liderul de piață.", "derc_033201"),
    ("frecau palmele", "Firmele rivale își frecau palmele văzând declinul accelerat al fostului favorit din industrie.", "derc_033201"),

    # ===== POZITIVE - "a băga sub preș" =====
    ("băga sub preș", "Investitorii își fac griji că reglementarea va băga sub preș problemele reale ale sectorului.", "derc_035167"),
    ("băgat sub preș", "Conducerea anterioară a băgat sub preș datoriile companiei timp de cinci ani consecutivi.", "derc_035167"),

    # ===== POZITIVE - "a arunca praf în ochi" =====
    ("arunce praf în ochi", "Apărarea a încercat să arunce praf în ochii juraților prin argumente tehnice complicate.", "derc_037145"),
    ("aruncă praf în ochi", "Politicianul aruncă praf în ochi alegătorilor cu promisiuni populiste lipsite de acoperire.", "derc_037145"),

    # ===== POZITIVE - "a trage chiulul" =====
    ("tras chiulul", "Deputații au tras chiulul de la ședința de luni, conform listei de prezență publicate oficial.", "derc_038202"),
    ("trag chiulul", "Funcționarii trag chiulul în mod sistematic de la ședințele tehnice ale comisiei interministeriale.", "derc_038202"),

    # ===== POZITIVE - "a pune paie pe foc" =====
    ("pus paie pe foc", "Ministrul a pus paie pe foc cu declarațiile sale despre cadrele didactice în plin scandal salarial.", "derc_039118"),
    ("pune paie pe foc", "Articolul de presă pune paie pe foc într-un dosar deja sensibil aflat pe masa procurorilor.", "derc_039118"),

    # ===== POZITIVE - "a scoate din mânecă" =====
    ("scos din mânecă", "Cei doi soți au scos din mânecă înțelegeri secrete pe care nici avocații nu le cunoșteau înainte.", "derc_040076"),
    ("scoate din mânecă", "Compania scoate din mânecă o nouă strategie de marketing pentru a salva trimestrul actual.", "derc_040076"),

    # ===== POZITIVE - "a ieși din fire" =====
    ("ieșit din fire", "Ministrul și-a ieșit din fire când reporterul i-a pus o întrebare incomodă despre dosarul fiscal.", "derc_004512"),
    ("iese din fire", "Antrenorul iese din fire la conferințele de presă când e întrebat despre transferurile ratate.", "derc_004512"),

    # ===== POZITIVE - "a o lua razna" =====
    ("luat-o razna", "Piețele financiare au luat-o razna după anunțul neașteptat al Băncii Naționale privind dobânda.", "derc_007084"),

    # ===== POZITIVE - "a pierde răbdarea" =====
    ("pierdut răbdarea", "Sindicaliștii și-au pierdut răbdarea după luni de promisiuni neonorate din partea ministerului.", "derc_010256"),
    ("pierd răbdarea", "Părinții își pierd răbdarea cu programul școlar haotic și cer ministrului o întâlnire urgentă.", "derc_010256"),

    # ===== POZITIVE - "a se lupta din răsputeri" =====
    ("luptat din răsputeri", "Pompierii s-au luptat din răsputeri să stingă focul care amenința blocul din apropiere.", "derc_013012"),

    # ===== POZITIVE - "a-l trage la răspundere" =====
    ("tras la răspundere", "Acuzatul a fost tras la răspundere abia după ce a fost confruntat cu probele video din timpul anchetei.", "derc_034088"),
    ("trag la răspundere", "Comisia parlamentară îl trag la răspundere pe fostul ministru pentru deciziile din mandat.", "derc_034088"),

    # ===== POZITIVE - "a băga de seamă" =====
    ("băgat de seamă", "Martorul a spus că a băgat de seamă comportamentul suspect al inculpatului încă din prima zi.", "derc_024256"),

    # ===== POZITIVE - "a fi luat prin surprindere" =====
    ("luate prin surprindere", "Companiile au fost luate prin surprindere de noile prețuri la gaze și nu au mai avut timp să se adapteze.", "derc_041184"),
    ("luat prin surprindere", "Ministerul a fost luat prin surprindere de decizia Curții Constituționale anunțată ieri.", "derc_041184"),

    # ===== POZITIVE - "a o lua de la capăt" =====
    ("luat-o de la capăt", "Sportiva a luat-o de la capăt cu un nou antrenor după accidentarea care a ținut-o departe un an.", "derc_029178"),

    # ===== POZITIVE - "a-și pune în cap" =====
    ("pus în cap", "Tânărul scriitor și-a pus în cap să termine romanul până la finalul verii, în ciuda criticilor.", "derc_030256"),

    # ===== POZITIVE - "a-și face socoteala" =====
    ("făcut socoteala", "Antreprenorii și-au făcut socoteala că noile taxe le vor scădea profitul cu cel puțin 15 la sută.", "derc_031089"),
    ("face socoteala", "Echipa face socoteala câte resurse mai are disponibile pentru ultimele două luni ale proiectului.", "derc_031089"),

    # ===== VARIAȚII INSERȚIE =====
    ("pune sistematic bețe în roate", "Opoziția pune sistematic bețe în roate guvernului la fiecare proiect strategic, conform observatorilor.", "derc_001023"),
    ("făcut din simplu țânțar un întreg armăsar", "Vedeta a făcut din simplu țânțar un întreg armăsar pe baza unei observații banale a unui reporter.", "derc_008291"),
    ("tăiat în continuare frunză la câini", "Funcționarii au tăiat în continuare frunză la câini, ignorând directivele venite de la nivel central.", "derc_002145"),
    ("pune mereu bețe în roate", "Decidentul pune mereu bețe în roate proiectelor pe care nu le poate controla direct.", "derc_001023"),
    ("băgat adânc mâna în foc", "Garantul a băgat adânc mâna în foc pentru integritatea afacerii cu partenerii internaționali.", "derc_006117"),

    # ===== VARIAȚII SUBSTITUȚIE =====
    ("duse de nas", "Companiile occidentale au fost duse de nas de partenerii locali timp de mai multe luni.", "derc_003401"),
    ("pun piedici", "Aleșii pun piedici fiecărei reforme propuse de coaliție, în ciuda promisiunilor electorale.", "derc_001023"),
    ("băgat degetul în foc", "Demonstranții au băgat degetul în foc pentru cauza colegilor lor reținuți de poliție.", "derc_006117"),
    ("dus cu zăhărelul", "Alegătorii au fost duși cu zăhărelul de promisiuni populiste înainte de scrutinul de duminică.", "derc_003401"),
    ("ridică obstacole", "Birocrația ridică obstacole în calea oricărei investiții străine de mai bine de un deceniu.", "derc_001023"),

    # ===== NEGATIVE - SENS LITERAL (FP-uri) =====
    ("tăiat frunzele", "Grădinarii au tăiat frunzele uscate din parcul central înaintea sărbătorilor de toamnă pentru curățenie.", "derc_002145"),
    ("băgat mâna", "Mecanicul a băgat mâna în motor pentru a verifica nivelul uleiului și starea filtrelor de aer.", "derc_006117"),
    ("dat cu piciorul", "Atacantul a dat cu piciorul în minge cu toată forța, dar portarul advers a parat spectaculos lovitura.", "derc_005233"),
    ("freca", "Bunica freca rufele la mână în curte, cu apă încălzită pe sobă și săpun de casă tradițional.", "derc_026017"),
    ("pus bețele", "Copiii au pus bețele de chibrit în formă de pătrat pe masa din bucătărie pentru a învăța geometrie.", "derc_001023"),
    ("luat-o razna", "Vântul puternic a luat-o razna prin văile montane, dărâmând copaci și întrerupând curentul electric.", "derc_007084"),
    ("bați apa în piuă", "Pentru aluatul perfect, trebuie să bați apa în piuă cu zahărul timp de zece minute, până devine spumoasă.", "derc_021034"),
    ("stins focul", "Pompierii au stins focul în două ore, după ce flăcările cuprinseseră acoperișul depozitului industrial.", "derc_027112"),
    ("pus umăr", "Înainte de iarnă, recomandăm să puneți umăr la umăr scândurile pentru a proteja straturile de legume.", "derc_017145"),
    ("sărit ca ars", "Sportivul a sărit ca ars peste obstacolul final, asigurându-și astfel medalia de aur la concurs.", "derc_023089"),
    ("închis ochii", "Pacientul a închis ochii câteva minute pentru a se relaxa înainte de procedura medicală programată.", "derc_015234"),
    ("freacă palmele", "Bărbatul își freacă palmele de frigul puternic de afară, în așteptarea autobuzului întârziat.", "derc_033201"),
    ("pune punctul", "Profesorul pune punctul cu cretă albă pe tabla neagră, finalizând demonstrația matematică.", "derc_012445"),
    ("dat apă", "Țăranul a dat apă vitelor de două ori pe zi, conform programului tradițional al gospodăriei sale.", "derc_018291"),
    ("trage", "Calul trage căruța încărcată cu fân pe drumul forestier, în ritm constant și fără efort vizibil.", "derc_003401"),

    # ===== AMBIGUE =====
    ("crescut cu", "Exporturile au crescut cu 30 la sută față de aceeași perioadă a anului trecut, conform datelor oficiale.", "derc_028045"),
    ("dat peste cap", "Alpinistul s-a dat peste cap în avalanșă, dar a reușit să iasă teafăr cu ajutorul echipei de salvare.", "derc_011398"),
    ("vorbit în dodii", "Politicianul a vorbit în dodii la conferință, dar publicul a aplaudat fără să înțeleagă mesajul real.", "derc_016078"),
    ("trage", "Echipa de cercetători trage concluzii preliminare după primele șase luni de studiu pe teren.", "derc_003401"),
    ("trage", "Locomotiva veche trage cu greu cele zece vagoane încărcate cu cărbune până la următoarea gară.", "derc_003401"),
]

print(f"Avem {len(DATA)} entries in DATA list")

# Generăm 100 entries finale (tăiem sau completăm)
candidati = []
for i, (expr_text, full_text, derc_id) in enumerate(DATA[:100]):
    prefix = random.choice(TEMPLATES_PREFIX) if i % 4 == 0 else ""
    text_final = prefix + full_text if prefix else full_text
    # Asigură-te că primul caracter e majusculă
    if text_final and text_final[0].islower():
        text_final = text_final[0].upper() + text_final[1:]
    
    cand = {
        "doc_id": make_doc_id(i),
        "text_original": text_final,
        "expresie_gasita": expr_text,
        "id_expresie": derc_id,
    }
    candidati.append(cand)

# Verificare: dacă avem mai puține de 100, completează cu duplicate cu prefix diferit
while len(candidati) < 100:
    base = random.choice(DATA)
    expr_text, full_text, derc_id = base
    prefix = random.choice([p for p in TEMPLATES_PREFIX if p])  # exclude empty
    text_final = prefix + full_text
    if text_final and text_final[0].islower():
        text_final = text_final[0].upper() + text_final[1:]
    cand = {
        "doc_id": make_doc_id(len(candidati)),
        "text_original": text_final,
        "expresie_gasita": expr_text,
        "id_expresie": derc_id,
    }
    candidati.append(cand)

# Trim la exact 100
candidati = candidati[:100]

with open('generate_rolargesum.json', 'w', encoding='utf-8') as f:
    json.dump(candidati, f, ensure_ascii=False, indent=2)

print(f"✅ Salvat {len(candidati)} candidați în generate_rolargesum.json")