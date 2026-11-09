# Source NotebookLM — NIS2 et chiffrement : l'Assemblée ouvre le débat sur la loi Résilience (9 novembre 2026)

## Contexte : une directive en retard de deux ans

La directive (UE) 2022/2555, dite NIS2, est le grand texte européen de cybersécurité des entités essentielles et importantes. Entrée en vigueur en janvier 2023, elle devait être transposée par les États membres au plus tard le 17 octobre 2024. La France a présenté son projet de loi « relatif à la résilience des infrastructures critiques et au renforcement de la cybersécurité » en octobre 2024. Le Sénat l'a adopté le 12 mars 2025. À l'Assemblée nationale, une commission spéciale l'a examiné à l'automne 2025, puis le texte a été inscrit en séance, retiré de l'ordre du jour début octobre 2026, avant de revenir : la discussion en séance publique s'ouvre le lundi 9 novembre 2026 à 16 heures et se poursuit toute la semaine selon la presse. Selon les informations de presse, la Commission européenne a franchi toutes les étapes de la procédure en manquement — mise en demeure, avis motivé, puis saisine de la Cour de justice de l'Union européenne en juillet 2026 contre plusieurs États dont la France.

## Ce que la directive impose

NIS2 élargit le périmètre de la première directive de 2016 : davantage de secteurs, et deux catégories d'entités, les « essentielles » et les « importantes ». La presse évoque environ 15 000 entités concernées en France, y compris de grandes collectivités. Ces entités doivent adopter des mesures de gestion des risques de cybersécurité, notifier les incidents significatifs dans des délais courts et répondre de la sécurité de leur chaîne d'approvisionnement. L'article 34 de la directive prévoit des amendes administratives pouvant atteindre 10 millions d'euros ou 2 % du chiffre d'affaires mondial pour les entités essentielles, et 7 millions d'euros ou 1,4 % pour les entités importantes. Pour un chercheur ou un consultant en sécurité offensive, cela signifie que l'audit de sécurité cesse d'être seulement une bonne pratique : il devient un élément de la preuve de diligence réglementaire.

## L'article 16 bis : le chiffrement dans la loi

Le cœur politique du débat n'est pourtant pas NIS2 elle-même, mais un article que le Sénat y a ajouté. L'article 16 bis, issu d'un amendement du sénateur Olivier Cadic, adopté par 181 voix contre 134 (scrutin public n° 227 du 12 mars 2025), interdirait d'imposer aux fournisseurs de services de chiffrement la création de « portes dérobées », c'est-à-dire d'accès cachés permettant de lire des communications chiffrées de bout en bout. Cette disposition est née d'un débat antérieur, lors de l'examen de la loi sur le narcotrafic, où l'obligation faite aux messageries de transmettre le contenu déchiffré de certaines personnes surveillées avait été proposée puis supprimée par les députés. Le Gouvernement s'était opposé à l'article 16 bis au Sénat.

## Le fait nouveau : un engagement politique

Selon la presse du 9 novembre 2026, les positions ont bougé. Un rapport confié au député Florent Boudié, dont la mission a duré plus longtemps que prévu, recommanderait de renoncer aux portes dérobées et de supprimer l'article 16 bis, tout en demandant une « solution technique » d'accès ciblé qui n'affaiblirait pas le chiffrement. La ministre déléguée chargée du numérique, Anne Le Hénanff, a indiqué que l'exécutif soutiendrait la suppression de l'article, qu'elle qualifie de « cavalier législatif », et s'engagerait à ne pas réintroduire de portes dérobées dans les messageries jusqu'à la fin de la session parlementaire. Selon NosParlementaires, six amendements de suppression ont été jugés acceptables en commission le 14 octobre, mais ils ne seront intégrés au texte qu'après un vote en séance ; la presse mentionne aussi 397 amendements déposés pour la séance, dont dix sur l'article 16 bis, y compris une réécriture signée par des députés du Rassemblement national.

## Les nuances juridiques à ne pas perdre

