class SearchForm(Form):

    prenom = TextField('Preacute;nom')
    nom = TextField('Nom')
    ville = TextField('Ville')
    entreprise = TextField('Entreprise')

    def setprenom(self, prenom):

        self.prenom.choices = prenom
        #blank choice
        self.prenom.choices.insert(0, ('', ''))

    def setnom(self, pays_dict):

        self.nom.choices = nom
        #blank choice
        self.nom.choices.insert(0, ('', ''))

    def ville(self, ville):

        self.ville.choices = ville
        #blank choice
        self.ville.choices.insert(0, ('', ''))

    def entreprise(self, entreprise):

        self.entreprise.choices = entreprise
        #blank choice
        self.entreprise.choices.insert(0, ('', ''))