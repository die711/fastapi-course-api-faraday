"""Moving is_active to user table

Revision ID: 000727811d31
Revises: 
Create Date: 2024-07-14 00:41:57.049879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import os
import json

# revision identifiers, used by Alembic.
revision: str = '000727811d31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = op.create_table('users',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String(length=100), nullable=False),
                            sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
                            sa.Column('is_active', sa.Boolean(), nullable=True),
                            sa.Column('created_at', sa.DateTime(), nullable=False),
                            sa.Column('updated_at', sa.DateTime(), nullable=False),
                            sa.PrimaryKeyConstraint('id')
                            )

    with open(os.path.join(os.path.dirname(__file__), '../data/students.json')) as f:
        students_data = f.read()

    op.bulk_insert(users, json.loads(students_data))

    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('courses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=200), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_table('profiles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(length=50), nullable=False),
                    sa.Column('last_name', sa.String(length=50), nullable=False),
                    sa.Column('bio', sa.Text(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_profiles_id'), 'profiles', ['id'], unique=False)
    op.create_table('sections',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=200), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('course_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_sections_id'), 'sections', ['id'], unique=False)
    op.create_table('student_course',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('student_id', sa.Integer(), nullable=False),
                    sa.Column('course_id', sa.Integer(), nullable=False),
                    sa.Column('completed', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_student_course_id'), 'student_course', ['id'], unique=False)
    op.create_table('content_blocks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=200), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('type', sa.Enum('lesson', 'quiz', 'assigment', name='contenttype'), nullable=True),
                    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=False),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.Column('section_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_content_blocks_id'), 'content_blocks', ['id'], unique=False)
    op.create_table('completed_content_blocks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('student_id', sa.Integer(), nullable=False),
                    sa.Column('content_block_id', sa.Integer(), nullable=False),
                    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=True),
                    sa.Column('feedback', sa.Text(), nullable=True),
                    sa.Column('grade', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['content_block_id'], ['content_blocks.id'], ),
                    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_completed_content_blocks_id'), 'completed_content_blocks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_completed_content_blocks_id'), table_name='completed_content_blocks')
    op.drop_table('completed_content_blocks')
    op.drop_index(op.f('ix_content_blocks_id'), table_name='content_blocks')
    op.drop_table('content_blocks')
    op.drop_index(op.f('ix_student_course_id'), table_name='student_course')
    op.drop_table('student_course')
    op.drop_index(op.f('ix_sections_id'), table_name='sections')
    op.drop_table('sections')
    op.drop_index(op.f('ix_profiles_id'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
