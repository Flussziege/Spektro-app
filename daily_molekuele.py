moleküle_daily = [
    # ─────────────────────────────────────────────────────────────
    # Alkane / Cycloalkane
    # ─────────────────────────────────────────────────────────────
    {"name_de": ["Neopentan", "1,1-Dimethylpropan"], "name_en": ["Neopentane", "1,1-Dimethylpropane"], "smiles": "CC(C)(C)C", "difficulty": "medium"},
    {"name_de": "2,2-Dimethylbutan", "name_en": "2,2-Dimethylbutane", "smiles": "CC(C)(C)CC", "difficulty": "medium"},
    {"name_de": "Decalin", "name_en": "Decalin", "smiles": "C1CCC2CCCCC2C1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Alkene
    # ─────────────────────────────────────────────────────────────
    {"name_de": ["(E)-But-2-en", "(E)-2-Buten"], "name_en": ["(E)-But-2-ene", "(E)-2-Butene"], "smiles": "C/C=C/C", "difficulty": "medium"},
    {"name_de": ["(Z)-But-2-en", "(Z)-2-Buten"], "name_en": ["(Z)-But-2-ene", "(Z)-2-Butene"], "smiles": "C/C=C\\C", "difficulty": "medium"},
    {"name_de": "(E)-Pent-2-en", "name_en": "(E)-Pent-2-ene", "smiles": "C/C=C/CC", "difficulty": "medium"},
    {"name_de": "(Z)-Pent-2-en", "name_en": "(Z)-Pent-2-ene", "smiles": "C/C=C\\CC", "difficulty": "medium"},
    {"name_de": "2-Methylbut-1-en", "name_en": "2-Methylbut-1-ene", "smiles": "C=C(C)CC", "difficulty": "medium"},
    {"name_de": "2-Methylbut-2-en", "name_en": "2-Methylbut-2-ene", "smiles": "CC=C(C)C", "difficulty": "medium"},
    {"name_de": "Cyclohexen", "name_en": "Cyclohexene", "smiles": "C1=CCCCC1", "difficulty": "medium"},
    {"name_de": "Styrol", "name_en": "Styrene", "smiles": "C=Cc1ccccc1", "difficulty": "medium"},
    {"name_de": "Allylalkohol", "name_en": "Allyl alcohol", "smiles": "C=CCO", "difficulty": "medium"},
    {"name_de": "Acrylsäuremethylester", "name_en": "Methyl acrylate", "smiles": "C=CC(=O)OC", "difficulty": "medium"},
    {"name_de": "2-Octen", "name_en": "2-Octene", "smiles": "CC=CCCCCC", "difficulty": "medium"},
    {"name_de": "(E)-1,2-Diphenylethen", "name_en": "(E)-1,2-Diphenylethene", "smiles": "C(=C/c1ccccc1)\\c1ccccc1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Alkine
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Hex-3-in", "name_en": "Hex-3-yne", "smiles": "CCC#CCC", "difficulty": "medium"},
    {"name_de": "Phenylacetylen", "name_en": "Phenylacetylene", "smiles": "C#Cc1ccccc1", "difficulty": "medium"},
    {"name_de": "Propargylalkohol", "name_en": "Propargyl alcohol", "smiles": "C#CCO", "difficulty": "medium"},

    # ─────────────────────────────────────────────────────────────
    # Alkohole / Diole / Triole
    # ─────────────────────────────────────────────────────────────
    {"name_de": "2-Methylpropan-1-ol", "name_en": "2-Methylpropan-1-ol", "smiles": "CC(C)CO", "difficulty": "medium"},
    {"name_de": "2-Methylpropan-2-ol", "name_en": "2-Methylpropan-2-ol", "smiles": "CC(C)(C)O", "difficulty": "medium"},
    {"name_de": "Cyclohexanol", "name_en": "Cyclohexanol", "smiles": "OC1CCCCC1", "difficulty": "medium"},
    {"name_de": "Benzylalkohol", "name_en": "Benzyl alcohol", "smiles": "OCc1ccccc1", "difficulty": "medium"},
    {"name_de": "2-Phenylethanol", "name_en": "2-Phenylethanol", "smiles": "OCCc1ccccc1", "difficulty": "medium"},
    {"name_de": "Ethylenglykol", "name_en": "Ethylene glycol", "smiles": "OCCO", "difficulty": "medium"},
    {"name_de": "1,2-Propandiol", "name_en": "1,2-Propanediol", "smiles": "CC(O)CO", "difficulty": "medium"},
    {"name_de": "1,3-Propandiol", "name_en": "1,3-Propanediol", "smiles": "OCCCO", "difficulty": "medium"},
    {"name_de": "Glycerin", "name_en": "Glycerol", "smiles": "OCC(O)CO", "difficulty": "medium"},
    {"name_de": "2-Phenyl-1-propanol", "name_en": "2-Phenyl-1-propanol", "smiles": "CC(CO)c1ccccc1", "difficulty": "hard"},
    {"name_de": "1-(3-Nitrophenyl)ethanol", "name_en": "1-(3-Nitrophenyl)ethanol", "smiles": "CC(O)c1cccc([N+](=O)[O-])c1", "difficulty": "hard"},
    {"name_de": "1,1-Diphenylethanol", "name_en": "1,1-Diphenylethanol", "smiles": "CC(O)(c1ccccc1)c1ccccc1", "difficulty": "hard"},
    {"name_de": "Geraniol", "name_en": "Geraniol", "smiles": "CC(C)=CCCC(C)=CCO", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Ether / Epoxide
    # ─────────────────────────────────────────────────────────────
    {"name_de": ["Methyl-tert-butylether", "1-Methoxy-2-methylpropan"], "name_en": ["Methyl tert-butyl ether", "1-Methoxy-2-methylpropane"], "smiles": "COC(C)(C)C", "difficulty": "medium"},
    {"name_de": ["Anisol", "Methoxybenzol"], "name_en": ["Anisole", "Methoxybenzene"], "smiles": "COc1ccccc1", "difficulty": "medium"},
    {"name_de": ["Phenetol", "Ethoxybenzol"], "name_en": ["Phenetole", "Ethoxybenzene"], "smiles": "CCOc1ccccc1", "difficulty": "medium"},
    {"name_de": ["Tetrahydrofuran", "Oxolan"], "name_en": ["Tetrahydrofuran", "Oxolane"], "smiles": "C1CCOC1", "difficulty": "medium"},
    {"name_de": "1,4-Dioxan", "name_en": "1,4-Dioxane", "smiles": "O1CCOCC1", "difficulty": "medium"},
    {"name_de": "Oxiran (Ethylenoxid)", "name_en": "Oxirane (ethylene oxide)", "smiles": "C1CO1", "difficulty": "medium"},
    {"name_de": ["Propylenoxid", "2-Methyloxiran"], "name_en": ["Propylene oxide", "2-Methyloxirane"], "smiles": "CC1CO1", "difficulty": "medium"},
    {"name_de": ["Hydrochinondimethylether", "1,4-Dimethoxybenzol"], "name_en": ["Hydroquinone dimethyl ether", "1,4-Dimethoxybenzene"], "smiles": "COc1ccc(OC)cc1", "difficulty": "hard"},
    {"name_de": "Butoxybenzol", "name_en": "Butoxybenzene", "smiles": "CCCCOc1ccccc1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Aldehyde
    # ─────────────────────────────────────────────────────────────
    {"name_de": "2-Methylpropanal", "name_en": "2-Methylpropanal", "smiles": "CC(C)C=O", "difficulty": "medium"},
    {"name_de": "2,2-Dimethylpropanal", "name_en": "2,2-Dimethylpropanal", "smiles": "CC(C)(C)C=O", "difficulty": "medium"},
    {"name_de": ["Acrolein", "Propenal"], "name_en": ["Acrolein", "Propenal"], "smiles": "C=CC=O", "difficulty": "medium"},
    {"name_de": "(E)-Crotonaldehyd", "name_en": "(E)-Crotonaldehyde", "smiles": "C/C=C/C=O", "difficulty": "medium"},
    {"name_de": ["Benzaldehyd", "Benzenecarbaldehyd"], "name_en": ["Benzaldehyde", "Benzenecarbaldehyde"], "smiles": "O=Cc1ccccc1", "difficulty": "medium"},
    {"name_de": "4-Methylbenzaldehyd", "name_en": "4-Methylbenzaldehyde", "smiles": "Cc1ccc(C=O)cc1", "difficulty": "hard"},
    {"name_de": "4-Methoxybenzaldehyd", "name_en": "4-Methoxybenzaldehyde", "smiles": "COc1ccc(C=O)cc1", "difficulty": "hard"},
    {"name_de": "4-Hydroxybenzaldehyd", "name_en": "4-Hydroxybenzaldehyde", "smiles": "O=Cc1ccc(O)cc1", "difficulty": "hard"},
    {"name_de": "Salicylaldehyd", "name_en": "Salicylaldehyde", "smiles": "O=Cc1ccccc1O", "difficulty": "hard"},
    {"name_de": ["Furfural", "Furan-2-carbaldehyd"], "name_en": ["Furfural", "Furan-2-carbaldehyde"], "smiles": "O=Cc1ccco1", "difficulty": "hard"},
    {"name_de": "Vanillin", "name_en": "Vanillin", "smiles": "COc1cc(C=O)ccc1O", "difficulty": "hard"},
    {"name_de": "3-Nitrobenzaldehyd", "name_en": "3-Nitrobenzaldehyde", "smiles": "O=Cc1cccc([N+](=O)[O-])c1", "difficulty": "hard"},
    {"name_de": "Citral", "name_en": "Citral", "smiles": "CC(C)=CCCC(C)=CC=O", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Ketone
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Pentan-3-on", "name_en": "Pentan-3-one", "smiles": "CCC(=O)CC", "difficulty": "medium"},
    {"name_de": "3-Methylbutan-2-on", "name_en": "3-Methylbutan-2-one", "smiles": "CC(=O)C(C)C", "difficulty": "medium"},
    {"name_de": "4-Methylpentan-2-on", "name_en": "4-Methylpentan-2-one", "smiles": "CC(=O)CC(C)C", "difficulty": "medium"},
    {"name_de": "Cyclohexanon", "name_en": "Cyclohexanone", "smiles": "O=C1CCCCC1", "difficulty": "medium"},
    {"name_de": ["Acetophenon", "1-Phenylethanon"], "name_en": ["Acetophenone", "1-Phenylethanone"], "smiles": "CC(=O)c1ccccc1", "difficulty": "medium"},
    {"name_de": ["Propiophenon", "1-Phenylpropanon"], "name_en": ["Propiophenone", "1-Phenylpropanone"], "smiles": "CCC(=O)c1ccccc1", "difficulty": "hard"},
    {"name_de": ["Benzophenon", "Diphenylethanon"], "name_en": ["Benzophenone", "Diphenylethanone"], "smiles": "O=C(c1ccccc1)c1ccccc1", "difficulty": "hard"},
    {"name_de": ["Benzil", "Diphenyletan-1,2-dion"], "name_en": ["Benzil", "Diphenylethane-1,2-dione"], "smiles": "O=C(c1ccccc1)C(=O)c1ccccc1", "difficulty": "hard"},
    {"name_de": ["p-Benzochinon", "Cyclohexadien-1,4-dion"], "name_en": ["p-Benzoquinone", "Cyclohexadiene-1,4-dione"], "smiles": "O=C1C=CC(=O)C=C1", "difficulty": "hard"},
    {"name_de": ["Chalcon", "1,3-Diphenylprop-2-en-1-on"], "name_en": ["Chalcone", "1,3-Diphenylprop-2-en-1-one"], "smiles": "O=C(/C=C/c1ccccc1)c1ccccc1", "difficulty": "hard"},
    {"name_de": "(4-Nitrophenyl)(p-tolyl)methanon", "name_en": "(4-Nitrophenyl)(p-tolyl)methanone", "smiles": "Cc1ccc(C(=O)c2ccc([N+](=O)[O-])cc2)cc1", "difficulty": "hard"},
    {"name_de": "Dibenzylidenaceton", "name_en": "Dibenzylideneacetone", "smiles": "O=C(C=Cc1ccccc1)/C=C/c1ccccc1", "difficulty": "hard"},
    {"name_de": "Indigo", "name_en": "Indigo", "smiles": "O=C1/C(=C2\\Nc3ccccc3C2=O)Nc2ccccc21", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Carbonsäuren
    # ─────────────────────────────────────────────────────────────
    {"name_de": ["Isobuttersäure", "2-Methylpropansäure"], "name_en": ["Isobutyric acid", "2-Methylpropanoic acid"], "smiles": "CC(C)C(=O)O", "difficulty": "medium"},
    {"name_de": "Acrylsäure", "name_en": "Acrylic acid", "smiles": "C=CC(=O)O", "difficulty": "medium"},
    {"name_de": "Methacrylsäure", "name_en": "Methacrylic acid", "smiles": "C=C(C)C(=O)O", "difficulty": "medium"},
    {"name_de": "Benzoesäure", "name_en": "Benzoic acid", "smiles": "O=C(O)c1ccccc1", "difficulty": "medium"},
    {"name_de": ["Salicylsäure", "2-Hydroxybenzoesäure"], "name_en": ["Salicylic acid", "2-Hydroxybenzoic acid"], "smiles": "O=C(O)c1ccccc1O", "difficulty": "hard"},
    {"name_de": "4-Hydroxybenzoesäure", "name_en": "4-Hydroxybenzoic acid", "smiles": "O=C(O)c1ccc(O)cc1", "difficulty": "hard"},
    {"name_de": "Zimtsäure", "name_en": "Cinnamic acid", "smiles": "O=C(O)C=Cc1ccccc1", "difficulty": "hard"},
    {"name_de": "Oxalsäure", "name_en": "Oxalic acid", "smiles": "O=C(O)C(=O)O", "difficulty": "medium"},
    {"name_de": "Malonsäure", "name_en": "Malonic acid", "smiles": "O=C(O)CC(=O)O", "difficulty": "medium"},
    {"name_de": "Bernsteinsäure", "name_en": "Succinic acid", "smiles": "O=C(O)CCC(=O)O", "difficulty": "medium"},
    {"name_de": ["Aspirin", "2-Acetoxybenzoesäure"], "name_en": ["Aspirin", "2-Acetoxybenzoic acid"], "smiles": "CC(=O)Oc1ccccc1C(=O)O", "difficulty": "hard"},
    {"name_de": "p-Toluolsulfonsäure", "name_en": "p-Toluenesulfonic acid", "smiles": "Cc1ccc(S(=O)(=O)O)cc1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Ester / Anhydride / Carbonate
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Propylacetat", "name_en": "Propyl acetate", "smiles": "CC(=O)OCCC", "difficulty": "medium"},
    {"name_de": "Isopropylacetat", "name_en": "Isopropyl acetate", "smiles": "CC(=O)OC(C)C", "difficulty": "medium"},
    {"name_de": "Methylpropionat", "name_en": "Methyl propionate", "smiles": "CCC(=O)OC", "difficulty": "medium"},
    {"name_de": "Methylbutyrat", "name_en": "Methyl butyrate", "smiles": "CCCC(=O)OC", "difficulty": "medium"},
    {"name_de": "Methylbenzoat", "name_en": "Methyl benzoate", "smiles": "COC(=O)c1ccccc1", "difficulty": "medium"},
    {"name_de": ["Ethylbenzoat", "Benzoesäureethylester"], "name_en": ["Ethyl benzoate", "Ethyl benzoate"], "smiles": "CCOC(=O)c1ccccc1", "difficulty": "medium"},
    {"name_de": "Methylsalicylat", "name_en": "Methyl salicylate", "smiles": "COC(=O)c1ccccc1O", "difficulty": "hard"},
    {"name_de": "Benzylacetat", "name_en": "Benzyl acetate", "smiles": "CC(=O)OCc1ccccc1", "difficulty": "medium"},
    {"name_de": "Methylmethacrylat", "name_en": "Methyl methacrylate", "smiles": "C=C(C)C(=O)OC", "difficulty": "medium"},
    {"name_de": "Dimethylcarbonat", "name_en": "Dimethyl carbonate", "smiles": "COC(=O)OC", "difficulty": "medium"},
    {"name_de": "Essigsäureanhydrid", "name_en": "Acetic anhydride", "smiles": "CC(=O)OC(=O)C", "difficulty": "medium"},
    {"name_de": "Butylmalonsäurediethylester", "name_en": "Diethyl butylmalonate", "smiles": "CCCCC(C(=O)OCC)C(=O)OCC", "difficulty": "hard"},
    {"name_de": "Trimyristin", "name_en": "Trimyristin", "smiles": "CCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCC", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Amide / Harnstoff-Derivate
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Acetamid", "name_en": "Acetamide", "smiles": "CC(=O)N", "difficulty": "medium"},
    {"name_de": "Propionamid", "name_en": "Propionamide", "smiles": "CCC(=O)N", "difficulty": "medium"},
    {"name_de": "Benzamid", "name_en": "Benzamide", "smiles": "NC(=O)c1ccccc1", "difficulty": "medium"},
    {"name_de": "N-Methylacetamid", "name_en": "N-Methylacetamide", "smiles": "CC(=O)NC", "difficulty": "medium"},
    {"name_de": "N,N-Dimethylacetamid", "name_en": "N,N-Dimethylacetamide", "smiles": "CC(=O)N(C)C", "difficulty": "medium"},
    {"name_de": "Dimethylformamid (DMF)", "name_en": "Dimethylformamide (DMF)", "smiles": "CN(C)C=O", "difficulty": "medium"},
    {"name_de": "Harnstoff", "name_en": "Urea", "smiles": "NC(N)=O", "difficulty": "medium"},
    {"name_de": "Acetanilid", "name_en": "Acetanilide", "smiles": "CC(=O)Nc1ccccc1", "difficulty": "hard"},
    {"name_de": "Paracetamol", "name_en": "Paracetamol", "smiles": "CC(=O)Nc1ccc(O)cc1", "difficulty": "hard"},
    {"name_de": "Methylcarbamat", "name_en": "Methyl carbamate", "smiles": "COC(=O)N", "difficulty": "medium"},
    {"name_de": "Ethyl-N-methylcarbamat", "name_en": "Ethyl N-methylcarbamate", "smiles": "CCOC(=O)NC", "difficulty": "medium"},

    # ─────────────────────────────────────────────────────────────
    # Amine
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Isopropylamin", "name_en": "Isopropylamine", "smiles": "CC(N)C", "difficulty": "medium"},
    {"name_de": "tert-Butylamin", "name_en": "tert-Butylamine", "smiles": "CC(C)(C)N", "difficulty": "medium"},
    {"name_de": "Diethylamin", "name_en": "Diethylamine", "smiles": "CCNCC", "difficulty": "medium"},
    {"name_de": "Triethylamin", "name_en": "Triethylamine", "smiles": "CCN(CC)CC", "difficulty": "medium"},
    {"name_de": ["Anilin", "Phenylamin"], "name_en": ["Aniline", "Phenylamine"], "smiles": "Nc1ccccc1", "difficulty": "medium"},
    {"name_de": ["p-Toluidin", "4-Methylanilin"], "name_en": ["p-Toluidine", "4-Methylaniline"], "smiles": "Cc1ccc(N)cc1", "difficulty": "hard"},
    {"name_de": ["p-Anisidin", "4-Methoxyanilin"], "name_en": ["p-Anisidine", "4-Methoxyaniline"], "smiles": "COc1ccc(N)cc1", "difficulty": "hard"},
    {"name_de": "N-Methylanilin", "name_en": "N-Methylaniline", "smiles": "CNc1ccccc1", "difficulty": "hard"},
    {"name_de": "Benzylamin", "name_en": "Benzylamine", "smiles": "NCc1ccccc1", "difficulty": "medium"},
    {"name_de": "Piperidin", "name_en": "Piperidine", "smiles": "N1CCCCC1", "difficulty": "medium"},
    {"name_de": "Pyrrolidin", "name_en": "Pyrrolidine", "smiles": "N1CCCC1", "difficulty": "medium"},
    {"name_de": "Morpholin", "name_en": "Morpholine", "smiles": "O1CCNCC1", "difficulty": "medium"},
    {"name_de": "p-Chloroanilin", "name_en": "p-Chloroaniline", "smiles": "Nc1ccc(Cl)cc1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Nitrile / Nitro / Imin
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Isobutyronitril", "name_en": "Isobutyronitrile", "smiles": "CC(C)C#N", "difficulty": "medium"},
    {"name_de": "Acrylnitril", "name_en": "Acrylonitrile", "smiles": "C=CC#N", "difficulty": "medium"},
    {"name_de": "Benzonitril", "name_en": "Benzonitrile", "smiles": "N#Cc1ccccc1", "difficulty": "medium"},
    {"name_de": "1-Nitropropan", "name_en": "1-Nitropropane", "smiles": "CCC[N+](=O)[O-]", "difficulty": "medium"},
    {"name_de": "Nitrobenzol", "name_en": "Nitrobenzene", "smiles": "[O-][N+](=O)c1ccccc1", "difficulty": "medium"},
    {"name_de": "o-Nitrotoluol", "name_en": "o-Nitrotoluene", "smiles": "Cc1ccccc1[N+](=O)[O-]", "difficulty": "hard"},
    {"name_de": "m-Nitrotoluol", "name_en": "m-Nitrotoluene", "smiles": "Cc1cccc([N+](=O)[O-])c1", "difficulty": "hard"},
    {"name_de": "p-Nitrotoluol", "name_en": "p-Nitrotoluene", "smiles": "Cc1ccc([N+](=O)[O-])cc1", "difficulty": "hard"},
    {"name_de": "2-Nitrophenol", "name_en": "2-Nitrophenol", "smiles": "O=[N+]([O-])c1ccccc1O", "difficulty": "hard"},
    {"name_de": "4-Nitrophenol", "name_en": "4-Nitrophenol", "smiles": "O=[N+]([O-])c1ccc(O)cc1", "difficulty": "hard"},
    {"name_de": "Ethanimin", "name_en": "Ethanimine", "smiles": "CC=[NH]", "difficulty": "medium"},
    {"name_de": "Benzylidenanilin", "name_en": "Benzylideneaniline", "smiles": "c1ccccc1/C=N/c2ccccc2", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Halogenverbindungen
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Tetrachlormethan", "name_en": "Carbon tetrachloride", "smiles": "ClC(Cl)(Cl)Cl", "difficulty": "medium"},
    {"name_de": "2-Chlorpropan", "name_en": "2-Chloropropane", "smiles": "CC(Cl)C", "difficulty": "medium"},
    {"name_de": "tert-Butylchlorid", "name_en": "tert-Butyl chloride", "smiles": "CC(C)(C)Cl", "difficulty": "medium"},
    {"name_de": "Fluorbenzol", "name_en": "Fluorobenzene", "smiles": "Fc1ccccc1", "difficulty": "medium"},
    {"name_de": "Chlorbenzol", "name_en": "Chlorobenzene", "smiles": "Clc1ccccc1", "difficulty": "medium"},
    {"name_de": "Brombenzol", "name_en": "Bromobenzene", "smiles": "Brc1ccccc1", "difficulty": "medium"},
    {"name_de": "Benzylchlorid", "name_en": "Benzyl chloride", "smiles": "ClCc1ccccc1", "difficulty": "medium"},
    {"name_de": "Benzylbromid", "name_en": "Benzyl bromide", "smiles": "BrCc1ccccc1", "difficulty": "medium"},
    {"name_de": "p-Dichlorbenzol", "name_en": "p-Dichlorobenzene", "smiles": "Clc1ccc(Cl)cc1", "difficulty": "hard"},
    {"name_de": "o-Chlortoluol", "name_en": "o-Chlorotoluene", "smiles": "Cc1ccccc1Cl", "difficulty": "hard"},
    {"name_de": "m-Chlortoluol", "name_en": "m-Chlorotoluene", "smiles": "Cc1cccc(Cl)c1", "difficulty": "hard"},
    {"name_de": "p-Chlortoluol", "name_en": "p-Chlorotoluene", "smiles": "Cc1ccc(Cl)cc1", "difficulty": "hard"},
    {"name_de": "Acetylchlorid", "name_en": "Acetyl chloride", "smiles": "CC(=O)Cl", "difficulty": "medium"},
    {"name_de": "2-Brommesitylen", "name_en": "2-Bromomesitylene", "smiles": "Cc1cc(C)c(Br)c(C)c1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Aromaten / Phenole / Substitutionsmuster
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Benzol", "name_en": "Benzene", "smiles": "c1ccccc1", "difficulty": "medium"},
    {"name_de": ["Toluol", "Methylbenzol"], "name_en": ["Toluene", "Methylbenzene"], "smiles": "Cc1ccccc1", "difficulty": "medium"},
    {"name_de": "Ethylbenzol", "name_en": "Ethylbenzene", "smiles": "CCc1ccccc1", "difficulty": "medium"},
    {"name_de": "Cumol (Isopropylbenzol)", "name_en": "Cumene (isopropylbenzene)", "smiles": "CC(C)c1ccccc1", "difficulty": "medium"},
    {"name_de": "n-Propylbenzol", "name_en": "n-Propylbenzene", "smiles": "CCCc1ccccc1", "difficulty": "medium"},
    {"name_de": ["o-Xylol", "1,2-Dimethylbenzol"], "name_en": ["o-Xylene", "1,2-Dimethylbenzene"], "smiles": "Cc1ccccc1C", "difficulty": "hard"},
    {"name_de": ["m-Xylol", "1,3-Dimethylbenzol"], "name_en": ["m-Xylene", "1,3-Dimethylbenzene"], "smiles": "Cc1cccc(C)c1", "difficulty": "hard"},
    {"name_de": ["p-Xylol", "1,4-Dimethylbenzol"], "name_en": ["p-Xylene", "1,4-Dimethylbenzene"], "smiles": "Cc1ccc(C)cc1", "difficulty": "hard"},
    {"name_de": "Mesitylen", "name_en": "Mesitylene", "smiles": "Cc1cc(C)cc(C)c1", "difficulty": "hard"},
    {"name_de": ["Phenol", "Hydroxybenzol"], "name_en": ["Phenol", "Hydroxybenzene"], "smiles": "Oc1ccccc1", "difficulty": "medium"},
    {"name_de": ["o-Kresol", "2-Methylphenol"], "name_en": ["o-Cresol", "2-Methylphenol"], "smiles": "Cc1ccccc1O", "difficulty": "hard"},
    {"name_de": ["m-Kresol", "3-Methylphenol"], "name_en": ["m-Cresol", "3-Methylphenol"], "smiles": "Cc1cccc(O)c1", "difficulty": "hard"},
    {"name_de": ["p-Kresol", "4-Methylphenol"], "name_en": ["p-Cresol","4-Methylphenol"], "smiles": "Cc1ccc(O)cc1", "difficulty": "hard"},
    {"name_de": ["Catechol", "1,2-Dihydroxybenzol"], "name_en": ["Catechol", "1,2-Dihydroxybenzene"], "smiles": "Oc1ccccc1O", "difficulty": "hard"},
    {"name_de": ["Resorcin", "1,3-Dihydroxybenzol"], "name_en": ["Resorcinol", "1,3-Dihydroxybenzene"], "smiles": "Oc1cccc(O)c1", "difficulty": "hard"},
    {"name_de": ["Hydrochinon", "1,4-Dihydroxybenzol"], "name_en": ["Hydroquinone", "1,4-Dihydroxybenzene"], "smiles": "Oc1ccc(O)cc1", "difficulty": "hard"},
    {"name_de": "Guajacol", "name_en": "Guaiacol", "smiles": "COc1ccccc1O", "difficulty": "hard"},
    {"name_de": "Naphthalin", "name_en": "Naphthalene", "smiles": "c1ccc2ccccc2c1", "difficulty": "hard"},
    {"name_de": "2-Naphthol", "name_en": "2-Naphthol", "smiles": "Oc1ccc2ccccc2c1", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Schwefel / Phosphor
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Methanthiol", "name_en": "Methanethiol", "smiles": "CS", "difficulty": "medium"},
    {"name_de": "Ethanthiol", "name_en": "Ethanethiol", "smiles": "CCS", "difficulty": "medium"},
    {"name_de": "Dimethylsulfid", "name_en": "Dimethyl sulfide", "smiles": "CSC", "difficulty": "medium"},
    {"name_de": "Thioanisol", "name_en": "Thioanisole", "smiles": "CSc1ccccc1", "difficulty": "hard"},
    {"name_de": ["Thiophenol", "Benzentiol"], "name_en": ["Thiophenol", "Benzenethiol"], "smiles": "Sc1ccccc1", "difficulty": "hard"},
    {"name_de": ["DMSO", "Dimethylsulfoxid"], "name_en": ["DMSO", "Dimethyl sulfoxide"], "smiles": "CS(=O)C", "difficulty": "medium"},
    {"name_de": "Dimethylsulfon", "name_en": "Dimethyl sulfone", "smiles": "CS(=O)(=O)C", "difficulty": "medium"},
    {"name_de": "Triethylphosphat", "name_en": "Triethyl phosphate", "smiles": "CCOP(=O)(OCC)OCC", "difficulty": "hard"},

    # ─────────────────────────────────────────────────────────────
    # Heteroaromaten / höheres Niveau
    # ─────────────────────────────────────────────────────────────
    {"name_de": "Pyridin", "name_en": "Pyridine", "smiles": "c1ccncc1", "difficulty": "medium"},
    {"name_de": "Pyrrol", "name_en": "Pyrrole", "smiles": "c1cc[nH]c1", "difficulty": "medium"},
    {"name_de": "Furan", "name_en": "Furan", "smiles": "c1ccoc1", "difficulty": "medium"},
    {"name_de": "Thiophen", "name_en": "Thiophene", "smiles": "c1ccsc1", "difficulty": "medium"},
    {"name_de": "Indol", "name_en": "Indole", "smiles": "c1ccc2[nH]ccc2c1", "difficulty": "hard"},
    {"name_de": "Quinolin", "name_en": "Quinoline", "smiles": "c1ccc2ncccc2c1", "difficulty": "hard"},
    {"name_de": "8-Hydroxychinolin", "name_en": "8-Hydroxyquinoline", "smiles": "Oc1cccc2ncccc12", "difficulty": "hard"},
]