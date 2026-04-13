moleküle = [
    # ─────────────────────────────────────────────────────────────
    # Alkane / Cycloalkane
    # ─────────────────────────────────────────────────────────────
    {"name": "Methan", "smiles": "C"},
    {"name": "Ethan", "smiles": "CC"},
    {"name": "Propan", "smiles": "CCC"},
    {"name": "Butan", "smiles": "CCCC"},
    {"name": "Isobutan", "smiles": "CC(C)C"},
    {"name": "Pentan", "smiles": "CCCCC"},
    {"name": "2-Methylbutan", "smiles": "CC(C)CC"},
    {"name": "Neopentan", "smiles": "CC(C)(C)C"},
    {"name": "1,1-Dimethylpropan", "smiles": "CC(C)(C)C"},
    {"name": "Hexan", "smiles": "CCCCCC"},
    {"name": "2-Methylpentan", "smiles": "CC(C)CCC"},
    {"name": "3-Methylpentan", "smiles": "CCC(C)CC"},
    {"name": "2,2-Dimethylbutan", "smiles": "CC(C)(C)CC"},
    {"name": "Heptan", "smiles": "CCCCCCC"},
    {"name": "Octan", "smiles": "CCCCCCCC"},
    {"name": "Cyclopropan", "smiles": "C1CC1"},
    {"name": "Cyclobutan", "smiles": "C1CCC1"},
    {"name": "Cyclopentan", "smiles": "C1CCCC1"},
    {"name": "Cyclohexan", "smiles": "C1CCCCC1"},
    {"name": "Methylcyclohexan", "smiles": "CC1CCCCC1"},
    {"name": "Decalin", "smiles": "C1CCC2CCCCC2C1"},

    # ─────────────────────────────────────────────────────────────
    # Alkene
    # ─────────────────────────────────────────────────────────────
    {"name": "Ethen", "smiles": "C=C"},
    {"name": "Propen", "smiles": "C=CC"},
    {"name": "But-1-en", "smiles": "C=CCC"},
    {"name": "But-2-en", "smiles": "CC=CC"},
    {"name": "(E)-But-2-en", "smiles": "C/C=C/C"},
    {"name": "(Z)-But-2-en", "smiles": "C/C=C\\C"},
    {"name": "2-Methylpropen", "smiles": "C=C(C)C"},
    {"name": "Pent-1-en", "smiles": "C=CCCC"},
    {"name": "Pent-2-en", "smiles": "CC=CCC"},
    {"name": "(E)-Pent-2-en", "smiles": "C/C=C/CC"},
    {"name": "(Z)-Pent-2-en", "smiles": "C/C=C\\CC"},
    {"name": "2-Methylbut-1-en", "smiles": "C=C(C)CC"},
    {"name": "2-Methylbut-2-en", "smiles": "CC=C(C)C"},
    {"name": "Cyclohexen", "smiles": "C1=CCCCC1"},
    {"name": "Styrol", "smiles": "C=Cc1ccccc1"},
    {"name": "Allylalkohol", "smiles": "C=CCO"},
    {"name": "Acrylsäuremethylester", "smiles": "C=CC(=O)OC"},

    # ─────────────────────────────────────────────────────────────
    # Alkine
    # ─────────────────────────────────────────────────────────────
    {"name": "Ethin", "smiles": "C#C"},
    {"name": "Propin", "smiles": "C#CC"},
    {"name": "But-1-in", "smiles": "C#CCC"},
    {"name": "But-2-in", "smiles": "CC#CC"},
    {"name": "Pent-1-in", "smiles": "C#CCCC"},
    {"name": "Hex-1-in", "smiles": "C#CCCCC"},
    {"name": "Hex-3-in", "smiles": "CCC#CCC"},
    {"name": "Phenylacetylen", "smiles": "C#Cc1ccccc1"},
    {"name": "Propargylalkohol", "smiles": "C#CCO"},

    # ─────────────────────────────────────────────────────────────
    # Alkohole / Diole / Triole
    # ─────────────────────────────────────────────────────────────
    {"name": "Methanol", "smiles": "CO"},
    {"name": "Ethanol", "smiles": "CCO"},
    {"name": "Propan-1-ol", "smiles": "CCCO"},
    {"name": "Propan-2-ol", "smiles": "CC(O)C"},
    {"name": "Butan-1-ol", "smiles": "CCCCO"},
    {"name": "Butan-2-ol", "smiles": "CCC(O)C"},
    {"name": "2-Methylpropan-1-ol", "smiles": "CC(C)CO"},
    {"name": "2-Methylpropan-2-ol", "smiles": "CC(C)(C)O"},
    {"name": "Pentan-1-ol", "smiles": "CCCCCO"},
    {"name": "Cyclohexanol", "smiles": "OC1CCCCC1"},
    {"name": "Benzylalkohol", "smiles": "OCc1ccccc1"},
    {"name": "2-Phenylethanol", "smiles": "OCCc1ccccc1"},
    {"name": "Ethylenglykol", "smiles": "OCCO"},
    {"name": "1,2-Propandiol", "smiles": "CC(O)CO"},
    {"name": "1,3-Propandiol", "smiles": "OCCCO"},
    {"name": "Glycerin", "smiles": "OCC(O)CO"},

    # ─────────────────────────────────────────────────────────────
    # Ether / Epoxide
    # ─────────────────────────────────────────────────────────────
    {"name": "Dimethylether", "smiles": "COC"},
    {"name": "Diethylether", "smiles": "CCOCC"},
    {"name": "Methyl-tert-butylether", "smiles": "COC(C)(C)C"},
    {"name": "Anisol", "smiles": "COc1ccccc1"},
    {"name": "Phenetol", "smiles": "CCOc1ccccc1"},
    {"name": "Tetrahydrofuran", "smiles": "C1CCOC1"},
    {"name": "1,4-Dioxan", "smiles": "O1CCOCC1"},
    {"name": "Oxiran (Ethylenoxid)", "smiles": "C1CO1"},
    {"name": "Propylenoxid", "smiles": "CC1CO1"},

    # ─────────────────────────────────────────────────────────────
    # Aldehyde
    # ─────────────────────────────────────────────────────────────
    {"name": "Methanal", "smiles": "C=O"},
    {"name": "Formaldehyd", "smiles": "C=O"},
    {"name": "Ethanal", "smiles": "CC=O"},
    {"name": "Propanal", "smiles": "CCC=O"},
    {"name": "Butanal", "smiles": "CCCC=O"},
    {"name": "2-Methylpropanal", "smiles": "CC(C)C=O"},
    {"name": "2,2-Dimethylpropanal", "smiles": "CC(C)(C)C=O"},
    {"name": "Acrolein", "smiles": "C=CC=O"},
    {"name": "(E)-Crotonaldehyd", "smiles": "C/C=C/C=O"},
    {"name": "Benzaldehyd", "smiles": "O=Cc1ccccc1"},
    {"name": "4-Methylbenzaldehyd", "smiles": "Cc1ccc(C=O)cc1"},
    {"name": "4-Methoxybenzaldehyd", "smiles": "COc1ccc(C=O)cc1"},
    {"name": "4-Hydroxybenzaldehyd", "smiles": "O=Cc1ccc(O)cc1"},
    {"name": "Salicylaldehyd", "smiles": "O=Cc1ccccc1O"},
    {"name": "Furfural", "smiles": "O=Cc1ccco1"},
    {"name": "Vanillin", "smiles": "COc1cc(C=O)ccc1O"},

    # ─────────────────────────────────────────────────────────────
    # Ketone
    # ─────────────────────────────────────────────────────────────
    {"name": "Propanon (Aceton)", "smiles": "CC(=O)C"},
    {"name": "Butan-2-on", "smiles": "CCC(=O)C"},
    {"name": "Pentan-2-on", "smiles": "CCCC(=O)C"},
    {"name": "Pentan-3-on", "smiles": "CCC(=O)CC"},
    {"name": "3-Methylbutan-2-on", "smiles": "CC(=O)C(C)C"},
    {"name": "4-Methylpentan-2-on", "smiles": "CC(=O)CC(C)C"},
    {"name": "Cyclohexanon", "smiles": "O=C1CCCCC1"},
    {"name": "Acetophenon", "smiles": "CC(=O)c1ccccc1"},
    {"name": "Propiophenon", "smiles": "CCC(=O)c1ccccc1"},
    {"name": "Benzophenon", "smiles": "O=C(c1ccccc1)c1ccccc1"},
    {"name": "Benzil", "smiles": "O=C(c1ccccc1)C(=O)c1ccccc1"},
    {"name": "p-Benzochinon", "smiles": "O=C1C=CC(=O)C=C1"},
    {"name": "Chalcon", "smiles": "O=C(/C=C/c1ccccc1)c1ccccc1"},

    # ─────────────────────────────────────────────────────────────
    # Carbonsäuren
    # ─────────────────────────────────────────────────────────────
    {"name": "Ameisensäure", "smiles": "O=CO"},
    {"name": "Essigsäure", "smiles": "CC(=O)O"},
    {"name": "Propionsäure", "smiles": "CCC(=O)O"},
    {"name": "Buttersäure", "smiles": "CCCC(=O)O"},
    {"name": "Isobuttersäure", "smiles": "CC(C)C(=O)O"},
    {"name": "Acrylsäure", "smiles": "C=CC(=O)O"},
    {"name": "Methacrylsäure", "smiles": "C=C(C)C(=O)O"},
    {"name": "Benzoesäure", "smiles": "O=C(O)c1ccccc1"},
    {"name": "Salicylsäure", "smiles": "O=C(O)c1ccccc1O"},
    {"name": "4-Hydroxybenzoesäure", "smiles": "O=C(O)c1ccc(O)cc1"},
    {"name": "Zimtsäure", "smiles": "O=C(O)C=Cc1ccccc1"},
    {"name": "Oxalsäure", "smiles": "O=C(O)C(=O)O"},
    {"name": "Malonsäure", "smiles": "O=C(O)CC(=O)O"},
    {"name": "Bernsteinsäure", "smiles": "O=C(O)CCC(=O)O"},
    {"name": "Aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O"},

    # ─────────────────────────────────────────────────────────────
    # Ester / Anhydride / Carbonate
    # ─────────────────────────────────────────────────────────────
    {"name": "Methylacetat", "smiles": "CC(=O)OC"},
    {"name": "Ethylacetat", "smiles": "CC(=O)OCC"},
    {"name": "Propylacetat", "smiles": "CC(=O)OCCC"},
    {"name": "Isopropylacetat", "smiles": "CC(=O)OC(C)C"},
    {"name": "Methylpropionat", "smiles": "CCC(=O)OC"},
    {"name": "Methylbutyrat", "smiles": "CCCC(=O)OC"},
    {"name": "Methylbenzoat", "smiles": "COC(=O)c1ccccc1"},
    {"name": "Ethylbenzoat", "smiles": "CCOC(=O)c1ccccc1"},
    {"name": "Methylsalicylat", "smiles": "COC(=O)c1ccccc1O"},
    {"name": "Benzylacetat", "smiles": "CC(=O)OCc1ccccc1"},
    {"name": "Methylmethacrylat", "smiles": "C=C(C)C(=O)OC"},
    {"name": "Dimethylcarbonat", "smiles": "COC(=O)OC"},
    {"name": "Essigsäureanhydrid", "smiles": "CC(=O)OC(=O)C"},

    # ─────────────────────────────────────────────────────────────
    # Amide / Harnstoff-Derivate
    # ─────────────────────────────────────────────────────────────
    {"name": "Acetamid", "smiles": "CC(=O)N"},
    {"name": "Propionamid", "smiles": "CCC(=O)N"},
    {"name": "Benzamid", "smiles": "NC(=O)c1ccccc1"},
    {"name": "N-Methylacetamid", "smiles": "CC(=O)NC"},
    {"name": "N,N-Dimethylacetamid", "smiles": "CC(=O)N(C)C"},
    {"name": "Dimethylformamid (DMF)", "smiles": "CN(C)C=O"},
    {"name": "Harnstoff", "smiles": "NC(N)=O"},
    {"name": "Acetanilid", "smiles": "CC(=O)Nc1ccccc1"},
    {"name": "Paracetamol", "smiles": "CC(=O)Nc1ccc(O)cc1"},

    # ─────────────────────────────────────────────────────────────
    # Amine
    # ─────────────────────────────────────────────────────────────
    {"name": "Methylamin", "smiles": "CN"},
    {"name": "Ethylamin", "smiles": "CCN"},
    {"name": "Propylamin", "smiles": "CCCN"},
    {"name": "Isopropylamin", "smiles": "CC(N)C"},
    {"name": "tert-Butylamin", "smiles": "CC(C)(C)N"},
    {"name": "Dimethylamin", "smiles": "CNC"},
    {"name": "Diethylamin", "smiles": "CCNCC"},
    {"name": "Triethylamin", "smiles": "CCN(CC)CC"},
    {"name": "Anilin", "smiles": "Nc1ccccc1"},
    {"name": "p-Toluidin", "smiles": "Cc1ccc(N)cc1"},
    {"name": "p-Anisidin", "smiles": "COc1ccc(N)cc1"},
    {"name": "N-Methylanilin", "smiles": "CNc1ccccc1"},
    {"name": "Benzylamin", "smiles": "NCc1ccccc1"},
    {"name": "Piperidin", "smiles": "N1CCCCC1"},
    {"name": "Pyrrolidin", "smiles": "N1CCCC1"},
    {"name": "Morpholin", "smiles": "O1CCNCC1"},

    # ─────────────────────────────────────────────────────────────
    # Nitrile / Nitro / Imin
    # ─────────────────────────────────────────────────────────────
    {"name": "Acetonitril", "smiles": "CC#N"},
    {"name": "Propionitril", "smiles": "CCC#N"},
    {"name": "Isobutyronitril", "smiles": "CC(C)C#N"},
    {"name": "Acrylnitril", "smiles": "C=CC#N"},
    {"name": "Benzonitril", "smiles": "N#Cc1ccccc1"},
    {"name": "Nitromethan", "smiles": "C[N+](=O)[O-]"},
    {"name": "Nitroethan", "smiles": "CC[N+](=O)[O-]"},
    {"name": "1-Nitropropan", "smiles": "CCC[N+](=O)[O-]"},
    {"name": "Nitrobenzol", "smiles": "[O-][N+](=O)c1ccccc1"},
    {"name": "o-Nitrotoluol", "smiles": "Cc1ccccc1[N+](=O)[O-]"},
    {"name": "m-Nitrotoluol", "smiles": "Cc1cccc([N+](=O)[O-])c1"},
    {"name": "p-Nitrotoluol", "smiles": "Cc1ccc([N+](=O)[O-])cc1"},
    {"name": "p-Nitrophenol", "smiles": "Oc1ccc([N+](=O)[O-])cc1"},
    {"name": "Ethanimin", "smiles": "CC=[NH]"},
    {"name": "Benzylidenanilin", "smiles": "c1ccccc1/C=N/c2ccccc2"},

    # ─────────────────────────────────────────────────────────────
    # Halogenverbindungen
    # ─────────────────────────────────────────────────────────────
    {"name": "Chlormethan", "smiles": "CCl"},
    {"name": "Dichlormethan", "smiles": "ClCCl"},
    {"name": "Chloroform", "smiles": "ClC(Cl)Cl"},
    {"name": "Tetrachlormethan", "smiles": "ClC(Cl)(Cl)Cl"},
    {"name": "Bromethan", "smiles": "CCBr"},
    {"name": "1-Chlorpropan", "smiles": "CCCCl"},
    {"name": "2-Chlorpropan", "smiles": "CC(Cl)C"},
    {"name": "1-Brombutan", "smiles": "CCCCBr"},
    {"name": "tert-Butylchlorid", "smiles": "CC(C)(C)Cl"},
    {"name": "Fluorbenzol", "smiles": "Fc1ccccc1"},
    {"name": "Chlorbenzol", "smiles": "Clc1ccccc1"},
    {"name": "Brombenzol", "smiles": "Brc1ccccc1"},
    {"name": "Benzylchlorid", "smiles": "ClCc1ccccc1"},
    {"name": "Benzylbromid", "smiles": "BrCc1ccccc1"},
    {"name": "p-Dichlorbenzol", "smiles": "Clc1ccc(Cl)cc1"},
    {"name": "o-Chlortoluol", "smiles": "Cc1ccccc1Cl"},
    {"name": "m-Chlortoluol", "smiles": "Cc1cccc(Cl)c1"},
    {"name": "p-Chlortoluol", "smiles": "Cc1ccc(Cl)cc1"},

    # ─────────────────────────────────────────────────────────────
    # Aromaten / Phenole / Substitutionsmuster
    # ─────────────────────────────────────────────────────────────
    {"name": "Benzol", "smiles": "c1ccccc1"},
    {"name": "Toluol", "smiles": "Cc1ccccc1"},
    {"name": "Ethylbenzol", "smiles": "CCc1ccccc1"},
    {"name": "Cumol (Isopropylbenzol)", "smiles": "CC(C)c1ccccc1"},
    {"name": "n-Propylbenzol", "smiles": "CCCc1ccccc1"},
    {"name": "o-Xylol", "smiles": "Cc1ccccc1C"},
    {"name": "m-Xylol", "smiles": "Cc1cccc(C)c1"},
    {"name": "p-Xylol", "smiles": "Cc1ccc(C)cc1"},
    {"name": "Mesitylen", "smiles": "Cc1cc(C)cc(C)c1"},
    {"name": "Phenol", "smiles": "Oc1ccccc1"},
    {"name": "o-Kresol", "smiles": "Cc1ccccc1O"},
    {"name": "m-Kresol", "smiles": "Cc1cccc(O)c1"},
    {"name": "p-Kresol", "smiles": "Cc1ccc(O)cc1"},
    {"name": "Catechol", "smiles": "Oc1ccccc1O"},
    {"name": "Resorcin", "smiles": "Oc1cccc(O)c1"},
    {"name": "Hydrochinon", "smiles": "Oc1ccc(O)cc1"},
    {"name": "Guajacol", "smiles": "COc1ccccc1O"},

    # ─────────────────────────────────────────────────────────────
    # Schwefel / Phosphor
    # ─────────────────────────────────────────────────────────────
    {"name": "Methanthiol", "smiles": "CS"},
    {"name": "Ethanthiol", "smiles": "CCS"},
    {"name": "Dimethylsulfid", "smiles": "CSC"},
    {"name": "Thioanisol", "smiles": "CSc1ccccc1"},
    {"name": "Thiophenol", "smiles": "Sc1ccccc1"},
    {"name": "Dimethylsulfoxid", "smiles": "CS(=O)C"},
    {"name": "Dimethylsulfon", "smiles": "CS(=O)(=O)C"},
    {"name": "Triethylphosphat", "smiles": "CCOP(=O)(OCC)OCC"},

    # ─────────────────────────────────────────────────────────────
    # Heteroaromaten / höheres Niveau
    # ─────────────────────────────────────────────────────────────
    {"name": "Pyridin", "smiles": "c1ccncc1"},
    {"name": "Pyrrol", "smiles": "c1cc[nH]c1"},
    {"name": "Furan", "smiles": "c1ccoc1"},
    {"name": "Thiophen", "smiles": "c1ccsc1"},
    {"name": "Indol", "smiles": "c1ccc2[nH]ccc2c1"},
    {"name": "Quinolin", "smiles": "c1ccc2ncccc2c1"},

    # ─────────────────────────────────────────────────────────────
    # Teste für trans/cis
    # ─────────────────────────────────────────────────────────────
    {"name": "(E)-2-Buten", "smiles": "C/C=C/C"},
    {"name": "(Z)-2-Buten", "smiles": "C/C=C\\C"},

    # ─────────────────────────────────────────────────────────────
    # Teste für Neue Funktionen im IR
    # ─────────────────────────────────────────────────────────────
    {"name": "Acetylchlorid", "smiles": "CC(=O)Cl"},
    {"name": "DMSO", "smiles": "CS(=O)C"},
    {"name": "Dimethylsulfoxid", "smiles": "CS(=O)C"},
    {"name": "Dimethylsulfon", "smiles": "CS(=O)(=O)C"},
    {"name": "Methylcarbamat", "smiles": "COC(=O)N"},
    {"name": "Ethyl-N-methylcarbamat", "smiles": "CCOC(=O)NC"},
]

