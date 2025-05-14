-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mer. 14 mai 2025 à 16:54
-- Version du serveur : 11.7.2-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `marsamaroc`
--

-- --------------------------------------------------------

--
-- Structure de la table `authentification_affectationengin`
--

CREATE TABLE `authentification_affectationengin` (
  `id` int(11) NOT NULL,
  `navire_id` int(11) NOT NULL,
  `engin_id` int(11) NOT NULL,
  `date_debut` datetime DEFAULT current_timestamp(),
  `date_fin` datetime DEFAULT NULL,
  `chauffeur_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `authentification_affectationengin`
--

INSERT INTO `authentification_affectationengin` (`id`, `navire_id`, `engin_id`, `date_debut`, `date_fin`, `chauffeur_id`) VALUES
(9, 96, 5, '2025-05-14 10:39:19', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `authentification_driver`
--

CREATE TABLE `authentification_driver` (
  `id` int(11) NOT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `matricule` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `CIN` varchar(20) DEFAULT NULL,
  `shiftPeriod` varchar(20) DEFAULT NULL,
  `supervisor` longtext DEFAULT NULL,
  `equipment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '[]' CHECK (json_valid(`equipment`)),
  `address` text DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `joinDate` date DEFAULT NULL,
  `is_flexible` tinyint(1) DEFAULT 0
) ;

--
-- Déchargement des données de la table `authentification_driver`
--

INSERT INTO `authentification_driver` (`id`, `firstname`, `lastname`, `matricule`, `phone`, `email`, `CIN`, `shiftPeriod`, `supervisor`, `equipment`, `address`, `birthdate`, `joinDate`, `is_flexible`) VALUES
(23, 'Said', 'Aissaoui', 'MM2024', '0666555441', '', '', 'morning', 'Said', '[\"Grue mobile\"]', '80000\r\nAgadir', '2025-05-07', '2025-05-13', 0),
(26, 'mounir', 'Aissaoui', 'MM2011', '0666555441', '', '', 'morning', 'Said', '[\"Grue mobile\"]', '80000\r\nAgadir', '2017-02-13', '2025-05-14', 0);

-- --------------------------------------------------------

--
-- Structure de la table `authentification_enginmarchandise`
--

