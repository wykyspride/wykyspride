from django.db import models
from django.contrib.auth.models import User

    # ###############################################################################
  #                   CREATION DES MODELES: FICHIERS DE DONNEES                   #
#################################################################################


#TEST
class tes1(models.Model):
    champ1=models.TextField()
    champ2=models.TextField(default=0)


#CATEGORIE
class categorie(models.Model):
    idcat=models.AutoField(primary_key=True)
    libelle=models.CharField(max_length=100)

    class Meta:
        verbose_name=("Categorie")
        verbose_name_plural=("Categories")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#FOURNISSEUR
class fournisseur(models.Model):
    idfour=models.AutoField(primary_key=True)
    nomfour=models.CharField(max_length=200)
    contact=models.CharField(max_length=20)
    admail=models.EmailField(max_length=50)
    localisation=models.CharField(max_length=300)
    photoid=models.ImageField(default=0)

    class Meta:
        verbose_name=("Fournisseur")
        verbose_name_plural=("Fournisseurs")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#MODE DE REGLEMENT
class modepaie(models.Model):
    idmode=models.AutoField(primary_key=True)
    libelle=models.CharField(max_length=50)

    class Meta:
        verbose_name=("Mode Reglement")
        verbose_name_plural=("Modes Reglement")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#STATUT
class statut(models.Model):
    idstatut=models.AutoField(primary_key=True)
    libelle=models.CharField(max_length=15)

    class Meta:
        verbose_name=("Statut")
        verbose_name_plural=("Statuts")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#PRODUITS
class produit(models.Model):
    idpro=models.AutoField(primary_key=True)
    categorie = models.ForeignKey(categorie, on_delete=models.CASCADE)
    fournisseur=models.ForeignKey(fournisseur, on_delete=models.CASCADE)
    nom=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    prixu=models.DecimalField(max_digits=100000, decimal_places=2,default=0)
    qte=models.IntegerField(default=0)
    imageprod=models.ImageField()

    class Meta:
        verbose_name=("Produit")
        verbose_name_plural=("Produits")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#CLIENTS



class client(models.Model):
    Genre_Type=(
        ( 'Homme','Homme'),
        ('Femme', 'Femme'),
        ('Autre', 'Autre'),
 )

    idcli=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    contact=models.CharField(max_length=20)
    admail=models.EmailField(max_length=50)
    localisation=models.CharField(max_length=200)
    genre=models.CharField(max_length=10,choices=Genre_Type)


    class Meta:
        verbose_name=("Client")
        verbose_name_plural=("Clients")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name



#LIGNES DE COMMANDE DRAFT
class lignecomdraft(models.Model):
    idlignedraf=models.AutoField(primary_key=True)
    idprod=models.ForeignKey(produit,on_delete=models.CASCADE)
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    statut=models.CharField(max_length=10, default='draft')
    qte=models.IntegerField(default=0)
    prixu=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    prixtotal=models.DecimalField(max_digits=100000,default=0,decimal_places=2)

    class Meta:
        verbose_name=("Ligne Panier")
        verbose_name_plural=("Lignes Panier")
        #Calcul des totaux par ligne de commande
    @property
    def get_prixtotal(self):
        prixtotal=self.prixu*self.qte





#COMMANDES
class commande(models.Model):
    idcom=models.AutoField(primary_key=True)
    idstatut=models.ForeignKey(statut,on_delete=models.CASCADE)
    datecom=models.DateField()
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    totalht=models.DecimalField(max_digits=100000,default=0, decimal_places=2)
    totalttc=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    remise=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    totalpaye=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    nbreligne=models.IntegerField(default=0)
    commentaire=models.CharField(max_length=500)

    class Meta:
        verbose_name=("Commande")
        verbose_name_plural=("Commandes")

    def _str_(self):
     return self.name

#Calcul du total de toutes les lignes du bon de commande
@property
def get_prixtotal(self):
    lignecom=self.lignecom_set.all()
    totalttc=sum(lignecom.get_prixtotal for lignecom in lignecom )

#Calcul du total à payer après remise
@property
def get_totalpaye(self):
    totalpaye=self.totalttc-self.remise


