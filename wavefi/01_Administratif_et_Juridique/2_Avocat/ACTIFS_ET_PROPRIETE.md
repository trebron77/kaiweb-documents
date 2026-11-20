# Actifs et propriété intellectuelle — dossier SASU

> Préparé le 2026-11-19. À valider par Maître Peuillot et par le comptable.
> Objet : faire en sorte que la SASU KaiWeb Marketing **détienne réellement** ses actifs,
> aujourd'hui rattachés à des comptes personnels.

## 1. Inventaire des actifs

| Actif | Nature | Détenteur actuel | Risque si non transféré |
| --- | --- | --- | --- |
| Code source FenuaFact | Logiciel | Dépôt GitHub personnel (`trebron77/fenua-voice-quotes`) | La société exploite un logiciel qu'elle ne possède pas |
| Code / application WaveFi | Logiciel | Compte Lovable personnel | Idem |
| `fenuafact.com` | Nom de domaine | Compte Namecheap personnel | Perte du domaine en cas de litige ou de vente |
| `wavefi.tech` et sous-domaines | Noms de domaine | Compte Namecheap personnel | Idem |
| Base de données et authentification | Données, infrastructure | Projet Supabase personnel | Transfert de données clients impossible sans accord |
| Encaissement des abonnements | Contrat marchand | Compte Dodo Payments personnel | Revenus rattachés à une personne physique |
| Numéro WhatsApp Business et app Meta | Actif numérique | Compte Meta personnel | Coupure du canal principal du produit |
| Comptes de messagerie (`support@`, `contact@`) | Noms de domaine mail | Zoho personnel | Perte de la continuité de service |
| Marques « FenuaFact » et « WaveFi » | Signes distinctifs | Non déposées à ce jour | Aucun monopole, risque de conflit |

## 2. Deux mécanismes possibles

| Mécanisme | Principe | Conséquences |
| --- | --- | --- |
| **Apport en nature** | Les actifs entrent au capital de la SASU lors de la constitution | Valorisation nécessaire ; engage la responsabilité de l'apporteur ; doit être fait **avant** l'immatriculation pour être simple |
| **Cession à la société** | La société achète les actifs à la personne physique après immatriculation | Prix de cession à justifier ; plus-value éventuelle ; formalisme plus lourd mais plus souple |

**Le calendrier décide** : si la société n'est pas encore immatriculée, l'apport en nature est la voie naturelle. Après immatriculation, seule la cession reste possible.

## 3. Points à faire trancher par le cabinet

1. Faut-il privilégier l'apport en nature (avant immatriculation) ou la cession (après) ?
2. Comment valoriser un logiciel développé par le dirigeant lui-même, sans facture d'achat ?
3. Quelles formalités pour les noms de domaine (transfert du titulaire, pas seulement du contact) ?
4. Les comptes techniques (Supabase, Dodo, Meta) peuvent-ils passer au nom de la société sans perte de données ni interruption de service ?
5. Faut-il déposer les marques « FenuaFact » et « WaveFi » auprès de la DICIP, et sous quelles classes ?

## 4. Ce qu'il faut préparer côté documents

| Pièce | Où l'obtenir |
| --- | --- |
| Capture du dépôt GitHub et de son historique | GitHub → Settings |
| Factures d'achat des noms de domaine | Namecheap → Billing |
| Contrats Supabase, Dodo, Meta | Espaces clients respectifs |
| Description technique du logiciel | [`REPRISE_MVP.md`](../../../fenuafact/product/REPRISE_MVP.md) et [`ETAT_TECHNIQUE.md`](../../../fenuafact/ops/ETAT_TECHNIQUE.md) |

## 5. Vérification Meta Business — dépend de la SASU

| Prérequis | État | Bloqué par |
| --- | --- | --- |
| Entité juridique immatriculée | ❌ | SASU |
| Justificatif d'existence (statuts, avis d'immatriculation) | ❌ | SASU |
| Justificatif d'adresse au nom de la société | ⚠️ contrat de domiciliation signé (Papeete Coworking) | à mettre au nom de la SASU |
| Numéro TAHITI | ❌ | CCISM après immatriculation |
| Compte business Meta rattaché à l'entité | ⚠️ actuellement « Individu » | transfert d'entité |

**Conséquence pratique** : la vérification Meta ne peut pas être lancée avant l'immatriculation. En attendant, l'application reste en mode Live avec la limite de 250 conversations par jour — suffisant pour un pilote.

## 6. Ordre recommandé

1. Obtenir la convention et la facture du cabinet → régler les 50 000 FCFP
2. Finaliser l'article 4 des statuts avec l'adresse du siège
3. Signer les statuts, déposer à la CCISM, obtenir le TAHITI
4. Trancher l'apport en nature / cession avec le cabinet
5. Transférer les domaines, comptes et dépôts au nom de la SASU
6. Lancer la vérification Meta Business
7. Déposer les marques
