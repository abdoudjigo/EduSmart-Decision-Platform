-- =====================================================
-- Projet : EduSmart Decision Platform
-- Source 2 : MySQL - Plateforme Learning

DROP DATABASE IF EXISTS edusmart_learning;
CREATE DATABASE edusmart_learning;
USE edusmart_learning;

-- =====================================================
-- 1. TABLE MODULES
CREATE TABLE modules (
    id_module CHAR(36) PRIMARY KEY,
    code_module VARCHAR(20) NOT NULL UNIQUE,
    nom_module VARCHAR(150) NOT NULL,
    categorie VARCHAR(100) NOT NULL,
    niveau VARCHAR(30) NOT NULL,
    duree_heures INT,
    actif BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_duree_module
    CHECK (duree_heures > 0)
);

-- =====================================================
-- 2. TABLE COURS
CREATE TABLE cours (
    id_cours CHAR(36) PRIMARY KEY,
    id_module CHAR(36) NOT NULL,
    titre VARCHAR(200) NOT NULL,
    ordre INT,
    duree_minutes INT,
    type_cours VARCHAR(30) NOT NULL,
    statut VARCHAR(20) DEFAULT 'PUBLIE',
    CONSTRAINT fk_cours_module
    FOREIGN KEY(id_module)
    REFERENCES modules(id_module),
    CONSTRAINT chk_ordre_cours
    CHECK (ordre > 0),
    CONSTRAINT chk_duree_cours
    CHECK (duree_minutes > 0)
);

-- =====================================================
-- 3. TABLE QUIZ
CREATE TABLE quiz (
    id_quiz CHAR(36) PRIMARY KEY,
    id_cours CHAR(36) NOT NULL,
    titre VARCHAR(150) NOT NULL,
    nb_questions INT,
    score_max DECIMAL(5,2),
    duree_minutes INT,
    CONSTRAINT fk_quiz_cours
    FOREIGN KEY(id_cours)
    REFERENCES cours(id_cours),
    CONSTRAINT chk_questions
    CHECK (nb_questions > 0),
    CONSTRAINT chk_score
    CHECK (score_max > 0),
    CONSTRAINT chk_duree_quiz
    CHECK (duree_minutes > 0)
);

-- =====================================================
-- 4. TABLE NOTES
CREATE TABLE notes (
    id_note CHAR(36) PRIMARY KEY,
    id_quiz CHAR(36) NOT NULL,
    student_code VARCHAR(30) NOT NULL,
    date_passage TIMESTAMP NOT NULL,
    score DECIMAL(5,2),
    tentative INT DEFAULT 1,
    valide BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_notes_quiz
    FOREIGN KEY(id_quiz)
    REFERENCES quiz(id_quiz),
    CONSTRAINT chk_score_note
    CHECK (score >= 0)
);

-- =====================================================
-- 5. TABLE PROGRESSION
CREATE TABLE progression (
    id_progression CHAR(36) PRIMARY KEY,
    student_code VARCHAR(30) NOT NULL,
    id_module CHAR(36) NOT NULL,
    pourcentage DECIMAL(5,2),
    dernier_cours CHAR(36),
    date_maj TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_progression_module
    FOREIGN KEY(id_module)
    REFERENCES modules(id_module),
    CONSTRAINT chk_pourcentage
    CHECK (
        pourcentage BETWEEN 0 AND 100
    ),
    CONSTRAINT unique_progression
    UNIQUE(
        student_code,
        id_module
    )
);


-- =====================================================
-- 6. TABLE TEMPS_CONNEXION
CREATE TABLE temps_connexion (
    id_connexion CHAR(36) PRIMARY KEY,
    student_code VARCHAR(30) NOT NULL,
    date_connexion TIMESTAMP NOT NULL,
    date_deconnexion TIMESTAMP NULL,
    duree_minutes INT,
    appareil VARCHAR(50),
    navigateur VARCHAR(50),
    adresse_ip VARCHAR(45),
    CONSTRAINT chk_duree_connexion
    CHECK (duree_minutes >= 0)
);