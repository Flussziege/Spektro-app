import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image, ImageTk
import io

#Dateien import
import liste_neu
from liste_neu import moleküle
import generator #13C
import generator2 #IR
import generator5 #EA
import hnmr #1H-NMR


root = tk.Tk()
root.title("Professional UI")
root.state("zoomed")
root.configure(bg="white")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="white")
style.configure("TLabel", background="white")

style.configure("Vertical.TScrollbar",
    gripcount=0,
    background="#d0d0d0",
    troughcolor="white",
    bordercolor="white",
    lightcolor="white",
    darkcolor="white"
)

style.map("Vertical.TScrollbar",
    background=[("active", "#a0a0a0")]
)

PRIMARY = "#2a72d4"
BG = "white"
TEXT = "#1a1a1a"

eingabe = tk.StringVar()
main_name_var = tk.StringVar()
app_state = {
    "smiles": None,
    "bild": False
}

# =========================
# FRAMES (Seiten)
# =========================
input_frame = ttk.Frame(root, padding=30)
result_frame = ttk.Frame(root, padding=30)
quizz_frame = ttk.Frame(root, padding=30)
antwort_frame = ttk.Frame(root, padding=30)


input_frame.pack(fill="both", expand=True)

# =========================
# STYLES
# =========================
style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 11))
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
style.configure("Accent.TButton",
                background=PRIMARY,
                foreground="white",
                padding=8,
                font=("Segoe UI", 10, "bold"))
style.map("Accent.TButton", background=[("active", "#1f5bb5")])

style.configure("TEntry",
                fieldbackground="white",
                bordercolor="#cccccc",
                padding=5)

style.configure("White.TFrame", background="white")
style.configure("TNotebook", background="white")
style.configure("TNotebook.Tab", background="white")

# =========================
# FUNKTION: WECHSELN
# =========================

def nochmal():
        #zufälliges Smiles auswählen
    molekül = random.choice(moleküle)

    name = molekül["name"]
    app_state["smiles"] = molekül["smiles"]

    # Seite wechseln
    antwort_frame.pack_forget()
    quizz_frame.pack(fill="both", expand=True)

    answer_entry.bind("<KeyRelease>", on_keyrelease)
    answer_entry.bind("<Down>", navigate_listbox)
    answer_entry.bind("<Up>", navigate_listbox)
    answer_entry.bind("<Return>", navigate_listbox)

    eingabe.set("")  # Eingabefeld wird geleert
    answer_var.set("")

    quizz_title_label.config(text="Identifizieren Sie das Molekül!")

    create_tabs(app_state["smiles"], notebook_widget=quizz_notebook, show_title=False, verbose=False, show_integrals=False)





# Zurück zum Start

def zurück_start():

    # Seite wechseln
    result_frame.pack_forget()
    quizz_frame.pack_forget()
    input_frame.pack(fill="both", expand=True)

    eingabe.set("")  # Eingabefeld wird geleert
    answer_var.set("")
    eingabe.set("")
    main_name_var.set("")
    app_state["smiles"]=None
    app_state["bild"] = False

def zurück_start2():

    # Seite wechseln
    antwort_frame.pack_forget()
    input_frame.pack(fill="both", expand=True)

    eingabe.set("")  # Eingabefeld wird geleert
    answer_var.set("")
    eingabe.set("")
    main_name_var.set("")
    app_state["smiles"]=None
    app_state["bild"] = None


def quizz_starten():

    #zufälliges Smiles auswählen
    molekül = random.choice(moleküle)

    name = molekül["name"]
    app_state["smiles"] = molekül["smiles"]
    app_state["bild"]=False

    # Seite wechseln
    input_frame.pack_forget()
    quizz_frame.pack(fill="both", expand=True)

    answer_entry.bind("<KeyRelease>", on_keyrelease)
    answer_entry.bind("<Down>", navigate_listbox)
    answer_entry.bind("<Up>", navigate_listbox)
    answer_entry.bind("<Return>", navigate_listbox)

    quizz_title_label.config(text="Identifizieren Sie das Molekül!")


    create_tabs(app_state["smiles"], notebook_widget=quizz_notebook, show_title=False, show_integrals=False, verbose=False)

    
