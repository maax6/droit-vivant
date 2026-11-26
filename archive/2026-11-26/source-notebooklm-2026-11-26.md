# Source NotebookLM — Les 38 sanctions simplifiées de la CNIL (annonce du 17 novembre 2026)

## Contexte : une sanction « légère » mais un signal fort

Le 17 novembre 2026, la CNIL a publié un bilan : depuis juin 2026, elle a prononcé 38 nouvelles sanctions en procédure simplifiée, pour un total de 302 800 euros d'amendes. Avec les 23 sanctions de la période précédente, cela fait 61 sanctions simplifiées depuis le début de 2026. Ce chiffre contraste avec les grandes amendes médiatisées, par exemple celle de 5 millions d'euros prononcée pour la conservation de mots de passe clients en clair, traitée dans un module précédent. Ici, il s'agit de la « petite délinquance » du RGPD : des dossiers jugés sans difficulté juridique particulière, mais très représentatifs de ce que les organismes oublient le plus souvent.

## La procédure simplifiée : définitions

Selon la CNIL, la procédure simplifiée existe depuis 2022. Elle est réservée aux dossiers qui ne présentent pas de difficulté juridique particulière. Contrairement à la procédure ordinaire, où la formation restreinte délibère collégialement, c'est le président de la formation restreinte, ou l'un de ses membres, qui décide seul de la sanction. Trois caractéristiques ressortent de la page de la CNIL : l'amende ne peut pas dépasser 20 000 euros, l'organisme sanctionné n'est pas nommé publiquement, et les sommes sont recouvrées par le Trésor public pour être versées au budget de l'État. La base légale précise de cette procédure n'est pas indiquée sur la page que nous avons lue ; nous ne la citons donc pas ici.

Sur le plan des montants, l'ordre de grandeur est parlant : 302 800 euros répartis sur 38 sanctions donnent une moyenne d'environ 8 000 euros. Ce calcul est le nôtre, la CNIL ne publie pas de moyenne et ne détaille pas les montants par catégorie. Il faut donc le lire comme un repère, pas comme un barème.

## Ce que la CNIL a sanctionné

La CNIL indique que ces décisions portent principalement sur quatre sujets. Les chiffres donnés sont approximatifs : « une douzaine » pour deux catégories, ce qui ne totalise pas exactement 38.

Premier sujet, les cookies et traceurs, avec environ une douzaine d'amendes. Le fondement est l'article 82 de la loi Informatique et Libertés, qui transpose en droit français la règle européenne sur le stockage ou la lecture d'informations sur le terminal d'un utilisateur. Les manquements relevés sont de deux types : un défaut d'information dans les bandeaux, et le dépôt de cookies sans consentement, y compris après un refus de l'internaute, notamment pour des cookies publicitaires. Un refus qui n'est pas respecté est le cas le plus simple à prouver : il suffit de visiter le site, de refuser, puis d'observer les requêtes réseau.

Deuxième sujet, la sécurité des données, avec environ une douzaine d'organismes. Le fondement est l'article 32 du RGPD, qui impose des mesures techniques et organisationnelles appropriées. La CNIL cite des mots de passe insuffisamment robustes, des comptes génériques partagés entre plusieurs personnes et des fonctions de hachage non conformes, SHA-1 étant mentionné. Ce sont des défauts qu'un test d'intrusion ou un audit de configuration détecte en quelques minutes.

Troisième sujet, la prospection commerciale, avec six organismes. Le fondement est l'article L. 34-5 du code des postes et des communications électroniques, qui exige un consentement pour la prospection par voie électronique. Les reproches concernent la transmission de données à des partenaires ou la prospection sans consentement valable, y compris des formulaires de jeux-concours qui poussent à consentir.

Quatrième sujet, la non-coopération avec la CNIL, avec six organismes. L'article 18 de la loi Informatique et Libertés fait de la coopération une obligation légale. Les organismes concernés n'ont pas répondu aux demandes de la CNIL, par exemple sur la vidéosurveillance ou sur des demandes d'accès ou d'effacement. Ce motif est révélateur : ignorer la CNIL aggrave une situation qui aurait pu rester mineure.

## Les enjeux

