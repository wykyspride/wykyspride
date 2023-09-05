from django.contrib import admin

from .models import client,modepaie,fournisseur,categorie,lignecomdraft,commande,lignecom,statut,bl,lignebl,facture,Lignefac
from . import models
# Register your models here.
#AFFICHER LES PRODUITS SELON UN ORDRE DEFINI

@admin.register(models.fournisseur)
class fournisseur(admin.ModelAdmin):
    list_display=('idfour','nomfour','contact','admail','localisation','photoid') #Ordre d'affichage
    ordering=('idfour','nomfour') #Ordonner par ID
    list_filter=('idfour','nomfour')     #Filtrer
    search_fields=('nomfour','admail')     #Actier la zone de recherche

@admin.register(models.produit)
class produit(admin.ModelAdmin):
    list_display=('idpro','nom','description','prixu','qte','fournisseur') 


admin.site.register(client,)
admin.site.register(modepaie)
admin.site.register(categorie)
admin.site.register(lignecomdraft)
admin.site.register(commande)
admin.site.register(lignecom)
admin.site.register(statut)
admin.site.register(bl)
admin.site.register(lignebl)
admin.site.register(facture)
admin.site.register(Lignefac)