def smiles_to_image(smiles, size=(200, 200)):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    img = Draw.MolToImage(mol, size=size)
    return ImageTk.PhotoImage(img)

def update_main_suggestions(event=None):
    typed = main_name_var.get().strip().lower()

    if not typed:
        main_listbox.grid_remove()
        login_btn.config(state="normal" if eingabe.get().strip() else "disabled")
        return

    matches = [name for name in namen_liste if typed in name.lower()]
    matches.sort(key=lambda x: (x.lower() != typed, x))

    main_listbox.delete(0, tk.END)

    if matches:
        for name in matches:
            main_listbox.insert(tk.END, name)
        main_listbox.grid()
    else:
        main_listbox.grid_remove()

    # Aktiv nur bei exakter Übereinstimmung
    login_btn.config(state="normal" if typed in [n.lower() for n in namen_liste] else "disabled")


def fill_main_from_listbox(event=None):
    if main_listbox.curselection():
        value = main_listbox.get(main_listbox.curselection()[0])
        main_name_var.set(value)

        main_listbox.selection_clear(0, tk.END)
        main_listbox.grid_remove()

        eingabe.set("")  # SMILES leeren
        main_name_entry.icursor(tk.END)
        login_btn.config(state="normal")


#---Navigation

def navigate_main_listbox(event):
    if event.keysym == "Return":
        if main_listbox.winfo_ismapped() and main_listbox.curselection():
            fill_main_from_listbox()
        else:
            login_btn.invoke()
        return "break"

    if main_listbox.winfo_ismapped() and main_listbox.size() > 0:
        current = main_listbox.curselection()

        if event.keysym == "Down":
            index = current[0] + 1 if current else 0
            if index >= main_listbox.size():
                index = 0

        elif event.keysym == "Up":
            index = current[0] - 1 if current else main_listbox.size() - 1
            if index < 0:
                index = main_listbox.size() - 1

        main_listbox.select_clear(0, tk.END)
        main_listbox.select_set(index)
        main_listbox.activate(index)
        main_listbox.see(index)

        return "break"



def übernehmen():
    smiles_input = eingabe.get().strip()
    name_input = main_name_var.get().strip().lower()
    app_state["bild"]=True

    if name_input in name_to_smiles:
        app_state["smiles"] = name_to_smiles[name_input]

    elif smiles_input:
        app_state["smiles"] = smiles_input

    else:
        tk.messagebox.showwarning("Fehler", "Bitte SMILES oder gültigen Namen eingeben!")
        return

    input_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)

    result_title_label.config(text=app_state["smiles"])

    create_tabs(app_state["smiles"], notebook_widget=result_notebook, show_title=True, verbose=False, show_integrals=True)





# =========================
# INPUT SEITE
# =========================
input_frame.columnconfigure(0, weight=1)

title = ttk.Label(input_frame, text="Spektren Simulation", style="Title.TLabel")
title.grid(row=0, column=0, pady=(0, 20))

Input_Label = ttk.Label(input_frame, text="SMILES des Moleküls eingeben!")
Input_Label.grid(row=1, column=0)

entry = ttk.Entry(input_frame, textvariable=eingabe)
entry.grid(row=2, column=0, pady=5, sticky="ew")

# -----------------------------
# NAME EINGABE (wie Quiz)
# -----------------------------
Input_Label2 = ttk.Label(input_frame, text="Oder Namen auswählen!")
Input_Label2.grid(row=3, column=0)

main_name_frame = ttk.Frame(input_frame)
main_name_frame.grid(row=4, column=0, pady=5, sticky="ew")
main_name_frame.columnconfigure(0, weight=1)

main_name_entry = ttk.Entry(main_name_frame, textvariable=main_name_var)
main_name_entry.grid(row=0, column=0, sticky="ew")

