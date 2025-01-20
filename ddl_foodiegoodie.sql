-- Tabela: Uzytkownik
CREATE TABLE Uzytkownik (
    idUzytkownik SERIAL PRIMARY KEY,
    nazwaUzytkownika VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    haslo VARCHAR(80) NOT NULL
);

-- Tabela: Profil
CREATE TABLE Profil (
    idProfil SERIAL PRIMARY KEY,
    preferencjeDiety TEXT,
    FK_idUzytkownik INT,
    FOREIGN KEY (FK_idUzytkownik) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: Uprawnienia
CREATE TABLE Uprawnienia (
    idUprawnienia SERIAL PRIMARY KEY,
    nazwaUprawnienia VARCHAR(255) NOT NULL
);

-- Tabela: UprawnieniaUzytkownikow
CREATE TABLE UprawnieniaUzytkownikow (
    FK_idUprawnienia INT,
    FK_idUzytkownik INT,
    PRIMARY KEY (FK_idUprawnienia, FK_idUzytkownik),
    FOREIGN KEY (FK_idUprawnienia) REFERENCES Uprawnienia(idUprawnienia),
    FOREIGN KEY (FK_idUzytkownik) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: Wpis
CREATE TABLE Wpis (
    idWpis SERIAL PRIMARY KEY,
    FK_idAutor INT,
    tresc TEXT NOT NULL,
    dataDodania DATE,
    FOREIGN KEY (FK_idAutor) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: GlosyWpis
CREATE TABLE GlosyWpis (
    FK_idWpis INT,
    FK_idAutorGlosu INT,
    zaglosowano BOOLEAN,
    PRIMARY KEY (FK_idWpis, FK_idAutorGlosu),
    FOREIGN KEY (FK_idWpis) REFERENCES Wpis(idWpis),
    FOREIGN KEY (FK_idAutorGlosu) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: Forum
CREATE TABLE Forum (
    idForum SERIAL PRIMARY KEY,
    tytulPost VARCHAR(50),
    FK_idUzytkownik INT,
    FOREIGN KEY (FK_idUzytkownik) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: Post
CREATE TABLE Post (
    idPost SERIAL PRIMARY KEY,
    tytulPost VARCHAR(255),
    trescPost TEXT,
    dataDodaniaPostu DATE,
    FK_idForum INT,
    FK_idAutor INT,
    FOREIGN KEY (FK_idForum) REFERENCES Forum(idForum),
    FOREIGN KEY (FK_idAutor) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: Przepis
CREATE TABLE Przepis (
    idPrzepis SERIAL PRIMARY KEY,
    nazwaPrzepisu VARCHAR(50) NOT NULL,
    skladniki JSON,
    instrukcje JSON,
    startPublikacji DATE
);

-- Tabela: Ranking
CREATE TABLE Ranking (
    idRanking SERIAL PRIMARY KEY,
    nazwaRankingu VARCHAR(20),
    typRankingu VARCHAR(30)
);

-- Tabela: OcenyPrzepisu
CREATE TABLE OcenyPrzepisu (
    idOceny SERIAL PRIMARY KEY,
    FK_idPrzepis INT,
    FK_idOceniajacy INT,
    wartosc INT,
    FOREIGN KEY (FK_idPrzepis) REFERENCES Przepis(idPrzepis),
    FOREIGN KEY (FK_idOceniajacy) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: PrzepisyWRankingu
CREATE TABLE PrzepisyWRankingu (
    FK_idRanking INT,
    FK_idPrzepis INT,
    pozycja INT,
    PRIMARY KEY (FK_idRanking, FK_idPrzepis),
    FOREIGN KEY (FK_idRanking) REFERENCES Ranking(idRanking),
    FOREIGN KEY (FK_idPrzepis) REFERENCES Przepis(idPrzepis)
);

-- Tabela: KomentarzePrzepisu
CREATE TABLE KomentarzePrzepisu (
    idKomentarz SERIAL PRIMARY KEY,
    FK_idPrzepis INT,
    FK_idKomentarz INT,
    FK_idUzytkownika INT,
    dataKomentarza DATE,
    trescKomentarza VARCHAR(250),
    FOREIGN KEY (FK_idPrzepis) REFERENCES Przepis(idPrzepis),
    FOREIGN KEY (FK_idUzytkownika) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: ListaZakupow
CREATE TABLE ListaZakupow (
    idLista SERIAL PRIMARY KEY,
    nazwaListy VARCHAR(50),
    FK_idAutor INT,
    FOREIGN KEY (FK_idAutor) REFERENCES Uzytkownik(idUzytkownik)
);

-- Tabela: SzczegolyListy
CREATE TABLE SzczegolyListy (
    idSzczegoly SERIAL PRIMARY KEY,
    FK_idLista INT,
    produkt VARCHAR(50),
    ilosc FLOAT,
    jednostka VARCHAR(10),
    FOREIGN KEY (FK_idLista) REFERENCES ListaZakupow(idLista)
);

-- Tabela: KategorieDiety
CREATE TABLE KategorieDiety (
    idKategoria SERIAL PRIMARY KEY,
    nazwaKategorii VARCHAR(50)
);

-- Tabela: ListyZDietami
CREATE TABLE ListyZDietami (
    idListaDiety SERIAL PRIMARY KEY,
    FK_idLista INT,
    FK_idKategoria INT,
    FOREIGN KEY (FK_idLista) REFERENCES ListaZakupow(idLista),
    FOREIGN KEY (FK_idKategoria) REFERENCES KategorieDiety(idKategoria)
);
