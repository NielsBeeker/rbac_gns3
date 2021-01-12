CREATE database gns3_rbac;
use gns3_rbac;

CREATE TABLE IF NOT EXISTS USERS(
	USER_ID                		BIGINT                      	NOT NULL,
	NAME	                 	VARCHAR(30)                  	NOT NULL,
	PASSWORD			VARCHAR(256)			NOT NULL,
	RESOURCE_ID			BIGINT				NOT NULL,
	CONSTRAINT PK_USER PRIMARY KEY (USER_ID)
);

create table if not exists USERS_GROUP (
	USER_GROUP_ID              	BIGINT                      	NOT NULL,
	NAME	                 	VARCHAR(30)                  	NOT NULL,
	UPDATABLE					BOOLEAN 		                DEFAULT TRUE,
	CONSTRAINT PK_USERGROUP PRIMARY KEY (USER_GROUP_ID)
);

create table if not exists USERS_GROUP_MEMBERS (
	USER_MEMBER_ID             	BIGINT                      	NOT NULL,
	USERS_GROUP_ID	            BIGINT                  		NOT NULL,
	USER_ID						BIGINT 							NOT NULL,
	CONSTRAINT PK_USERGROUPMEMBER PRIMARY KEY (USER_MEMBER_ID)
);

alter table USERS_GROUP_MEMBERS add constraint FK_MEMBER_USER_GROUP 	foreign key (USERS_GROUP_ID) 	references USERS_GROUP (USER_GROUP_ID);
alter table USERS_GROUP_MEMBERS add constraint FK_MEMBER_USER 			foreign key (USER_ID) 			references USERS (USER_ID);



create table if not exists RESOURCES (
	RSC_ID                		BIGINT                      	NOT NULL,
	UUID	                 	VARCHAR(100)                  	NOT NULL,
	NAME	                 	VARCHAR(100)                  	NOT NULL,
	RSC_TYPE					VARCHAR(20)						NOT NULL,
	CONSTRAINT PK_RSC PRIMARY KEY (RSC_ID)
);

alter table USERS add constraint FK_MEMBER_USER_RSC 					foreign key (RESOURCE_ID) 		references RESOURCES (RSC_ID);

create table if not exists RESOURCES_GROUP (
	RSC_GROUP_ID              	BIGINT                      	NOT NULL,
	UUID	                 	VARCHAR(100)                  	NOT NULL,
	NAME	                 	VARCHAR(30)                  	NOT NULL,
	CONSTRAINT PK_RSCGROUP PRIMARY KEY (RSC_GROUP_ID)
);

create table if not exists RESOURCES_GROUP_MEMBERS (
	RESOURCE_MEMBER_ID          BIGINT                      	NOT NULL,
	RESOURCES_GROUP_ID	        BIGINT                  		NOT NULL,
	RESOURCE_ID					BIGINT 							NOT NULL,
	CONSTRAINT PK_RSCGROUPMEMBER PRIMARY KEY (RESOURCE_MEMBER_ID)
);

alter table RESOURCES_GROUP_MEMBERS add constraint FK_MEMBER_RSC_GROUP 		foreign key (RESOURCES_GROUP_ID) 	references RESOURCES_GROUP (RSC_GROUP_ID);
alter table RESOURCES_GROUP_MEMBERS add constraint FK_MEMBER_RSC 			foreign key (RESOURCE_ID) 			references RESOURCES (RSC_ID);



create table if not exists PERMISSIONS (
	PERM_ID                		BIGINT                      	NOT NULL,
	NAME	                 	VARCHAR(30)                  	NOT NULL,
	CONSTRAINT PK_PERM PRIMARY KEY (PERM_ID)
);



create table if not exists PERMISSIONS_GROUPS (
	PERM_GROUP_ID              	BIGINT                      	NOT NULL,
	NAME	                 	VARCHAR(30)                  	NOT NULL,
	CONSTRAINT PK_ROLE PRIMARY KEY (PERM_GROUP_ID)
);

create table if not exists PERMISSIONS_GROUP_MEMBERS (
	PERMISSION_MEMBER_ID        BIGINT                      	NOT NULL,
	PERMISSIONS_GROUP_ID	    BIGINT                  		NOT NULL,
	PERMISSION_ID				BIGINT 							NOT NULL,
	CONSTRAINT PK_PERMGROUPMEMBER PRIMARY KEY (PERMISSION_MEMBER_ID)
);

alter table PERMISSIONS_GROUP_MEMBERS add constraint FK_MEMBER_PERM_GROUP 		foreign key (PERMISSIONS_GROUP_ID) 	references PERMISSIONS_GROUPS (PERM_GROUP_ID);
alter table PERMISSIONS_GROUP_MEMBERS add constraint FK_MEMBER_PERM 			foreign key (PERMISSION_ID) 		references PERMISSIONS (PERM_ID);

CREATE TABLE if not exists ACE (
	ACE_ID        				BIGINT                      	NOT NULL,
	ALLOWED		 				BOOLEAN 		                DEFAULT FALSE,
	USER_GROUP_ID        		BIGINT                      	NOT NULL,
	RSC_GROUP_ID	    		BIGINT                  		NOT NULL,
	PERM_GROUP_ID				BIGINT 							NOT NULL,
	PRIORITY			INT 				NOT NULL,
	CONSTRAINT PK_ACE PRIMARY KEY (ACE_ID)
);

alter table ACE add constraint FK_ACE_USER_GROUP 		foreign key (USER_GROUP_ID) 		references USERS_GROUP (USER_GROUP_ID);
alter table ACE add constraint FK_ACE_RSC_GROUP			foreign key (RSC_GROUP_ID) 			references RESOURCES_GROUP (RSC_GROUP_ID);
alter table ACE add constraint FK_ACE_PERM_GROUP		foreign key (PERM_GROUP_ID) 		references PERMISSIONS_GROUPS (PERM_GROUP_ID);


