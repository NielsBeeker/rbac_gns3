from sqlalchemy import Column, ForeignKey, String, BigInteger, Boolean
from sqlalchemy.orm import relationship

from .fastapi_db import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    resource_id = Column(BigInteger, nullable=False)


class Resources(Base):
    __tablename__ = "resources"
    rsc_id = Column(BigInteger,primary_key=True, index=True, nullable=False)
    uuid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    rsc_type = Column(String, nullable=False)


class Users_group_members(Base):
    __tablename__ = "users_group_members"
    user_member_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    users_group_id = Column(BigInteger, ForeignKey("users_group.user_group_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)


class Resource_group_members(Base):
    __tablename__ = "resource_group_member"
    resource_member_id = Column(BigInteger, primary_key=True, nullable=False)
    resource_group_id = Column(BigInteger, ForeignKey("resources_group.rsc_group_id"), nullable=False)
    resource_id = Column(BigInteger, ForeignKey("resources.rsc_id"), nullable=False)


class Resources_group(Base):
    __tablename__ = "resources_group"
    rsc_group_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    uuid = Column(String, nullable=False)
    name = Column(String, nullable=False)


class Users_group(Base):
    __tablename__ = "users_group"
    user_group_id = Column(BigInteger, index=True, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    updatable = Column(Boolean, default=True)


class Permissions(Base):
    __tablename__ = "permissions"
    perm_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)


class Permissions_group_members(Base):
    __tablename__ = "permissions_group_members"
    permission_member_id = Column(BigInteger, nullable=False, primary_key=True, index=True)
    permission_group_id = Column(BigInteger, ForeignKey("permissions_groups.permissions_groups_members"), nullable=False)
    permission_id = Column(BigInteger, ForeignKey("permissions.perm_id"), nullable=False)


class Permissions_groups(Base):
    __tablename__ = "permissions_groups"
    perm_group_id = Column(BigInteger, index=True, primary_key=True, nullable=False)
    name = Column(String, nullabe=False)


class Ace(Base):
    __tablename__ = "ace"
    ace_id = Column(BigInteger, nullable=False, primary_key=True, index=True)
    allowed = Column(Boolean, default=False)
    user_group_id = Column(BigInteger, ForeignKey("users_group.users_group_id"), nullable=False)
    rsc_group_id = Column(BigInteger, ForeignKey("resources_group.rsc_group_id"), nullable=False)
    perm_group_id = Column(BigInteger, ForeignKey("permissions_groups.perm_group_id"), nullable=False)