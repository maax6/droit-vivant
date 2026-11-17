# NIS2 et loi Résilience : sanctions, notification d'incident et calendrier, le jour du vote solennel

## Contexte

Le 17 novembre 2026, l'Assemblée nationale doit se prononcer par un vote solennel sur le projet de loi relatif à la résilience des infrastructures critiques et au renforcement de la cybersécurité, qui transpose en droit français la directive (UE) 2022/2555, dite NIS2. Cette directive européenne, adoptée fin 2022, devait être transposée avant le 17 octobre 2024. Avec près de deux ans de retard, la France arrive au bout d'un parcours parlementaire heurté : un examen au Sénat en 2025, un retrait de l'ordre du jour début octobre 2026, puis un retour dans l'hémicycle le 9 novembre. Selon la presse, la Commission européenne a saisi la Cour de justice de l'Union européenne début juillet 2026 pour défaut de transposition, la France figurant parmi les États visés ; les articles consultés ne s'accordent pas sur le nombre de pays concernés.

Ce module ne traite pas le chiffrement (article 16 bis, supprimé le 10 novembre) ni le détail des amendements, déjà couverts les 9, 11 et 13 novembre. Il se concentre sur ce que la directive impose concrètement à une organisation : quoi signaler, à quel rythme, et quel risque financier elle encourt.

## Définitions

NIS2 distingue deux catégories d'entités. Les entités essentielles sont celles des secteurs les plus critiques (énergie, transport, santé, infrastructures numériques, administration publique, espace, etc.) au-dessus de certains seuils de taille. Les entités importantes relèvent d'une liste plus large de secteurs (services postaux, gestion des déchets, fabrication de certains produits, fournisseurs numériques, recherche). La distinction compte pour deux raisons : le niveau de supervision (contrôle a priori pour les essentielles, a posteriori pour les importantes) et les plafonds d'amende.

Un incident significatif est un incident qui a causé ou est susceptible de causer une perturbation opérationnelle grave ou des pertes financières pour l'entité, ou qui a affecté ou est susceptible d'affecter d'autres personnes en causant un dommage matériel ou moral considérable. La qualification relève de l'entité, sous le contrôle de l'autorité.

## Le régime de notification (article 23)

La directive organise un signalement en plusieurs étapes. Sans retard injustifié et en tout état de cause dans les 24 heures après avoir eu connaissance de l'incident significatif, l'entité transmet une alerte précoce, qui indique notamment si l'on soupçonne une action illicite ou malveillante et si l'incident pourrait avoir un impact transfrontière. Dans les 72 heures, elle notifie l'incident avec une première évaluation de sa gravité et de son impact et, le cas échéant, des indicateurs de compromission. Un rapport final suit au plus tard un mois après la notification, avec une description détaillée, le type de menace ou la cause profonde probable, les mesures d'atténuation appliquées et, si pertinent, l'impact transfrontière. En cas d'incident encore en cours à l'échéance, un rapport d'avancement est exigé puis le rapport final un mois après le traitement.

Le point technique majeur pour un praticien : l'horloge démarre à la prise de connaissance, pas à la survenue de l'incident. La qualité de la détection, de la journalisation et du processus de qualification interne détermine donc directement la capacité de tenir 24 heures.

## Les sanctions (article 34)

Pour les entités essentielles, les États membres doivent prévoir des amendes administratives d'un maximum d'au moins 10 millions d'euros ou 2 % du chiffre d'affaires annuel mondial total de l'exercice précédent de l'entreprise, le montant le plus élevé étant retenu. Pour les entités importantes, le plafond est d'au moins 7 millions d'euros ou 1,4 %. Ces montants sont des plafonds, pas des tarifs : les autorités doivent apprécier la gravité, la durée, le caractère intentionnel ou négligent, les mesures prises pour atténuer le dommage et la coopération de l'entité. La directive prévoit aussi, outre les amendes, des injonctions, des audits de sécurité et, pour les entités essentielles, la possibilité de suspendre temporairement une certification ou une autorisation et d'interdire temporairement à une personne d'exercer des fonctions dirigeantes. Elle traite enfin de la responsabilité des organes de direction, qui doivent approuver et superviser les mesures de gestion des risques (article 20).

## Ce que dit la presse du texte français

