import statistics
import pygame
import sys
import math
import time
import copy


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """

    display = None  #Reprezinta ecranul jocului
    scalare = 90    #Scalarea si tranzatia sunt doua valori fixe care ajuta la pozitionarea pieselor
    translatie = 30
    razaPct = 10    #Raza cercului unui nod din graf (a unui loc in care se poate muta)
    razaPiesa = 20  #Raza unei piese de mutat
    piesaAlba_img = None    #Imaginea piesei albe (cainii)
    piesaNeagra_img = None  #Imaginea piesei negre (jaguarul)
    piesaSelectata_img = None   #Imaginea unei piese selectate si a configuratiei castigatoare
    JMIN = None #Reprezinta piesa corespunzatoare jucatorului
    JMAX = None #Reprezinta piese corespunzatoare calculatorului

    def __init__(self, caini=None, jaguar=None):
        """
        Constructorul clasei, primeste ca parametrii pozitiile translatate ale cainilor si a jaguarului,
        folosite pentru a muta piesele pe tabla de joc.
        Daca este prima data cand construim tabla de joc, vom initializa pozitiile nodurilor si ale
        muchiilor, precum si pozitiile pieselor pe tabla initiala, pe care le vom translata.
        """
        self.noduri = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
            (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
            (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
                    (1, 5), (2, 5), (3, 5),
            (0, 6),         (2, 6),         (4, 6)
        ]
        self.muchii = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8), (8, 9), (10, 11), (11, 12), (12, 13),
                       (13, 14),
                       (15, 16), (16, 17), (17, 18), (18, 19), (20, 21), (21, 22), (22, 23), (23, 24), (25, 26),
                       (26, 27), (28, 29), (29, 30),
                       (0, 5), (5, 10), (10, 15), (15, 20), (1, 6), (6, 11), (11, 16), (16, 21), (2, 7), (7, 12),
                       (12, 17), (17, 22),
                       (3, 8), (8, 13), (13, 18), (18, 23), (4, 9), (9, 14), (14, 19), (19, 24), (22, 26), (26, 29),
                       (0, 6), (6, 2), (2, 8), (8, 4), (10, 6), (6, 12), (12, 8), (8, 14), (10, 16), (16, 12), (12, 18),
                       (18, 14),
                       (20, 16), (16, 22), (22, 18), (18, 24), (22, 25), (25, 28), (22, 27), (27, 30)
                       ]
        self.coordonateNoduri = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in self.noduri]
        if caini and jaguar:
            self.pieseAlbe = caini
            self.piesaNeagra = jaguar
        else:
            self.caini = [
                (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                (0, 2), (1, 2),         (3, 2), (4, 2)
            ]
            self.jaguar = (2, 2)
            self.pieseAlbe = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in self.caini]
            self.piesaNeagra = [self.__class__.translatie + self.__class__.scalare * x for x in self.jaguar]

    @classmethod
    def initializeaza(cls, display):
        """
        Functia primeste ca parametru ecranul pe care se desfasoara jocul si incarca imaginile
        pieselor.
        """
        cls.display = display
        diametruPiesa = 2 * cls.razaPiesa
        cls.piesaAlba_img = pygame.image.load('piesa-alba.png')
        cls.piesaAlba_img = pygame.transform.scale(cls.piesaAlba_img, (diametruPiesa, diametruPiesa))
        cls.piesaNeagra_img = pygame.image.load('piesa-neagra.png')
        cls.piesaNeagra_img = pygame.transform.scale(cls.piesaNeagra_img, (diametruPiesa, diametruPiesa))
        cls.piesaSelectata_img = pygame.image.load('piesa-rosie.png')
        cls.piesaSelectata_img = pygame.transform.scale(cls.piesaSelectata_img, (diametruPiesa, diametruPiesa))

    def deseneaza_grid(self, ecran, nodPiesaSelectata=None, final=None):
        """
        Aceasta metoda este folosita pentru a desena tabla de joc si piesele la un moment dat,
        dar este folosita si pentru afisarea selectiei unei piese, folosind parametrul nodPiesaSelectata,
        sau pentru afisarea configuratiei finale, castigatoare.
        """
        culoareEcran = (255, 255, 255)
        culoareLinii = (0, 0, 0)
        ecran.fill(culoareEcran)
        for nod in self.coordonateNoduri:
            pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=self.__class__.razaPct, width=0)
        for muchie in self.muchii:
            p0 = self.coordonateNoduri[muchie[0]]
            p1 = self.coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseAlbe:
            ecran.blit(self.__class__.piesaAlba_img, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        ecran.blit(self.__class__.piesaNeagra_img, (self.piesaNeagra[0] - self.__class__.razaPiesa, self.piesaNeagra[1] - self.__class__.razaPiesa))
        if nodPiesaSelectata:
            ecran.blit(self.__class__.piesaSelectata_img, (nodPiesaSelectata[0] - self.__class__.razaPiesa, nodPiesaSelectata[1] - self.__class__.razaPiesa))
        if final:
            if len(self.pieseAlbe) <= 9:
                ecran.blit(self.__class__.piesaSelectata_img, (self.piesaNeagra[0] - self.__class__.razaPiesa, self.piesaNeagra[1] - self.__class__.razaPiesa))
            else:
                n0 = self.coordonateNoduri.index(self.piesaNeagra)
                for nod in self.pieseAlbe:
                    n1 = self.coordonateNoduri.index(nod)
                    if ((n0, n1) in self.muchii or
                            (n1, n0) in self.muchii):
                        ecran.blit(self.__class__.piesaSelectata_img, (
                        nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        pygame.display.update()

    @classmethod
    def jucator_opus(cls, jucator):
        """
        O functie ce returneaza piesa oponentului
        """
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN


    def final(self):
        """
        O functie care determina castigatorul, in cazul in care acesta exista si returneaza:
        False -> daca nu ne aflam intr-o configuratie castigatoare
        '1' -> daca a castigat jaguarul, capturand 5 caini
        '2' -> daca au castigat cainii, incoltind jaguarul
        """
        if len(self.pieseAlbe) <= 9:
            return '1'
        else:
            for nod in self.coordonateNoduri:
                n0 = self.coordonateNoduri.index(nod)
                n1 = self.coordonateNoduri.index(self.piesaNeagra)
                if ((n0, n1) in self.muchii or
                    (n1, n0) in self.muchii):
                    if nod not in self.pieseAlbe:
                        return False
            return '2'

    def directie(self, nod1, nod2):
        """
        O functie auxiliara care ajuta la deplasarea piesei negre, in cazul in care aceasta poate captura
        o piesa alba.
        Functia returneaza indexul nodului aflat pe aceiasi directie cu piesa care se doreste a fi capturata.
        """
        nod1 = [(x - self.__class__.translatie) // self.__class__.scalare for x in nod1]
        nod2 = [(x - self.__class__.translatie) // self.__class__.scalare for x in nod2]

        if nod1[0] == nod2[0] and nod1[1] - 1 == nod2[1]:   #N
            try:
                nod_nou = [nod2[0] * self.__class__.scalare + self.__class__.translatie,
                           (nod2[1] - 1) * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] + 1 == nod2[0] and nod1[1] - 1 == nod2[1]: #NE
            try:
                nod_nou = [(nod2[0] + 1) * self.__class__.scalare + self.__class__.translatie,
                           (nod2[1] - 1) * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] + 1 == nod2[0] and nod1[1] == nod2[1]:  #E
            try:
                nod_nou = [(nod2[0] + 1) * self.__class__.scalare + self.__class__.translatie,
                           nod2[1] * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] + 1 == nod2[0] and nod1[1] + 1== nod2[1]:  #SE
            try:
                nod_nou = [(nod2[0] + 1) * self.__class__.scalare + self.__class__.translatie,
                           (nod2[1] + 1) * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] == nod2[0] and nod1[1] + 1 == nod2[1]: #S
            try:
                nod_nou = [nod2[0] * self.__class__.scalare + self.__class__.translatie,
                           (nod2[1] + 1) * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] - 1 == nod2[0] and nod1[1] + 1 == nod2[1]: #SV
            try:
                nod_nou = [(nod2[0] - 1) * self.__class__.scalare + self.__class__.translatie,
                           (nod2[1] + 1) * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] - 1 == nod2[0] and nod1[1] == nod2[1]: #V
            try:
                nod_nou = [(nod2[0] - 1) * self.__class__.scalare + self.__class__.translatie,
                           nod2[1] * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False
        elif nod1[0] - 1 == nod2[0] and nod1[1] - 1 == nod2[1]: #NV
            try:
                nod_nou = [(nod2[0] - 1) * self.__class__.scalare + self.__class__.translatie,
                           (nod2[1] - 1) * self.__class__.scalare + self.__class__.translatie]
                return self.coordonateNoduri.index(nod_nou)
            except:
                return False

    def mutari(self, jucator):
        """
        O functie care returneaza lista mutarilor posibile din configuratia actuala, utila pentru realizarea
        mutarii calculatorului.
        """
        l_mutari = []
        if jucator == '1':  # Daca calculatorul joaca cu jaguarul, vom determina pozitiile in care acesta poate sa mute
            n0 = self.coordonateNoduri.index(self.piesaNeagra)
            for nod in self.coordonateNoduri:
                n1 = self.coordonateNoduri.index(nod)
                if ((n0, n1) in self.muchii) or ((n1, n0) in self.muchii):
                    if nod not in self.pieseAlbe:   # Daca nodul pe care vrem sa muta este liber putem realiza mutarea
                        copie_caini = copy.deepcopy(self.pieseAlbe)
                        l_mutari.append(Joc(copie_caini, nod))
                    else:   # In caz contrar, inseamna ca este posibil sa putem captura o piesa alba
                        piesa_dupa_saritura = self.directie(self.piesaNeagra, nod)
                        if (piesa_dupa_saritura is not False) and \
                                (self.coordonateNoduri[piesa_dupa_saritura] not in self.pieseAlbe):
                            # Verificam posibilitatea capturarii piesei albe si realizam schimbarea, daca e posibila
                            copie_caini = copy.deepcopy(self.pieseAlbe)
                            copie_caini.remove(nod)
                            l_mutari.append(Joc(copie_caini, self.coordonateNoduri[piesa_dupa_saritura]))
        else:   # In cazul in care calculatorul joaca cu cainii, vom determina mutarile posibile acestora
            for piesaAlba in self.pieseAlbe:
                n0 = self.coordonateNoduri.index(piesaAlba)
                for nod in self.coordonateNoduri:
                    n1 = self.coordonateNoduri.index(nod)
                    if ((n0, n1) in self.muchii) or ((n1, n0) in self.muchii):
                        if nod != self.piesaNeagra and nod not in self.pieseAlbe:
                            # Verificam daca putem muta piesele albe in noduri goale
                            copie_caini = copy.deepcopy(self.pieseAlbe)
                            copie_caini.remove(piesaAlba)
                            copie_caini.append(nod)
                            l_mutari.append(Joc(copie_caini, self.piesaNeagra))
        return l_mutari

    def estimeaza_scor(self, adancime, estimare='2'):
        """
        O functie care estimeaza scorul pentru o configuratie a tablei de joc, utila pentru
        mutarea calculatorului, realizata cu algoritmii alpha-beta si min-max.
        """
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)  # In cazul in care ne aflam intr-o configuratie finala vom returna o valoare mare
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime) # In cazul in care ne aflam intr-o configuratie finala vom returna o valoare mica
        else:   # In cazul in care nu ne aflam intr-o configuratie finala
            """
            Estimarea 1 (defensiva):
            -> calculatorul joaca cu JAGUARUL: scorul scade cu cat mai multe piese albe sunt in jurul celei negre;
                in acest fel, jaguarul va tinde sa ocupe pozitiile in care nu este inconjurat
            -> calculatorul joaca cu CAINII: scorul scade cu cat mai multe piese albe sunt in pericol de a fi capturate;
                astfel, cainii vor incerca sa ocupe pozitiile in care nu vor fi capturati
            Estimarea 2 (ofensiva):
            -> calculatorul joaca cu JAGUARUL: scorul creste cu cat mai multe piese albe sunt in pericol de a fi
            capturate; astfel, jaguarul va incerca sa ocupe pozitiile in care poate sa captureze piese
            -> calculatorul joaca cu CAINII: scorul creste cu cat mai multe piese albe sunt imprejurul piesei negre;
            in acest mod, cainii vor incerca sa ocupe pozitii in care sa inconjuare jaguarul
            """
            if estimare == '1':
                if self.__class__.JMAX == '1':
                    scor = 0
                    n0 = self.coordonateNoduri.index(self.piesaNeagra)
                    for nod in self.pieseAlbe:
                        n1 = self.coordonateNoduri.index(nod)
                        if ((n0, n1) in self.muchii) or ((n1, n0) in self.muchii):
                            scor -= 1
                    return scor
                else:
                    scor = 0
                    n0 = self.coordonateNoduri.index(self.piesaNeagra)
                    for nod in self.pieseAlbe:
                        n1 = self.coordonateNoduri.index(nod)
                        if ((n0, n1) in self.muchii) or ((n1, n0) in self.muchii):
                            piesa_dupa_saritura = self.directie(self.piesaNeagra, nod)
                            if (piesa_dupa_saritura is not False) and \
                                    (self.coordonateNoduri[piesa_dupa_saritura] not in self.pieseAlbe):
                                scor -= 1
                    return scor
            else:
                if self.__class__.JMAX == '1':
                    scor = 0
                    n0 = self.coordonateNoduri.index(self.piesaNeagra)
                    for nod in self.pieseAlbe:
                        n1 = self.coordonateNoduri.index(nod)
                        if ((n0, n1) in self.muchii) or ((n1, n0) in self.muchii):
                            piesa_dupa_saritura = self.directie(self.piesaNeagra, nod)
                            if (piesa_dupa_saritura is not False) and \
                                    (self.coordonateNoduri[piesa_dupa_saritura] not in self.pieseAlbe):
                                scor += 1
                    return scor
                else:
                    scor = 0
                    n0 = self.coordonateNoduri.index(self.piesaNeagra)
                    for nod in self.pieseAlbe:
                        n1 = self.coordonateNoduri.index(nod)
                        if ((n0, n1) in self.muchii) or ((n1, n0) in self.muchii):
                            scor += 1
                    return scor

    def sirAfisare(self):
        """
        Aceasta functie este folosita pentru a afisa configuratia actuala a tablei de joc in consola.
        """
        sir = ""
        for nod in self.noduri:
            nod_translatat = [self.__class__.translatie + self.__class__.scalare * x for x in nod]
            if nod == (1, 5):
                if nod_translatat in self.pieseAlbe:
                    sir += "  C "
                elif nod_translatat == self.piesaNeagra:
                    sir += "  J "
                else:
                    sir += "  . "
            elif nod == (0, 6) or nod == (2, 6):
                if nod_translatat in self.pieseAlbe:
                    sir += "C   "
                elif nod_translatat == self.piesaNeagra:
                    sir += "J   "
                else:
                    sir += ".   "
            elif nod[0] == 4 or nod == (3, 5):
                if nod_translatat in self.pieseAlbe:
                    sir += "C\n"
                elif nod_translatat == self.piesaNeagra:
                    sir += "J\n"
                else:
                    sir += ".\n"
            else:
                if nod_translatat in self.pieseAlbe:
                    sir += "C "
                elif nod_translatat == self.piesaNeagra:
                    sir += "J "
                else:
                    sir += ". "
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta.
    Are ca proprietate tabla de joc.
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili).
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile
    posibile in urma mutarii unui jucator.
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Joc curent:" + self.j_curent + ")\n"
        return sir


class Buton:
    """
    Clasa buton este folosita pentru a instantia butoanele initiale, folosite pentru a alege cu ce piesa vom juca,
    ce algoritm vom folosi si ce nivel de dificultate vom alege.
    """

    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    """
    O clasa folosita pentru a grupa mai multe butoane, folosita pentru a realiza alegerea butoanelor
    din aceiasi categorie: Piesa, Algoritm, Dificultate.
    """

    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)
            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break
    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)
            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    """
    O functie care afiseaza castigatorul si returneaza True in cazul in care acesta exista.
    Pentru jocul Adugo nu exista remiza.
    """
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == '1':
            print("A castigat jaguarul!")
        else:
            print("Au castigat cainii!")
        return True
    return False


def afisare_finala(timpi, nr_noduri, timp_total, mutari_jucator, mutari_calculator):
    """
    O metoda folosita pentru afisarea valorilor finale: timpii de gandire ai calculatorului,
    numarul de noduri calculate pentru o mutare, precum si timpul final de joc si numarul total de mutari.
    """
    print("Timp minim de gandire al calculatorului: " + str(min(timpi)))
    print("Timp maxim de gandire al calculatorului: " + str(max(timpi)))
    print("Timp mediu de gandire al calculatorului: " + str(sum(timpi) / len(timpi)))
    print("Mediana timpului de gandire al calculatorului: " + str(statistics.median(timpi)))

    print("Numar minim de noduri generate la o mutare: " + str(min(nr_noduri)))
    print("Numar maxim de noduri generate la o mutare: " + str(max(nr_noduri)))
    print("Numar mediu de noduri generate la o mutare: " + str(sum(nr_noduri) / len(nr_noduri)))
    print("Mediana numarului de noduri generate la o mutare: " + str(statistics.median(nr_noduri)))

    print("Timp final de joc: " + str(timp_total))
    print("Numar total de mutari jucator: " + str(mutari_jucator))
    print("Numar total de mutari calculator: " + str(mutari_calculator))


def distEuclid(p0, p1):
    """
    O functie care ne ajuta sa calculam dista dintre doua puncte, utila pentru validarea unei pozitii.
    """
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def deseneaza_alegeri(display, tabla_curenta):
    """
    O functie folosita pentru a desena meniul jocului.
    """
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="1"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="2")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Jaguar", valoare="1"),
            Buton(display=display, w=80, h=30, text="Caini", valoare="2")
        ],
        indiceSelectat=0)
    btn_dif = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Incepator", valoare="1"),
            Buton(display=display, w=80, h=30, text="Mediu", valoare="2"),
            Buton(display=display, w=80, h=30, text="Avansat", valoare="3")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=240, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dif.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0, 0, 0))
                                tabla_curenta.deseneaza_grid(display)
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_dif.getValoare()
        pygame.display.update()


def main():
    """
    Functia main ruleaza jocul.
    """
    # Initializare pygame si setari ecran
    pygame.init()
    pygame.display.set_caption('Feta Almar-Eran - Jocul Adugo')
    ecran = pygame.display.set_mode(size=(800, 600))

    # initializare tabla de joc
    tabla_curenta = Joc()
    Joc.initializeaza(ecran)

    # Afisare meniului de joc
    Joc.JMIN, tip_algoritm, dificultate = deseneaza_alegeri(ecran, tabla_curenta)
    if tip_algoritm == '1':
        print("Ati ales algoritmul minmax")
    else:
        print("Ati ales algoritmul alpha-beta")
    if Joc.JMIN == '1':
        print("Jucati cu jaguarul")
    else:
        print("Jucati cu cainii")
    Joc.JMAX = '2' if Joc.JMIN == '1' else '1'
    if dificultate == '1':
        print("Dificultate: Incepator")
        ADANCIME_MAX = 2
    elif dificultate == '2':
        print("Dificultate: Mediu")
        ADANCIME_MAX = 3
    else:
        print("Dificultate: Avansat")
        ADANCIME_MAX = 4
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala -> incepe jaguarul
    stare_curenta = Stare(tabla_curenta, '1', ADANCIME_MAX)
    tabla_curenta.deseneaza_grid(ecran)
    de_mutat = False
    print("Muta " + ("negru" if stare_curenta.j_curent == '1' else "alb"))
    t_inainte = int(round(time.time() * 1000))
    t_inceput = int(round(time.time() * 1000))
    timpi = []
    nr_noduri = []
    timp_total = 0
    mutari_jucator = 0
    mutari_calculator = 0
    while True:
        if stare_curenta.j_curent == Joc.JMIN:  # Mutarea jucatorului
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Inchidem fereasta si afisam datele finale
                    afisare_finala(timpi, nr_noduri, timp_total, mutari_jucator, mutari_calculator)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click
                    pos = pygame.mouse.get_pos()  # coordonatele clickului
                    for nod in stare_curenta.tabla_joc.coordonateNoduri:
                        if distEuclid(pos, nod) <= Joc.razaPct: # determinam nodul pe care s-a facut click
                            if nod in stare_curenta.tabla_joc.pieseAlbe or nod == stare_curenta.tabla_joc.piesaNeagra:
                                if (Joc.JMIN == '1' and nod == stare_curenta.tabla_joc.piesaNeagra) or \
                                        (Joc.JMIN == '2' and nod in stare_curenta.tabla_joc.pieseAlbe):
                                    if de_mutat == nod: # Deselectam piesa daca era deja selectata
                                        de_mutat = False
                                        stare_curenta.tabla_joc.deseneaza_grid(ecran)
                                    else:   # Selectam piesa pentru a o muta
                                        de_mutat = nod
                                        stare_curenta.tabla_joc.deseneaza_grid(ecran, de_mutat)
                                # Verificam daca putem realiza o captura a jaguarului
                                elif de_mutat and (Joc.JMIN == '1' and nod in stare_curenta.tabla_joc.pieseAlbe):
                                    piesa_dupa_saritura = stare_curenta.tabla_joc.directie(de_mutat, nod)
                                    if (piesa_dupa_saritura is not False) and \
                                            (stare_curenta.tabla_joc.coordonateNoduri[piesa_dupa_saritura] not in
                                             stare_curenta.tabla_joc.pieseAlbe):
                                        stare_curenta.tabla_joc.pieseAlbe.remove(nod)
                                        stare_curenta.tabla_joc.piesaNeagra = stare_curenta.tabla_joc.coordonateNoduri[
                                            piesa_dupa_saritura]
                                        stare_curenta.tabla_joc.deseneaza_grid(ecran)
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        mutari_jucator += 1
                                        de_mutat = False
                                        t_dupa = int(round(time.time() * 1000))
                                        print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                                        print("Numarul de noduri generate la aceasta mutare: " + str(len(stare_curenta.mutari_posibile)))
                                        nr_noduri.append(len(stare_curenta.mutari_posibile))
                                        print("Muta " + ("alb" if stare_curenta.j_curent == '1' else "negru"))
                                        if afis_daca_final(stare_curenta):
                                            stare_curenta.tabla_joc.deseneaza_grid(ecran, None, True)
                                            timp_total = int(round(time.time() * 1000)) - t_inceput
                                            afisare_finala(timpi, nr_noduri, timp_total, mutari_jucator, mutari_calculator)
                                            break
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                            else: # Daca selectam un nod gol
                                if de_mutat:    # Daca avem o piesa de mutat
                                    n0 = stare_curenta.tabla_joc.coordonateNoduri.index(nod)
                                    n1 = stare_curenta.tabla_joc.coordonateNoduri.index(de_mutat)
                                    if ((n0, n1) in stare_curenta.tabla_joc.muchii or
                                            (n1, n0) in stare_curenta.tabla_joc.muchii):
                                        if Joc.JMIN == '1':
                                            if nod not in stare_curenta.tabla_joc.pieseAlbe:
                                                stare_curenta.tabla_joc.piesaNeagra = nod
                                        else:
                                            stare_curenta.tabla_joc.pieseAlbe.remove(de_mutat)
                                            stare_curenta.tabla_joc.pieseAlbe.append(nod)
                                        stare_curenta.tabla_joc.deseneaza_grid(ecran)
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        mutari_jucator += 1
                                        de_mutat = False
                                        t_dupa = int(round(time.time() * 1000))
                                        print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                                        print("Numarul de noduri generate la aceasta mutare: " + str(
                                            len(stare_curenta.mutari_posibile)))
                                        nr_noduri.append(len(stare_curenta.mutari_posibile))
                                        print("Muta " + ("alb" if stare_curenta.j_curent == '1' else "negru"))
                                        if afis_daca_final(stare_curenta):
                                            stare_curenta.tabla_joc.deseneaza_grid(ecran, None, True)
                                            timp_total = int(round(time.time() * 1000)) - t_inceput
                                            afisare_finala(timpi, nr_noduri, timp_total, mutari_jucator, mutari_calculator)
                                            break
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
        else:  # jucatorul e JMAX (calculatorul)
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))
            mutari_calculator += 1
            stare_curenta.tabla_joc.deseneaza_grid(ecran)
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            timpi.append(t_dupa - t_inainte)
            print("Estimare: " + str(stare_curenta.estimare))
            print("Numarul de noduri generate la aceasta mutare: " + str(len(stare_curenta.mutari_posibile)))
            nr_noduri.append(len(stare_curenta.mutari_posibile))
            print("Muta " + ("alb" if stare_curenta.j_curent == '1' else "negru"))
            if afis_daca_final(stare_curenta):
                stare_curenta.tabla_joc.deseneaza_grid(ecran, None, True)
                timp_total = int(round(time.time() * 1000)) - t_inceput
                afisare_finala(timpi, nr_noduri, timp_total, mutari_jucator, mutari_calculator)
                break
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            t_inainte = int(round(time.time() * 1000))


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