main_listbox = tk.Listbox(main_name_frame, height=5)
main_listbox.grid(row=1, column=0, sticky="ew")
main_listbox.grid_remove()

main_name_entry.bind("<KeyRelease>", lambda e: None if e.keysym in ("Up","Down","Return") else update_main_suggestions())
main_name_entry.bind("<Down>", navigate_main_listbox)
main_name_entry.bind("<Up>", navigate_main_listbox)
main_name_entry.bind("<Return>", navigate_main_listbox)

main_listbox.bind("<<ListboxSelect>>", fill_main_from_listbox)

#------------------------------------

login_btn = ttk.Button(input_frame, text="Okay", style="Accent.TButton", command=übernehmen)
login_btn.grid(row=5, column=0, pady=20, sticky="ew")

text_label = ttk.Label(input_frame, text="Teste dein Wissen!", style="TLabel")
text_label.grid(row=6, column=0, pady=20)

quizz_btn = ttk.Button(input_frame, text="Quiz", style="Accent.TButton", command=quizz_starten)
quizz_btn.grid(row=7, column=0, pady=20, sticky="ew")

input_frame.grid_rowconfigure(6, weight=1)

# exit button
exit_button = ttk.Button(input_frame, text='Programm beenden', style="Accent.TButton", command=lambda: root.quit())
exit_button.grid(row=8, column=0, pady=20, sticky="ew")


# =========================
# RESULT SEITE
# =========================

# Layout für result_frame
result_frame.columnconfigure(0, weight=1)
result_frame.columnconfigure(1, weight=0)

# Titel (links)
result_title_label = ttk.Label(result_frame, text="", style="Title.TLabel")
result_title_label.grid(row=0, column=0, sticky="w", pady=10)

# Button (rechts)
back_button = ttk.Button(result_frame, text="Zurück", style="Accent.TButton", command=zurück_start)
back_button.grid(row=0, column=1, sticky="e", pady=10)

result_notebook = ttk.Notebook(result_frame)
result_notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")
result_frame.rowconfigure(1, weight=1)



# =========================
# TABS ERSTELLEN
# =========================
def create_tabs(smiles, notebook_widget, show_title=True, show_integrals: bool = True, verbose: bool = True):
    # Alte Tabs löschen
    for tab in notebook_widget.winfo_children():
        tab.destroy()

    # 13C NMR Tab
    tab1 = ttk.Frame(notebook_widget)
    notebook_widget.add(tab1, text="13C NMR")
    fig1 = generator.simulate_13c_nmr(smiles, seed=42, plot=False, show_title=show_title,easymode=False)
    #print("13C:", type(fig1))
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True)

    # 1H NMR Tab 
    from nmr_scroll_tab import add_1h_nmr_tab
    nmr_data = add_1h_nmr_tab(notebook_widget, smiles,
                           show_integrals=show_integrals, show_title=show_title)
    
    #Altes IR:
       
    #tab2 = ttk.Frame(notebook_widget)
    #notebook_widget.add(tab2, text="1H NMR")
    #fig2 = hnmr.simulate_1h_nmr(smiles, seed=42, plot=True, verbose=verbose, show_integrals=show_integrals, show_title = show_title)
    #print("HNMR:", type(fig2))
    #canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
    #canvas2.draw()
    #canvas2.get_tk_widget().pack(fill="both", expand=True)"""

    # IR Tab
    tab3 = ttk.Frame(notebook_widget)
    notebook_widget.add(tab3, text="IR")
    fig3 = generator2.simulate_ir(smiles, seed=42, plot=False, show_title=show_title)
    #print("IR:", type(fig3))
    canvas3 = FigureCanvasTkAgg(fig3, master=tab3)  
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill="both", expand=True)

    # MS Tab (Platzhalter)
    tab4 = ttk.Frame(notebook_widget)
    notebook_widget.add(tab4, text="MS")

    #EA Tab
    tab5 = ttk.Frame(notebook_widget)
    notebook_widget.add(tab5, text="EA")

    tab5.columnconfigure(0, weight=1)

    # Titel
    title = ttk.Label(tab5, text="Elementaranalyse", style="Title.TLabel")
    title.grid(row=0, column=0, pady=(20, 10))

    # Frame für die Liste
    list_frame = ttk.Frame(tab5)
    list_frame.grid(row=1, column=0, sticky="n")

    # Daten berechnen
    result = generator5.elementaranalyse(smiles)

    if result:
        for i, (el, perc) in enumerate(sorted(result.items())):
            
            # Element (groß + fett)
            el_label = ttk.Label(
                list_frame,
                text=el,
                font=("Segoe UI", 18, "bold")
            )
            el_label.grid(row=i, column=0, padx=20, pady=10, sticky="e")

            # Prozentwert (groß)
            perc_label = ttk.Label(
                list_frame,
                text=f"{perc:.2f} %",
                font=("Segoe UI", 18)
            )
            perc_label.grid(row=i, column=1, padx=20, pady=10, sticky="w")
    
    if app_state["bild"]:
        tab6 = ttk.Frame(notebook_widget, style="White.TFrame")
        notebook_widget.add(tab6, text="Struktur")
        img = smiles_to_image(smiles)
        label = tk.Label(tab6, image=img, bg="white")
        label.image = img  # wichtig, sonst wird es gelöscht
        label.pack(fill="both", expand=True)



