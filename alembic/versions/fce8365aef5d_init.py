"""init

Revision ID: fce8365aef5d
Revises: 
Create Date: 2021-05-27 14:43:11.947884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fce8365aef5d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('text_en', sa.String(length=255), nullable=False),
    sa.Column('text_ru', sa.String(length=255), nullable=False),
    sa.Column('link_text_en', sa.String(length=255), nullable=False),
    sa.Column('link_text_ru', sa.String(length=255), nullable=False),
    sa.Column('link', sa.String(length=255), nullable=True),
    sa.Column('text_color', sa.String(length=255), nullable=True),
    sa.Column('text_left_offset', sa.String(length=10), nullable=True),
    sa.Column('text_right_offset', sa.String(length=10), nullable=True),
    sa.Column('text_top_offset', sa.String(length=10), nullable=True),
    sa.Column('text_bottom_offset', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('parent_category_id', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['parent_category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_category_parent_category_id'), 'category', ['parent_category_id'], unique=False)
    op.create_table('characteristic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('currency_rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('description_en', sa.String(length=255), nullable=False),
    sa.Column('description_ru', sa.String(length=255), nullable=False),
    sa.Column('short_description_en', sa.String(length=255), nullable=False),
    sa.Column('short_description_ru', sa.String(length=255), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('promo_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('value', sa.String(length=60), nullable=False),
    sa.Column('discount', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('disable_on_use', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('signup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('user_name', sa.String(length=60), nullable=False),
    sa.Column('user_email', sa.String(length=80), nullable=False),
    sa.Column('user_password', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('characteristic_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('characteristic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['characteristic_id'], ['characteristic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_characteristic_value_characteristic_id'), 'characteristic_value', ['characteristic_id'], unique=False)
    op.create_table('feature_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('feature_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['feature_type_id'], ['feature_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feature_value_feature_type_id'), 'feature_value', ['feature_type_id'], unique=False)
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('discount', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('product_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_product_type_id'), 'product', ['product_type_id'], unique=False)
    op.create_table('product_type_instagram_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('link', sa.String(length=255), nullable=False),
    sa.Column('product_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_type_instagram_link_product_type_id'), 'product_type_instagram_link', ['product_type_id'], unique=False)
    op.create_table('product_type_x_category',
    sa.Column('product_type_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_type.id'], ),
    sa.PrimaryKeyConstraint('product_type_id', 'category_id')
    )
    op.create_index(op.f('ix_product_type_x_category_product_type_id'), 'product_type_x_category', ['product_type_id'], unique=False)
    op.create_table('product_type_x_feature_type',
    sa.Column('product_type_id', sa.Integer(), nullable=False),
    sa.Column('feature_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['feature_type_id'], ['feature_type.id'], ),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_type.id'], ),
    sa.PrimaryKeyConstraint('product_type_id', 'feature_type_id')
    )
    op.create_index(op.f('ix_product_type_x_feature_type_feature_type_id'), 'product_type_x_feature_type', ['feature_type_id'], unique=False)
    op.create_index(op.f('ix_product_type_x_feature_type_product_type_id'), 'product_type_x_feature_type', ['product_type_id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Product_type_x_characteristic_value',
    sa.Column('product_type_id', sa.Integer(), nullable=False),
    sa.Column('characteristic_value_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['characteristic_value_id'], ['characteristic_value.id'], ),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_type.id'], ),
    sa.PrimaryKeyConstraint('product_type_id', 'characteristic_value_id')
    )
    op.create_index(op.f('ix_Product_type_x_characteristic_value_characteristic_value_id'), 'Product_type_x_characteristic_value', ['characteristic_value_id'], unique=False)
    op.create_index(op.f('ix_Product_type_x_characteristic_value_product_type_id'), 'Product_type_x_characteristic_value', ['product_type_id'], unique=False)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user_name', sa.String(length=255), nullable=False),
    sa.Column('user_phone_number', sa.String(length=255), nullable=False),
    sa.Column('user_address', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('promo_code_value', sa.String(length=60), nullable=True),
    sa.Column('promo_code_discount', sa.Integer(), nullable=True),
    sa.Column('promo_code_amount', sa.Float(), nullable=True),
    sa.Column('promo_code_products_ids', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('status', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_image_product_id'), 'product_image', ['product_id'], unique=False)
    op.create_table('product_x_feature_value',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('feature_value_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['feature_value_id'], ['feature_value.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'feature_value_id')
    )
    op.create_index(op.f('ix_product_x_feature_value_feature_value_id'), 'product_x_feature_value', ['feature_value_id'], unique=False)
    op.create_index(op.f('ix_product_x_feature_value_product_id'), 'product_x_feature_value', ['product_id'], unique=False)
    op.create_table('product_x_promo_code',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('promo_code_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['promo_code_id'], ['promo_code.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'promo_code_id')
    )
    op.create_index(op.f('ix_product_x_promo_code_product_id'), 'product_x_promo_code', ['product_id'], unique=False)
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('product_price_per_item', sa.Integer(), nullable=False),
    sa.Column('product_discount', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_item_order_id'), 'order_item', ['order_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_item_order_id'), table_name='order_item')
    op.drop_table('order_item')
    op.drop_index(op.f('ix_product_x_promo_code_product_id'), table_name='product_x_promo_code')
    op.drop_table('product_x_promo_code')
    op.drop_index(op.f('ix_product_x_feature_value_product_id'), table_name='product_x_feature_value')
    op.drop_index(op.f('ix_product_x_feature_value_feature_value_id'), table_name='product_x_feature_value')
    op.drop_table('product_x_feature_value')
    op.drop_index(op.f('ix_product_image_product_id'), table_name='product_image')
    op.drop_table('product_image')
    op.drop_table('order')
    op.drop_index(op.f('ix_Product_type_x_characteristic_value_product_type_id'), table_name='Product_type_x_characteristic_value')
    op.drop_index(op.f('ix_Product_type_x_characteristic_value_characteristic_value_id'), table_name='Product_type_x_characteristic_value')
    op.drop_table('Product_type_x_characteristic_value')
    op.drop_table('user')
    op.drop_index(op.f('ix_product_type_x_feature_type_product_type_id'), table_name='product_type_x_feature_type')
    op.drop_index(op.f('ix_product_type_x_feature_type_feature_type_id'), table_name='product_type_x_feature_type')
    op.drop_table('product_type_x_feature_type')
    op.drop_index(op.f('ix_product_type_x_category_product_type_id'), table_name='product_type_x_category')
    op.drop_table('product_type_x_category')
    op.drop_index(op.f('ix_product_type_instagram_link_product_type_id'), table_name='product_type_instagram_link')
    op.drop_table('product_type_instagram_link')
    op.drop_index(op.f('ix_product_product_type_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_feature_value_feature_type_id'), table_name='feature_value')
    op.drop_table('feature_value')
    op.drop_index(op.f('ix_characteristic_value_characteristic_id'), table_name='characteristic_value')
    op.drop_table('characteristic_value')
    op.drop_table('signup')
    op.drop_table('promo_code')
    op.drop_table('product_type')
    op.drop_table('group')
    op.drop_table('feature_type')
    op.drop_table('currency_rate')
    op.drop_table('characteristic')
    op.drop_index(op.f('ix_category_parent_category_id'), table_name='category')
    op.drop_table('category')
    op.drop_table('banner')
    # ### end Alembic commands ###
