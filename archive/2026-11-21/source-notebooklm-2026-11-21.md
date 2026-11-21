# Mots de passe en clair, comptes partagés, données gardées dix ans : la sanction CNIL de 5 millions d'euros

## Contexte

Le 18 novembre 2026, la Commission nationale de l'informatique et des libertés (CNIL) a publié un communiqué annonçant une amende de 5 millions d'euros contre une société dont elle ne donne pas le nom. La décision a été prise par la formation restreinte, l'organe de la CNIL chargé de prononcer les sanctions, dans une délibération référencée SAN-2026-016 et datée du 12 novembre 2026. Il s'agit d'un montant élevé pour un dossier où le communiqué ne mentionne aucune fuite de données : la sanction vise des pratiques, pas un incident.

Cette affaire s'inscrit dans une série de décisions récentes de la CNIL en matière de cybersécurité. Le 9 novembre, elle avait annoncé dix sanctions visant des collectivités territoriales, avec des amendes de 3 000 à 20 000 euros. Ici, le registre change : une société, une amende de 5 millions, et un catalogue de défauts qui parlera à tous les techniciens.

## Les textes en jeu

Le règlement général sur la protection des données (RGPD, règlement (UE) 2016/679) pose plusieurs obligations. L'article 32 exige du responsable de traitement et du sous-traitant des mesures techniques et organisationnelles appropriées au risque : il cite notamment la pseudonymisation et le chiffrement, la capacité à garantir la confidentialité des systèmes, et des tests réguliers de l'efficacité des mesures. L'article 5, paragraphe 1, point e, énonce le principe de limitation de la conservation : les données ne doivent pas être gardées sous une forme permettant l'identification des personnes plus longtemps que nécessaire au regard des finalités.

L'article 83 organise les amendes administratives. Les manquements à l'article 32 relèvent du palier le plus bas, jusqu'à 10 millions d'euros ou 2 % du chiffre d'affaires mondial annuel ; les manquements aux principes de base de l'article 5 relèvent du palier supérieur, jusqu'à 20 millions d'euros ou 4 %. Le montant retenu doit tenir compte de critères comme la gravité, la durée, le nombre de personnes concernées et les capacités financières de l'organisme.

## Ce que la CNIL a constaté

Selon le communiqué, la CNIL a été alertée, puis a mené un contrôle. Elle a retenu deux manquements.

Premier manquement, la sécurité (article 32). Les mots de passe d'accès aux espaces clients étaient conservés en clair, c'est-à-dire sans hachage : quiconque accède à la base peut les lire et les réutiliser, y compris sur d'autres services si les clients ont recyclé leur mot de passe. Par ailleurs, des identifiants et mots de passe étaient partagés entre plusieurs salariés pour accéder aux bases de données clients et à l'outil d'accès. La CNIL souligne que seuls des comptes individuels permettent une traçabilité efficace : avec un compte partagé, impossible de dire qui a consulté quoi, donc impossible de détecter ou d'investiguer un usage abusif.

Second manquement, la durée de conservation (article 5-1-e). Un formulaire de contact était conservé plus de dix ans, et les données de connexion étaient gardées au-delà de la durée d'un an que la société s'était elle-même fixée dans sa politique interne. Le point est notable : la société n'a pas respecté sa propre règle.

Le communiqué précise que ces mesures étaient absentes au jour des contrôles et jusqu'à l'engagement de la procédure de sanction. Pendant la procédure, la société a supprimé les mots de passe et l'historique, instauré une purge mensuelle des données clients et renforcé sa sécurité. La CNIL indique que le montant de l'amende tient compte de la gravité des manquements portant sur des principes essentiels de sécurité, du nombre de personnes concernées et des capacités financières de la société.

## Ce qu'on ne sait pas

Il est important de distinguer les faits publiés des suppositions. Le communiqué ne nomme pas la société ni son secteur. Il ne donne ni le nombre de clients concernés, ni la durée pendant laquelle les mots de passe étaient en clair. Il ne mentionne aucune fuite de données. La CNIL a décidé de publier la délibération « à des fins pédagogiques », sans identifier l'organisme. Le texte de la délibération sur Légifrance n'a pas pu être consulté pour ce module : toute précision supplémentaire doit y être vérifiée. Aucune personnalité publique n'est liée à l'affaire, et rien ne permet d'associer une marque à ces faits.

## Pourquoi c'est important

D'abord, la leçon juridique : la CNIL peut sanctionner l'absence de mesures de sécurité élémentaires sans attendre un incident. Le manquement à l'article 32 existe dès lors que les mesures sont inadaptées au risque, qu'il y ait eu compromission ou non. Pour les responsables de traitement, la conformité ne se mesure donc pas à l'absence de fuite mais à la qualité des contrôles en place.

Ensuite, la leçon technique. Hacher les mots de passe avec un algorithme adapté, interdire les comptes partagés, journaliser les accès nominativement, purger les données selon une durée définie et réellement appliquée : voilà des points de contrôle clairs. La CNIL ne prescrit pas ici de technologie précise, mais le standard attendu est lisible.

Enfin, la leçon de gouvernance : une politique de conservation sans mécanisme de purge ne protège pas. L'écart entre la durée annoncée (un an) et la pratique constatée est ce qui transforme un document interne en élément à charge.

## Références

La délibération SAN-2026-016 du 12 novembre 2026 de la formation restreinte de la CNIL ; le communiqué de la CNIL du 18 novembre 2026 ; le RGPD, articles 5, 32 et 83 ; la série de sanctions pour cybersécurité des collectivités annoncée le 9 novembre 2026.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Chacun des cinq angles ci-dessous peut être collé tel quel dans le champ de personnalisation pour orienter le podcast.

**Angle 1 — Check-list d'audit offensif.** Transforme les constats de la CNIL en points de contrôle techniques qu'un pentester ou un auditeur vérifierait : stockage des secrets, comptes partagés, traçabilité, purge. Précise ce qu'un auditeur peut constater sans accès à la base et ce qui exige un accès interne.

**Angle 2 — Architecture d'authentification.** Explique comment un espace client devrait stocker et vérifier les mots de passe, et ce que change le passage d'un modèle en clair à un modèle haché, salé et à compte individuel. Distingue clairement ce que dit la CNIL de ce qui relève des bonnes pratiques générales, sans attribuer à la décision des exigences qu'elle ne mentionne pas.

**Angle 3 — Comparaison avec les sanctions déjà traitées.** Compare cette amende de 5 millions avec les sanctions des collectivités (3 000 à 20 000 euros, procédure simplifiée) et avec d'autres sanctions CNIL pour sécurité insuffisante déjà abordées dans le dépôt. Explique ce qui fait varier le montant : nombre de personnes, gravité, capacités financières, palier de l'article 83.

**Angle 4 — Veille réglementaire automatisée.** Imagine comment automatiser la surveillance des sanctions et délibérations de la CNIL (flux, Légifrance, communiqués) pour extraire les manquements techniques récurrents et alimenter une base de contrôles. Discute les limites : décisions anonymisées, communiqués partiels.

**Angle 5 — Prospective contentieuse et lien avec NIS2.** Discute comment cette logique de sanction sans incident pourrait se combiner avec la transposition de NIS2 en cours (loi Résilience, adoptée en première lecture le 17 novembre, pas encore définitive). Distingue ce qui est acquis de ce qui reste hypothétique.
