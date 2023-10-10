from django.db import models



#utenti compilato
class Utente(models.Model):
    nome = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)



    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name_plural = "Utente"
test = Utente("name")





#####################################################################

#funzionante
class Commessa(models.Model):

    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)
    tipologia = models.CharField(max_length=200, null=True)
    ultimo_aggiornamento = models.DateField(null=True, blank=True)
    priorità = models.CharField(max_length=200, null=True)
    #FOREIGN KEYS DI COMMESSA
    id_servizio = models.ForeignKey('Task', null=True, on_delete=models.SET_NULL)
    cliente_finale = models.ForeignKey('Aziende', null=True, on_delete=models.SET_NULL)
    id_azienda = models.BigIntegerField(null=True)







    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Commessa"

#funzionante
class Task(models.Model):

    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    tipo = models.CharField(max_length=200,null=True)
    data_creazione = models.DateField(null=True, blank=True)
    sollecito = models.DateField(null=True, blank=True)
    priorità = models.CharField(max_length=200, null=True)
    id_commessa = models.BigIntegerField(null=True)

    # FOREIGN KEYS DI COMMESSA
    id_contatti = models.ForeignKey('Contatti', null=True, on_delete=models.SET_NULL)
    responsabile = models.ForeignKey('Utente', null=True, on_delete=models.SET_NULL)
    commesse = models.ManyToManyField(Commessa)


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Task"

#funzionante
class Contratti(models.Model):
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)
    ultimo_aggiornamento = models.DateField(null=True, blank=True)
    data_creazione = models.DateField(null=True, blank=True)

    # FOREIGN KEYS DI CONTRATTI
    id_commessa = models.ForeignKey('Commessa', null=True, on_delete=models.SET_NULL)
    sog_passivo = models.ForeignKey('Aziende', related_name='contratti_passivi', null=True, on_delete=models.SET_NULL)
    sog_attivo = models.ForeignKey('Aziende', related_name='contratti_attivi', null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Contratti"


class Aziende(models.Model):

    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)
    commesse = models.ManyToManyField(Commessa)
    p_iva = models.BigIntegerField(null=True)
    cod_fis = models.TextField(max_length=200, null=True)
    id_commessa = models.BigIntegerField(null=True)

    # FOREIGN KEYS DI AZIENDE
    responsabile = models.ForeignKey('Utente', null=True, on_delete=models.SET_NULL)





    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Aziende"

class Fatture(models.Model):
    A0 = "20"
    A1 = "21"
    A2 = "22"
    A3 = "23"

    ANNO = [
        (A0, "2020"),
        (A1, "2021"),
        (A2, "2022"),
        (A3, "2023")
    ]

    anno_competenza = models.CharField(
        max_length=2,
        choices=ANNO,
        null=True
    )
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #incassi
    data_incasso = models.DateField(null=True, blank=True)
    importo = models.FloatField(null=True)

    # FOREIGN KEYS DI FATTURE
    contratto = models.ForeignKey('Contratti', null=True, on_delete=models.SET_NULL)
    parte_passiva = models.ForeignKey(Aziende, null=True, on_delete=models.SET_NULL)
    commessa = models.ForeignKey(Commessa, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name_plural = "Fatture"





#sottoelemento di Fatture
# class Incassi(models.Model):
#     nome = models.ForeignKey(Fatture, null=True, on_delete=models.SET_NULL)
#     data_incasso = models.DateField(null=True, blank=True)
#     importo = models.FloatField(null=True)
#
#     def __str__(self):
#         return self.nome
#
#     class Meta:
#         verbose_name_plural = "Incassi"




#funzionante
class Servizio(models.Model):
    COMMERCIALE = "CO"
    FORMAZIONE = "FO"
    PROCACCIAMENTO = "PR"

    TIPOLOGIA_COMMESSA = [
        (COMMERCIALE, "Commerciale"),
        (FORMAZIONE, "Formazione 4.0"),
        (PROCACCIAMENTO, "Procacciamento"),
    ]
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    tipologia = models.CharField(
        max_length=2,
        choices=TIPOLOGIA_COMMESSA,
        null=True
    )
    link_fonte = models.TextField(max_length=200, null=True)
    documenti = models.FileField(null=True)

    # FOREIGN KEYS DI SERVIZIO
    referente = models.ForeignKey(Utente, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Servizio"

#funzionante
class Contatti(models.Model):
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)
    in_qualita_di = models.CharField(max_length=200, null=True)
    #titolare_effettivo = models.ForeignKey(Aziende, null=True, on_delete=models.SET_NULL)
    #azienda_di_appartenenza = models.ForeignKey(Aziende, null=True, on_delete=models.SET_NULL)
    commesse = models.ManyToManyField(Commessa)

    # FOREIGN KEYS DI CONTATTI
    legale_rappresentante = models.ForeignKey(Aziende, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Contatti"