moleküle.extend([
    {"name": "Benzoesäureethylester", "smiles": "CCOC(=O)c1ccccc1"},
    {"name": "Benzylalkohol", "smiles": "OCc1ccccc1"},
    {"name": "Benzaldehyd", "smiles": "O=Cc1ccccc1"},
    {"name": "Toluol", "smiles": "Cc1ccccc1"},
    {"name": "2-Nitrophenol", "smiles": "O=[N+]([O-])c1ccccc1O"},
    {"name": "4-Nitrophenol", "smiles": "O=[N+]([O-])c1ccc(O)cc1"},
    {"name": "Acetanilid", "smiles": "CC(=O)Nc1ccccc1"},
    {"name": "p-Chloroanilin", "smiles": "Nc1ccc(Cl)cc1"},
    {"name": "Hydrochinondimethylether", "smiles": "COc1ccc(OC)cc1"},
    {"name": "8-Hydroxychinolin", "smiles": "Oc1cccc2ncccc12"},
    {"name": "Phenol", "smiles": "Oc1ccccc1"},
    {"name": "Naphthalin", "smiles": "c1ccc2ccccc2c1"},
    {"name": "2-Naphthol", "smiles": "Oc1ccc2ccccc2c1"},
    {"name": "p-Toluolsulfonsäure", "smiles": "Cc1ccc(S(=O)(=O)O)cc1"},
    {"name": "2-Octen", "smiles": "CC=CCCCCC"},
    {"name": "Cyclohexen", "smiles": "C1=CCCCC1"},
    {"name": "Butoxybenzol", "smiles": "CCCCOc1ccccc1"},
    {"name": "2-Phenyl-1-propanol", "smiles": "CC(CO)c1ccccc1"},
    {"name": "3-Nitrobenzaldehyd", "smiles": "O=Cc1cccc([N+](=O)[O-])c1"},
    {"name": "2-Brommesitylen", "smiles": "Cc1cc(C)c(Br)c(C)c1"},
    {"name": "(4-Nitrophenyl)(p-tolyl)methanon", "smiles": "Cc1ccc(C(=O)c2ccc([N+](=O)[O-])cc2)cc1"},
    {"name": "1-(3-Nitrophenyl)ethanol", "smiles": "CC(O)c1cccc([N+](=O)[O-])c1"},
    {"name": "Geraniol", "smiles": "CC(C)=CCCC(C)=CCO"},
    {"name": "Citral", "smiles": "CC(C)=CCCC(C)=CC=O"},
    {"name": "Benzylacetat", "smiles": "CC(=O)OCc1ccccc1"},
    {"name": "Dibenzylidenaceton", "smiles": "O=C(C=Cc1ccccc1)/C=C/c1ccccc1"},
    {"name": "Butylmalonsäurediethylester", "smiles": "CCCCC(C(=O)OCC)C(=O)OCC"},
    {"name": "1,1-Diphenylethanol", "smiles": "CC(O)(c1ccccc1)c1ccccc1"},
    {"name": "(E)-1,2-Diphenylethen", "smiles": "C(=C/c1ccccc1)\\c1ccccc1"},
    {"name": "Trimyristin", "smiles": "CCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC"},
    {"name": "Indigo", "smiles": "O=C1/C(=C2\\Nc3ccccc3C2=O)Nc2ccccc21"},
])