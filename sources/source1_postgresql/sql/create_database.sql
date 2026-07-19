-- =====================================================
-- Projet : EduSmart Decision Platform
-- base, tables, contraintes, relation
-- Base : edusmart_academic --> 

DROP DATABASE IF EXISTS edusmart_academic;
CREATE DATABASE edusmart_academic;

\connect edusmart_academic
-- Extension UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- Création des tables
-- =====================================================

-- 1. etudiants
CREATE TABLE etudiants (
    id_etudiant UUID PRIMARY KEY,
    matricule VARCHAR(20) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    sexe CHAR(1) NOT NULL CHECK (sexe IN ('M', 'F')),
    date_naissance DATE NOT NULL CHECK (date_naissance < CURRENT_DATE),
    telephone VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    adresse TEXT,
    ville VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    pays VARCHAR(100) DEFAULT 'Sénégal',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 2. filieres
CREATE TABLE filieres (
    id_filiere UUID PRIMARY KEY,
    code_filiere VARCHAR(20) NOT NULL UNIQUE,
    nom_filiere VARCHAR(150) NOT NULL,
    departement VARCHAR(100) NOT NULL,
    niveau VARCHAR(30) NOT NULL,
    duree_mois INTEGER NOT NULL CHECK (duree_mois > 0),
    cout_total NUMERIC(12,2) NOT NULL CHECK (cout_total >= 0),
    statut VARCHAR(20) DEFAULT 'ACTIVE'
);

-- 3. classes
CREATE TABLE classes (
    id_classe UUID PRIMARY KEY,
    code_classe VARCHAR(30) NOT NULL UNIQUE,
    nom_classe VARCHAR(100) NOT NULL,
    id_filiere UUID NOT NULL,
    annee_academique VARCHAR(20) NOT NULL,
    capacite INTEGER NOT NULL CHECK (capacite > 0),
    salle VARCHAR(30),
    responsable VARCHAR(100),
    CONSTRAINT fk_classe_filiere
    FOREIGN KEY (id_filiere)
    REFERENCES filieres(id_filiere)
);

-- 4. inscriptions
CREATE TABLE inscriptions (
    id_inscription UUID PRIMARY KEY,
    id_etudiant UUID NOT NULL,
    id_classe UUID NOT NULL,
    date_inscription DATE NOT NULL,
    statut VARCHAR(30) DEFAULT 'INSCRIT',
    type_inscription VARCHAR(30) NOT NULL,
    bourse BOOLEAN DEFAULT FALSE,
    reduction NUMERIC(5,2)
    CHECK (reduction BETWEEN 0 AND 100),
    CONSTRAINT fk_inscription_etudiant
    FOREIGN KEY (id_etudiant)
    REFERENCES etudiants(id_etudiant),
    CONSTRAINT fk_inscription_classe
    FOREIGN KEY (id_classe)
    REFERENCES classes(id_classe)
);

-- 5. paiements
CREATE TABLE paiements (
    id_paiement UUID PRIMARY KEY,
    id_inscription UUID NOT NULL,
    reference VARCHAR(50) UNIQUE,
    date_paiement DATE NOT NULL,
    montant NUMERIC(12,2)
    CHECK (montant >= 0),
    mode_paiement VARCHAR(30) NOT NULL,
    statut VARCHAR(30) DEFAULT 'VALIDE',
    tranche VARCHAR(20) NOT NULL,
    CONSTRAINT fk_paiement_inscription
    FOREIGN KEY (id_inscription)
    REFERENCES inscriptions(id_inscription)
);