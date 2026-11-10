# Source NotebookLM — Cybersécurité des collectivités : la CNIL prononce dix sanctions (10 novembre 2026)

## Contexte : pourquoi les collectivités sont une cible

Une commune, un département ou un établissement public traite des données très diverses : état civil, inscriptions à la cantine et à l'école, paiements des familles, aides sociales, images de vidéosurveillance. Ces organismes ont souvent des budgets informatiques limités et dépendent de prestataires, notamment d'éditeurs de logiciels métier. Ils sont donc exposés aux rançongiciels et aux fuites de données, avec un impact direct sur les habitants. La Commission nationale de l'informatique et des libertés (CNIL) a fait de la cybersécurité des collectivités un thème prioritaire de ses contrôles de 2025. Le 9 novembre 2026, elle en a publié le résultat : dix sanctions financières visant des collectivités territoriales et un établissement public, prononcées en novembre 2026 selon la procédure simplifiée.

## Le cadre juridique

Le règlement général sur la protection des données (RGPD, règlement (UE) 2016/679) s'applique à toute personne publique responsable d'un traitement. Deux articles sont au coeur de cette série de sanctions. L'article 32 impose au responsable de traitement et au sous-traitant de mettre en oeuvre des mesures techniques et organisationnelles appropriées au risque : on parle d'une obligation de moyens, appréciée selon l'état de l'art, les coûts, la nature des données et les risques pour les personnes. L'article 35 impose, avant la mise en oeuvre d'un traitement susceptible d'engendrer un risque élevé pour les droits et libertés, une analyse d'impact relative à la protection des données (AIPD). La CNIL cite aussi l'article 90 de la loi Informatique et Libertés, qui prévoit l'analyse d'impact pour certains traitements relevant du régime de la sécurité et de la justice pénale, ce qui correspond au cas qu'elle mentionne de la vidéosurveillance de la voie publique. À cela s'ajoute le droit propre à l'administration : l'ordonnance n° 2005-1516 du 8 décembre 2005 et le référentiel général de sécurité (RGS) exigent l'homologation de sécurité d'un système d'information avant sa mise en service.

La procédure de sanction simplifiée est une voie accélérée réservée aux dossiers peu complexes. Elle est confiée à un membre unique de la formation restreinte et l'amende y est plafonnée à 20 000 euros. Ce plafond explique la fourchette annoncée : de 3 000 à 20 000 euros, soit, d'après la CNIL, le maximum légal de cette procédure pour les cas les plus sérieux.

## Ce que la CNIL a constaté

La CNIL a détaillé les manquements, ce qui en fait presque une liste de contrôle d'audit. Sur l'article 32, elle relève d'abord des accès distants insuffisamment authentifiés, notamment pour les utilisateurs à privilèges : des administrateurs ne disposaient pas d'authentification multifacteur. Elle relève ensuite la gestion des prestataires : certains, comme des éditeurs de logiciels, avaient un accès permanent au réseau sans autorisation au cas par cas, ou utilisaient des comptes partagés entre plusieurs employés, ce qui détruit l'imputabilité des actions. Elle constate une détection d'anomalies inefficace, avec une journalisation incomplète ou des journaux non examinés en temps réel ou à bref délai. Elle pointe une segmentation réseau insuffisante, qui permet à un attaquant de se déplacer latéralement. Elle signale des systèmes d'exploitation de serveurs obsolètes, qui ne reçoivent plus de correctifs de sécurité de l'éditeur, ainsi que des mots de passe faibles, transmis en clair aux utilisateurs ou stockés sans garantie de confidentialité. Enfin, certains systèmes n'avaient pas été homologués avant leur mise en service. La CNIL ajoute que certaines collectivités contrôlées avaient subi une ou plusieurs violations de données que des mesures appropriées auraient pu éviter.

Sur l'article 35, plusieurs collectivités n'avaient pas réalisé d'analyse d'impact avant de déployer des traitements à risque élevé. La CNIL cite des services en ligne pour les parents, destinés à gérer les activités scolaires et périscolaires, qui concernent des enfants, personnes vulnérables, et des données bancaires, ainsi que la vidéosurveillance de la voie publique.

## Le calcul de l'amende

