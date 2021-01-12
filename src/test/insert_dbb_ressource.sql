
/* Resources */

INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (1, 'AAAA-BBBB-1111', '/v2/', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (2, 'AAAA-BBBB-1112', '/v3/projects', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (3, 'AAAA-BBBB-1113', '/v3/projects/AAAA-BBBB-1113', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (4, 'AAAA-BBBB-1234', 'GOD USER', 'USER');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (5, 'AAAA-BBBB-6666', 'MARCEL USER', 'USER');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (6, 'CCCC-BBBB-1111', '/v3/projects/AAAA-BBBB-1113/nodes/CCCC-BBBB-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (7, 'DDDD-BBBB-1111', '/v3/projects/AAAA-BBBB-1113/nodes/CCCC-BBBB-1111/links/DDDD-BBBB-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (8, 'DDDD-BBBB-1112', '/v3/projects/AAAA-BBBB-1113/nodes/CCCC-BBBB-1111/links/DDDD-BBBB-1112', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (9, 'UUUUU-AAAA-1111', 'UN TRUC', 'OBJECT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (10, 'UUUUU-AAAA-1112', 'UN AUTRE TRUC', 'OBJECT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (11, 'AAAA-BBBB-6667', 'MAURICE USER', 'USER');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (12, 'AAAA-BBBB-6668', 'MICHEL USER', 'USER');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (13, 'AAAA-BBBB-6669', 'ROBERT USER', 'USER');

INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (1, 'GROUP-AAAA-1111', 'ALL CCCC-BBBB-1111 nodes');
INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (2, 'GROUP-AAAA-1112', 'tous les trucs');
INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (3, 'GROUP-AAAA-1113', 'tous les gus');
INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (4, 'GROUP-AAAA-1114', 'tous les projets');
INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (5, 'GROUP-AAAA-1115', 'le projet AAAA-BBBB-1113');

INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (1, 1, 6);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (2, 1, 7);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (3, 1, 8);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (4, 2, 9);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (5, 2, 10);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (6, 3, 4);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (7, 3, 5);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (8, 4, 2);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (9, 5, 3);

/* Users */

INSERT INTO USERS (USER_ID, NAME, PASSWORD, RESOURCE_ID) VALUES (1, 'GOD', 'unmotdepassehaché1', 4);
INSERT INTO USERS (USER_ID, NAME, PASSWORD, RESOURCE_ID) VALUES (2, 'MARCEL', 'unmotdepassehaché2', 5);
INSERT INTO USERS (USER_ID, NAME, PASSWORD, RESOURCE_ID) VALUES (3, 'MAURICE', 'unmotdepassehaché3', 11);
INSERT INTO USERS (USER_ID, NAME, PASSWORD, RESOURCE_ID) VALUES (4, 'MICHEL', 'unmotdepassehaché4', 12);
INSERT INTO USERS (USER_ID, NAME, PASSWORD, RESOURCE_ID) VALUES (5, 'ROBERT', 'unmotdepassehaché5', 13);

INSERT INTO USERS_GROUP (USER_GROUP_ID, NAME, UPDATABLE) VALUES (1, 'ADMINS', 0);
INSERT INTO USERS_GROUP (USER_GROUP_ID, NAME, UPDATABLE) VALUES (2, 'USERS', 1);
INSERT INTO USERS_GROUP (USER_GROUP_ID, NAME, UPDATABLE) VALUES (3, 'AUDITORS', 1);

INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (1, 1, 1);
INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (2, 2, 2);
INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (3, 2, 3);
INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (4, 2, 4);
INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (5, 2, 5);
INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (6, 3, 4);

/* PERMISSIONS */

INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (1, 'CREATE');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (2, 'READ');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (3, 'UPDATE');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (4, 'DELETE');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (5, 'USE');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (6, 'NODE_CONSOLE');

INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (1, 'ADMINISTRATOR');
INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (2, 'READONLY');
INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (3, 'USERONLY');

INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (1, 1, 1);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (2, 1, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (3, 1, 3);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (4, 1, 4);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (5, 1, 5);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (6, 1, 6);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (7, 2, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (8, 3, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (9, 3, 5);


/* ACE */

INSERT INTO ACE (ACE_ID, ALLOWED, USER_GROUP_ID, RSC_GROUP_ID, PERM_GROUP_ID, PRIORITY) VALUES (1, 1, 1, 4, 1, 1);
INSERT INTO ACE (ACE_ID, ALLOWED, USER_GROUP_ID, RSC_GROUP_ID, PERM_GROUP_ID, PRIORITY) VALUES (2, 1, 2, 5, 2, 1);
INSERT INTO ACE (ACE_ID, ALLOWED, USER_GROUP_ID, RSC_GROUP_ID, PERM_GROUP_ID, PRIORITY) VALUES (3, 1, 2, 1, 3, 2);














INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (14, 'AAAA-BBBB-1114', '/v3/version', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (15, 'AAAA-BBBB-1115', '/v3/iou_license', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (16, 'AAAA-BBBB-1116', '/v3/appliances', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (17, 'AAAA-BBBB-1117', '/v3/computes', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (18, 'AAAA-BBBB-1118', '/v3/computes/CCCC-AAAA-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (19, 'AAAA-BBBB-1119', '/v3/projects', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (20, 'AAAA-BBBB-1121', '/v3/projects/AAAA-BBBB-1121', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (21, 'AAAA-BBBB-1122', '/v3/projects/AAAA-BBBB-1121/links', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (22, 'AAAA-BBBB-1123', '/v3/projects/AAAA-BBBB-1121/links/LLLL-AAAA-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (23, 'AAAA-BBBB-1124', '/v3/projects/AAAA-BBBB-1121/links/LLLL-AAAA-1111/reset', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (24, 'AAAA-BBBB-1125', '/v3/projects/AAAA-BBBB-1121/links/LLLL-AAAA-1111/capture/start', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (25, 'AAAA-BBBB-1126', '/v3/projects/AAAA-BBBB-1121/links/LLLL-AAAA-1111/capture/stream', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (26, 'AAAA-BBBB-1127', '/v3/gns3vm', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (27, 'AAAA-BBBB-1128', '/v3/gns3vm/engines', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (28, 'AAAA-BBBB-1129', '/v3/projects/AAAA-BBBB-1121/nodes', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (29, 'AAAA-BBBB-1131', '/v3/projects/AAAA-BBBB-1121/nodes/NNNN-AAAA-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (30, 'AAAA-BBBB-1132', '/v3/projects/AAAA-BBBB-1121/nodes/NNNN-AAAA-1111/start', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (31, 'AAAA-BBBB-1133', '/v3/projects/AAAA-BBBB-1121/nodes/NNNN-AAAA-1111/duplicate', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (32, 'AAAA-BBBB-1134', '/v3/projects/AAAA-BBBB-1121/nodes/NNNN-AAAA-1111/links', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (33, 'AAAA-BBBB-1135', '/v3/projects/AAAA-BBBB-1121/nodes/NNNN-AAAA-1111/files/FFFF-AAAA-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (34, 'AAAA-BBBB-1136', '/v3/projects/AAAA-BBBB-1121/nodes/console/reset', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (35, 'AAAA-BBBB-1137', '/v3/projects/AAAA-BBBB-1121/nodes/NNNN-AAAA-1111/console/reset', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (36, 'AAAA-BBBB-1138', '/v3/notification', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (37, 'AAAA-BBBB-1139', '/v3/projects/load', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (38, 'AAAA-BBBB-1141', '/v3/projects/AAAA-BBBB-1121/stats', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (39, 'AAAA-BBBB-1142', '/v3/projects/AAAA-BBBB-1121/export', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (40, 'AAAA-BBBB-1143', '/v3/projects/AAAA-BBBB-1121/duplicate', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (41, 'AAAA-BBBB-1144', '/v3/projects/AAAA-BBBB-1121/snapshots', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (42, 'AAAA-BBBB-1145', '/v3/projects/AAAA-BBBB-1122/snapshots/SSSS-AAAA-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (43, 'AAAA-BBBB-1146', '/v3/symbols', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (44, 'AAAA-BBBB-1147', '/v3/symbols/XXXX-AAAA-1111/raw', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (45, 'AAAA-BBBB-1148', '/v3/symbols/default_symbols', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (46, 'AAAA-BBBB-1149', '/v3/templates', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (47, 'AAAA-BBBB-1151', '/v3/templates/TTTT-AAAA-1111', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (48, 'AAAA-BBBB-1152', '/v3/templates/TTTT-AAAA-1111/duplicate', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (49, 'AAAA-BBBB-9999', 'NIELS', 'USER');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (50, 'AAAA-BBBB-1153', '/v3/templates/', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (51, 'AAAA-BBBB-1154', '/v3/symbols/', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (52, 'AAAA-BBBB-1155', '/v3/images/', 'ENDPOINT');
INSERT INTO RESOURCES (RSC_ID, UUID, NAME, RSC_TYPE) VALUES (53, 'AAAA-BBBB-1156', '/v3/images', 'ENDPOINT');




INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (6, 'GROUP-AAAA-1116', 'template_admin resources');
INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (7, 'GROUP-AAAA-1117', 'symbol_admin resources');
INSERT INTO RESOURCES_GROUP (RSC_GROUP_ID, UUID, NAME) VALUES (8, 'GROUP-AAAA-1118', 'image_admin resources');

INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (10, 6, 46);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (11, 6, 50);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (12, 7, 43);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (13, 7, 51);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (14, 8, 52);
INSERT INTO RESOURCES_GROUP_MEMBERS (RESOURCE_MEMBER_ID, RESOURCES_GROUP_ID, RESOURCE_ID) VALUES (15, 8, 53);


#PAS ENCORE FAIT
INSERT INTO USERS (USER_ID, NAME, PASSWORD, RESOURCE_ID) VALUES (6, 'NIELS', 'secret', 49);


INSERT INTO USERS_GROUP (USER_GROUP_ID, NAME, UPDATABLE) VALUES (4, 'TEST_GROUP', 1);


INSERT INTO USERS_GROUP_MEMBERS (USER_MEMBER_ID, USERS_GROUP_ID, USER_ID) VALUES (7, 4, 6);



INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (7, 'NODE_POWER_MGNT');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (8, 'NODE_SNAPSHOT');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (9, 'LINK_CAPTURE');
INSERT INTO PERMISSIONS (PERM_ID, NAME) VALUES (10, 'LINK_FILTER');


INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (5, 'TEMPLATEADMIN');
INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (6, 'IMAGEADMIN');
INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (7, 'SYMBOLEADMIN');
INSERT INTO PERMISSIONS_GROUPS (PERM_GROUP_ID, NAME) VALUES (4, 'USERADMIN');

#TEMPLATE ADMIN
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (10, 5, 1);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (11, 5, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (12, 5, 3);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (13, 5, 4);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (14, 5, 5);

#IMAGE ADMIN
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (15, 6, 1);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (16, 6, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (17, 6, 3);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (18, 6, 4);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (19, 6, 5);

#USER ADMIN

INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (20, 4, 1);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (21, 4, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (22, 4, 3);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (23, 4, 4);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (24, 4, 5);

#SYMBOLE ADMIN

INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (25, 7, 1);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (26, 7, 2);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (27, 7, 3);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (28, 7, 4);
INSERT INTO PERMISSIONS_GROUP_MEMBERS (PERMISSION_MEMBER_ID, PERMISSIONS_GROUP_ID, PERMISSION_ID) VALUES (29, 7, 5);


INSERT INTO ACE (ACE_ID, ALLOWED, USER_GROUP_ID, RSC_GROUP_ID, PERM_GROUP_ID, PRIORITY) VALUES (4, 1, 3, 6, 5, 1);
INSERT INTO ACE (ACE_ID, ALLOWED, USER_GROUP_ID, RSC_GROUP_ID, PERM_GROUP_ID, PRIORITY) VALUES (5, 1, 3, 7, 6, 1);
INSERT INTO ACE (ACE_ID, ALLOWED, USER_GROUP_ID, RSC_GROUP_ID, PERM_GROUP_ID, PRIORITY) VALUES (6, 1, 3, 8, 7, 1);