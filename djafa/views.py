from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from .form import prodform
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db.models import Q
from .models import produit,categorie,fournisseur,client,commande,lignecomdraft,lignecom,facture,reglement,bl,lignebl,Lignefac
from datetime import datetime
from django.template import loader
from django.template.loader import get_template

# Creation des utilisateurs
def adduser(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        first_name = request.POST.get('nomcomplet', None)
        last_name = request.POST.get('contact', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)

#ENREGISTREMENT DANS LE FICHIER CLIENT
        nom=request.POST.get('nomcomplet')
        contact=request.POST.get('contact')
        admail=request.POST.get('email')
        localisation=request.POST.get('localisation')
        genre=request.POST.get('genre')
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mots de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"
        # register
        if error == False:
            user = User(username = name, email = email,first_name=first_name,last_name=last_name)
            user.save()
            user.password = password
            user.set_password(user.password)
            user.save()

        #Enregistrement client
            user_id=user.id
            saveclient=client.objects.create(user_id=user_id,nom=nom,contact=contact,admail=admail,localisation=localisation,genre=genre)
            saveclient.save()
            return redirect('conex')

    context = {'error':error,'message':message}
    return render(request, 'adduser.html', context)


#CONNEXION
def conex(request):

    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('espaceclient')
            else:
                print("mot de passe incorrecte")
        else:
            print("L'utilisateur n'existe pas")
    return render(request, 'conex.html', {})


#DECONNEXION
def deconex(request):
    logout(request)
    return redirect('conex')


#ESPACE CLIENT
def espaceclient(request):
    if request.user.is_authenticated:
        client_id=request.user.id
        #Recuperation de articles de mon panier
        contenupaner=lignecomdraft.objects.filter(client_id=client_id)
        #Recuperation du total des lignes
        leprixtotal=0
        for p in contenupaner:
            leprixtotal+=p.prixtotal

        #Recuperation de mes commandes
        mescommandes=commande.objects.filter(client_id=client_id)
        monpanier=lignecomdraft.objects.filter(client=request.user).count() #Recuperation du panier
        context={'contenupaner':contenupaner,'mescommandes':mescommandes,'monpanier':monpanier,'leprixtotal':leprixtotal}

        #Cas de validation de la commande
        if request.method=="POST":
           #Enregistrement de la commande
              if request.user.is_authenticated:
                client_id=request.user.id
                idstatut_id=1
                datecom=datetime.today()
                totalht=leprixtotal #Recuperer la somme des lignes
                totalttc=leprixtotal
                remise=0
                totalpaye=leprixtotal
                savecom=commande.objects.create(idstatut_id=idstatut_id,datecom=datecom,client_id=client_id,totalht=totalht,totalttc=totalttc,remise=remise,totalpaye=totalpaye)
                savecom.save()                      
           
            #Enregistrement des lignes de commande
                for lignec in  contenupaner:
                  client_id=lignec.client_id
                  idcom_id=savecom.idcom
                  idprod_id=lignec.idprod_id
                  qte=lignec.qte
                  prixu=lignec.prixu
                  prixtotal=lignec.prixtotal
                  savelignecom=lignecom.objects.create(idcom_id=idcom_id,idprod_id=idprod_id,qte=qte,prixu=prixu,prixtotal=prixtotal)
                  savelignecom.save()
                  lignec.delete()
              return redirect('espaceclient')
    else:
         print('Veuillez vous connecter')
         return redirect('conex')
    return render(request, 'espaceclient.html',context)


#MOT DE PASSE OUBLIE
def mdpoublie(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            print("Processus de recuperation en cours")
            html = """
                <p> Hello, merci de cliquer pour modifier votre email </p>
            """
            msg = EmailMessage( "Modification de mot de passe!", html, "ekobenan10@gmail.com", ["ekobenan10@gmail.com"],)
            msg.content_subtype = 'html'
            msg.send()
            message = "Processus de recuperation en cours"
            success = True
        else:
            print("L'utisateur n'existe pas")
            error = True
            message = "L'utisateur n'existe pas"
    context = {'success': success,'error':error,'message':message}
    return render(request, "mdpoublie.html", context)


#home
def home(request):
    listeimageprod=produit.objects.all()
    if request.user.is_authenticated:
        monpanier=lignecomdraft.objects.filter(client=request.user).count() #Recuperation du panier
        if request.method=="GET":
                nom=request.GET.get('recherche')
                if nom is not None:
                    listeimageprod=produit.objects.filter(nom__icontains=nom)
        context={'listeimageprod':listeimageprod,'monpanier':monpanier}
        return render (request,'home.html',context)
    else:
            if request.method=="GET":
                nom=request.GET.get('recherche')
                if nom is not None:
                    listeimageprod=produit.objects.filter(nom__icontains=nom)
                context={'listeimageprod':listeimageprod}
                return render(request,'home.html',context)



#Creation des articles
def ajoutprod(request):
     lesfournisseur=fournisseur.objects.all()
     lescatproduit=categorie.objects.all()
     context={'lesfournisseur':lesfournisseur,'lescatproduit':lescatproduit}

    #Recuperation des fournisseurs et type de categorie
     if request.method=="POST":
        #Definition des champs du formulaire
          categorie_id=request.POST.get('categorie_id')
          fournisseur_id=request.POST.get('fournisseur_id')
          nom=request.POST.get('nom')
          description=request.POST.get('description')
          prixu=request.POST.get('prixu')
          qte=request.POST.get('qte')
          imageprod=request.POST.get('imageprod')
          NewEnregistrement=produit.objects.create(categorie_id=categorie_id,fournisseur_id=fournisseur_id,nom=nom,description=description,prixu=prixu,qte=qte,imageprod=imageprod)
          NewEnregistrement.save()
          return redirect ('espacegestion')
     return render (request,'ajoutprod.html',context)


#Liste es produits, affichage dans tableau
def listeprod (request):
    listeproduit=produit.objects.all()
    context={'listeproduit':listeproduit}
    return render(request,'listeprod.html',context)

#Modification de produit
def modifprod (request,idpro):
    lesfournisseur=fournisseur.objects.all()
    lescatproduit=categorie.objects.all()
    leproduit=produit.objects.get(idpro=idpro)
    context={'lesfournisseur':lesfournisseur,'lescatproduit':lescatproduit,'leproduit':leproduit}
    if request.method=="POST":
        idpro=leproduit.idpro
        leproduit.categorie_id=leproduit.categorie_id
        leproduit.fournisseur_id=request.POST.get('fournisseur_id')
        leproduit.nom=request.POST.get('nom')
        leproduit.description=request.POST.get('description')
        leproduit.prixu=request.POST.get('prixu')
        leproduit.qte=request.POST.get('qte')
        leproduit.imageprod=request.POST.get('imageprod')
        leproduit.save()
        return redirect ('espacegestion')
    return render(request,'modifprod.html',context)


#SUPPRIMER le produit
def deleteprod (request,idpro):
    leproduit=produit.objects.get(idpro=idpro)
    nom=leproduit.nom
    context={'nom':nom}
    if request.method=="POST":
        leproduit.delete()
        return redirect('espacegestion')
    return render (request,'delete.html',context)


#Affichage des details d'un produit puis ajout dans le panier
def detailprod(request,idpro):
    message=[] 
    leproduit=produit.objects.get(idpro=idpro)
    if request.user.is_authenticated:
        monpanier=lignecomdraft.objects.filter(client=request.user).count() #Recuperation du panier
        context={'leproduit':leproduit,'monpanier':monpanier}
    else:
        context={'leproduit':leproduit}

    #Enregistrement dans panier
    if request.method=="POST":
        if request.user.is_authenticated:
         statut='draft'
         qte=request.POST.get('qte')
         prixtotal=request.POST.get('prixtotal')
         client_id=request.user.id
         Newpanier=lignecomdraft.objects.create(prixtotal=prixtotal,qte=qte,prixu=leproduit.prixu,statut=statut,client_id=client_id,idprod_id=leproduit.idpro)
         Newpanier.save()
         return redirect ('home')
        else:
            message='Veuillez vous connecter'
            print('Veuillez vous connecter')
            return redirect ('conex')
    return render(request, 'detailprod.html', context)


    ################################################################################
  #                   GESTION DES CLIENTS                                        #
#################################################################################


#Liste des commmandes, affichage dans tableau
def listecom (request):
    listecom=commande.objects.all()
    context={'listecom':listecom}
    return render(request,'listecom.html',context)

#Creation des Commandes
def ajoutcom(request):
     lesproduit=produit.objects.all()
     monpanier=lignecomdraft.objects.filter(client=request.user).count() #Recuperation du panier
     context={'lesproduit':lesproduit,'monpanier':monpanier}

    #Recuperation des fournisseurs et type de categorie
     if request.method=="POST":
        #Definition des champs du formulaire
          idcom=request.POST.get('idcom')
          idstatut=request.POST.get('idstatut')
          datecom=request.POST.get('datecom')
          #client=request.POST.get('client')
          client=request.user.id
          totalht=request.POST.get('totalht')
          totalttc=request.POST.get('totalttc')
          remise=request.POST.get('remise')
          totalpaye=request.POST.get('totalpaye')
          commentaire=request.POST.get('commentaire')
          NewEnregistrement=commande.objects.create(idcom=idcom,idstatut=idstatut,datecom=datecom,client=client,totalht=totalht,totalttc=totalttc,remise=remise,totalpaye=totalpaye,commentaire=commentaire)
          NewEnregistrement.save()
          return redirect ('espaceclient')
     return render (request,'ajoutcom.html',context)


#Espace de Gestion
def espacegestion (request):
    liestepanier=lignecomdraft.objects.all()
    listecommande=commande.objects.all()
    listebl=bl.objects.all()
    listefacture=facture.objects.all()
    listereglement=reglement.objects.all()
    listeclient=client.objects.all()
    listefour=fournisseur.objects.all()
    listeprod=produit.objects.all()
    context={'liestepanier':liestepanier,'listecommande':listecommande,'listefacture':listefacture,'listereglement':listereglement,'listebl':listebl,'listeprod':listeprod,'listefour':listefour,'listeclient':listeclient}
    return render (request, 'espacegestion.html',context)


#Details commandes
def detailcom(request,idcom):
     lacommande=commande.objects.get(idcom=idcom)
     detailcomande=lignecom.objects.filter(idcom_id=lacommande.idcom)
     monpanier=lignecomdraft.objects.filter(client=request.user).count() #Recuperation du panier
     context={'detailcomande':detailcomande,'lacommande':lacommande,'monpanier':monpanier}

#Transformation de la commande en achat: Etablissement BL
     if request.method=="POST":
           #Enregistrement du bl
                client_id=lacommande.client_id
                idcom_id=lacommande.idcom
                idstatut_id=lacommande.idstatut_id
                dateliv=datetime.today()
                totalht=lacommande.totalht
                totalttc=lacommande.totalttc
                remise=lacommande.remise
                totalpaye=lacommande.totalpaye
                savebl=bl.objects.create(idcom_id=idcom_id,idstatut_id=idstatut_id,dateliv=dateliv,client_id=client_id,totalht=totalht,totalttc=totalttc,remise=remise,totalpaye=totalpaye)
                savebl.save()                      
           
            #Enregistrement des lignes du bl
                for lignecomand in  detailcomande:
                    bl_id=savebl.idlignebl
                    idcom_id=lignecomand.idcom_id
                    idprod_id=lignecomand.idprod_id
                    qte=lignecomand.qte
                    prixu=lignecomand.prixu
                    prixtotal=lignecomand.prixtotal
                    savelignebl=lignebl.objects.create(bl_id=bl_id,idcom_id=idcom_id,idprod_id=idprod_id,qte=qte,prixu=prixu,prixtotal=prixtotal)
                    savelignebl.save()
                return redirect('espacegestion')
     return render(request,'detailcom.html',context)

#RECUPERATION DES DETAILS DU BL
def detailbl(request,idlignebl):
    lebl=bl.objects.get(idlignebl=idlignebl)
    idbl=lebl.idlignebl
    contenubl=lignebl.objects.filter(bl_id=idbl)
    context={'lebl':lebl, 'contenubl':contenubl}

#Transformation du BL en Facture
    if request.method=="POST":
           #Enregistrement de la facture
                bl_id=idbl
                client_id=lebl.client_id
                idcom_id=lebl.idcom_id
                idstatut_id=lebl.idstatut_id
                datefact=datetime.today()
                totalht=lebl.totalht
                totalttc=lebl.totalttc
                remise=lebl.remise
                totalpaye=lebl.totalpaye
                savefac=facture.objects.create(bl_id=bl_id,idcom_id=idcom_id,idstatut_id=idstatut_id,datefact=datefact,client_id=client_id,totalht=totalht,totalttc=totalttc,remise=remise,totalpaye=totalpaye)
                savefac.save()                      
           
            #Enregistrement des lignes de la facture
                for lignedubl in  contenubl:
                    idfac_id=savefac.idfac
                    idcom_id=lignedubl.idcom_id
                    idprod_id=lignedubl.idprod_id
                    qte=lignedubl.qte
                    prixu=lignedubl.prixu
                    prixtotal=lignedubl.prixtotal
                    savelignefac=Lignefac.objects.create(idfac_id=idfac_id,idcom_id=idcom_id,idprod_id=idprod_id,qte=qte,prixu=prixu,prixtotal=prixtotal)
                    savelignefac.save()
                return redirect('espacegestion')
    return render(request,"detailbl.html",context)

#REGLEMENT FACTURES
def reglefac(request):
    return render(request,"reglefac.html")
