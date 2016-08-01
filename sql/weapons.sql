SELECT * FROM csgo_1.weapons;

/*Weapon classes: same as classes: 1 Support, 2 Engineer, 3 Recon, 4 Assault*/
/* Weapon types: 1 primary, 2 secondary, 3 grenades, 4 other stuff*/

INSERT INTO csgo_1.weapons (name, slug, rank, class, team, type) VALUES
/* CT Assault primary */
('Famas','weapon_famas',1,4,'CT',1),
('M4A1-S','weapon_m4a1_silencer',6,4,'CT',1),
('M4A4','weapon_m4a1',16,4,'CT',1), /* fix me */
('AUG','weapon_aug',31,4,'CT',1),
/* CT Assault secondary */
('USP-S','weapon_usp_silencer',1,4,'CT',2),
('P2000','weapon_hkp2000',6,4,'CT',2),
('P250','weapon_p250',11,4,'CT',2),
('Five-Seven','weapon_fiveseven',26,4,'CT',2),
('CZ75 Auto','weapon_cz75a',36,4,'CT',2),
('Deagle','weapon_deagle',56,4,'CT',2),
('R8 Revolver','weapon_revolver',56,4,'CT',2),
/* CT Assault grenades */
('HE Grenade 1x','weapon_hegrenade',1,4,'CT',3),
('Flashbang 1x','weapon_flashbang',1,4,'CT',3),
/* CT Engineer primary */
('MP9','weapon_mp9',1,2,'CT',1),
('MP7','weapon_mp7',6,2,'CT',1),
('PP-Bizon','weapon_bizon',16,2,'CT',1),
('UMP-45','weapon_ump45',31,2,'CT',1),
('P90','weapon_p90',51,2,'CT',1),
/* CT Engineer secondary */
('USP-S','weapon_usp_silencer',1,2,'CT',2),
('P2000','weapon_hkp2000',6,2,'CT',2),
('P250','weapon_p250',11,2,'CT',2),
('Five-Seven','weapon_fiveseven',26,2,'CT',2),
('CZ75 Auto','weapon_cz75a',36,2,'CT',2),
('Deagle','weapon_deagle',56,2,'CT',2),
('R8 Revolver','weapon_revolver',56,2,'CT',2),
/* CT Engineer grenades */
('Incendiary Grenade 1x','weapon_incgrenade',1,2,'CT',3),
('Smoke Grenade 1x','weapon_smokegrenade',1,2,'CT',3),
/* CT Support primary */
('MP9','weapon_mp9',1,1,'CT',1),
('Nova','weapon_nova',6,1,'CT',1),
('XM1014','weapon_xm1014',11,1,'CT',1),
('Mag-7','weapon_mag7',26,1,'CT',1),
('M249','weapon_m249',46,1,'CT',1),
('Negev','weapon_negev',56,1,'CT',1),
/* CT Support secondary */
('USP-S','weapon_usp_silencer',1,1,'CT',2),
('P2000','weapon_hkp2000',6,1,'CT',2),
('P250','weapon_p250',11,1,'CT',2),
('Five-Seven','weapon_fiveseven',26,1,'CT',2),
('CZ75 Auto','weapon_cz75a',36,1,'CT',2),
('Deagle','weapon_deagle',56,1,'CT',2),
('R8 Revolver','weapon_revolver',56,1,'CT',2),
/* CT Support grenades */
('Flashbang 2x','weapon_flashbang',1,1,'CT',3),
/* CT Recon primary */
('SSG08','weapon_ssg08',1,3,'CT',1),
('SCAR-20','weapon_scar20',31,3,'CT',1),
('AWP','weapon_awp',46,3,'CT',1),
/* CT Recon secondary */
('USP-S','weapon_usp_silencer',1,3,'CT',2),
('P2000','weapon_hkp2000',6,3,'CT',2),
('P250','weapon_p250',11,3,'CT',2),
('Five-Seven','weapon_fiveseven',26,3,'CT',2),
('CZ75 Auto','weapon_cz75a',36,3,'CT',2),
('Deagle','weapon_deagle',56,3,'CT',2),
('R8 Revolver','weapon_revolver',56,3,'CT',2),
/* CT Recon grenades */
('Decoy Grenade 1x','weapon_decoy',1,3,'CT',3),
('Smoke Grenade 1x','weapon_smokegrenade',1,3,'CT',3),
/* T Assault primary */
('Galil AR','weapon_galilar',1,4,'T',1),
('AK-47','weapon_ak47',31,4,'T',1),
('SG 556','weapon_sg556',51,4,'T',1),
/* T Assault secondary */
('Glock-18','weapon_glock',1,4,'T',2),
('Dual Barettas','weapon_elite',6,4,'T',2),
('P250','weapon_p250',11,4,'T',2),
('TEC-9','weapon_tec9',26,4,'T',2),
('CZ75 Auto','weapon_cz75a',36,4,'T',2),
('Deagle','weapon_deagle',56,4,'T',2),
('R8 Revolver','weapon_revolver',56,4,'T',2),
/* T Assault grenades */
('HE Grenade 1x','weapon_hegrenade',1,4,'T',3),
('Flashbang 1x','weapon_flashbang',1,4,'T',3),
/* T Engineer primary */
('Mac-10','weapon_mac10',1,2,'T',1),
('MP7','weapon_mp7',6,2,'T',1),
('PP-Bizon','weapon_bizon',16,2,'T',1),
('UMP-45','weapon_ump45',31,2,'T',1),
('P90','weapon_p90',51,2,'T',1),
/* T Engineer secondary */
('Glock-18','weapon_glock',1,2,'T',2),
('Dual Barettas','weapon_elite',6,2,'T',2),
('P250','weapon_p250',11,2,'T',2),
('TEC-9','weapon_tec9',26,2,'T',2),
('CZ75 Auto','weapon_cz75a',36,2,'T',2),
('Deagle','weapon_deagle',56,2,'T',2),
('R8 Revolver','weapon_revolver',56,2,'T',2),
/* T Engineer grenades */
('Molotov Cocktail 1x','weapon_molotov',1,2,'T',3),
('Smoke Grenade 1x','weapon_smokegrenade',1,2,'T',3),
/* T Support primary */
('Mac-10','weapon_mac10',1,1,'T',1),
('Nova','weapon_nova',6,1,'T',1),
('XM1014','weapon_xm1014',11,1,'T',1),
('Sawed-Off','weapon_sawedoff',26,1,'T',1),
('M249','weapon_m249',46,1,'T',1),
('Negev','weapon_negev',56,1,'T',1),
/* T Support secondary */
('Glock-18','weapon_glock',1,1,'T',2),
('Dual Barettas','weapon_elite',6,1,'T',2),
('P250','weapon_p250',11,1,'T',2),
('TEC-9','weapon_tec9',26,1,'T',2),
('CZ75 Auto','weapon_cz75a',36,1,'T',2),
('Deagle','weapon_deagle',56,1,'T',2),
('R8 Revolver','weapon_revolver',56,1,'T',2),
/* T Support grenades */
('Flashbang 2x','weapon_flashbang',1,1,'T',3),
/* T Recon primary */
('SSG08','weapon_ssg08',1,3,'T',1),
('G3SG1','weapon_g3sg1',31,3,'T',1),
('AWP','weapon_awp',46,3,'T',1),
/* T Recon secondary */
('Glock-18','weapon_glock',1,3,'T',2),
('Dual Barettas','weapon_elite',6,3,'T',2),
('P250','weapon_p250',11,3,'T',2),
('TEC-9','weapon_tec9',26,3,'T',2),
('CZ75 Auto','weapon_cz75a',36,3,'T',2),
('Deagle','weapon_deagle',56,3,'T',2),
('R8 Revolver','weapon_revolver',56,3,'T',2),
/* T Recon grenades */
('Decoy Grenade 1x','weapon_decoy',1,3,'T',3),
('Smoke Grenade 1x','weapon_smokegrenade',1,3,'T',3)
