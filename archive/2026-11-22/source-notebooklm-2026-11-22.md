# Health Data Hub, Microsoft et le risque américain : ce que dit le Conseil d'État (décision du 20 mars 2026)

## Contexte

Les données de santé comptent parmi les données personnelles les plus sensibles. Le règlement général sur la protection des données (RGPD, règlement (UE) 2016/679) les range dans des catégories particulières et impose au responsable de traitement, comme à son sous-traitant, des garanties renforcées. En France, le Système national des données de santé (SNDS) rassemble des données issues de l'assurance maladie et des hôpitaux. La Plateforme des données de santé, souvent appelée Health Data Hub, est un groupement d'intérêt public chargé de faciliter l'accès à ces données pour la recherche et l'intérêt général. Sa plateforme technique est hébergée chez Microsoft, ce qui nourrit depuis des années un débat de souveraineté : un fournisseur établi dans l'Union peut-il, lorsqu'il appartient à un groupe américain, être contraint de répondre à une demande d'accès émanant d'autorités des États-Unis ?

Ce module ne porte pas sur une actualité de la semaine. Il revient sur une décision du Conseil d'État du 20 mars 2026, car elle fixe une grille de lecture utile pour qui audite des architectures cloud traitant des données sensibles. Précisons d'emblée ses limites : elle concerne une autorisation précise, pour un projet précis, et ne vaut pas validation générale.

## L'affaire

Le 13 février 2025, la CNIL a adopté la délibération n° 2025-014. Elle autorise l'Agence européenne des médicaments (EMA), dans le cadre du projet DARWIN EU, à mettre en œuvre un traitement automatisé de données personnelles pour réaliser des études d'incidence et de prévalence sur la population générale française. L'autorisation vaut trois ans. Le traitement suppose une extraction depuis le SNDS par la Plateforme des données de santé, qui agit comme sous-traitant de l'EMA. L'hébergement est assuré par Microsoft Ireland Operations Ltd, filiale irlandaise d'un groupe établi aux États-Unis, dans des centres de données situés en France.

Deux requêtes ont été jointes, enregistrées sous les numéros 503159 et 504171. La première émane notamment de l'association Les Licornes célestes, avec l'intervention de plusieurs sociétés du numérique (dont Clever Cloud) et du Conseil national du logiciel libre. La seconde est portée par les associations Interhop et Constances, le Syndicat de la médecine générale, la Fédération Sud Santé Sociaux et la Ligue des droits de l'homme. La CNIL est défenderesse. La décision a été rendue le 20 mars 2026 par la 10ème chambre de la section du contentieux, après une séance du 5 février 2026.

## Ce que juge le Conseil d'État

Le raisonnement se déroule en plusieurs temps.

