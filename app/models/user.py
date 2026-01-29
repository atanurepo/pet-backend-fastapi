import uuid
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from sqlalchemy.sql import func

class User(Base):
	__tablename__ = "user_profile"
	
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 			# Surrogate PK
	user_id = Column(UUID(as_uuid=True), nullable=False)							# Business key (same for all versions)
	full_name = Column(String, nullable=False)
	email = Column(String, nullable=False)
	phone = Column(String(20), nullable=False)
	auth_provider = Column(String, nullable=False)
	oauth_id = Column(String, nullable=False)
	password_hash = Column(String, nullable=True)
	is_active = Column(Boolean, nullable=True)
	effective_start_dt = Column(DateTime, nullable=False, server_default=func.now())
	effective_end_dt = Column(DateTime, nullable=True)
	version_no = Column(Integer, nullable=False, default=1)
	created_at = Column(DateTime,nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