La CNIL indique que les montants tiennent compte du nombre et de la gravité des manquements, des catégories de données concernées (mineurs, coordonnées bancaires), du budget de chaque collectivité, du nombre de personnes touchées et des mesures correctives prises. Elle ne publie pas, dans son annonce, le détail par organisme : les noms et les montants individuels ne figurent pas dans le texte que nous avons pu consulter, et nous n'avons pas pu confirmer les numéros de délibération. Il faut donc se garder de toute attribution à une commune précise.

## Enjeux pour un chercheur en cybersécurité

Premier enjeu : la CNIL traduit l'article 32, volontairement abstrait, en défauts techniques vérifiables. Cela permet de relier chaque constat à un test d'audit : revue des accès distants, présence de MFA sur les comptes d'administration, inventaire des comptes de prestataires, qualité de la collecte de journaux, cloisonnement du réseau, cycle de vie des systèmes, politique de mots de passe. Deuxième enjeu : l'angle de la chaîne d'approvisionnement. Les contrôles ont aussi porté sur les prestataires des collectivités ; les accès permanents des éditeurs sont un vecteur d'attaque classique et un point de responsabilité partagé. Un précédent récent du dépôt, la sanction contre l'éditeur NEXPUBLICA, montre que l'obligation de sécurité pèse aussi directement sur l'éditeur. Troisième enjeu : l'articulation avec NIS2. Le projet de loi Résilience, qui transpose la directive (UE) 2022/2555, est en discussion à l'Assemblée nationale, mais le RGPD s'applique déjà : une collectivité n'a pas à attendre cette loi pour être sanctionnée sur la sécurité de ses données personnelles. Quatrième enjeu : la procédure simplifiée montre que la CNIL peut traiter vite et en nombre ; ces dix décisions annoncent une pression de contrôle continue sur le secteur public local.

## Limites et prudence

Ce module repose sur l'annonce officielle de la CNIL du 9 novembre 2026 et sur un article de presse secondaire du 10 novembre 2026. Il ne nomme aucun organisme sanctionné, puisque l'annonce n'en désigne pas. Les sanctions peuvent faire l'objet de recours. Ce contenu est pédagogique et ne constitue pas un conseil juridique.

## Références

Règlement (UE) 2016/679, articles 32 et 35 ; loi n° 78-17 du 6 janvier 1978, article 90 ; ordonnance n° 2005-1516 du 8 décembre 2005 ; annonce de la CNIL du 9 novembre 2026 « Cybersécurité des collectivités territoriales : la CNIL prononce dix sanctions ».

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez l'un des cinq angles suivants selon ce que vous voulez approfondir.

**Angle 1 — Audit offensif et points de contrôle.** Transforme la liste des manquements de l'article 32 en checklist de test d'intrusion et d'audit : accès distants, MFA des administrateurs, comptes partagés, journalisation, segmentation, systèmes obsolètes, mots de passe. Pour chaque point, précise comment un attaquant l'exploiterait et comment un auditeur le vérifierait.

**Angle 2 — Architecture et prestataires.** Concentre-toi sur l'architecture type d'une collectivité : accès distants, VPN, comptes d'éditeurs, services en ligne pour les familles. Explique où se situent les risques de chaîne d'approvisionnement et quels contrôles techniques (accès à la demande, bastion, comptes nominatifs) répondraient aux critiques de la CNIL.

**Angle 3 — Comparaison avec d'autres sanctions du dépôt.** Compare ces sanctions simplifiées plafonnées à 20 000 euros avec la sanction de 1,7 million d'euros contre l'éditeur NEXPUBLICA et avec les sanctions plus lourdes déjà traitées. Discute de ce qui fait varier le montant et de la répartition de responsabilité entre administration cliente et éditeur.

**Angle 4 — Veille réglementaire automatisée.** Imagine comment un consultant en automatisation pourrait suivre les annonces et délibérations de la CNIL (flux, Légifrance), extraire articles visés, montants et défauts techniques, et alimenter une base de constats par secteur pour anticiper les contrôles.

**Angle 5 — Prospective : RGPD, NIS2 et contrôle du secteur public.** Discute de l'articulation entre ces sanctions RGPD et le futur régime NIS2 en France : quelles collectivités entreront dans le périmètre, quels contrôles de l'ANSSI s'ajouteront à ceux de la CNIL, et quelle pression contentieuse attendre dans les prochains mois.
