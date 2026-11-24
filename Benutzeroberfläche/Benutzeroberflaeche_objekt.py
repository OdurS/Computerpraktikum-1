import tkinter as tk


class GUI:

    def __init__(
        self,
        Name="Matheprojekt",
        Vollbild=True,
        Hintergrund="#202B3C"
    ):

        self.Root = tk.Tk()
        self.Root.title(Name)
        self.Root.configure(bg=Hintergrund)

        self.Hintergrund = Hintergrund

        if Vollbild:
            self.Root.attributes("-fullscreen", True)

        self.Root.bind("<Escape>", lambda event: self.beenden())

        self.Seiten = {}
        self.AktuelleSeite = None
        self.Verlauf = []
        self.Startseite = None

    def add_Seite(self, Name, Farbe=None):

     if Name in self.Seiten:
        raise ValueError("Seite existiert bereits.")

     NeueSeite = Seite(self, Name, Farbe)

     self.Seiten[Name] = NeueSeite

     if self.Startseite is None:
            self.Startseite = NeueSeite

     return NeueSeite

    def zeige(self, Seite):

        if isinstance(Seite, str):
            Seite = self.Seiten[Seite]

        if Seite not in self.Seiten.values():
            raise ValueError("Seite gehört nicht zu diesem Fenster.")

        if self.AktuelleSeite is not Seite:

            if self.AktuelleSeite is not None:
                self.Verlauf.append(self.AktuelleSeite)

            self.AktuelleSeite = Seite

        Seite.Frame.tkraise()

    def zurueck(self):

        if self.Verlauf:

            Seite = self.Verlauf.pop()
            self.AktuelleSeite = Seite
            Seite.Frame.tkraise()

        else:
            self.zur_Startseite()

    def zur_Startseite(self):

        if self.Startseite is None:
            return

        self.Verlauf.clear()
        self.AktuelleSeite = self.Startseite
        self.Startseite.Frame.tkraise()

    def start(self):

        if self.Startseite is not None:
            self.zeige(self.Startseite)

        self.Root.mainloop()

    def beenden(self):
        self.Root.destroy()


class Seite:

    def __init__(self, Fenster, Name, Farbe=None):

        self.Fenster = Fenster
        self.Name = Name

        if Farbe is None:
            Farbe = Fenster.Hintergrund

        self.Farbe = Farbe

        self.Frame = tk.Frame(
            Fenster.Root,
            bg=Farbe
        )

        self.Frame.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.Buttons = {}
        self.Ausgabefelder = {}
        self.Textfelder = {}
        self.Eingabefelder = {}

    def add_Button(
        self,
        Name,
        Farbe,
        Befehl,
        Position,
        Groesse=(200, 60),
        Textfarbe="white",
        Schriftgroesse=16
    ):

        Button = tk.Button(
            self.Frame,
            text=Name,
            bg=Farbe,
            fg=Textfarbe,
            command=Befehl,
            font=("Arial", Schriftgroesse, "bold"),
            relief="flat",
            cursor="hand2"
        )

        Button.place(
            x=Position[0],
            y=Position[1],
            width=Groesse[0],
            height=Groesse[1]
        )

        Objekt = GUI_Element(Button, Position, Groesse)

        self.Buttons[Name] = Objekt

        return Objekt

    def add_Label(
        self,
        Name,
        Text,
        Position,
        Groesse=(300, 60),
        Farbe=None,
        Textfarbe="white",
        Schriftgroesse=16
    ):

        if Farbe is None:
            Farbe = self.Farbe

        Label = tk.Label(
            self.Frame,
            text=Text,
            bg=Farbe,
            fg=Textfarbe,
            font=("Arial", Schriftgroesse),
            justify="left"
        )

        Label.place(
            x=Position[0],
            y=Position[1],
            width=Groesse[0],
            height=Groesse[1]
        )

        Objekt = GUI_Element(Label, Position, Groesse)

        self.Ausgabefelder[Name] = Objekt

        return Objekt

    def add_Textfeld(
        self,
        Name,
        Text,
        Position,
        Groesse=(400, 200),
        Farbe="white",
        Textfarbe="black",
        Schriftgroesse=14
    ):

        Textfeld = tk.Text(
            self.Frame,
            bg=Farbe,
            fg=Textfarbe,
            font=("Arial", Schriftgroesse),
            wrap="word"
        )

        Textfeld.insert("1.0", Text)

        Textfeld.place(
            x=Position[0],
            y=Position[1],
            width=Groesse[0],
            height=Groesse[1]
        )

        Objekt = GUI_Element(Textfeld, Position, Groesse)

        self.Textfelder[Name] = Objekt

        return Objekt

    def add_Eingabefeld(
        self,
        Name,
        Position,
        Groesse=(250, 40),
        Farbe="white",
        Textfarbe="black",
        Schriftgroesse=14
    ):

        Eingabe = tk.Entry(
            self.Frame,
            bg=Farbe,
            fg=Textfarbe,
            font=("Arial", Schriftgroesse)
        )

        Eingabe.place(
            x=Position[0],
            y=Position[1],
            width=Groesse[0],
            height=Groesse[1]
        )

        Objekt = GUI_Element(Eingabe, Position, Groesse)

        self.Eingabefelder[Name] = Objekt

        return Objekt

    def add_BackButton(
        self,
        Name="Zurück",
        Farbe="#E67E22",
        Position=(30, 30),
        Groesse=(160, 55)
    ):

        return self.add_Button(
            Name,
            Farbe,
            self.Fenster.zurueck,
            Position,
            Groesse
        )

    def add_HomeButton(
        self,
        Name="Startseite",
        Farbe="#16A085",
        Position=(210, 30),
        Groesse=(180, 55)
    ):

        return self.add_Button(
            Name,
            Farbe,
            self.Fenster.zur_Startseite,
            Position,
            Groesse
        )


class GUI_Element:

    def __init__(self, Widget, Position, Groesse):

        self.Widget = Widget
        self.Position = Position
        self.Groesse = Groesse

    def set_Position(self, Position):

        self.Position = Position

        self.Widget.place(
            x=Position[0],
            y=Position[1]
        )

    def set_Groesse(self, Groesse):

        self.Groesse = Groesse

        self.Widget.place(
            width=Groesse[0],
            height=Groesse[1]
        )

    def set_Farbe(self, Farbe):

        self.Widget.configure(bg=Farbe)

    def set_Text(self, Text):

        if isinstance(self.Widget, tk.Text):
            self.Widget.delete("1.0", tk.END)
            self.Widget.insert("1.0", Text)

        elif isinstance(self.Widget, tk.Entry):
            self.Widget.delete(0, tk.END)
            self.Widget.insert(0, Text)

        else:
            self.Widget.configure(text=Text)

    def get_Text(self):

        if isinstance(self.Widget, tk.Text):
            return self.Widget.get("1.0", tk.END).rstrip()

        elif isinstance(self.Widget, tk.Entry):
            return self.Widget.get()

        else:
            return self.Widget.cget("text")

    def hide(self):
        self.Widget.place_forget()

    def show(self):

        self.Widget.place(
            x=self.Position[0],
            y=self.Position[1],
            width=self.Groesse[0],
            height=self.Groesse[1]
        )


#Beispiel(zum sehen wie es angewendet wird):
        """Seite = Seite(self, Name, Farbe)
        
            NeueSeite = Seite(self, Name, Farbe)
            self.Seiten[Name] = NeueSeite

            if self.Startseite is None:
            self.Startseite = NeueSeite

            return NeueSeite        
        """