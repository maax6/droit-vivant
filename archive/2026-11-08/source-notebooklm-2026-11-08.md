# Sécurité des logiciels d'éditeurs et RGPD : la sanction de 1,7 M€ contre NEXPUBLICA FRANCE

*Document pédagogique pour NotebookLM. Droit Vivant, 8 novembre 2026. Il ne constitue pas un conseil juridique personnalisé.*

## Pourquoi ce sujet aujourd'hui

Les dossiers chauds du moment, la transposition de la directive NIS2 devant l'Assemblée nationale et les négociations européennes sur le règlement CSAR (« Chat Control »), ont déjà été traités dans ce dépôt, le 7 novembre et le 27 octobre. Aucun développement nouveau et confirmé n'a été trouvé depuis : l'examen de NIS2 est annoncé pour le lundi 9 novembre, et aucune date officielle n'a été vérifiée pour un éventuel septième trilogue sur le CSAR. Ce module change donc d'angle et revient sur une sanction de la CNIL qui illustre très concrètement ce que les textes de cybersécurité exigent : celle prononcée contre NEXPUBLICA FRANCE.

## Le cadre juridique

Le règlement général sur la protection des données (RGPD, règlement (UE) 2016/679) pose, à l'article 5, paragraphe 1, point f), un principe d'intégrité et de confidentialité : les données doivent être traitées de façon à garantir une sécurité appropriée, y compris la protection contre l'accès non autorisé. L'article 32 le décline en obligation opérationnelle : le responsable du traitement et le sous-traitant doivent mettre en œuvre des mesures techniques et organisationnelles appropriées au regard de l'état des connaissances, des coûts, de la nature des données et des risques pour les personnes.

En France, la CNIL contrôle et sanctionne. La loi du 6 janvier 1978, dans ses articles 20 et suivants, organise la procédure : un contrôle, un rapport, puis une séance de la formation restreinte, qui peut prononcer une amende administrative. Les décisions sont publiées, notamment sur Légifrance. La délibération commentée ici vise aussi la décision du Conseil constitutionnel n° 2025-1154 QPC du 8 août 2025 parmi ses références.

## L'affaire

NEXPUBLICA FRANCE, anciennement INETUM SOFTWARE FRANCE, édite et héberge un logiciel de gestion de la relation avec les usagers, appelé PCRM. Ce logiciel est utilisé par des collectivités et organismes, notamment des maisons départementales des personnes handicapées (MDPH). Fin novembre 2022, des clients ont signalé à la CNIL des violations de données : des usagers accédaient à des documents qui concernaient d'autres personnes.

La CNIL a procédé à un contrôle sur place. Un rapport a été notifié le 16 juin 2025 et la formation restreinte a siégé le 27 novembre 2025. Par la délibération SAN-2025-015 du 22 décembre 2025, publiée le 24 décembre 2025, elle a prononcé une amende de 1 700 000 euros. La page de la CNIL retient un manquement à l'article 32 du RGPD ; le texte intégral cite aussi l'article 5, paragraphe 1, point f).

Selon la CNIL, les mesures de sécurité étaient insuffisantes. Des vulnérabilités connues, notamment grâce à des audits, n'ont été corrigées qu'après les incidents. La formation restreinte relève un défaut de connaissance de l'état de l'art et des principes de base de la sécurité, et considère que le fait d'exercer une activité spécialisée de conseil informatique aggrave le manquement. Pour fixer le montant, elle prend en compte la capacité financière de la société, le nombre de personnes concernées et la sensibilité des données, liée au handicap. Elle n'a pas prononcé d'injonction, car les mesures correctives avaient déjà été prises.

## Ce que la décision enseigne

Premièrement, l'obligation de sécurité n'est pas réservée à l'administration cliente. Un éditeur qui conçoit et héberge le logiciel porte une responsabilité propre, parce qu'il détermine l'architecture, les contrôles d'accès et le rythme des correctifs. Le fait que le client soit un service public ne dilue pas cette responsabilité.

Deuxièmement, savoir et ne pas corriger est aggravant. Quand des audits ont identifié des faiblesses, l'argument selon lequel les failles étaient théoriques tient mal : la CNIL constate que les corrections sont venues après les incidents.

Troisièmement, la sensibilité des données pèse sur le montant. Des documents liés au handicap relèvent de données dont la divulgation peut avoir des conséquences lourdes pour les personnes. Plus le risque pour les personnes est élevé, plus le niveau de sécurité attendu l'est aussi.

Quatrièmement, la correction tardive ne supprime pas la sanction : elle explique ici l'absence d'injonction, mais l'amende a été prononcée.

## Lien avec les autres régimes

Cette décision éclaire le débat sur NIS2. La directive vise à imposer aux entités essentielles et importantes des mesures de gestion des risques, de notification d'incidents et de contrôle par l'autorité nationale, ici l'ANSSI. Le RGPD, lui, protège les données personnelles et se déclenche dès qu'un traitement est insuffisamment sécurisé, quel que soit le secteur. Un même incident peut ainsi relever de plusieurs régimes. Cette sanction rappelle aussi que le droit français et européen sanctionne déjà l'insuffisance de sécurité, indépendamment de l'adoption de la loi de transposition de NIS2.

## Limites de cette analyse

Le contenu repose sur la page de la CNIL et sur la délibération publiée sur Légifrance, dont seule une partie du texte intégral a été relue. La sanction peut être contestée devant le Conseil d'État. Le lecteur doit consulter le texte complet avant toute utilisation professionnelle.

## Références

- CNIL, « Data security: NEXPUBLICA FRANCE fined €1,700,000 », 24 décembre 2025 : https://www.cnil.fr/en/data-security-nexpublica-france-fined-eur1700000
- Légifrance, délibération SAN-2025-015 du 22 décembre 2025 : https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000053151799
- Règlement (UE) 2016/679 : https://eur-lex.europa.eu/eli/reg/2016/679/oj

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez l'un des cinq angles ci-dessous et collez-le tel quel dans le champ de personnalisation.

**Angle 1 — Audit offensif de la chaîne logicielle.** Concentre-toi sur ce que la décision implique pour un test d'intrusion visant un logiciel de gestion d'usagers : cloisonnement entre comptes, contrôle d'accès aux documents, et ce qu'un auditeur doit documenter pour prouver que des failles connues ont été traitées à temps.

**Angle 2 — Responsabilité éditeur contre client.** Explique comment répartir la responsabilité entre l'éditeur-hébergeur et l'administration cliente, et quelles clauses contractuelles et preuves de sécurité un client public devrait exiger de ses fournisseurs.

**Angle 3 — Comparaison avec les autres sanctions du dépôt.** Compare ce cas avec les autres sanctions de la CNIL et décisions sur la sécurité traitées dans le dépôt, en mettant en regard les critères de fixation du montant : sensibilité des données, capacité financière, nombre de personnes.

**Angle 4 — Veille réglementaire automatisée.** Propose comment automatiser la veille sur les délibérations de la formation restreinte, via les flux Légifrance et CNIL, pour détecter les manquements à l'article 32, extraire montants et visas, et alimenter une base de jurisprudence consultable.

**Angle 5 — Prospective NIS2 et RGPD.** Examine comment la future transposition de NIS2 se combinera avec l'article 32 du RGPD pour un éditeur de logiciels destinés au secteur public, et quels risques de cumul de sanctions ou de contrôles ANSSI et CNIL en découleront.
