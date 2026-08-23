# Quand l'État doit écrire à ses agents, et peut-être à des parents d'élèves : l'article 34 du RGPD à l'épreuve d'une intrusion à l'Éducation nationale

## Un compte, une nuit, vingt-cinq ans de données

Certains incidents tiennent en une phrase, et toutes leurs conséquences juridiques en découlent. Celle-ci figure dans le communiqué du ministère de l'Éducation nationale du 31 juillet 2026 : l'accès frauduleux a été réalisé dans la nuit du 25 juillet 2026, « à la suite de l'usurpation d'un compte professionnel », et a visé « le système d'information dédié à la formation des personnels ». Pas de faille exotique : un compte légitime, utilisé par quelqu'un qui n'aurait pas dû l'utiliser, sur une application que peu rangeraient spontanément parmi les joyaux de la couronne d'un ministère.

Le centre opérationnel de sécurité du ministère est alerté dès le 26 juillet ; l'accès externe est suspendu, une cellule de crise activée. Le périmètre annoncé frappe par sa profondeur temporelle : les données susceptibles d'avoir été exfiltrées concernent les agents ayant exercé en académie **depuis 2001** — identité, statut et fonctions, auxquels s'ajoutent, pour une partie d'entre eux, coordonnées, adresse postale, numéro de téléphone et **numéro de sécurité sociale**. Le ministère précise que ce système ne contient ni données bancaires, ni mots de passe, ni données d'élèves. Plainte est déposée ; l'ANSSI et la CNIL sont saisies.

Le 18 août 2026, un second communiqué actualise le dossier, et c'est lui qui fait l'actualité. La plainte a été déposée **contre X auprès du parquet de Paris** et une enquête judiciaire est en cours. Surtout, deux informations de nature différente : une exécution — « l'ensemble des personnels susceptibles d'être concernés ont été informés individuellement » — et une incertitude — « des publications intervenues hier font état de la mise en ligne de ces données et revendiquent la détention de données relatives à des élèves ». Le ministère poursuit ses expertises et pose par avance sa règle : si d'autres personnes sont concernées, elles seront informées individuellement, et « s'il devait s'agir d'élèves, leurs représentants légaux le seraient également ».

Précaution nécessaire : à ce stade, **aucune autorité n'a jugé** que le ministère aurait manqué à ses obligations de sécurité. Les revendications d'un attaquant ne démontrent pas un périmètre ; l'appréciation appartient à la CNIL, puis le cas échéant au juge.

## Deux obligations que l'on confond toujours

Le langage courant parle de « déclarer la fuite ». Le RGPD connaît deux obligations distinctes, avec deux destinataires et deux seuils.

L'**article 33** organise la notification à l'**autorité de contrôle** : « dans les meilleurs délais et, si possible, 72 heures au plus tard », sauf si la violation est *peu susceptible* d'engendrer un risque. Le seuil est bas — un simple risque suffit. Son paragraphe 5 ajoute une obligation souvent négligée : documenter **toute** violation, y compris non notifiée. L'absence de notification doit donc elle-même être justifiée par écrit.

L'**article 34** organise la communication à la **personne concernée**. Le seuil est plus élevé — un **risque élevé** — mais l'obligation est plus lourde : communication dans les meilleurs délais, en **termes clairs et simples**, avec nature de la violation, point de contact, conséquences probables et mesures prises. Trois exceptions seulement (§ 3) : données rendues incompréhensibles, par exemple par chiffrement approprié ; mesures ultérieures écartant le risque élevé ; efforts disproportionnés, la communication individuelle étant alors remplacée par une **communication publique** d'efficacité équivalente — une modalité de substitution, jamais une dispense. Et le § 4 referme le dispositif : à défaut, l'autorité peut **exiger** la communication. Les lignes directrices 9/2022 du CEPD, version 2.0, en fournissent la méthode d'appréciation du risque.

## Pourquoi l'immunité d'amende de l'État ne change rien

Une objection revient dès qu'un incident touche une administration : la CNIL ne pouvant infliger d'amende à l'État, rien ne se passerait. L'objection est mal calibrée. L'article 83, § 7, du RGPD ouvre aux États membres une option, que la France a exercée à l'article 20, III, de la loi n° 78-17 du 6 janvier 1978 — point documenté dans le module du 18 août 2026 à propos de la DGFiP. Mais cette option porte sur les **amendes** seules. Elle ne touche ni les obligations de fond, ni les autres mesures correctrices : mise en demeure, injonction, limitation du traitement — ni, spécifiquement, le pouvoir d'exiger la communication au titre de l'article 34, § 4. Une administration qui ne peut être condamnée à payer peut parfaitement être contrainte d'écrire. Elle peut aussi se voir opposer une demande de **réparation** fondée sur l'article 82, examinée dans le module du 22 août 2026.

## Le cas des mineurs

Si les expertises confirment la présence de données d'élèves, une couche d'exigences s'ajoute. L'**article 12, § 1**, du RGPD impose une information « en des termes clairs et simples, en particulier pour toute information destinée spécifiquement à un enfant ». En droit français, l'**article 45 de la loi n° 78-17** précise que, pour le mineur de moins de quinze ans, le responsable rédige les informations « en des termes clairs et simples, aisément compréhensibles par le mineur ». Informer les représentants légaux est cohérent avec l'exercice des droits d'un enfant, mais ne dispense pas de cette exigence de lisibilité : un courrier juridiquement irréprochable et incompréhensible pour son destinataire ne remplit pas l'obligation. C'est l'un des rares endroits où le droit des données impose littéralement une contrainte de rédaction.

