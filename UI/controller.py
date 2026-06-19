import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._model.creaGrafo(self._view._ddAnno.value)
        n,m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"grafo correttamnete creato, è formato da {n} nodi e {m} archi"))
        self._view.update_page()


    def handleDettagli(self, e):
        if self._choiceTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("selezionare un team dal menu"))
            self._view.update_page()
            return

        viciniTuple=self._model.getVicini(self._choiceTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"il nodo {self._choiceTeam} ha {len(viciniTuple)} vicini"))
        self._view._txt_result.controls.append(ft.Text(f"una lista ordinata di vicini "))
        for v in viciniTuple:
            self._view._txt_result.controls.append(ft.Text(
                f"il nodo {v[0]} - peso: {v[1]}"
            ))
        self._view.update_page()



    def handlePercorso(self, e):
        pass


    def _fillDDYears(self):
        years=self._model.getAllYear()

        #yearsDD=[]
        #for year in years:
        #    yearsDD.append(ft.dropdown.Option(year))

        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddAnno.options=yearsDD
        self._view.update_page()

    def handleYearSelection(self,e):

        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("selezionare un anno dal drodown"))
            return

        self._view._txtOutSquadre.controls.clear()

        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.append(ft.Text(f"per il {self._view._ddAnno.value} sono iscritte {len(teams)}squadre"))

        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(t))
            self._view._ddSquadra.options.append(ft.dropdown.Option(
                data = t, text = t.name, on_click = self.readDDTeams))

        self._view.update_page()

    def readDDTeams(self,e):
        if e.control.data is None:
            self._choiceTeam = None
        else:
            self._choiceTeam = e.control.data
        print (f" selezioanto il team {self._choiceTeam}")




