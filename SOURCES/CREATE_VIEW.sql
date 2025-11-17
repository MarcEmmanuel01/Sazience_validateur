--tiers
SELECT * FROM [x3data].[SAZIENCE].[BPARTNER]
CREATE VIEW TABLE_TIERS AS
SELECT BPRNUM_0 AS Code_tiers
FROM [x3data].[SAZIENCE].[BPARTNER]
WHERE ENAFLG_0 = 2;


--journal
SELECT * FROM [x3data].[SAZIENCE].[GJOURNAL]
CREATE VIEW TABLE_JOURNAL AS
SELECT JOU_0 AS Code_Journaux
FROM [x3data].[SAZIENCE].[GJOURNAL]
WHERE ENAFLG_0 = 2;


--Numero de compe comptable
SELECT * FROM [x3data].[SAZIENCE].[GACCOUNT]
CREATE VIEW TABLE_COMPTE_COMPTABLE AS
SELECT ACC_0 AS Comptes_comptables
FROM [x3data].[SAZIENCE].[GACCOUNT]
WHERE ENAFLG_0 = 2;



--Axe Analytique
SELECT * FROM [x3data].[SAZIENCE].[CACCE]
CREATE VIEW TABLE_AXE_ANALYTIQUES AS
SELECT CCE_0 AS Axe_analytiques
FROM [x3data].[SAZIENCE].[CACCE]
WHERE ENAFLG_0 = 2;





CREATE VIEW source_saisies_pieces AS
SELECT 
    acc.Comptes_comptables,
    bpr.Code_tiers, 
    jou.Code_Journaux,
    cce.Axe_analytiques
FROM 
    (SELECT ACC_0 AS Comptes_comptables, ROW_NUMBER() OVER (ORDER BY ACC_0) as rn 
     FROM [x3data].[SAZIENCE].[GACCOUNT] 
     WHERE ENAFLG_0 = 2) acc
FULL OUTER JOIN 
    (SELECT BPRNUM_0 AS Code_tiers, ROW_NUMBER() OVER (ORDER BY BPRNUM_0) as rn 
     FROM [x3data].[SAZIENCE].[BPARTNER] 
     WHERE ENAFLG_0 = 2) bpr ON acc.rn = bpr.rn
FULL OUTER JOIN 
    (SELECT JOU_0 AS Code_Journaux, ROW_NUMBER() OVER (ORDER BY JOU_0) as rn 
     FROM [x3data].[SAZIENCE].[GJOURNAL] 
     WHERE ENAFLG_0 = 2) jou ON COALESCE(acc.rn, bpr.rn) = jou.rn
FULL OUTER JOIN 
    (SELECT CCE_0 AS Axe_analytiques, ROW_NUMBER() OVER (ORDER BY CCE_0) as rn 
     FROM [x3data].[SAZIENCE].[CACCE] 
     WHERE ENAFLG_0 = 2) cce ON COALESCE(acc.rn, bpr.rn, jou.rn) = cce.rn;