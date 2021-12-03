"""Initiate database

Revision ID: 2e4f89dc0daf
Revises: 
Create Date: 2021-12-02 13:03:31.926684

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision = "2e4f89dc0daf"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "caption",
        sa.Column(
            "image_url", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column(
            "caption", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column("fetch_status", sa.Integer(), nullable=False),
        sa.Column("fetch_error", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("pk", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("pk"),
    )
    op.create_index(op.f("ix_caption_caption"), "caption", ["caption"], unique=False)
    op.create_index(
        op.f("ix_caption_fetch_error"), "caption", ["fetch_error"], unique=False
    )
    op.create_index(
        op.f("ix_caption_fetch_status"), "caption", ["fetch_status"], unique=False
    )
    op.create_index(
        op.f("ix_caption_image_url"), "caption", ["image_url"], unique=False
    )
    op.create_index(op.f("ix_caption_pk"), "caption", ["pk"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_caption_pk"), table_name="caption")
    op.drop_index(op.f("ix_caption_image_url"), table_name="caption")
    op.drop_index(op.f("ix_caption_fetch_status"), table_name="caption")
    op.drop_index(op.f("ix_caption_fetch_error"), table_name="caption")
    op.drop_index(op.f("ix_caption_caption"), table_name="caption")
    op.drop_table("caption")
    # ### end Alembic commands ###