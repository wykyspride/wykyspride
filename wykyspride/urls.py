from django.contrib import admin
from django.urls import path
from djafa.views import conex,adduser,espaceclient,deconex,mdpoublie,home,ajoutprod,listeprod,modifprod,detailprod,listecom,ajoutcom,espacegestion,detailcom,detailbl,reglefac,deleteprod
#POUR LA GESTION DES FICHIERS STATIC: IMAGE, VIDEOS
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('espaceclient',espaceclient,name='espaceclient'),# Epace Client 
    path('conex',conex,name='conex'),#Affichage de la page de connexion
    path('adduser',adduser,name='adduser'),# Ajout utilsateur


    path('admin/', admin.site.urls),
    path('',home,name='home'),# Ajout utilsateur
    path('deconex',deconex,name='deconex'),# Deconnexion de l'utilisateur
    path('mdpoublie',mdpoublie,name='mdpoublie'),# Mot de passe oublié


    path('ajoutprod', ajoutprod, name='ajoutprod'),
    path('listeprod', listeprod, name='listeprod'),
    path('modifprod/<int:idpro>',modifprod,name='modifprod'),#Recuperation du produit pour modification
    path('detailprod/<int:idpro>',detailprod,name='detailprod'),#Recuperation des details du produit
    path('detailcom/<int:idcom>',detailcom,name='detailcom'),#Recuperation des details dune commande
    path('detailbl/<int:idlignebl>',detailbl,name='detailbl'),#Recuperation du bl
    path('reglefac',reglefac,name='reglefac'),#Recuperation du bl



    path('ajoutcom', ajoutcom, name='ajoutcom'),
    path('listecom', listecom, name='listecom'),
    #path('e/<int:idpro>',ajoutpanier,name='home'),#Recuperation des details du produit
    path('espacegestion',espacegestion,name='espacegestion'),
    path('deleteprod/<int:idpro>',deleteprod,name='deleteprod'),#SUPPRESSION DE PRODUIT des details du produit

]


#RECUPERATION DES FICHIERS STATIC
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)