Premier temps : la portée de l'autorisation. Le Conseil d'État relève que la délibération a pour seul objet d'autoriser un traitement de données de santé hébergées en France et qu'elle ne saurait avoir pour effet d'autoriser un transfert de données de santé vers les États-Unis. Dès lors, les requérants ne peuvent utilement contester la validité de la décision d'adéquation du 10 juillet 2023 (décision d'exécution (UE) 2023/1795, relative au cadre de protection des données UE–États-Unis) : cette décision n'est pas le fondement de l'autorisation attaquée. De même, l'article R. 1461-1 du code de la santé publique, qui interdit certains transferts de données de santé hors de l'Union, ne peut être invoqué utilement contre une autorisation qui n'en permet aucun.

Deuxième temps : les transferts de données d'usage technique. Des données de connexion des utilisateurs de la plateforme peuvent être accessibles à des administrateurs de Microsoft situés aux États-Unis. Le Conseil d'État relève que ces transferts reposent sur des clauses contractuelles types, qui constituent des garanties appropriées au sens de l'article 46 du RGPD, et qu'ils ne concernent ni les personnes dont les données sont étudiées ni des données de santé.

Troisième temps : le risque d'accès par les autorités américaines. Le Conseil d'État reconnaît qu'il ne peut être totalement exclu que les données fassent l'objet de demandes d'accès de ces autorités par l'intermédiaire de la société mère de l'hébergeur. Mais il retient que des mesures de sécurité encadrent les données : pseudonymisation sous le contrôle de la CNAM et de la Plateforme des données de santé, conservation limitée des données brutes extraites, analyse du risque de réidentification à chaque export, analyse des traces d'usage. La durée limitée de trois ans est également prise en compte. Il en déduit que la CNIL n'a pas commis d'erreur d'appréciation au regard des articles 28 et 32 du RGPD, relatifs au sous-traitant et à la sécurité du traitement.

Quatrième temps : l'hébergement. L'article L. 1111-8 du code de la santé publique exige une certification d'hébergeur de données de santé. Le Conseil d'État relève que Microsoft Ireland en dispose, avec un audit régulier par un organisme accrédité, mais ne peut pas obtenir la qualification SecNumCloud, du fait de son appartenance à un groupe soumis au droit américain.

Cinquième temps : la loi SREN. Les requérants invoquaient l'article 31 de la loi du 21 mai 2024, qui prévoit des exigences de protection contre les accès extraterritoriaux pour l'hébergement de données sensibles. Faute de décret en Conseil d'État pris à la date de la délibération, ces dispositions ne pouvaient pas être invoquées contre elle.

Enfin, le Conseil d'État décline de saisir la Cour de justice de l'Union européenne d'une question préjudicielle sur l'article 28 § 3 du RGPD, faute de doute raisonnable sur l'interprétation. Les requêtes sont rejetées, y compris les demandes de frais de justice.

## Définitions utiles

La pseudonymisation remplace les identifiants directs par un pseudonyme, mais les données restent personnelles tant qu'une réidentification est possible. Le transfert au sens du chapitre V du RGPD (articles 44 à 46) désigne la communication ou la mise à disposition de données vers un pays tiers ; l'article 45 permet une décision d'adéquation, l'article 46 des garanties appropriées comme les clauses contractuelles types. SecNumCloud est une qualification de l'ANSSI qui impose notamment une protection contre les lois extra-européennes. Une question préjudicielle est une saisine de la CJUE par une juridiction nationale.

## Enjeux

La décision montre que le juge administratif français raisonne en termes de proportionnalité des garanties plutôt que de risque nul. Il admet que le risque d'accès étranger subsiste et le traite comme un risque résiduel évalué au regard du dispositif concret. Pour un auditeur, le message est de documenter la localisation, le périmètre des flux (y compris les données d'usage et de télémétrie), les mesures de pseudonymisation, la gouvernance des clés, la durée de conservation et la traçabilité. Les requérants, de leur côté, ont obtenu que le débat soit tranché au fond, sans que la question de la souveraineté du cloud ne soit éteinte : la loi SREN prévoit un régime dont l'effet dépend de textes d'application.

Une mise en garde de méthode : la source de cette synthèse est le texte de la décision et le communiqué du Conseil d'État. Aucune décision plus récente sur ce dossier n'a été vérifiée pour ce module.

## Références

Conseil d'État, 20 mars 2026, n° 503159 et 504171 ; CNIL, délibération n° 2025-014 du 13 février 2025 ; RGPD, articles 28, 32, 44 à 46 ; décision d'exécution (UE) 2023/1795 ; code de la santé publique, articles L. 1111-8 et R. 1461-1 ; loi n° 2024-449 du 21 mai 2024, article 31.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisis l'angle qui correspond à ce que tu veux travailler, puis colle-le tel quel.

**Angle 1 — Audit offensif de l'hébergement.** Concentre-toi sur les points de contrôle techniques qu'un auditeur vérifierait : localisation réelle des données, flux de télémétrie vers les administrateurs du fournisseur, gestion des clés de chiffrement, journaux d'accès. Distingue ce que la décision juge suffisant de ce qu'un test d'intrusion chercherait à contourner.

**Angle 2 — Architecture et flux de données.** Reconstitue l'architecture décrite : SNDS, Plateforme des données de santé, EMA, hébergeur. Explique à quel endroit passent les données de santé, les données pseudonymisées et les données d'usage, et pourquoi le juge traite ces flux différemment.

**Angle 3 — Comparaison avec les autres régimes déjà traités.** Compare la logique du juge ici (risque résiduel, garanties proportionnées) avec les décisions de sanction CNIL sur la sécurité des données (article 32) et avec le régime de sanctions de NIS2 abordé dans les modules précédents. Montre où les raisonnements convergent et divergent.

**Angle 4 — Veille réglementaire automatisée.** Propose des signaux à surveiller automatiquement : décret d'application de l'article 31 de la loi SREN, évolutions du cadre de protection des données UE–États-Unis, nouvelles qualifications SecNumCloud, délibérations CNIL. Explique comment structurer ces sources dans un flux de veille.

**Angle 5 — Prospective contentieuse.** Imagine les évolutions possibles du contentieux : un recours visant la décision d'adéquation devant le juge de l'Union, l'effet futur du décret SREN, d'autres autorisations CNIL similaires. Indique clairement ce qui relève de l'hypothèse et non de la décision.