Premier enjeu : la prévisibilité. Même sans publication des noms, la liste des griefs permet à n'importe quel organisme de se comparer. Une checklist se dégage : le refus de cookies est-il effectif, les mots de passe sont-ils stockés avec un algorithme de hachage actuel, les comptes sont-ils nominatifs, le consentement à la prospection est-il libre et séparé, les courriers de la CNIL reçoivent-ils une réponse.

Deuxième enjeu : l'anonymat des décisions. Comme la CNIL ne peut pas divulguer le nom de l'organisme dans cette procédure, l'effet dissuasif repose sur le volume plutôt que sur la réputation. C'est une différence importante avec les sanctions ordinaires, publiées avec le nom de la société.

Troisième enjeu : le contrôle à grande échelle. Parmi les 38 sanctions, 23 proviennent de plaintes, selon la page de la CNIL. Autrement dit, ce sont des particuliers qui déclenchent une grande partie des dossiers, ce qui rapproche le sujet de la décision de la Cour de justice du 5 novembre 2026 sur l'accès du plaignant à son dossier, traitée dans un module précédent.

Quatrième enjeu : la sécurité comme obligation de moyens vérifiable. L'article 32 du RGPD ne fixe pas d'algorithme précis, mais la CNIL considère manifestement qu'un hachage comme SHA-1 pour des mots de passe ne répond plus à l'état de l'art. Pour un chercheur en sécurité, cela transforme une bonne pratique technique en point de contrôle réglementaire.

## Limites de ce module

Ce module repose sur la page d'annonce de la CNIL. Nous n'avons pas lu les délibérations individuelles, qui ne nomment pas les organismes ; nous ne pouvons donc pas dire quelle amende correspond à quel manquement. La fourchette de montants par catégorie n'est pas publiée. Enfin, l'annonce ne permet pas de conclure qu'un manquement donné entraîne systématiquement une amende : chaque dossier est apprécié individuellement.

## Références

Annonce de la CNIL du 17 novembre 2026, « La CNIL a prononcé 38 nouvelles sanctions en procédure simplifiée depuis juin 2026 » ; page de la CNIL sur la procédure de sanction simplifiée ; règlement (UE) 2016/679, articles 6 et 32 ; loi du 6 janvier 1978 relative à l'informatique, aux fichiers et aux libertés, articles 18 et 82 ; code des postes et des communications électroniques, article L. 34-5.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez un angle et collez-le tel quel dans le champ de personnalisation.

**Angle 1 — Checklist d'audit offensif.** Concentre-toi sur les manquements techniquement vérifiables de l'annonce : refus de cookies non respecté, hachage SHA-1, comptes partagés, mots de passe faibles. Pour chacun, explique comment un auditeur le détecterait (analyse du trafic réseau, revue de configuration, test de force brute) et quel article du RGPD ou de la loi Informatique et Libertés il met en jeu.

**Angle 2 — Automatiser le contrôle de conformité.** Imagine un outil qui surveille en continu les points de contrôle cités : dépôt de traceurs après refus, algorithmes de hachage, comptes génériques. Discute de ce qu'on peut automatiser, de ce qui exige un jugement juridique, et des limites d'un scan externe par rapport à un audit interne.

**Angle 3 — Petites amendes contre grandes sanctions.** Compare cette procédure simplifiée (20 000 € maximum, décideur unique, anonymat) avec les sanctions ordinaires de la CNIL déjà traitées dans le dépôt, comme celle de 5 millions d'euros sur les mots de passe en clair. Explique ce que change le plafond et l'absence de publication pour la dissuasion.

**Angle 4 — Le rôle des plaintes.** Sur 38 sanctions, 23 viennent de plaintes. Analyse ce que cela implique pour la stratégie de contrôle de la CNIL, le lien avec la jurisprudence récente de la Cour de justice sur l'accès du plaignant à son dossier, et ce qu'un organisme peut faire pour réduire le risque de plainte.

**Angle 5 — Prospective réglementaire.** Replace ces sanctions dans la montée en puissance de la cybersécurité réglementaire en France : loi Résilience et NIS2 en cours d'adoption, obligations de sécurité du RGPD. Discute de la manière dont un organisme sanctionné aujourd'hui pour un hachage faible pourrait l'être demain sous un autre régime, sans conclure à des certitudes sur le calendrier législatif.