# =========================
# Quiz SEITE
# =========================

canvas = tk.Canvas(quizz_frame, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(quizz_frame, orient="vertical", command=canvas.yview)

scrollable_frame = ttk.Frame(canvas)

# EINMALIG window erstellen
window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

# Resize korrekt binden
def resize_quiz(event):
    canvas.itemconfig(window_id, width=event.width)

canvas.bind("<Configure>", resize_quiz)

# Scrollregion update
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

quizz_frame.rowconfigure(0, weight=1)
quizz_frame.columnconfigure(0, weight=1)

scrollable_frame.columnconfigure(0, weight=1)

scrollable_frame.rowconfigure(0, weight=0)  # Titel
scrollable_frame.rowconfigure(1, weight=1)
scrollable_frame.rowconfigure(2, weight=0)


def _on_mousewheel_quizz(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind("<Enter>", lambda e: canvas.bind("<MouseWheel>", _on_mousewheel_quizz))
canvas.bind("<Leave>", lambda e: canvas.unbind("<MouseWheel>"))



# Titel (links)
quizz_title_label = ttk.Label(scrollable_frame, text="", style="Title.TLabel")
quizz_title_label.grid(row=0, column=0, sticky="w", pady=10)

# Button (rechts)
back_button = ttk.Button(scrollable_frame, text="Zurück", style="Accent.TButton", command=zurück_start)
back_button.grid(row=0, column=1, sticky="e", pady=10)

quizz_notebook = ttk.Notebook(scrollable_frame)
quizz_notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")
result_frame.rowconfigure(1, weight=1)


namen_liste = [m["name"] for m in moleküle]

name_to_smiles = {m["name"].lower(): m["smiles"] for m in moleküle}
smiles_to_name = {m["smiles"].lower(): m["name"] for m in moleküle}

#-----------------------------
# Antwort Feld
# ----------------------



antwort_frame.rowconfigure(0, weight=1)
antwort_frame.columnconfigure(0, weight=1)

antwort_canvas = tk.Canvas(antwort_frame, bg="white", highlightthickness=0)
antwort_scrollbar = ttk.Scrollbar(antwort_frame, orient="vertical", command=antwort_canvas.yview)

antwort_scrollable_frame = ttk.Frame(antwort_canvas)

antwort_scrollable_frame.columnconfigure(0, weight=1)
antwort_scrollable_frame.columnconfigure(1, weight=1)

def resize_antwort_frame(event):
    antwort_canvas.itemconfig(antwort_window, width=event.width)

antwort_canvas.bind("<Configure>", resize_antwort_frame)

antwort_scrollable_frame.bind(
    "<Configure>",
    lambda e: antwort_canvas.configure(scrollregion=antwort_canvas.bbox("all"))
)

antwort_window = antwort_canvas.create_window((0, 0), window=antwort_scrollable_frame, anchor="nw")
antwort_canvas.configure(yscrollcommand=antwort_scrollbar.set)

antwort_canvas.grid(row=0, column=0, sticky="nsew")
antwort_scrollbar.place(relx=0.999, rely=0, relheight=1)


def _on_mousewheel_antwort(event):
    antwort_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

antwort_canvas.bind("<Enter>", lambda e: antwort_canvas.bind_all("<MouseWheel>", _on_mousewheel_antwort))
antwort_canvas.bind("<Leave>", lambda e: antwort_canvas.unbind_all("<MouseWheel>"))


#------------------
# Antwort abgegeben
#------------------

def fill_from_listbox(event=None):
    if suggestion_listbox.curselection():
        value = suggestion_listbox.get(suggestion_listbox.curselection()[0])
        answer_var.set(value)
        
        # 🔥 WICHTIG: Auswahl löschen!
        suggestion_listbox.selection_clear(0, tk.END)
        
        suggestion_listbox.grid_remove()
        submit_btn.config(state="normal")
        answer_entry.icursor(tk.END)

def abgeben():
    parent = antwort_scrollable_frame

    # 🔥 Schutz: nur im Quiz erlauben
    if not quizz_frame.winfo_ismapped():
        return

    # alten Inhalt löschen
    for widget in antwort_scrollable_frame.winfo_children():
        widget.destroy()

    user_input = answer_var.get().strip().lower()
    user_smiles = name_to_smiles.get(user_input)

    correct = user_smiles is not None and user_smiles.lower() == app_state["smiles"].lower()

    richtiger_name = smiles_to_name.get(app_state["smiles"].lower(), "Unbekannt")
    user_name = user_input.title() if user_smiles else "Unbekannt"

    # Seite wechseln
    quizz_frame.pack_forget()
    antwort_frame.pack(fill="both", expand=True, pady=20)

    # Grid sauber zentrieren
    parent.columnconfigure(0, weight=1)
    parent.columnconfigure(1, weight=1)

    # Titel
    ttk.Label(
        parent,
        text="Ergebnis",
        font=("Arial", 24, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=20)

    if correct:
        ttk.Label(
            parent,
            text="✅ Richtig!",
            font=("Arial", 22, "bold"),
            foreground="green"
        ).grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(
            parent,
            text=richtiger_name,
            font=("Arial", 20)
        ).grid(row=2, column=0, columnspan=2, pady=10)

        img = smiles_to_image(app_state["smiles"], size=(320, 320))
        if img:
            lbl = tk.Label(parent, image=img)
            lbl.image = img
            lbl.grid(row=3, column=0, columnspan=2, pady=20)

    else:
        ttk.Label(
            parent,
            text="❌ Falsch!",
            font=("Arial", 22, "bold"),
            foreground="red"
        ).grid(row=1, column=0, columnspan=2, pady=10)

        # LINKS (richtig)
        left_frame = ttk.Frame(parent)
        left_frame.grid(row=2, column=0, padx=40, sticky="n")

        ttk.Label(
            left_frame,
            text=f"Richtig: {richtiger_name}",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=10)

        correct_img = smiles_to_image(app_state["smiles"], size=(320, 320))
        if correct_img:
            lbl_c = tk.Label(left_frame, image=correct_img)
            lbl_c.image = correct_img
            lbl_c.grid(row=1, column=0, pady=10)

        # RECHTS (falsch)
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=2, column=1, padx=40, sticky="n")

        ttk.Label(
            right_frame,
            text=f"Dein Molekül: {user_name}",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=10)

        user_img = smiles_to_image(user_smiles, size=(320, 320))
        if user_img:
            lbl_u = tk.Label(right_frame, image=user_img)
            lbl_u.image = user_img
            lbl_u.grid(row=1, column=0, pady=10)

    # Buttons unten (immer mittig)
    button_frame = ttk.Frame(parent)
    button_frame.grid(row=4, column=0, columnspan=2, pady=30)

    ttk.Button(button_frame, text="Startseite", style="Accent.TButton",
               command=zurück_start2).pack(side="left", padx=20)

    ttk.Button(button_frame, text="Noch ein Quiz", style="Accent.TButton",
               command=nochmal).pack(side="right", padx=20)
    
    antwort_canvas.yview_moveto(0)

def go_to_input(result_frame):
    result_frame.pack_forget()  # Ergebnis ausblenden
    input_frame.pack(fill="both", expand=True)  # zurück zum Input-Frame


# -----------------------------
# Quiz-Antwortfeld mit verbessertem Autocomplete
# -----------------------------
answer_var = tk.StringVar()
answer_frame = ttk.Frame(scrollable_frame)
answer_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
answer_frame.columnconfigure(0, weight=1)

answer_entry = ttk.Entry(answer_frame, textvariable=answer_var)
answer_entry.grid(row=0, column=0, sticky="ew")

# Listbox für Vorschläge
suggestion_listbox = tk.Listbox(answer_frame, height=5)
suggestion_listbox.grid(row=1, column=0, sticky="ew")
suggestion_listbox.grid_remove()  # zuerst verstecken

submit_btn = ttk.Button(answer_frame, text="Abgeben", style="Accent.TButton", state="disabled", command=abgeben)
submit_btn.grid(row=0, column=1, padx=10)


# -----------------------------
# Funktionen
# -----------------------------
def update_suggestions(event=None):
    typed = answer_var.get().strip().lower()
    
    # Wenn Feld leer -> Vorschläge verstecken und Button deaktivieren
    if not typed:
        suggestion_listbox.grid_remove()
        submit_btn.config(state="disabled")
        return

    # Filtert Namen, die das getippte enthalten
    matches = [name for name in namen_liste if typed in name.lower()]

    # Exakte Übereinstimmung nach oben
    matches.sort(key=lambda x: (x.lower() != typed, x))

    # Listbox aktualisieren
    suggestion_listbox.delete(0, tk.END)
    if matches:
        for name in matches:
            suggestion_listbox.insert(tk.END, name)
        suggestion_listbox.grid()
    else:
        suggestion_listbox.grid_remove()

    # Button nur bei exakter Übereinstimmung aktivieren
    submit_btn.config(state="normal" if typed in [n.lower() for n in namen_liste] else "disabled")


def on_keyrelease(event=None):
    # Pfeiltasten und Enter sollen die Vorschläge nicht neu filtern
    if event.keysym in ("Up", "Down", "Return"):
        return
    update_suggestions()

def navigate_listbox(event):

    # 🔥 ENTER IMMER ERLAUBEN
    if event.keysym == "Return":
        if suggestion_listbox.winfo_ismapped() and suggestion_listbox.curselection():
            fill_from_listbox()
        else:
            submit_btn.invoke()
        return "break"

    # Nur für Pfeiltasten Listbox prüfen
    if suggestion_listbox.winfo_ismapped() and suggestion_listbox.size() > 0:
        current = suggestion_listbox.curselection()

        if event.keysym == "Down":
            index = current[0] + 1 if current else 0
            if index >= suggestion_listbox.size():
                index = 0

        elif event.keysym == "Up":
            index = current[0] - 1 if current else suggestion_listbox.size() - 1
            if index < 0:
                index = suggestion_listbox.size() - 1

        suggestion_listbox.select_clear(0, tk.END)
        suggestion_listbox.select_set(index)
        suggestion_listbox.activate(index)
        suggestion_listbox.see(index)

        return "break"

# -----------------------------
# Events binden
# -----------------------------
answer_entry.bind("<KeyRelease>", on_keyrelease)
answer_entry.bind("<Down>", navigate_listbox)
answer_entry.bind("<Up>", navigate_listbox)
answer_entry.bind("<Return>", navigate_listbox)
suggestion_listbox.bind("<<ListboxSelect>>", fill_from_listbox)





# =========================
root.mainloop()