## Prévenir d'un phishing sans ressembler à un phishing

Le risque créé n'est ici ni bancaire, ni celui d'un mot de passe compromis : c'est l'**hameçonnage crédible** et l'**usurpation d'identité**. Un message citant votre académie, votre statut exact, votre adresse et votre numéro de sécurité sociale ne déclenche aucun signal d'alerte habituel — le ministère rappelle d'ailleurs qu'il ne demande jamais identifiants, mots de passe ou coordonnées bancaires par courriel ou téléphone.

D'où un paradoxe familier des responsables de la sécurité : le courriel qui prévient d'un risque de phishing ressemble par construction à un phishing. Il arrive sans être attendu, évoque un incident, demande de la vigilance, renvoie vers une procédure. Les bonnes pratiques en découlent : un message **dédié**, jamais noyé dans une lettre d'information ; des conseils **concrets et actionnables** ; un canal **vérifiable indépendamment**, en passant par son autorité académique plutôt qu'en cliquant. Le NIR mérite une mention à part : contrairement à une carte bancaire, il n'est pas révocable. Une fois exposé, il l'est durablement.

## Ce que l'affaire donne à auditer

Le récit officiel se lit comme une liste de points de contrôle. L'**authentification des comptes d'agents** sur les applications périphériques d'abord : un système de formation est rarement au centre d'un exercice de sécurité, il est pourtant une porte d'entrée nominative vers un annuaire de personnes. La **détection des extractions anormales** ensuite : un compte usurpé reste parfaitement légitime pour un contrôle d'accès — bons identifiants, bons droits — et ne devient suspect que pour un moteur de comportement, sur la volumétrie, les horaires ou la pagination systématique. C'est la différence entre autoriser et surveiller. Puis la capacité à **reconstituer le périmètre exact** des enregistrements consultés : question technique en apparence, condition d'exécution de l'article 34 en réalité, car tant qu'on ignore ce qui a été lu, on ne sait pas qui prévenir et l'on élargit la communication par précaution — ce qui dilue le message et alimente la fraude qu'on veut prévenir. Enfin les **durées de conservation** : des données remontant à 2001 dans un système de formation interrogent l'article 5, § 1, e). Chaque année conservée sans nécessité est un multiplicateur du volume exfiltré le jour de l'incident. Et le registre des violations de l'article 33, § 5, reste le premier document qu'une autorité demande à voir.

## Références

- Ministère de l'Éducation nationale, communiqués des 31 juillet et 18 août 2026.
- Règlement (UE) 2016/679 (RGPD), articles 4, 12), 5, 12, 32, 33, 34 et 83, § 7.
- Loi n° 78-17 du 6 janvier 1978, articles 20, III, et 45.
- Code pénal, article 226-17 (défaut de mesures de sécurité : 5 ans et 300 000 €).
- CEPD, lignes directrices 9/2022 sur la notification de violations de données, version 2.0.
- CNIL, « Violations de données personnelles : les règles à suivre ».

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Cinq entrées possibles dans le même dossier. Choisir un seul angle et le coller tel quel dans le champ de personnalisation.

**Angle 1 — Audit offensif d'une application périphérique.** Concentre-toi sur le vecteur décrit par le ministère : l'usurpation d'un compte professionnel sur un système de formation. Déroule les points de contrôle qu'un auditeur examinerait — authentification multifacteur sur les applications non critiques, résistance au bourrage d'identifiants et au phishing d'agents, cloisonnement entre annuaire ministériel et applications satellites, limitation de débit et pagination des interfaces d'export. Explique pourquoi les applications jugées secondaires concentrent souvent le plus grand nombre d'identités.

**Angle 2 — Journalisation et exécution concrète de l'article 34.** Traite la question « qui devons-nous prévenir ? » comme un problème d'ingénierie. Détaille ce qu'un système doit journaliser pour reconstituer le périmètre des enregistrements consultés par un compte légitime détourné, la différence entre journal d'authentification et journal d'accès aux données, la protection en intégrité de ces journaux, et les conséquences d'une journalisation insuffisante sur la portée de la communication imposée par le RGPD.

**Angle 3 — Comparaison avec les autres dossiers du dépôt.** Mets ce module en perspective avec ceux du 18 août 2026 (violation à la DGFiP, pouvoirs de la CNIL et immunité d'amende de l'État) et du 22 août 2026 (réparation au titre de l'article 82 et charge de la preuve, arrêt CJUE C-340/21). Explique comment trois régimes distincts — obligation d'informer, mesures correctrices, réparation civile — s'appliquent au même incident, et pourquoi l'absence d'amende possible contre l'État n'en neutralise aucun des deux autres.

**Angle 4 — Veille réglementaire automatisée sur les violations publiques.** Imagine le pipeline qu'un consultant en automatisation construirait pour suivre les incidents affectant des administrations françaises : sources officielles à surveiller (communiqués ministériels, actualités CNIL, bulletins ANSSI, JORF), extraction structurée des éléments juridiquement pertinents (date de découverte, catégories de données, information individuelle effectuée, saisine de l'autorité), et détection automatique des écarts entre le récit public et les exigences des articles 33 et 34.

**Angle 5 — Prospective : IA générative et industrialisation de la fraude consécutive.** Projette le raisonnement sur les mois à venir. Discute de l'effet des modèles génératifs sur la crédibilité des campagnes d'hameçonnage nourries par des fuites nominatives détaillées, des conséquences pour la rédaction des communications de l'article 34 — comment prévenir sans fournir un modèle de message que les fraudeurs imiteront — et de l'hypothèse d'une doctrine plus exigeante des autorités sur les canaux d'information vérifiables.
