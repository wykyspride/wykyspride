from .models import produit
from django import forms

class prodform (forms.ModelForm):
    class Meta:
        model=produit
        fields=('categorie','fournisseur','nom','description','prixu','qte','imageprod')