#LIGNES DE COMMANDE
class lignecom(models.Model):
    idlcom=models.AutoField(primary_key=True)
    idcom=models.ForeignKey(commande,on_delete=models.CASCADE)
    idprod=models.ForeignKey(produit,on_delete=models.CASCADE)
    qte=models.IntegerField(default=0)
    prixu=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    prixtotal=models.DecimalField(max_digits=100000,default=0,decimal_places=2)

    class Meta:
        verbose_name=("Ligne Commande")
        verbose_name_plural=("Lignes Commande")
        #Calcul des totaux par ligne de commande
    @property
    def get_prixtotal(self):
        prixtotal=self.prixu*self.qte


#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#BON DE LIVRAISON

class bl(models.Model):
    idlignebl=models.AutoField(primary_key=True)
    idcom=models.ForeignKey(commande,on_delete=models.CASCADE)
    client=models.ForeignKey(User,on_delete=models.CASCADE,default="" )
    dateliv=models.DateField()
    totalht=models.DecimalField(max_digits=100000,default=0, decimal_places=2)
    totalttc=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    remise=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    totalpaye=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    commentaire=models.CharField(max_length=500)
    idstatut=models.ForeignKey(statut,on_delete=models.CASCADE)

    class Meta:
        verbose_name=("BL")
        verbose_name_plural=("BL")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name


#LIGNE DE BL
class lignebl(models.Model):
    idlcom=models.AutoField(primary_key=True)
    idcom=models.ForeignKey(commande,on_delete=models.CASCADE)
    bl=models.ForeignKey(bl,on_delete=models.CASCADE)
    idprod=models.ForeignKey(produit,on_delete=models.CASCADE)
    qte=models.IntegerField(default=0)
    prixu=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    prixtotal=models.DecimalField(max_digits=100000,default=0,decimal_places=2)

    class Meta:
        verbose_name=("Ligne BL")
        verbose_name_plural=("Lignes BL")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#FACTURE
class facture(models.Model):
    idfac=models.AutoField(primary_key=True)
    idcom=models.ForeignKey(commande,on_delete=models.CASCADE)
    bl=models.ForeignKey(bl,on_delete=models.CASCADE,default=0)
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    datefact=models.DateField()
    totalht=models.DecimalField(max_digits=100000,default=0, decimal_places=2)
    totalttc=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    remise=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    totalpaye=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    commentaire=models.CharField(max_length=500)
    idstatut=models.ForeignKey(statut,on_delete=models.CASCADE)

    class Meta:
        verbose_name=("Facture")
        verbose_name_plural=("Factures")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#LIGNE DE FACTURE
class Lignefac(models.Model):
    idlignefac=models.AutoField(primary_key=True)
    idcom=models.ForeignKey(commande,on_delete=models.CASCADE)
    idfac=models.ForeignKey(facture,on_delete=models.CASCADE)
    idprod=models.ForeignKey(produit,on_delete=models.CASCADE)
    qte=models.IntegerField(default=0)
    prixu=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    prixtotal=models.DecimalField(max_digits=100000,default=0,decimal_places=2)

    class Meta:
        verbose_name=("Ligne Facture")
        verbose_name_plural=("Lignes Factures")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

#REGLEMENT
class reglement(models.Model):
    idregl=models.AutoField(primary_key=True)
    client=models.ForeignKey(User,on_delete=models.CASCADE,default="" )
    idcom=models.ForeignKey(commande,on_delete=models.CASCADE)
    bl=models.ForeignKey(bl,on_delete=models.CASCADE,default=0)
    totalfacture=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    totalreglement=models.DecimalField(max_digits=100000,default=0,decimal_places=2)
    commentaire=models.CharField(max_length=500)
    statut=models.ForeignKey(statut,on_delete=models.CASCADE)

    class Meta:
        verbose_name=("Reglement")
        verbose_name_plural=("Reglements")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name


#LIGNE DE Reglement
class lignereglement(models.Model):
    idlignereg=models.AutoField(primary_key=True)
    idreg=models.ForeignKey(reglement,on_delete=models.CASCADE)
    idmode=models.ForeignKey(modepaie,on_delete=models.CASCADE)
    datereg=models.DateField()
    montantregle=models.IntegerField(default=0)
    commentaire=models.CharField(max_length=500)

    class Meta:
        verbose_name=("Ligne Reglement")
        verbose_name_plural=("Lignes Reglement")

#SURCHARGE POUR AFFICHER LES VALEURS DANS LE TABLEAU DE L'ESPACE ADMIN 
def _str_(self):
    return self.name

