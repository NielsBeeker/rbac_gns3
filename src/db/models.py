import sqlalchemy

from .fastapi_db import metadata

db_User = sqlalchemy.Table(
    "USERS",
    metadata,
    sqlalchemy.Column("USER_ID", sqlalchemy.BigInteger, primary_key=True, index=True, nullable=False),
    sqlalchemy.Column("NAME", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("PASSWORD", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("RESOURCE_ID", sqlalchemy.BigInteger,  sqlalchemy.ForeignKey("RESOURCES.RSC_ID"), nullable=False)
)

Resources = sqlalchemy.Table(
    "RESOURCES",
    metadata,
    sqlalchemy.Column("RSC_ID", sqlalchemy.BigInteger, primary_key=True, index=True, nullable=False),
    sqlalchemy.Column("UUID", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("NAME", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("RSC_TYPE", sqlalchemy.String, nullable=False)
)


Users_group_members = sqlalchemy.Table(
    "USERS_GROUP_MEMBERS",
    metadata,
    sqlalchemy.Column("USER_MEMBER_ID", sqlalchemy.BigInteger, primary_key=True, index=True, nullable=False),
    sqlalchemy.Column("USERS_GROUP_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("USERS_GROUP.USER_GROUP_ID"), nullable=False),
    sqlalchemy.Column("USER_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("USERS.USER_ID"), nullable=False)
)

Resources_group_members = sqlalchemy.Table(
    "RESOURCES_GROUP_MEMBERS",
    metadata,
    sqlalchemy.Column("RESOURCE_MEMBER_ID", sqlalchemy.BigInteger, primary_key=True, nullable=False),
    sqlalchemy.Column("RESOURCE_GROUP_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("RESOURCES_GROUP.RSC_GROUP_ID"), nullable=False),
    sqlalchemy.Column("RESOURCE_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("RESOURCES.RSC_ID"), nullable=False),
)

Resources_group = sqlalchemy.Table(
    "RESOURCES_GROUP",
    metadata,
    sqlalchemy.Column("RSC_GROUP_ID", sqlalchemy.BigInteger, primary_key=True, index=True, nullable=False),
    sqlalchemy.Column("UUID", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("NAME", sqlalchemy.String, nullable=False)
)

Users_group = sqlalchemy.Table(
    "USERS_GROUP",
    metadata,
    sqlalchemy.Column("USER_GROUP_ID", sqlalchemy.BigInteger, index=True, nullable=False, primary_key=True),
    sqlalchemy.Column("NAME", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("UPDATABLE", sqlalchemy.Boolean, default=True),
)

Permissions = sqlalchemy.Table(
    "PERMISSIONS",
    metadata,
    sqlalchemy.Column("PERM_ID", sqlalchemy.BigInteger, primary_key=True, index=True, nullable=False),
    sqlalchemy.Column("NAME", sqlalchemy.String, nullable=False)
)

Permissions_group_members = sqlalchemy.Table(
    "PERMISSIONS_GROUP_MEMBERS",
    metadata,
    sqlalchemy.Column("PERMISSION_MEMBER_ID", sqlalchemy.BigInteger, nullable=False, primary_key=True, index=True),
    sqlalchemy.Column("PERMISSION_GROUP_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("PERMISSIONS_GROUPS.PERMISSIONS_GROUPS_MEMBERS"), nullable=False),
    sqlalchemy.Column("PERMISSION_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("PERMISSIONS.PERM_ID"), nullable=False)
)

Permissions_groups = sqlalchemy.Table(
    "PERMISSIONS_GROUPS",
    metadata,
    sqlalchemy.Column("PERM_GROUP_ID", sqlalchemy.BigInteger, index=True, primary_key=True, nullable=False),
    sqlalchemy.Column("NAME", sqlalchemy.String(30))
)

Ace = sqlalchemy.Table(
    "ACE",
    metadata,
    sqlalchemy.Column("ACE_ID", sqlalchemy.BigInteger, nullable=False, primary_key=True, index=True),
    sqlalchemy.Column("ALLOWED", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("USER_GROUP_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("USERS_GROUP.USERS_GROUP_ID"), nullable=False),
    sqlalchemy.Column("RSC_GROUP_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("RESOURCES_GROUP.RSC_GROUP_ID"), nullable=False),
    sqlalchemy.Column("PERM_GROUP_ID", sqlalchemy.BigInteger, sqlalchemy.ForeignKey("PERMISSIONS_GROUPS.PERM_GROUP_ID"), nullable=False),
    sqlalchemy.Column("PRIORITY", sqlalchemy.Integer, nullable=False),
)