Selon la presse (Journal du Net, ActuIA, AFP via Boursorama), le projet de loi vise de l'ordre de 15 000 à 20 000 entités, les estimations divergeant entre rapporteurs et gouvernement, contre environ 500 soumises aujourd'hui à la supervision de l'ANSSI. Le texte reprendrait les plafonds de 10 millions ou 2 % et de 7 millions ou 1,4 %. L'État et les collectivités seraient exonérés d'amende, mais soumis à des plans de remédiation avec l'ANSSI, et les députés ont prévu des sanctions pour les responsables publics qui n'appliqueraient pas la remédiation. Les injonctions pourraient être assorties de délais de un à douze mois. Aucun délai de mise en conformité n'est inscrit dans la loi, l'objectif étant une conformité de toutes les entités à fin 2028. L'ANSSI pourrait rendre publiques certaines de ses mesures d'exécution. Une déclaration d'incident unique, orientée vers l'ANSSI et la CNIL (et l'AMF et l'ACPR pour la finance), a été adoptée contre l'avis de la ministre, mais son sort dépendra de la commission mixte paritaire.

Ces éléments proviennent de sources secondaires et doivent être recoupés sur le texte adopté, que je n'ai pas consulté. Le résultat du vote du 17 novembre n'était pas disponible au moment de la rédaction : l'AFP indiquait que l'adoption faisait peu de doute, la France insoumise annonçant voter contre.

## Acteurs

La ministre déléguée chargée de l'intelligence artificielle et du numérique, Anne Le Hénanff, porte le texte pour le Gouvernement. Le rapporteur général est le député Éric Bothorel, qui a indiqué vouloir utiliser la commission mixte paritaire pour corriger certaines dispositions. Le directeur général de l'ANSSI, Vincent Strubel, est cité par la presse sur la capacité de l'agence à absorber ce nouveau périmètre. Ces noms sont cités comme parties au débat législatif, sans aucune imputation de faute.

## Enjeux

Trois tensions traversent le dossier. La première est l'écart entre l'ambition de supervision et les moyens : passer de quelques centaines à plus de dix mille entités suppose des effectifs, des référentiels et un calendrier réaliste. La deuxième est l'articulation des guichets : plusieurs autorités (ANSSI, CNIL, régulateurs financiers) reçoivent déjà des notifications selon des régimes différents, et le guichet unique est contesté. La troisième est la proportionnalité : des plafonds calculés sur le chiffre d'affaires mondial concernent surtout les grands groupes, alors que la masse des entités importantes sera des PME, pour lesquelles l'enjeu pratique est le coût de la conformité plus que l'amende théorique.

## Prochaines étapes

Après le vote de l'Assemblée, le texte, qui diffère de la version du Sénat, ira en commission mixte paritaire de sept députés et sept sénateurs. Un texte commun devra ensuite être voté par les deux chambres. Suivront des décrets en Conseil d'État et un référentiel de l'ANSSI. Ce calendrier explique pourquoi toute lecture opérationnelle doit rester prudente : les définitions de périmètre, les délais et le guichet d'incident peuvent encore bouger.

## Références

Directive (UE) 2022/2555, articles 20, 21, 23 et 34, sur EUR-Lex. Dossier législatif DLR5L17N50731 sur assemblee-nationale.fr. Presse : AFP (Boursorama), Journal du Net, ActuIA, consultées comme sources secondaires.

Contenu pédagogique ; ne constitue pas un conseil juridique personnalisé.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez un angle et collez-le tel quel dans le champ de personnalisation.

**Angle 1 — Audit offensif de la chaîne de notification.** Concentre-toi sur la capacité d'une organisation à tenir l'alerte sous 24 h : sources de détection, journalisation, critères de qualification d'un incident significatif. Explique comment un test d'intrusion ou un exercice red team peut mesurer l'horloge de prise de connaissance et les angles morts.

**Angle 2 — Architecture et API concernées.** Décris quels systèmes et flux d'une entité (SIEM, ticketing, canaux vers l'ANSSI et la CNIL) interviennent dans la notification en trois temps. Discute ce qu'un guichet unique changerait côté intégration et automatisation.

**Angle 3 — Comparaison des régimes de sanction.** Compare les plafonds NIS2 (10 M€ ou 2 %, 7 M€ ou 1,4 %) avec les sanctions RGPD déjà étudiées dans cette série et avec les autres modules du dépôt. Souligne les différences d'assiette, de déclencheur et d'autorité.

**Angle 4 — Veille réglementaire automatisée.** Propose comment suivre automatiquement le dossier législatif (scrutins, textes de CMP, décrets, référentiel ANSSI) et alerter quand périmètre, délais ou guichet changent. Insiste sur le recoupement avec les sources officielles.

**Angle 5 — Prospective contentieuse et réglementaire.** Anticipe les scénarios : issue de la CMP, procédure en manquement devant la CJUE, premiers contrôles de l'ANSSI à l'horizon 2028, contestations de la qualification d'entité essentielle. Distingue ce qui est établi de ce qui est spéculatif.