CREATE TABLE `authentification_enginmarchandise` (
  `id` int(11) NOT NULL,
  `engin_id` int(11) NOT NULL,
  `type_marchandise_id` bigint(20) UNSIGNED NOT NULL,
  `date_ajout` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `authentification_enginmarchandise`
--

INSERT INTO `authentification_enginmarchandise` (`id`, `engin_id`, `type_marchandise_id`, `date_ajout`) VALUES
(1, 3, 3, '2025-05-14 00:04:16'),
(2, 5, 1, '2025-05-14 00:13:23'),
(3, 4, 2, '2025-05-14 00:13:23'),
(4, 6, 3, '2025-05-14 00:13:23'),
(5, 7, 4, '2025-05-14 00:13:23');

-- --------------------------------------------------------

--
-- Structure de la table `authentification_feuilleservice`
--

CREATE TABLE `authentification_feuilleservice` (
  `id` int(11) NOT NULL,
  `navire_id` int(11) NOT NULL,
  `date_creation` datetime DEFAULT current_timestamp(),
  `created_by_id` int(11) NOT NULL,
  `statut` varchar(20) DEFAULT 'draft' CHECK (`statut` in ('draft','active','completed'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `authentification_navire`
--

CREATE TABLE `authentification_navire` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `imo` varchar(7) NOT NULL,
  `type_operation` varchar(10) NOT NULL,
  `port_origine` varchar(100) NOT NULL,
  `poste` varchar(10) NOT NULL,
  `heure_arrivee` datetime NOT NULL,
  `duree_sejour` int(11) NOT NULL,
  `heure_depart` datetime NOT NULL,
  `type_marchandise` varchar(20) NOT NULL,
  `chef_escale_id` int(11) NOT NULL,
  `statut` varchar(20) NOT NULL DEFAULT 'En attente',
  `date_creation` datetime NOT NULL DEFAULT current_timestamp(),
  `date_modification` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `authentification_navire`
--

INSERT INTO `authentification_navire` (`id`, `nom`, `imo`, `type_operation`, `port_origine`, `poste`, `heure_arrivee`, `duree_sejour`, `heure_depart`, `type_marchandise`, `chef_escale_id`, `statut`, `date_creation`, `date_modification`) VALUES
(96, 'Tanger Express', '7451555', 'import', 'usa', '1', '2025-05-14 00:38:00', 4, '2025-05-14 11:38:00', 'containers', 1, 'Accosté', '2025-05-14 10:39:19', '2025-05-14 10:49:28');

-- --------------------------------------------------------

--
-- Structure de la table `authentification_typemarchandise`
--

CREATE TABLE `authentification_typemarchandise` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code` varchar(50) NOT NULL,
  `libelle` varchar(100) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `authentification_typemarchandise`
--

INSERT INTO `authentification_typemarchandise` (`id`, `code`, `libelle`, `description`) VALUES
(1, 'containers', 'Conteneurs', 'Marchandises transportées en conteneurs'),
(2, 'bulk', 'Vrac', 'Marchandises en vrac comme les grains ou les liquides'),
(3, 'general', 'Marchandises Générales', 'Marchandises diverses non spécialisées'),
(4, 'vehicles', 'Véhicules', 'Voitures, camions et autres véhicules à moteur');

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(3, 'Chef Escale'),
(1, 'Conducteurs'),
(2, 'RH');

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(1, 2, 25),
(2, 2, 26),
(3, 2, 27),
(4, 2, 28);

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Peut ajouter une demande d\'absence', 7, 'add_absence'),
(26, 'Peut modifier une demande d\'absence', 7, 'change_absence'),
(27, 'Peut supprimer une demande d\'absence', 7, 'delete_absence'),
(28, 'Peut voir les demandes d\'absence', 7, 'view_absence'),
(29, 'Can add Chauffeur', 8, 'add_driver'),
(30, 'Can change Chauffeur', 8, 'change_driver'),
(31, 'Can delete Chauffeur', 8, 'delete_driver'),
(32, 'Can view Chauffeur', 8, 'view_driver'),
(33, 'Can add chef escale', 9, 'add_chefescale'),
(34, 'Can change chef escale', 9, 'change_chefescale'),
(35, 'Can delete chef escale', 9, 'delete_chefescale'),
(36, 'Can view chef escale', 9, 'view_chefescale'),
(37, 'Can add Navire', 10, 'add_navire'),
(38, 'Can change Navire', 10, 'change_navire'),
(39, 'Can delete Navire', 10, 'delete_navire'),
(40, 'Can view Navire', 10, 'view_navire'),
(41, 'Can add chef escale profile', 11, 'add_chefescaleprofile'),
(42, 'Can change chef escale profile', 11, 'change_chefescaleprofile'),
(43, 'Can delete chef escale profile', 11, 'delete_chefescaleprofile'),
(44, 'Can view chef escale profile', 11, 'view_chefescaleprofile'),
(45, 'Can add engin', 12, 'add_engin'),
(46, 'Can change engin', 12, 'change_engin'),
(47, 'Can delete engin', 12, 'delete_engin'),
(48, 'Can view engin', 12, 'view_engin');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$w1mU6MEWFb4fbRaN4wKpeS$U5jO5scUIEyOr8KarVYrSLYcufPpDxy60f8snyDe2RE=', '2025-05-13 15:53:56.314668', 1, 'said', '', '', 'saidaissaoui@marsamaroc.co.ma', 1, 1, '2025-04-24 16:51:55.374017'),
(3, 'pbkdf2_sha256$1000000$x2oXd5PmPaxPPX9jRu5C4b$PKdTtRwMOG7LPkbpCi6wi8KJU01Q0JaJc8Rzt/56B5c=', '2025-05-12 16:58:25.995992', 1, 'Mohamed_KASMI', '', '', 'Mohamed_KASMIi@marsamaroc.co.ma', 1, 1, '2025-04-29 21:27:50.227404'),
(14, 'pbkdf2_sha256$260000$N2Y1pZJ6...', NULL, 0, 'saad', 'Saad', 'Benali', 'saad@marsamaroc.ma', 0, 1, '2025-05-11 19:54:29.000000'),
(15, 'pbkdf2_sha256$260000$N2Y1pZJ6...', NULL, 0, 'mohamed', 'Mohamed', 'Amrani', 'mohamed@marsamaroc.ma', 0, 1, '2025-05-11 19:54:29.000000'),
(16, 'pbkdf2_sha256$260000$N2Y1pZJ6...', NULL, 0, 'ahmed', 'Ahmed', 'Elouardi', 'ahmed@marsamaroc.ma', 0, 1, '2025-05-11 19:54:29.000000'),
(18, 'pbkdf2_sha256$1000000$IxkgCQMT5mQUWbJQYpkJSo$xIhppaLqd2dugZ1qkPfTK/EMzs+nYmclRxMSW6b1O24=', '2025-05-12 17:00:00.473983', 0, 'amina_elouardi', 'Amina', 'El Ouardi', 'a.elouardi@marsamaroc.ma', 1, 1, '2025-05-11 22:37:20.922028');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 3),
(2, 3, 3);

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `chefs_escale`
--

CREATE TABLE `chefs_escale` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `chefs_escale`
--

INSERT INTO `chefs_escale` (`id`, `nom`) VALUES
(1, 'Ahmed El Mansouri'),
(2, 'said'),
(3, 'Youssef Amrani');

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-05-08 22:25:21.917564', '3', 'Chef Escale', 1, '[{\"added\": {}}]', 3, 1),
(2, '2025-05-08 22:44:35.868697', '3', 'Chef Escale', 2, '[]', 3, 1);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(9, 'authentification', 'chefescale'),
(11, 'authentification', 'chefescaleprofile'),
(8, 'authentification', 'driver'),
(12, 'authentification', 'engin'),
(10, 'authentification', 'navire'),
(5, 'contenttypes', 'contenttype'),
(7, 'rh', 'absence'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-04-23 19:24:50.910264'),
(2, 'auth', '0001_initial', '2025-04-23 19:24:51.484560'),
(3, 'admin', '0001_initial', '2025-04-23 19:24:51.626414'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-04-23 19:24:51.651931'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-23 19:24:51.682705'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-04-23 19:24:51.841824'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-04-23 19:24:51.948595'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-04-23 19:24:52.011448'),
(9, 'auth', '0004_alter_user_username_opts', '2025-04-23 19:24:52.025651'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-04-23 19:24:52.110190'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-04-23 19:24:52.115658'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-04-23 19:24:52.131883'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-04-23 19:24:52.203935'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-04-23 19:24:52.261567'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-04-23 19:24:52.367477'),
(16, 'auth', '0011_update_proxy_permissions', '2025-04-23 19:24:52.393371'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-04-23 19:24:52.469440'),
(18, 'sessions', '0001_initial', '2025-04-23 19:24:52.576082'),
(19, 'authentification', '0001_initial', '2025-05-09 09:31:17.901135'),
(20, 'authentification', '0002_chefescaleprofile', '2025-05-09 09:31:17.922385'),
(21, 'authentification', '0003_remove_chefescale_nuit_end_time_and_more', '2025-05-09 09:31:17.929321'),
(22, 'authentification', '0004_alter_driver_supervisor', '2025-05-09 09:31:17.932262'),
(23, 'authentification', '0002_alter_engin_table', '2025-05-11 18:37:36.626125');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('21dh9h1srcabwepv3e7jid7wf18up3a4', 'e30:1uCJgD:ZYp62tw_LCCgA2b05uha2CFjBfxJUrHxJPg36dE1Pj0', '2025-05-20 14:53:57.091858'),
('cr9hjjq4divrdgquw1503tlit2j0idnd', 'e30:1u80JO:oYmsK5XILpxDN4mx7g8buIBTXm5nIAAXsYbMFx2oWcU', '2025-05-08 17:24:34.402501'),
('nm8amp012d1mwwabg4dmpfjr410vwqva', 'e30:1u7zxQ:v3li_zGRMqRMLeDuSGI--CNsCN8wVv1QyQKqEtPTOfg', '2025-05-08 17:01:52.812443'),
('tdqzdafp2xy5oor79m2i7qj3hhyjanuw', 'e30:1u7zqw:3rhdUc1kESvpEraWXKewoaj6AoGilshOyFLq8EysXwE', '2025-05-08 16:55:10.158203'),
('zg2cqgt6p0xutgemsa09dty089amfej7', '.eJxVjEEOgjAQRe_StWlKOy2OS_ecgcxMp4IaSCisjHdXEha6_e-9_zI9bevQb1WXfszmYhpz-t2Y5KHTDvKdpttsZZ7WZWS7K_ag1XZz1uf1cP8OBqrDt3YRQVLKSFwUEEIuIEWxDcpBfOuiQwZfkofki7YgJJ6R-Rw5NJTM-wPulDg6:1uErx6:VW--GFjab0nG9oj5Dx9Gr-YOJPB2R0n5upUUJjXRKaQ', '2025-05-27 15:53:56.327496');

-- --------------------------------------------------------

--
-- Structure de la table `engin`
--

CREATE TABLE `engin` (
  `id` int(11) NOT NULL,
  `matricule` varchar(50) NOT NULL,
  `type_engin` varchar(100) NOT NULL,
  `marque` varchar(100) NOT NULL,
  `modele` varchar(100) NOT NULL,
  `annee_fabrication` int(11) NOT NULL,
  `statut` varchar(20) NOT NULL,
  `maintenance_info` text DEFAULT NULL,
  `date_acquisition` date NOT NULL,
  `kilometrage` decimal(10,2) NOT NULL,
  `prochaine_maintenance` decimal(10,2) DEFAULT NULL,
  `commentaires` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `engin`
--

INSERT INTO `engin` (`id`, `matricule`, `type_engin`, `marque`, `modele`, `annee_fabrication`, `statut`, `maintenance_info`, `date_acquisition`, `kilometrage`, `prochaine_maintenance`, `commentaires`, `created_at`, `updated_at`, `created_by_id`) VALUES
(3, 'E001', 'Chariot élévateur', 'Toyota', '8FGCU25', 2018, 'disponible', '', '2020-03-01', 1200.50, NULL, '', '2025-05-12 16:56:19', '2025-05-14 10:12:43', 1),
(4, 'E002', 'Grue mobile', 'Liebherr', 'LTM 1090', 2016, 'disponible', '', '2019-06-15', 5400.00, NULL, '', '2025-05-12 16:56:19', '2025-05-14 00:42:36', 1),
(5, 'E003', 'Portique', 'Konecranes', 'RTG', 2017, 'disponible', '', '2021-02-10', 7800.75, NULL, '', '2025-05-12 16:56:19', '2025-05-14 10:44:23', 1),
(6, 'E004', 'Camion', 'Mercedes', 'Actros', 2019, 'disponible', '', '2022-01-20', 23000.00, NULL, '', '2025-05-12 16:56:19', '2025-05-14 00:33:40', 1),
(7, 'E005', 'Reachstacker', 'Kalmar', 'DRF450', 2020, 'disponible', '', '2023-04-05', 5100.10, NULL, '', '2025-05-12 16:56:19', '2025-05-14 10:12:49', 1);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `authentification_affectationengin`
--
ALTER TABLE `authentification_affectationengin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_affectation_navire` (`navire_id`),
  ADD KEY `fk_affectation_engin` (`engin_id`),
  ADD KEY `fk_affectation_chauffeur` (`chauffeur_id`);

--
-- Index pour la table `authentification_driver`
--
ALTER TABLE `authentification_driver`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `matricule` (`matricule`),
  ADD KEY `authentification_driver_supervisor_id_05dc3568` (`supervisor`(768));

--
-- Index pour la table `authentification_enginmarchandise`
--
ALTER TABLE `authentification_enginmarchandise`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_engin_marchandise` (`engin_id`,`type_marchandise_id`),
  ADD KEY `fk_type_marchandise` (`type_marchandise_id`);

--
-- Index pour la table `authentification_feuilleservice`
--
ALTER TABLE `authentification_feuilleservice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `navire_id` (`navire_id`),
  ADD KEY `created_by_id` (`created_by_id`);

--
-- Index pour la table `authentification_navire`
--
ALTER TABLE `authentification_navire`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `imo` (`imo`),
  ADD KEY `chef_escale_id` (`chef_escale_id`);

--
-- Index pour la table `authentification_typemarchandise`
--
ALTER TABLE `authentification_typemarchandise`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `chefs_escale`
--
ALTER TABLE `chefs_escale`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `engin`
--
ALTER TABLE `engin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `matricule` (`matricule`),
  ADD KEY `fk_created_by` (`created_by_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `authentification_affectationengin`
--
ALTER TABLE `authentification_affectationengin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `authentification_driver`
--
ALTER TABLE `authentification_driver`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `authentification_enginmarchandise`
--
ALTER TABLE `authentification_enginmarchandise`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `authentification_feuilleservice`
--
ALTER TABLE `authentification_feuilleservice`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `authentification_navire`
--
ALTER TABLE `authentification_navire`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98;

--
-- AUTO_INCREMENT pour la table `authentification_typemarchandise`
--
ALTER TABLE `authentification_typemarchandise`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `chefs_escale`
--
ALTER TABLE `chefs_escale`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `engin`
--
ALTER TABLE `engin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `authentification_affectationengin`
--
ALTER TABLE `authentification_affectationengin`
  ADD CONSTRAINT `fk_affectation_chauffeur` FOREIGN KEY (`chauffeur_id`) REFERENCES `authentification_driver` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_affectation_engin` FOREIGN KEY (`engin_id`) REFERENCES `engin` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_affectation_navire` FOREIGN KEY (`navire_id`) REFERENCES `authentification_navire` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `authentification_enginmarchandise`
--
ALTER TABLE `authentification_enginmarchandise`
  ADD CONSTRAINT `fk_engin` FOREIGN KEY (`engin_id`) REFERENCES `engin` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_type_marchandise` FOREIGN KEY (`type_marchandise_id`) REFERENCES `authentification_typemarchandise` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `authentification_feuilleservice`
--
ALTER TABLE `authentification_feuilleservice`
  ADD CONSTRAINT `authentification_feuilleservice_ibfk_1` FOREIGN KEY (`navire_id`) REFERENCES `authentification_navire` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `authentification_feuilleservice_ibfk_2` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `authentification_navire`
--
ALTER TABLE `authentification_navire`
  ADD CONSTRAINT `authentification_navire_ibfk_1` FOREIGN KEY (`chef_escale_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `engin`
--
ALTER TABLE `engin`
  ADD CONSTRAINT `fk_created_by` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