Premièrement, supprimer l'article 16 bis ne revient pas à autoriser les portes dérobées : le droit actuel ne les impose pas. La suppression retire simplement une protection explicite que le Sénat avait voulu graver dans la loi. Deuxièmement, l'engagement du Gouvernement est politique, limité dans le temps — la fin de la session — et il ne lie ni le Parlement, ni les gouvernements futurs. Troisièmement, un « cavalier législatif » est une disposition sans lien suffisant avec l'objet d'un texte ; le Conseil constitutionnel peut la censurer pour ce motif, ce qui explique que cet argument soit mobilisé. Enfin, rien n'est voté : la navette se poursuivra, avec une éventuelle commission mixte paritaire, puis des décrets d'application. Les services de renseignement continuent de réclamer un accès aux messages chiffrés, ce qui laisse la question ouverte sous une autre forme.

## Enjeux pour la cybersécurité

D'un côté, les défenseurs du chiffrement soulignent qu'une porte dérobée réservée aux autorités est techniquement une vulnérabilité exploitable par d'autres : elle affaiblit la sécurité de tous les utilisateurs et, paradoxalement, de ceux que NIS2 prétend protéger. De l'autre, le renseignement et les enquêteurs arguent que le chiffrement de bout en bout aveugle leurs outils face au terrorisme et à la criminalité organisée. Le débat français rejoint les discussions européennes sur le règlement visant à combattre les abus sexuels sur mineurs en ligne, déjà suivies dans ce dépôt, où l'analyse des messages avant chiffrement fait la même ligne de fracture.

## Références

- Directive (UE) 2022/2555 (NIS2), notamment l'article 34 sur les sanctions, et son échéance de transposition du 17 octobre 2024.
- Projet de loi Résilience, textes n° 1112 et 1779, dossier législatif DLR5L17N50731 de l'Assemblée nationale.
- Sénat, scrutin public n° 227 du 12 mars 2025 (amendement Cadic, article 16 bis).
- Presse (sources secondaires) : Clubic, IT for Business, NosParlementaires, 9 novembre 2026.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez un seul angle selon ce que vous voulez entendre ; chacun est rédigé pour être collé tel quel.

**Angle 1 — Audit offensif et preuve de diligence NIS2.** Concentre-toi sur ce que NIS2 change pour un pentester ou un red teamer : obligations de gestion des risques, notification d'incident, sécurité de la chaîne d'approvisionnement, et comment un rapport d'audit devient une pièce de preuve devant le régulateur. Précise ce qui relève du texte européen et ce qui dépendra encore des décrets d'application.

**Angle 2 — Architecture technique du chiffrement de bout en bout.** Explique pourquoi une porte dérobée « ciblée » est techniquement difficile : gestion des clés, accès côté client, escrow, scanning avant chiffrement. Compare ces options à ce que l'article 16 bis visait à interdire et à ce que le rapport Boudié appelle une « solution technique » d'accès ciblé.

**Angle 3 — Comparaison avec les autres dossiers du dépôt.** Mets en parallèle ce débat avec Chat Control (règlement européen sur les abus sexuels sur mineurs en ligne) et avec les sanctions CNIL sur l'obligation de sécurité (article 32 du RGPD) traitées récemment : même tension entre sécurité de tous et accès des autorités, régimes de sanction différents.

**Angle 4 — Veille réglementaire automatisée.** Propose comment suivre automatiquement un texte en navette : flux du dossier législatif de l'Assemblée et du Sénat, scrutins publics, amendements, ordre du jour, et alertes sur la commission mixte paritaire. Liste les sources officielles à interroger et les signaux à surveiller dans les prochains jours.

**Angle 5 — Prospective contentieuse et institutionnelle.** Analyse les scénarios après le vote : suppression ou maintien de l'article 16 bis, commission mixte paritaire, saisine éventuelle du Conseil constitutionnel (notamment pour cavalier législatif), et suite de la procédure de la Commission européenne devant la CJUE. Distingue clairement ce qui est acquis de ce qui reste hypothétique.
