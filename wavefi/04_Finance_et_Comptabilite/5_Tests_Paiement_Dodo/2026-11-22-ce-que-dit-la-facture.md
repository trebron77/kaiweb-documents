# Ce que la facture de test nous apprend

> Facture `inv_0NqLI2MLxNIPJd10CPnzA`, transaction `pay_0NqLI2MLxNIPJd0wijOP5`,
> datée du **23 octobre 2026**, conservée dans ce dossier.

## Les trois faits

| Élément | Valeur constatée |
|---|---|
| Adresse de facturation | **Papeete, Îles du Vent, 98714, PF** |
| **Taxe appliquée** | **0,00 %** — montant 0,00 USD |
| Devise de la facture | **USD** — 45,01 USD |
| Vendeur émetteur | **Dodo Payments Inc**, Dover, Delaware (EIN 993486577) |
| Produit | WaveFi Starter |
| Client facturé | « WaveFi project » |

## 1. Pour un client en Polynésie, la taxe est nulle

C'est la réponse à la question posée au support Dodo. Avec une adresse polynésienne, Dodo n'applique **aucune taxe**.

Le taux de 10 % vu dans l'aperçu des produits ne concerne donc **pas** nos clients : il vient d'un pays de référence de la prévisualisation, pas du pays de l'acheteur.

**Conséquence :** afficher 9 990 et encaisser 9 990 est cohérent. L'écart de 908 XPF que je redoutais n'existe pas pour un client polynésien.

## 2. La facture est en dollars, pas en francs pacifique

45,01 USD pour un Starter vendu 4 995 XPF : Dodo convertit en dollars, et la facture du client est libellée en **USD**.

Cela pose deux questions :
- **Le taux de change devient un paramètre commercial** : le prix en XPF est stable, mais la facture en USD bouge avec l'euro.
- **Un client local reçoit une facture en dollars d'une société du Delaware.** Pour un commerce, c'est un achat de service à l'étranger ; pour une personne publique, c'est rédhibitoire.

## 3. À vérifier : le paiement en XPF est-il possible ?

La page de paiement comportait un menu « Payer en XPF ». Si ce choix existe réellement, le client peut régler en francs et la facture suivra. À confirmer lors d'un prochain test : sélectionner XPF et vérifier la devise de la facture émise.

## Ce que ça confirme sur le modèle

Dodo est bien **Merchant of Record** : il vend, il facture, il gère la taxe. KaiWeb Marketing n'apparaît pas sur la facture du client.

C'est cohérent avec la clause 4.2 des CGV (deux canaux) et avec la règle : **toute vente locale ou publique passe en facturation directe**, pas par Dodo.

---

## Deuxième test — 23 novembre 2026, paiement en XPF

Facture `inv_0NsXcPpD6RHllL0YdpydG`, transaction `pay_0NsXcPpD6RHllL0TJJcRY`.
Produit : Pack +1 000 invités à 7 990 XPF. Carte Deblock, adresse Papeete.

### Ce qui est confirmé

| Point | Constat |
|---|---|
| Reçu envoyé au client | **CFP 7 990**, impôt CFP 0 — bien en francs |
| Libellé bancaire | **DODO_PAY_WAVEFI** (le réglage a fonctionné) |
| Taxe | **0 %** une seconde fois |
| Selecteur de devise | le XPF est bien proposé et fonctionne |

### Ce qui reste vrai malgré tout

**La facture PDF est toujours en USD** : `USD 70.63`, soit 113,1 XPF pour 1 USD. Choisir XPF au
paiement change le reçu, **pas la facture**. Celle-ci est émise dans la devise de Dodo.

### Nouveauté : le reverse charge

La case « Achat en tant qu'entreprise » cochée, avec un numéro fiscal, fait apparaître la mention
**« Amount of Tax subject to Reverse Charge »**. En B2B, Dodo ne collecte pas la taxe : le client
l'autoliquide. C'est le traitement normal d'une prestation entre professionnels, mais la facture le
mentionne explicitement.

### Le piège à retenir

**Le checkout s'ouvre par défaut en USD**, même avec une adresse polynésienne. Un client qui ne
touche pas au sélecteur paie en dollars sans s'en rendre compte. C'est exactement ce qui s'est
passé au premier test.
