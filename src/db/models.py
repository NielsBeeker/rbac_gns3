from sqlalchemy import Column, ForeignKey, String, BigInteger, Boolean, Table


from .fastapi_db import metadata

User = Table(
    "users",
    metadata,
    Column("user_id", BigInteger, primary_key=True, index=True, nullable=False),
    Column("name", String, nullable=False),
    Column("password", String, nullable=False),
    Column("ressource_id", ForeignKey("resources.rsc_id"), BigInteger, nullable=False),
)

Resources = Table(
    "resources",
    metadata,
    Column("rsc_id", BigInteger,primary_key=True, index=True, nullable=False),
    Column("uuid", String, nullable=False),
    Column("name", String, nullable=False),
    Column("rsc_type", String, nullable=False)
)


Users_group_members = Table(
    "users_group_members",
    metadata,
    Column("user_member_id", BigInteger, primary_key=True, index=True, nullable=False),
    Column("users_group_id", BigInteger, ForeignKey("users_group.user_group_id"), nullable=False),
    Column("user_id", BigInteger, ForeignKey("users.user_id"), nullable=False)
)

Resources_group_members = Table(
    "resources_group_members",
    metadata,
    Column("resource_member_id", BigInteger, primary_key=True, nullable=False),
    Column("resource_group_id", BigInteger, ForeignKey("resources_group.rsc_group_id"), nullable=False),
    Column("resource_id", BigInteger, ForeignKey("resources.rsc_id"), nullable=False),
)

Resources_group = Table(
    "resources_group",
    metadata,
    Column("rsc_group_id", BigInteger, primary_key=True, index=True, nullable=False),
    Column("uuid", String, nullable=False),
    Column("name", String, nullable=False)
)

Users_group = Table(
    "users_group",
    metadata,
    Column("user_group_id", BigInteger, index=True, nullable=False, primary_key=True),
    Column("name", String, nullable=False),
    Column("updatable", Boolean, default=True),
)

Permissions = Table(
    "permissions",
    metadata,
    Column("perm_id", BigInteger, primary_key=True, index=True, nullable=False),
    Column("name", String, nullable=False)
)

Permissions_group_members = Table(
    "permissions_group_members",
    metadata,
    Column("permission_member_id", BigInteger, nullable=False, primary_key=True, index=True),
    Column("permission_group_id", BigInteger, ForeignKey("permissions_groups.permissions_groups_members"), nullable=False),
    Column("permission_id", BigInteger, ForeignKey("permissions.perm_id"), nullable=False)
)

Permissions_groups = Table(
    "permissions_groups",
    metadata,
    Column("perm_group_id", BigInteger, index=True, primary_key=True, nullable=False),
    Column("name", String, nullabe=False)
)

Ace = Table(
    "ace",
    metadata,
    Column("ace_id", BigInteger, nullable=False, primary_key=True, index=True),
    Column("allowed", Boolean, default=False),
    Column("user_group_id", BigInteger, ForeignKey("users_group.users_group_id"), nullable=False),
    Column("rsc_group_id", BigInteger, ForeignKey("resources_group.rsc_group_id"), nullable=False),
    Column("perm_group_id", BigInteger, ForeignKey("permissions_groups.perm_group_id"), nullable=False),
)