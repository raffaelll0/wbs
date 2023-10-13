from django.db import models




class Utente(models.Model):
    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)
    email = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=200, null=True)



    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name_plural = "Utente"




class Commessa(models.Model):
    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ATTRIBUTI
    tipologia = models.CharField(max_length=200, null=True)
    ultimo_aggiornamento = models.DateField(null=True, blank=True)
    priorità = models.CharField(max_length=200, null=True)

    #ID ESTERNI
    id_azienda = models.BigIntegerField(null=True)

    #FOREIGN KEYS DI COMMESSA
    id_servizio = models.ForeignKey('Task', null=True, on_delete=models.SET_NULL)
    cliente_finale = models.ForeignKey('Aziende', null=True, on_delete=models.SET_NULL)



    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Commessa"




class Task(models.Model):

    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ATTRIBUTI
    tipo = models.CharField(max_length=200,null=True)
    data_creazione = models.DateField(null=True, blank=True)
    sollecito = models.DateField(null=True, blank=True)
    priorità = models.CharField(max_length=200, null=True)

    #ID ESTERNI
    id_commessa = models.BigIntegerField(null=True)
    id_utente = models.BigIntegerField(null=True)

    #MODELLI ESTERNI
    commesse = models.ManyToManyField(Commessa)

    # FOREIGN KEYS DI COMMESSA
    responsabile = models.ForeignKey('Utente', null=True, on_delete=models.SET_NULL)



    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Task"




class Contratti(models.Model):
    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ATTRIBUTI
    ultimo_aggiornamento = models.DateField(null=True, blank=True)
    data_creazione = models.DateField(null=True, blank=True)

    #ID ESTERNI
    id_commessa = models.BigIntegerField(null=True)
    id_attivo = models.BigIntegerField(null=True)
    id_passivo = models.BigIntegerField(null=True)

    #MODELLI ESTERNI
    commesse = models.ManyToManyField(Commessa)


    # FOREIGN KEYS DI CONTRATTI
    sog_passivo = models.ForeignKey('Aziende', related_name='contratti_passivi', null=True, on_delete=models.SET_NULL)
    sog_attivo = models.ForeignKey('Aziende', related_name='contratti_attivi', null=True, on_delete=models.SET_NULL)



    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Contratti"




class Aziende(models.Model):

    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ID ESTERNI
    id_commessa = models.BigIntegerField(null=True)
    id_utente = models.BigIntegerField(null=True)

    #ATTRIBUTI
    commesse = models.ManyToManyField(Commessa)
    p_iva = models.BigIntegerField(null=True)
    cod_fis = models.TextField(max_length=200, null=True)

    #MODELLI ESTERNI
    responsabile = models.ManyToManyField(Utente)

    # FOREIGN KEYS DI AZIENDE



    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Aziende"




class Fatture(models.Model):

    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ATTRIBUTI
    anno_competenza = models.CharField(max_length=200, null=True)

    #ATTRIBUTI INCASSI
    stato = models.CharField(max_length=200, null=True)
    importo = models.FloatField(null=True)

    # ID ESTERNI
    id_contratti = models.BigIntegerField(null=True)

    # FOREIGN KEYS DI FATTURE
    contratto = models.ForeignKey('Contratti', null=True, on_delete=models.SET_NULL)



    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name_plural = "Fatture"




#funzionante
class Servizio(models.Model):

    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ATTRIBUTI
    tipologia = models.CharField(max_length=200,null=True)
    link_fonte = models.TextField(max_length=200, null=True)
    documenti = models.TextField(null=True)

    #ID ESTERNI
    id_utente = models.BigIntegerField(null=True)

    # FOREIGN KEYS DI SERVIZIO
    responsabile = models.ManyToManyField(Utente)



    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Servizio"




#funzionante
class Contatti(models.Model):

    #ATTRIBUTI PRINCIPALI
    nome = models.CharField(max_length=200, null=True)
    id_monday = models.BigIntegerField(null=True)

    #ATTRIBUTI
    in_qualita_di = models.CharField(max_length=200, null=True)

    #ID ESTERNI
    id_azienda = models.BigIntegerField(null=True)
    id_commessa = models.BigIntegerField(null=True)

    #MODELLI ESTERNI
    commesse = models.ManyToManyField(Commessa)

    # FOREIGN KEYS DI CONTATTI
    azienda_di_appartenenza = models.ManyToManyField(Aziende)



    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Contatti"



